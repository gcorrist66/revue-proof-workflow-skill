#!/usr/bin/env python3
"""Validate a deliverable against the brief's structure spec — Pillar (brief-conformance), first
working version (references/brief-conformance.md).

Checks a deliverable against what the brief actually promised, independent of the design-system lock:
  - required sections are present, and (if declared) appear in the brief's order;
  - forbidden elements the brief banned do not appear;
  - placeholders the brief marked as not-yet-known are present verbatim, not silently guessed.

Section convention: a section is recognized by `data-section="name"` anywhere in the markup, or by
`<section id="name">`. This is a documented authoring convention, not DOM parsing — a deliverable that
doesn't use it will show as having zero sections, which itself is a legitimate finding.

Non-adversarial scope (references/brief-conformance.md): forbidden-element and placeholder matching are
literal, case-sensitive-for-placeholders substring checks. No attempt to resist evasion (obfuscation,
encoding, DOM tricks) — that hardening is intentionally deferred, matching how scripts/validate-output.py
started before it was hardened.

Stdlib only. Exit 0 = pass, 1 = violation(s), 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DATA_SECTION_PATTERN = re.compile(r'\bdata-section\s*=\s*"([^"]+)"', re.IGNORECASE)
SECTION_TAG_ID_PATTERN = re.compile(r'<section\b[^>]*\bid\s*=\s*"([^"]+)"', re.IGNORECASE)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_comments(text: str) -> str:
    """Drop HTML comments before checking structure — an authoring note that happens to mention
    `data-section="hero"` must not be mistaken for a real section."""
    return HTML_COMMENT_PATTERN.sub(" ", text)


def find_sections(text: str) -> list[str]:
    """Return section names in document order (first occurrence only, order-preserving)."""
    hits: list[tuple[int, str]] = []
    for m in DATA_SECTION_PATTERN.finditer(text):
        hits.append((m.start(), m.group(1)))
    for m in SECTION_TAG_ID_PATTERN.finditer(text):
        hits.append((m.start(), m.group(1)))
    hits.sort(key=lambda h: h[0])
    seen: set[str] = set()
    ordered: list[str] = []
    for _, name in hits:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def order_violations(required: list[str], found: list[str]) -> list[str]:
    """Pairwise order check: for every (a, b) with a before b in `required`, if both are present in
    `found`, a's first occurrence must precede b's. Returns human-readable violation strings."""
    position = {name: i for i, name in enumerate(found)}
    violations = []
    for i, a in enumerate(required):
        for b in required[i + 1:]:
            if a in position and b in position and position[a] > position[b]:
                violations.append(f"'{a}' must come before '{b}', found after")
    return violations


def check_forbidden(text: str, forbidden: list[dict]) -> list[dict]:
    hits = []
    for entry in forbidden:
        pattern = str(entry.get("pattern", "")).strip()
        if pattern and pattern in text:
            hits.append({"pattern": pattern, "why": entry.get("why", "")})
    return hits


def check_placeholders(text: str, required: list[str]) -> list[str]:
    return [p for p in required if p and p not in text]


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

    violations = order_violations(required, found) if structure.get("sectionOrder") else []

    forbidden_hits = check_forbidden(text, structure["forbiddenElements"])
    missing_placeholders = check_placeholders(text, structure["requiredPlaceholders"])

    passed = not missing_sections and not violations and not forbidden_hits and not missing_placeholders

    return {
        "deliverablePath": str(paths[0]) if len(paths) == 1 else [str(p) for p in paths],
        "sectionsFound": found,
        "missingSections": missing_sections,
        "orderViolations": violations,
        "forbiddenHits": [h["pattern"] for h in forbidden_hits],
        "forbiddenDetails": forbidden_hits,
        "missingPlaceholders": missing_placeholders,
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
    for v in conformance["orderViolations"]:
        print(f"- section order violation: {v}")
    for hit in conformance["forbiddenDetails"]:
        why = f" — {hit['why']}" if hit["why"] else ""
        print(f"- forbidden element present: {hit['pattern']!r}{why}")
    for p in conformance["missingPlaceholders"]:
        print(f"- required placeholder missing (may have been silently guessed instead): {p!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
