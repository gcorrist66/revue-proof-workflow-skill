#!/usr/bin/env python3
"""Validate a creative-production deliverable (HTML/CSS/SVG) against a revüe design-system lock.

Pillar 3 (output-audit) — hardened, evasion-resistant version. The audit is fail-closed: every color
the deliverable can express must map exactly to the lock's palette, every font must map to the lock's
typography, Hard-NO text must not appear in any recoverable form, and quantitative marketing claims
("4.9 stars", "200+ clients", "trusted by 500+") must be explicitly approved in the lock's `claims`
list. Anything the audit cannot verify (external stylesheets, binary formats, a deliverable with no
detectable colors) is a failure, not a pass.

What this version catches that the v1.0 scaffolding did not:
  - colors as hsl()/hsla(), modern space-separated rgb(), percentage channels, named CSS colors,
    CSS custom properties, gradients, SVG presentation attributes, legacy hash-less attribute hex
    (bgcolor="112233"), and colors inside base64/percent-encoded data URIs or atob("...") payloads;
  - Hard NOs split across tags or comments, HTML-entity-encoded, zero-width-joined, homoglyph-swapped
    (Cyrillic/Greek lookalikes), accent-masked, or hidden in attribute text (alt/aria/title);
  - near-miss off-palette shades (reported as near-misses of the closest lock color — still failures);
  - fabricated-metric patterns: star ratings, "N+" social-proof counts, "trusted by N", percent
    claims about customers/uptime/satisfaction, star-glyph runs, and "#1 rated" phrasing;
  - unverifiable deliverables: external stylesheets/scripts/@import, binary files, no colors found.

Known remaining limits (documented in references/output-audit.md): no raster pixel sampling (an
embedded photo/logo PNG is noted but not color-audited), no JS execution (computed styles built by
running code are not resolved; literal values inside scripts ARE scanned), no PDF parsing.

Stdlib only. Exit 0 = pass, 1 = violation(s), 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import colorsys
import html as html_lib
import json
import re
import unicodedata
import urllib.parse
from pathlib import Path

# --------------------------------------------------------------------------- color tables

# Full CSS Color Module Level 4 named-color table (147 names + rebeccapurple).
NAMED_COLORS = {
    "aliceblue": "#f0f8ff", "antiquewhite": "#faebd7", "aqua": "#00ffff", "aquamarine": "#7fffd4",
    "azure": "#f0ffff", "beige": "#f5f5dc", "bisque": "#ffe4c4", "black": "#000000",
    "blanchedalmond": "#ffebcd", "blue": "#0000ff", "blueviolet": "#8a2be2", "brown": "#a52a2a",
    "burlywood": "#deb887", "cadetblue": "#5f9ea0", "chartreuse": "#7fff00", "chocolate": "#d2691e",
    "coral": "#ff7f50", "cornflowerblue": "#6495ed", "cornsilk": "#fff8dc", "crimson": "#dc143c",
    "cyan": "#00ffff", "darkblue": "#00008b", "darkcyan": "#008b8b", "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9", "darkgreen": "#006400", "darkgrey": "#a9a9a9", "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b", "darkolivegreen": "#556b2f", "darkorange": "#ff8c00",
    "darkorchid": "#9932cc", "darkred": "#8b0000", "darksalmon": "#e9967a", "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b", "darkslategray": "#2f4f4f", "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1", "darkviolet": "#9400d3", "deeppink": "#ff1493",
    "deepskyblue": "#00bfff", "dimgray": "#696969", "dimgrey": "#696969", "dodgerblue": "#1e90ff",
    "firebrick": "#b22222", "floralwhite": "#fffaf0", "forestgreen": "#228b22", "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc", "ghostwhite": "#f8f8ff", "gold": "#ffd700", "goldenrod": "#daa520",
    "gray": "#808080", "green": "#008000", "greenyellow": "#adff2f", "grey": "#808080",
    "honeydew": "#f0fff0", "hotpink": "#ff69b4", "indianred": "#cd5c5c", "indigo": "#4b0082",
    "ivory": "#fffff0", "khaki": "#f0e68c", "lavender": "#e6e6fa", "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00", "lemonchiffon": "#fffacd", "lightblue": "#add8e6", "lightcoral": "#f08080",
    "lightcyan": "#e0ffff", "lightgoldenrodyellow": "#fafad2", "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90", "lightgrey": "#d3d3d3", "lightpink": "#ffb6c1", "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa", "lightskyblue": "#87cefa", "lightslategray": "#778899",
    "lightslategrey": "#778899", "lightsteelblue": "#b0c4de", "lightyellow": "#ffffe0",
    "lime": "#00ff00", "limegreen": "#32cd32", "linen": "#faf0e6", "magenta": "#ff00ff",
    "maroon": "#800000", "mediumaquamarine": "#66cdaa", "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3", "mediumpurple": "#9370db", "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee", "mediumspringgreen": "#00fa9a", "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585", "midnightblue": "#191970", "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1", "moccasin": "#ffe4b5", "navajowhite": "#ffdead", "navy": "#000080",
    "oldlace": "#fdf5e6", "olive": "#808000", "olivedrab": "#6b8e23", "orange": "#ffa500",
    "orangered": "#ff4500", "orchid": "#da70d6", "palegoldenrod": "#eee8aa", "palegreen": "#98fb98",
    "paleturquoise": "#afeeee", "palevioletred": "#db7093", "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9", "peru": "#cd853f", "pink": "#ffc0cb", "plum": "#dda0dd",
    "powderblue": "#b0e0e6", "purple": "#800080", "rebeccapurple": "#663399", "red": "#ff0000",
    "rosybrown": "#bc8f8f", "royalblue": "#4169e1", "saddlebrown": "#8b4513", "salmon": "#fa8072",
    "sandybrown": "#f4a460", "seagreen": "#2e8b57", "seashell": "#fff5ee", "sienna": "#a0522d",
    "silver": "#c0c0c0", "skyblue": "#87ceeb", "slateblue": "#6a5acd", "slategray": "#708090",
    "slategrey": "#708090", "snow": "#fffafa", "springgreen": "#00ff7f", "steelblue": "#4682b4",
    "tan": "#d2b48c", "teal": "#008080", "thistle": "#d8bfd8", "tomato": "#ff6347",
    "turquoise": "#40e0d0", "violet": "#ee82ee", "wheat": "#f5deb3", "white": "#ffffff",
    "whitesmoke": "#f5f5f5", "yellow": "#ffff00", "yellowgreen": "#9acd32",
}

# Non-color CSS keywords that are legal in color positions and carry no palette information.
COLOR_NEUTRAL_KEYWORDS = {"transparent", "currentcolor", "inherit", "initial", "unset", "revert", "none"}

GENERIC_FONT_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
    "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "fangsong",
    "inherit", "initial", "unset", "revert",
}

# --------------------------------------------------------------------------- regexes

# (?<!&) keeps numeric character references (&#108;) from being misread as hex colors.
HEX_PATTERN = re.compile(r"(?<!&)#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
# Fragment-only link targets (href="#add") and SVG local refs (url(#fade)) are ids, not colors.
# Restricted to href-type attributes: color-bearing attributes (fill="#e91e63") must NOT be scrubbed.
FRAGMENT_ATTR_PATTERN = re.compile(r"\b(?:href|xlink:href)\s*=\s*([\"'])#[\w-]*\1", re.IGNORECASE)
URL_FRAGMENT_PATTERN = re.compile(r"url\(\s*[\"']?#[\w-]*[\"']?\s*\)", re.IGNORECASE)
# rgb()/rgba(): legacy comma syntax, modern space syntax, integer or percentage channels.
RGB_PATTERN = re.compile(
    r"rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)(?:\s*[,/]\s*[\d.]+%?)?\s*\)",
    re.IGNORECASE,
)
# hsl()/hsla(): hue with optional unit, saturation/lightness as percentages.
HSL_PATTERN = re.compile(
    r"hsla?\(\s*(-?[\d.]+)(deg|grad|rad|turn)?\s*[\s,]+([\d.]+)%\s*[\s,]+([\d.]+)%"
    r"(?:\s*[,/]\s*[\d.]+%?)?\s*\)",
    re.IGNORECASE,
)
# Legacy HTML color attributes accept hex with no leading '#'.
ATTR_HEX_PATTERN = re.compile(
    r"\b(?:bgcolor|text|link|alink|vlink|color|fill|stroke|stop-color|flood-color|lighting-color)"
    r"\s*=\s*[\"']?#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b",
    re.IGNORECASE,
)
STYLE_BLOCK_PATTERN = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.IGNORECASE | re.DOTALL)
# Quoted OR unquoted attribute values — <div style=color:red> is legal HTML and must not evade.
STYLE_ATTR_PATTERN = re.compile(r"\bstyle\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s\"'>]+)", re.IGNORECASE)
COLOR_ATTR_PATTERN = re.compile(
    r"\b(?:fill|stroke|color|bgcolor|stop-color|flood-color|lighting-color|text|link|alink|vlink)"
    r"\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s\"'>]+)",
    re.IGNORECASE,
)
SCRIPT_BLOCK_PATTERN = re.compile(r"<script\b[^>]*>(.*?)</script\s*>", re.IGNORECASE | re.DOTALL)
# Inside scripts: literal assignments to color-ish targets, e.g. el.style.color = "tomato".
SCRIPT_COLOR_ASSIGN_PATTERN = re.compile(
    r"(?:color|background|backgroundcolor|fill|stroke|bordercolor)\s*[:=]\s*[\"']([^\"']{1,40})[\"']",
    re.IGNORECASE,
)
CSS_DECL_PATTERN = re.compile(r"([-\w]+)\s*:\s*([^;{}]+)")
DATA_URI_B64_PATTERN = re.compile(r"data:([\w/+.-]+);base64,([A-Za-z0-9+/=\s]{8,})")
DATA_URI_TEXT_PATTERN = re.compile(r"data:(image/svg\+xml|text/[\w+.-]+),([^\"')\s]+)")
ATOB_PATTERN = re.compile(r"atob\(\s*[\"']([A-Za-z0-9+/=]{8,})[\"']\s*\)")
EXTERNAL_STYLESHEET_PATTERN = re.compile(
    r"<link\b[^>]*\brel\s*=\s*[\"']?[^\"'>]*stylesheet", re.IGNORECASE
)
CSS_IMPORT_PATTERN = re.compile(r"@import\b", re.IGNORECASE)
EXTERNAL_SCRIPT_PATTERN = re.compile(r"<script\b[^>]*\bsrc\s*=", re.IGNORECASE)
IFRAME_PATTERN = re.compile(r"<iframe\b[^>]*\bsrc\s*=", re.IGNORECASE)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
CSS_JS_COMMENT_PATTERN = re.compile(r"/\*.*?\*/", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WS_PATTERN = re.compile(r"\s+")

BINARY_MAGICS = (b"%PDF", b"\x89PNG", b"\xff\xd8\xff", b"GIF8", b"PK\x03\x04", b"RIFF", b"\x00\x00\x01\x00")

# Common Cyrillic/Greek homoglyphs folded to ASCII (post-casefold, so lowercase forms only).
CONFUSABLES = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "у": "y", "і": "i", "ѕ": "s", "ԁ": "d", "һ": "h", "к": "k",
    "м": "m", "т": "t", "в": "b", "н": "h",
    "α": "a", "ο": "o", "ε": "e", "ι": "i", "κ": "k", "ρ": "p",
    "τ": "t", "υ": "u", "χ": "x", "ν": "v",
    "’": "'", "‘": "'",
})

# Zero-width / invisible separators (written as escapes so the source has no invisible literals).
# fold_text also drops every category-Cf character, so this set is belt-and-suspenders.
ZERO_WIDTH = {
    "\u200b", "\u200c", "\u200d", "\u200e", "\u200f", "\u2060", "\u2061", "\u2062",
    "\u2063", "\u2064", "\ufeff", "\u00ad", "\u180e", "\u2009", "\u200a", "\u202f",
}

# --------------------------------------------------------------------------- normalization

def normalize_hex(value: str) -> str:
    """Normalize a hex color to lowercase #rrggbb. Drops an alpha channel if present."""
    v = value.lstrip("#").lower()
    if len(v) in (3, 4):
        v = "".join(ch * 2 for ch in v[:3])
    elif len(v) == 8:
        v = v[:6]
    return f"#{v}"


def fold_text(text: str) -> str:
    """Fold a string for evasion-resistant matching: compatibility-normalize, strip format and
    combining characters, casefold, and map common homoglyphs to ASCII."""
    text = unicodedata.normalize("NFKC", text)
    text = unicodedata.normalize("NFKD", text)
    out = []
    for ch in text:
        if ch in ZERO_WIDTH:
            continue
        cat = unicodedata.category(ch)
        if cat in ("Mn", "Cf"):
            continue
        out.append(ch)
    return "".join(out).casefold().translate(CONFUSABLES)


def collapse_ws(text: str) -> str:
    return WS_PATTERN.sub(" ", text).strip()


def squash(text: str) -> str:
    """Remove every non-alphanumeric character — defeats separator-based splitting."""
    return re.sub(r"[^a-z0-9]", "", text)


def strip_comments(text: str) -> str:
    text = HTML_COMMENT_PATTERN.sub(" ", text)
    return CSS_JS_COMMENT_PATTERN.sub(" ", text)


def strip_tags(text: str) -> str:
    return TAG_PATTERN.sub(" ", text)


# --------------------------------------------------------------------------- extraction

def _channel(raw: str) -> int:
    raw = raw.strip()
    if raw.endswith("%"):
        val = round(255 * float(raw[:-1]) / 100)
    else:
        val = round(float(raw))
    return max(0, min(255, val))


def _hue_degrees(value: str, unit: str | None) -> float:
    h = float(value)
    unit = (unit or "deg").lower()
    if unit == "turn":
        h *= 360.0
    elif unit == "rad":
        h *= 180.0 / 3.141592653589793
    elif unit == "grad":
        h *= 0.9
    return h % 360.0


def style_contexts(text: str, is_css: bool) -> list[str]:
    """Extract the parts of the deliverable that are style-valued (where a bare word can be a color)."""
    contexts: list[str] = []
    if is_css:
        contexts.append(text)
    for m in STYLE_BLOCK_PATTERN.finditer(text):
        contexts.append(m.group(1))
    def unquote(v: str) -> str:
        return v[1:-1] if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0] else v

    for m in STYLE_ATTR_PATTERN.finditer(text):
        contexts.append(unquote(m.group(1)))
    for m in COLOR_ATTR_PATTERN.finditer(text):
        contexts.append("x:" + unquote(m.group(1)))  # attribute value as a pseudo-declaration
    for m in SCRIPT_BLOCK_PATTERN.finditer(text):
        for a in SCRIPT_COLOR_ASSIGN_PATTERN.finditer(m.group(1)):
            contexts.append("x:" + a.group(1))
    return contexts


# CSS properties whose values legitimately contain non-color words that collide with color names
# (e.g. a font family literally named "White Grotesk") — skipped for named-color token scanning.
NAMED_SCAN_SKIP_PROPS = {"font-family", "font", "content", "grid-template-areas", "counter-reset",
                         "counter-increment", "animation-name", "transition-property", "quotes"}


def extract_colors(text: str, is_css: bool) -> list[str]:
    found: set[str] = set()
    # Scrub fragment ids that would false-positive as short hex (href="#add", url(#fade)).
    text = FRAGMENT_ATTR_PATTERN.sub('=""', text)
    text = URL_FRAGMENT_PATTERN.sub("url()", text)
    for m in HEX_PATTERN.finditer(text):
        found.add(normalize_hex(m.group(0)))
    for m in RGB_PATTERN.finditer(text):
        try:
            r, g, b = (_channel(m.group(i)) for i in (1, 2, 3))
        except ValueError:
            continue
        found.add(f"#{r:02x}{g:02x}{b:02x}")
    for m in HSL_PATTERN.finditer(text):
        try:
            h = _hue_degrees(m.group(1), m.group(2))
            s = float(m.group(3)) / 100.0
            lt = float(m.group(4)) / 100.0
        except ValueError:
            continue
        r, g, b = colorsys.hls_to_rgb(h / 360.0, max(0.0, min(1.0, lt)), max(0.0, min(1.0, s)))
        found.add(f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}")
    for m in ATTR_HEX_PATTERN.finditer(text):
        found.add(normalize_hex(m.group(1)))
    # Named colors: only in style-valued contexts, only in value position, quoted strings stripped.
    for ctx in style_contexts(text, is_css):
        for decl in CSS_DECL_PATTERN.finditer(ctx):
            prop = decl.group(1).lower()
            if prop in NAMED_SCAN_SKIP_PROPS:
                continue
            value = re.sub(r"(\"[^\"]*\"|'[^']*')", " ", decl.group(2))
            for token in re.findall(r"[a-zA-Z]{3,20}", value):
                hexval = NAMED_COLORS.get(token.lower())
                if hexval:
                    found.add(hexval)
    return sorted(found)


def extract_fonts(text: str, is_css: bool) -> list[str]:
    fonts: set[str] = set()

    def add_families(value: str) -> None:
        for fam in value.split(","):
            fam = fam.strip().strip("\"'").strip()
            if fam and not re.match(r"^[\d.]", fam):
                fonts.add(fam)

    for ctx in style_contexts(text, is_css):
        for decl in CSS_DECL_PATTERN.finditer(ctx):
            prop = decl.group(1).lower()
            if prop == "font-family":
                add_families(decl.group(2))
            elif prop == "font":
                # shorthand: families follow the (mandatory) size token
                m = re.search(r"(?:\d[\w.%]*(?:\s*/\s*[\w.%]+)?)\s+(.+)$", decl.group(2).strip())
                if m:
                    add_families(m.group(1))
    for m in re.finditer(r"\bfont-family\s*=\s*([\"'])(.*?)\1", text, re.IGNORECASE):
        add_families(m.group(2))
    return sorted(fonts)


def decode_embedded_payloads(text: str, max_payloads: int = 20) -> tuple[list[str], list[str]]:
    """Decode base64/percent-encoded data URIs and atob() literals. Returns (decoded texts, notes)."""
    decoded: list[str] = []
    notes: list[str] = []
    count = 0
    for m in DATA_URI_B64_PATTERN.finditer(text):
        if count >= max_payloads:
            break
        raw = re.sub(r"\s+", "", m.group(2))
        try:
            blob = base64.b64decode(raw + "=" * (-len(raw) % 4), validate=False)
        except (binascii.Error, ValueError):
            continue
        count += 1
        if blob[:8].startswith(BINARY_MAGICS) or b"\x00" in blob[:256]:
            notes.append(f"embedded raster/binary data URI ({m.group(1)}) — not pixel-audited")
            continue
        try:
            decoded.append(blob.decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            notes.append(f"embedded data URI ({m.group(1)}) is not UTF-8 text — not audited")
    for m in DATA_URI_TEXT_PATTERN.finditer(text):
        if count >= max_payloads:
            break
        count += 1
        decoded.append(urllib.parse.unquote(m.group(2)))
    for m in ATOB_PATTERN.finditer(text):
        if count >= max_payloads:
            break
        try:
            blob = base64.b64decode(m.group(1) + "=" * (-len(m.group(1)) % 4), validate=False)
            decoded.append(blob.decode("utf-8", errors="strict"))
            count += 1
        except (binascii.Error, ValueError, UnicodeDecodeError):
            continue
    return decoded, notes


# --------------------------------------------------------------------------- checks

def scan_hard_nos(text: str, hard_nos: list[dict]) -> list[dict]:
    """Scan every recoverable text form for each Hard-NO pattern."""
    stripped = strip_comments(text)
    visible = html_lib.unescape(strip_tags(stripped))
    forms = [
        fold_text(collapse_ws(text)),                        # raw, attributes included
        fold_text(collapse_ws(html_lib.unescape(text))),     # entity-decoded raw
        fold_text(collapse_ws(visible)),                     # visible text (tags/comments gone)
    ]
    squashed_forms = [squash(f) for f in forms]
    hits = []
    for entry in hard_nos:
        pattern = str(entry.get("pattern", "")).strip()
        if not pattern:
            continue
        folded = fold_text(collapse_ws(pattern))
        squashed = squash(folded)
        found = any(folded in f for f in forms) or (squashed and any(squashed in f for f in squashed_forms))
        if found:
            hits.append({"pattern": pattern, "why": entry.get("why", "")})
    return hits


# Fabricated-metric / social-proof claim patterns. Each finds (snippet) candidates in visible text.
CLAIM_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("star rating", re.compile(
        r"\b[0-5]\.\d\s*(?:/\s*\d[\d,]*\+?|out of 5|★|⭐|\+?\s*stars?\b|-star\b|\s*star\b|\s*rating\b)",
        re.IGNORECASE)),
    ("star rating", re.compile(r"\b(?:rated|rating(?: of)?)\s*:?\s*[0-5]\.\d\b", re.IGNORECASE)),
    ("count claim", re.compile(
        r"\b\d[\d,]{0,6}\+\s*(?:happy\s+|satisfied\s+|five[- ]star\s+|5[- ]star\s+)?"
        r"(?:clients?|customers?|reviews?|projects?|users?|companies|brands|teams|members|"
        r"installs?|downloads?|orders?|bookings?|rentals?|years)\b", re.IGNORECASE)),
    ("trusted-by claim", re.compile(r"\btrusted by\b[^.!?\n<]{0,40}?\d[\d,]*\+?", re.IGNORECASE)),
    ("star glyphs", re.compile(r"[★⭐]{3,}")),
    ("percent claim", re.compile(
        r"\b\d{1,3}(?:\.\d)?%\s*(?:of\s+)?(?:customer|client|user|satisfaction|uptime|accuracy|"
        r"success|five[- ]star|renewal|retention)", re.IGNORECASE)),
    ("number-one claim", re.compile(r"(?:^|\s)#\s?1\s+(?:rated|choice|in\b|for\b)", re.IGNORECASE)),
]


def scan_claims(text: str, approved: list[str]) -> tuple[list[str], list[str]]:
    """Find quantitative marketing claims in visible text; split into (approved, unverified)."""
    stripped = strip_comments(text)
    visible = collapse_ws(html_lib.unescape(strip_tags(stripped)))
    folded_visible = fold_text(visible)
    approved_folded = [fold_text(collapse_ws(a)) for a in approved if str(a).strip()]
    found: list[str] = []
    seen: set[str] = set()
    for label, pattern in CLAIM_PATTERNS:
        for m in pattern.finditer(folded_visible):
            snippet = collapse_ws(m.group(0))
            key = squash(snippet)
            if key in seen:
                continue
            seen.add(key)
            found.append(snippet)
    ok, bad = [], []
    for snippet in found:
        s = fold_text(snippet)
        if any(s in a or a in s for a in approved_folded):
            ok.append(snippet)
        else:
            bad.append(snippet)
    return ok, bad


def near_miss(color: str, lock_colors: list[str], tolerance: int = 24) -> str | None:
    """If an out-of-lock color is within `tolerance` on every RGB channel of a lock color, name it."""
    try:
        r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        return None
    best, best_dist = None, tolerance + 1
    for lc in lock_colors:
        lr, lg, lb = (int(lc[i:i + 2], 16) for i in (1, 3, 5))
        dist = max(abs(r - lr), abs(g - lg), abs(b - lb))
        if 0 < dist < best_dist:
            best, best_dist = lc, dist
    return best


# --------------------------------------------------------------------------- lock + main

def load_lock(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["colors"] = sorted({normalize_hex(c) for c in data.get("colors", [])})
    data.setdefault("hardNos", [])
    data.setdefault("typography", [])
    data.setdefault("claims", [])
    return data


def audit_deliverable(paths: list[Path], lock: dict) -> dict:
    colors_found: set[str] = set()
    fonts_found: set[str] = set()
    hard_no_hits: dict[str, dict] = {}
    claims_ok: list[str] = []
    claims_bad: list[str] = []
    unverifiable: list[str] = []
    notes: list[str] = []

    for path in paths:
        raw_bytes = path.read_bytes()
        if raw_bytes[:8].startswith(BINARY_MAGICS) or b"\x00" in raw_bytes[:1024]:
            unverifiable.append(
                f"{path.name}: binary/unsupported format — the audit only reads HTML/CSS/SVG text; "
                "a format it cannot read cannot pass"
            )
            continue
        text = raw_bytes.decode("utf-8", errors="replace")
        is_css = path.suffix.lower() == ".css" or "<" not in text

        if EXTERNAL_STYLESHEET_PATTERN.search(text) or CSS_IMPORT_PATTERN.search(text):
            unverifiable.append(
                f"{path.name}: external stylesheet/@import — colors outside this file cannot be "
                "audited; inline the styles or pass the CSS file as an additional argument"
            )
        if EXTERNAL_SCRIPT_PATTERN.search(text):
            unverifiable.append(
                f"{path.name}: external script — styles set by code outside this file cannot be audited"
            )
        if IFRAME_PATTERN.search(text):
            unverifiable.append(f"{path.name}: iframe embeds content the audit cannot see")

        texts = [text]
        payloads, payload_notes = decode_embedded_payloads(text)
        texts.extend(payloads)
        notes.extend(payload_notes)

        for t in texts:
            t_no_comments = strip_comments(t)  # colors hidden in comments are dead code, but scan both
            # Entity-decoded pass too: browsers decode &#35;ff0000 inside attribute values.
            for scan_text in (t, t_no_comments, html_lib.unescape(t)):
                colors_found.update(extract_colors(scan_text, is_css))
            fonts_found.update(extract_fonts(t_no_comments, is_css))
            for hit in scan_hard_nos(t, lock["hardNos"]):
                hard_no_hits.setdefault(hit["pattern"], hit)
            ok, bad = scan_claims(t, lock["claims"])
            claims_ok.extend(ok)
            claims_bad.extend(bad)

    if not colors_found and not unverifiable:
        unverifiable.append(
            "no colors found in the deliverable — either it is unstyled or its colors live "
            "somewhere the audit cannot see; a deliverable whose palette cannot be verified cannot pass"
        )

    lock_colors = lock["colors"]
    colors_out = [c for c in sorted(colors_found) if c not in lock_colors]
    near_misses = {}
    for c in colors_out:
        nm = near_miss(c, lock_colors)
        if nm:
            near_misses[c] = nm

    fonts_out: list[str] = []
    if lock["typography"]:
        allowed = {f.casefold() for f in lock["typography"]} | GENERIC_FONT_FAMILIES
        fonts_out = [f for f in sorted(fonts_found) if f.casefold() not in allowed]

    # de-dup claims preserving order
    def dedup(items: list[str]) -> list[str]:
        seen, out = set(), []
        for i in items:
            if i not in seen:
                seen.add(i)
                out.append(i)
        return out

    claims_bad = dedup(claims_bad)
    passed = not colors_out and not hard_no_hits and not claims_bad and not fonts_out and not unverifiable

    return {
        "deliverablePath": str(paths[0]) if len(paths) == 1 else [str(p) for p in paths],
        "colorsFound": sorted(colors_found),
        "colorsOutOfLock": colors_out,
        "nearMisses": near_misses,
        "fontsFound": sorted(fonts_found),
        "fontsOutOfLock": fonts_out,
        "hardNoHits": [hard_no_hits[k]["pattern"] for k in hard_no_hits],
        "hardNoDetails": [{"pattern": v["pattern"], "why": v["why"]} for v in hard_no_hits.values()],
        "claimsApproved": dedup(claims_ok),
        "unverifiedClaims": claims_bad,
        "unverifiable": unverifiable,
        "notes": notes,
        "pass": passed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one or more deliverable files against a revüe design-system lock."
    )
    parser.add_argument("deliverable", type=Path, nargs="+",
                        help="Path(s) to HTML/CSS/SVG deliverable files (pass linked CSS too).")
    parser.add_argument("--lock", type=Path, required=True, help="Path to a lock JSON file.")
    parser.add_argument("--json", action="store_true",
                        help="Print the outputAudit object as JSON instead of a human report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for p in args.deliverable:
        if not p.exists():
            print(f"FAIL: deliverable not found: {p}")
            return 2
    if not args.lock.exists():
        print(f"FAIL: lock file not found: {args.lock}")
        return 2
    try:
        lock = load_lock(args.lock)
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid lock JSON: {exc}")
        return 2

    audit = audit_deliverable(args.deliverable, lock)
    audit["lockPath"] = str(args.lock)

    if args.json:
        print(json.dumps(audit, indent=2))
        return 0 if audit["pass"] else 1

    if audit["pass"]:
        print(
            f"PASS: {', '.join(str(p) for p in args.deliverable)} — "
            f"{len(audit['colorsFound'])} colors found, all in lock; no Hard-NO hits; "
            "no unverified claims."
        )
        return 0

    print("FAIL")
    for c in audit["colorsOutOfLock"]:
        nm = audit["nearMisses"].get(c)
        suffix = f" (near-miss of {nm} — still out of lock)" if nm else ""
        print(f"- color out of lock: {c}{suffix}")
    for f in audit["fontsOutOfLock"]:
        print(f"- font out of lock: {f}")
    for hit in audit["hardNoDetails"]:
        why = f" — {hit['why']}" if hit["why"] else ""
        print(f"- Hard NO hit: '{hit['pattern']}'{why}")
    for claim in audit["unverifiedClaims"]:
        print(f"- unverified metric claim: '{claim}' — not in the lock's approved claims list")
    for reason in audit["unverifiable"]:
        print(f"- unverifiable: {reason}")
    for note in audit["notes"]:
        print(f"- note: {note}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
