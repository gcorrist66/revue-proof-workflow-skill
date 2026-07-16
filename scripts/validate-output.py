#!/usr/bin/env python3
"""Validate a creative-production deliverable (HTML/CSS/SVG) against a revüe design-system lock.

Pillar 3 (output-audit) — FIRST working version. Extracts literal hex colors from the deliverable,
checks them against the lock's allowed color list, and scans the deliverable's raw text for literal
Hard-NO patterns. Exits non-zero on any violation. Stdlib only, no dependencies.

v1.0 scope: exact hex match (3/4-digit expanded to 6, 8-digit alpha truncated) and rgb()/rgba()
normalized to hex; case-insensitive substring match for Hard NOs. Does not resolve CSS variables,
hsl(), named CSS colors, or obfuscated/encoded text — see references/output-audit.md for what is
intentionally out of scope for this pass; evasion-resistant hardening is tracked in
HANDOFF-TO-FABLE.md.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HEX_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
RGB_PATTERN = re.compile(
    r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*[\d.]+\s*)?\)",
    re.IGNORECASE,
)


def normalize_hex(value: str) -> str:
    """Normalize a hex color to lowercase #rrggbb. Drops an alpha channel if present."""
    v = value.lstrip("#").lower()
    if len(v) in (3, 4):
        v = "".join(ch * 2 for ch in v[:3])
    elif len(v) == 8:
        v = v[:6]
    return f"#{v}"


def extract_colors(text: str) -> list[str]:
    found: set[str] = set()
    for m in HEX_PATTERN.finditer(text):
        found.add(normalize_hex(m.group(0)))
    for m in RGB_PATTERN.finditer(text):
        r, g, b = (int(m.group(i)) for i in (1, 2, 3))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            found.add(f"#{r:02x}{g:02x}{b:02x}")
    return sorted(found)


def load_lock(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["colors"] = sorted({normalize_hex(c) for c in data.get("colors", [])})
    data.setdefault("hardNos", [])
    return data


def scan_hard_nos(text: str, hard_nos: list[dict]) -> list[dict]:
    hits = []
    lowered = text.lower()
    for entry in hard_nos:
        pattern = str(entry.get("pattern", "")).strip()
        if pattern and pattern.lower() in lowered:
            hits.append({"pattern": pattern, "why": entry.get("why", "")})
    return hits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a deliverable against a revüe design-system lock."
    )
    parser.add_argument("deliverable", type=Path, help="Path to an HTML/CSS/SVG deliverable file.")
    parser.add_argument("--lock", type=Path, required=True, help="Path to a lock JSON file.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the outputAudit object as JSON instead of a human report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.deliverable.exists():
        print(f"FAIL: deliverable not found: {args.deliverable}")
        return 2
    if not args.lock.exists():
        print(f"FAIL: lock file not found: {args.lock}")
        return 2

    text = args.deliverable.read_text(encoding="utf-8", errors="replace")
    try:
        lock = load_lock(args.lock)
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid lock JSON: {exc}")
        return 2

    colors_found = extract_colors(text)
    colors_out_of_lock = [c for c in colors_found if c not in lock["colors"]]
    hard_no_hits = scan_hard_nos(text, lock["hardNos"])
    passed = not colors_out_of_lock and not hard_no_hits

    audit = {
        "deliverablePath": str(args.deliverable),
        "lockPath": str(args.lock),
        "colorsFound": colors_found,
        "colorsOutOfLock": colors_out_of_lock,
        "hardNoHits": [h["pattern"] for h in hard_no_hits],
        "pass": passed,
    }

    if args.json:
        print(json.dumps(audit, indent=2))
        return 0 if passed else 1

    if passed:
        print(
            f"PASS: {args.deliverable} — {len(colors_found)} colors found, all in lock; "
            "no Hard-NO hits."
        )
        return 0

    print("FAIL")
    if colors_out_of_lock:
        print(f"- colors out of lock: {', '.join(colors_out_of_lock)}")
    for hit in hard_no_hits:
        why = f" — {hit['why']}" if hit["why"] else ""
        print(f"- Hard NO hit: '{hit['pattern']}'{why}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
