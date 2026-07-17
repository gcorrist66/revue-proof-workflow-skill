#!/usr/bin/env python3
"""Validate a deliverable against the brief's structure spec (references/brief-conformance.md) —
hardened, evasion-resistant version.

Checks a deliverable against what the brief actually promised, independent of the design-system lock:
  - required sections are present, non-stub, visible, and (if declared) in the brief's order;
  - forbidden elements the brief banned do not appear — in any quoting/spacing/case/attribute-order
    variant, including multi-class values (`class="nav custom-header"` still hits a
    `class="custom-header"` ban);
  - placeholders the brief marked as not-yet-known are present, VISIBLE, and not entity-masked —
    a placeholder buried in a display:none container while a guessed value shows is a violation.

Section convention: `data-section="name"` (double-, single-, or un-quoted) anywhere in the markup, or
`<section id="name">`. A deliverable that doesn't use the convention shows zero sections, which fails
a brief that requires sections — structure that cannot be verified cannot conform.

Evasion resistance:
  - HTML comments are stripped first — a marker or placeholder inside a comment does not count.
  - A required section whose marker exists but whose span is empty/near-empty (a stub faked to satisfy
    presence) or hidden (display:none / visibility:hidden / zero size) fails as a stub.
  - Forbidden patterns are matched on normalized text (casefolded, whitespace-collapsed,
    quote-unified) and on a separator-squashed form; `class="X"` / `id="X"` bans additionally match X
    as a token inside any multi-valued class/id attribute, in any attribute order.
  - Placeholders are checked entity-decoded (an `&#91;`-masked placeholder still counts as present —
    it renders identically) but must appear at least once OUTSIDE a hidden container.

Stdlib only. Exit 0 = pass, 1 = violation(s), 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
from pathlib import Path

SECTION_MARKER_PATTERN = re.compile(
    r"""\bdata-section\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s"'>]+))""", re.IGNORECASE
)
SECTION_TAG_ID_PATTERN = re.compile(
    r"""<section\b[^>]*\bid\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s"'>]+))""", re.IGNORECASE
)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
CLASS_OR_ID_BAN_PATTERN = re.compile(r"""^\s*<?\s*[\w-]*\s*(class|id)\s*=\s*["']?([\w -]+)["']?\s*>?\s*$""", re.IGNORECASE)
ATTR_VALUE_PATTERN = {
    "class": re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", re.IGNORECASE),
    "id": re.compile(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", re.IGNORECASE),
}
HIDDEN_PATTERN = re.compile(
    r"(display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\.0+)?\s*[;}\"']"
    r"|(?:max-)?(?:width|height)\s*:\s*0(?:px|%)?\s*[;}\"']|\bhidden(?:\s|>|=))",
    re.IGNORECASE,
)
SECTION_BOUNDARY_PATTERN = re.compile(r"<section\b|data-section\s*=|<footer\b|</body", re.IGNORECASE)
STUB_MIN_VISIBLE_CHARS = 20   # a "section" with less visible text than this is a presence-faking stub
SECTION_SPAN_CAP = 20000


def strip_comments(text: str) -> str:
    """Drop HTML comments before checking structure — an authoring note that happens to mention
    `data-section="hero"` (or contain a placeholder) must not count as the real thing."""
    return HTML_COMMENT_PATTERN.sub(" ", text)


def normalize(text: str) -> str:
    """Casefold, unify quotes, collapse whitespace — evasion-resistant comparison form."""
    text = text.replace("'", '"')
    return re.sub(r"\s+", " ", text).casefold()


def squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.casefold())


def _marker_hits(text: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for pattern in (SECTION_MARKER_PATTERN, SECTION_TAG_ID_PATTERN):
        for m in pattern.finditer(text):
            name = next(g for g in m.groups() if g is not None)
            hits.append((m.start(), name.strip()))
    hits.sort(key=lambda h: h[0])
    return hits


def find_sections(text: str) -> list[str]:
    """Section names in document order (first occurrence only, order-preserving)."""
    seen: set[str] = set()
    ordered: list[str] = []
    for _, name in _marker_hits(text):
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _enclosing_tag(text: str, pos: int) -> tuple[str, int, int]:
    start = text.rfind("<", 0, pos)
    end = text.find(">", pos)
    if start == -1 or end == -1:
        return "", pos, pos
    return text[start:end + 1], start, end + 1


def section_spans(text: str) -> dict[str, str]:
    """Map each section name to the raw markup of its FIRST span (marker tag to next boundary)."""
    spans: dict[str, str] = {}
    for pos, name in _marker_hits(text):
        if name in spans:
            continue
        tag, tag_start, tag_end = _enclosing_tag(text, pos)
        boundary = SECTION_BOUNDARY_PATTERN.search(text, tag_end)
        end = boundary.start() if boundary else min(len(text), tag_start + SECTION_SPAN_CAP)
        spans[name] = text[tag_start:end]
    return spans


def stub_sections(text: str, required: list[str]) -> list[str]:
    """Required sections whose span is hidden or has less visible text than the stub floor —
    a marker faked to satisfy the presence check without shipping the section."""
    spans = section_spans(text)
    stubs: list[str] = []
    for name in required:
        span = spans.get(name)
        if span is None:
            continue  # missing entirely — reported by missingSections, not here
        tag = span[:span.find(">") + 1] if ">" in span else span
        visible = re.sub(r"\s+", " ", html_lib.unescape(TAG_PATTERN.sub(" ", span))).strip()
        if HIDDEN_PATTERN.search(tag):
            stubs.append(f"{name} (marker present but the section is hidden)")
        elif len(visible) < STUB_MIN_VISIBLE_CHARS:
            stubs.append(
                f"{name} (marker present but only {len(visible)} visible characters — "
                "a stub is not a section)"
            )
    return stubs


def order_violations(required: list[str], found: list[str]) -> list[str]:
    """Pairwise order check on required sections that are present."""
    position = {name: i for i, name in enumerate(found)}
    violations = []
    for i, a in enumerate(required):
        for b in required[i + 1:]:
            if a in position and b in position and position[a] > position[b]:
                violations.append(f"'{a}' must come before '{b}', found after")
    return violations


def check_forbidden(text: str, forbidden: list[dict]) -> list[dict]:
    """Normalized + squashed + token-aware matching. A ban written as `class="custom-header"` hits
    any quoting/spacing/case variant and any multi-class attribute containing that token."""
    norm_text = normalize(text)
    squashed_text = squash(text)
    hits = []
    for entry in forbidden:
        pattern = str(entry.get("pattern", "")).strip()
        if not pattern:
            continue
        found = normalize(pattern) in norm_text or (squash(pattern) and squash(pattern) in squashed_text)
        if not found:
            m = CLASS_OR_ID_BAN_PATTERN.match(pattern)
            if m:
                attr, banned_value = m.group(1).lower(), m.group(2).strip()
                banned_tokens = set(banned_value.casefold().split())
                for am in ATTR_VALUE_PATTERN[attr].finditer(text):
                    value = next(g for g in am.groups() if g is not None)
                    if banned_tokens <= set(value.casefold().split()):
                        found = True
                        break
        if found:
            hits.append({"pattern": pattern, "why": entry.get("why", "")})
    return hits


VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                 "meta", "param", "source", "track", "wbr"}
OPEN_OR_CLOSE_TAG_PATTERN = re.compile(r"<(/?)([a-zA-Z][\w-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")


def _ancestors_at(text: str, pos: int) -> list[str]:
    """Approximate the open-tag ancestor chain at `pos` with a simple tag stack (no DOM needed).
    Returns the full opening-tag strings still open at that position."""
    stack: list[tuple[str, str]] = []  # (tag name, full tag text)
    for m in OPEN_OR_CLOSE_TAG_PATTERN.finditer(text, 0, pos):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    break
        elif name not in VOID_ELEMENTS and not attrs.rstrip().endswith("/"):
            stack.append((name, m.group(0)))
    return [tag for _, tag in stack]


def check_placeholders(text: str, required: list[str]) -> tuple[list[str], list[str]]:
    """Returns (missing, hidden-only). A placeholder must appear at least once in the entity-decoded
    text, and at least one occurrence must have NO hidden element in its open-tag ancestor chain —
    a placeholder inside a display:none container while a guessed value shows is a violation."""
    decoded = html_lib.unescape(text)
    missing: list[str] = []
    hidden_only: list[str] = []
    for p in required:
        if not p:
            continue
        positions = [m.start() for m in re.finditer(re.escape(p), decoded)]
        if not positions:
            missing.append(p)
            continue
        visible_somewhere = False
        for pos in positions:
            if not any(HIDDEN_PATTERN.search(tag) for tag in _ancestors_at(decoded, pos)):
                visible_somewhere = True
                break
        if not visible_somewhere:
            hidden_only.append(p)
    return missing, hidden_only


def load_structure(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("requiredSections", [])
    data.setdefault("sectionOrder", False)
    data.setdefault("forbiddenElements", [])
    data.setdefault("requiredPlaceholders", [])
    return data


def audit_conformance(paths: list[Path], structure: dict) -> dict:
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in paths)
    text = strip_comments(text)

    found = find_sections(text)
    required = list(structure["requiredSections"])
    missing_sections = [s for s in required if s not in found]
    stubs = stub_sections(text, required)

    violations = order_violations(required, found) if structure.get("sectionOrder") else []

    forbidden_hits = check_forbidden(text, structure["forbiddenElements"])
    missing_placeholders, hidden_placeholders = check_placeholders(
        text, structure["requiredPlaceholders"]
    )

    passed = not (missing_sections or stubs or violations or forbidden_hits
                  or missing_placeholders or hidden_placeholders)

    return {
        "deliverablePath": str(paths[0]) if len(paths) == 1 else [str(p) for p in paths],
        "sectionsFound": found,
        "missingSections": missing_sections,
        "stubSections": stubs,
        "orderViolations": violations,
        "forbiddenHits": [h["pattern"] for h in forbidden_hits],
        "forbiddenDetails": forbidden_hits,
        "missingPlaceholders": missing_placeholders,
        "hiddenPlaceholders": hidden_placeholders,
        "pass": passed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a deliverable against a revüe brief structure spec."
    )
    parser.add_argument("deliverable", type=Path, nargs="+", help="Path(s) to deliverable file(s).")
    parser.add_argument("--structure", type=Path, required=True, help="Path to a structure spec JSON file.")
    parser.add_argument(
        "--json", action="store_true", help="Print the conformance object as JSON instead of a human report."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for p in args.deliverable:
        if not p.exists():
            print(f"FAIL: deliverable not found: {p}")
            return 2
    if not args.structure.exists():
        print(f"FAIL: structure spec not found: {args.structure}")
        return 2
    try:
        structure = load_structure(args.structure)
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid structure JSON: {exc}")
        return 2

    conformance = audit_conformance(args.deliverable, structure)
    conformance["structurePath"] = str(args.structure)

    if args.json:
        print(json.dumps(conformance, indent=2))
        return 0 if conformance["pass"] else 1

    if conformance["pass"]:
        print(
            f"PASS: {', '.join(str(p) for p in args.deliverable)} — "
            f"{len(conformance['sectionsFound'])} sections found, matches brief structure."
        )
        return 0

    print("FAIL")
    for s in conformance["missingSections"]:
        print(f"- missing required section: {s!r}")
    for s in conformance["stubSections"]:
        print(f"- stub/hidden required section: {s}")
    for v in conformance["orderViolations"]:
        print(f"- section order violation: {v}")
    for hit in conformance["forbiddenDetails"]:
        why = f" — {hit['why']}" if hit["why"] else ""
        print(f"- forbidden element present: {hit['pattern']!r}{why}")
    for p in conformance["missingPlaceholders"]:
        print(f"- required placeholder missing (may have been silently guessed instead): {p!r}")
    for p in conformance["hiddenPlaceholders"]:
        print(f"- required placeholder present only inside hidden markup: {p!r} — hiding the "
              "placeholder while showing a guessed value is the exact dishonesty this check exists for")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
