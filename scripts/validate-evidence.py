#!/usr/bin/env python3
"""Validate that a revüe handoff contains required proof sections and evidence.

v0.4.0: patterns are stem-tolerant (plurals match), the ship-conflict check is scoped to strong
negative signals to avoid false positives, and --strict requires an evidence freshness marker.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "Outcome",
    "Verdict",
    "Evidence",
    "Assumptions",
    "Risks / Blockers",
    "Decisions Needed",
    "Next Action",
]

VERDICT_PATTERN = re.compile(
    r"Verdict:\s*(ship with changes|ship|caution|block|pending)\b",
    re.IGNORECASE,
)

# Scoped to strong, unambiguous "not done / substitute only" signals. Bare words like "missing" or
# "blocker" were removed because they appear in resolved contexts and caused false positives.
SHIP_CONFLICT_PATTERN = re.compile(
    r"("
    r"not verified|not created|no verified|no native|"
    r"could not (?:open|verify|confirm|run|build)|"
    r"unverified|only an? (?:png|svg|preview|draft|mock)|interim (?:package|export)"
    r")",
    re.IGNORECASE,
)

# Stem-tolerant: plurals and common variants match.
DESIGN_PROOF_PATTERNS = {
    "source_format": re.compile(r"(figma|canva|svgs?|pdfs?|html|\.fig|source files?|share links?)", re.IGNORECASE),
    "editability": re.compile(r"(editabl\w*|layers?|text nodes?|source structure|native)", re.IGNORECASE),
    "preview": re.compile(r"(previews?|screenshots?|pngs?|dimensions?|captures?|[0-9]{2,5}\s*[xX]\s*[0-9]{2,5})", re.IGNORECASE),
    "states": re.compile(r"(desktop|mobile|tablet|states?|artboards?|frames?)", re.IGNORECASE),
}

# A capture/recency marker so a review can't claim proof with no provenance.
FRESHNESS_PATTERN = re.compile(
    r"(captured|verified by|as of|this session|screenshots?|snapshot|observed|inspected|"
    r"run at|dated|today|live)",
    re.IGNORECASE,
)

DESIGN_SCORECARD_CHECKS = [
    "Exact requested format",
    "Source editability",
    "Desktop/mobile states",
    "Preview fidelity",
    "Brand fit",
    "Stakeholder access",
    "Developer clarity",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a revüe handoff Markdown file.")
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--mode", choices=["general", "design-handoff"], default="general")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require a Mode section, an evidence freshness marker, and reject ship verdicts with unresolved-blocker language.",
    )
    return parser.parse_args()


def section_present(markdown: str, section: str) -> bool:
    return bool(re.search(rf"^##\s+{re.escape(section)}\s*$", markdown, re.MULTILINE))


def section_body(markdown: str, section: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$(.*?)(^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def verdict_value(markdown: str) -> str | None:
    match = VERDICT_PATTERN.search(markdown)
    return match.group(1).lower() if match else None


def main() -> int:
    args = parse_args()
    if not args.handoff.exists():
        print(f"FAIL: file not found: {args.handoff}")
        return 2

    markdown = args.handoff.read_text(encoding="utf-8")
    failures: list[str] = []

    for section in REQUIRED_SECTIONS:
        if not section_present(markdown, section):
            failures.append(f"missing section: {section}")

    if args.strict and not section_present(markdown, "Mode"):
        failures.append("missing section: Mode")

    verdict = verdict_value(markdown)
    if not verdict:
        failures.append("missing valid verdict line")

    evidence_body = section_body(markdown, "Evidence")
    if not evidence_body:
        failures.append("evidence section is empty")

    if args.strict and evidence_body and not FRESHNESS_PATTERN.search(evidence_body):
        failures.append("evidence lacks a capture/recency marker (how/when it was observed)")

    if args.strict and verdict == "ship":
        review_text = "\n".join(
            [evidence_body, section_body(markdown, "Risks / Blockers"), section_body(markdown, "Assumptions")]
        )
        if SHIP_CONFLICT_PATTERN.search(review_text):
            failures.append("ship verdict conflicts with unresolved blocker or substitute-deliverable language")

    if args.mode == "design-handoff":
        combined = "\n".join(
            [
                evidence_body,
                section_body(markdown, "Outcome"),
                section_body(markdown, "Assumptions"),
                section_body(markdown, "Risks / Blockers"),
                section_body(markdown, "Scorecard"),
            ]
        )
        for label, pattern in DESIGN_PROOF_PATTERNS.items():
            if not pattern.search(combined):
                failures.append(f"design-handoff proof missing: {label}")

        if args.strict:
            scorecard_body = section_body(markdown, "Scorecard")
            stakeholder_body = section_body(markdown, "Stakeholder Summary")
            if not scorecard_body:
                failures.append("design-handoff missing section: Scorecard")
            if not stakeholder_body:
                failures.append("design-handoff missing section: Stakeholder Summary")
            for check in DESIGN_SCORECARD_CHECKS:
                if check not in scorecard_body:
                    failures.append(f"design scorecard missing check: {check}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: revüe handoff contains required sections, verdict, and mode-appropriate evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
