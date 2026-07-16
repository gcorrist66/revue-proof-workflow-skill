#!/usr/bin/env python3
"""Validate that a revüe handoff contains required proof sections and evidence."""

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
    r"Verdict:\s*(ship|ship with changes|caution|block|pending)\b",
    re.IGNORECASE,
)

SHIP_CONFLICT_PATTERN = re.compile(
    r"\b("
    r"not verified|not created|missing|blocker|blocked|"
    r"no verified|no native|does not have|could not|"
    r"only .*png|only .*svg|only .*preview|interim"
    r")\b",
    re.IGNORECASE,
)

DESIGN_PROOF_PATTERNS = {
    "source_format": re.compile(r"\b(figma|canva|svg|pdf|html|\.fig|source file|share link)\b", re.IGNORECASE),
    "editability": re.compile(r"\b(editable|editability|layers|text nodes|source structure|native)\b", re.IGNORECASE),
    "preview": re.compile(r"\b(preview|screenshot|png|dimensions?|[0-9]{2,5}\s*x\s*[0-9]{2,5})\b", re.IGNORECASE),
    "states": re.compile(r"\b(desktop|mobile|tablet|state|states|artboards?|frames?)\b", re.IGNORECASE),
}

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
    parser.add_argument(
        "--mode",
        choices=["general", "design-handoff"],
        default="general",
        help="Apply mode-specific proof checks.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require a Mode section and reject ship verdicts with unresolved blocker language.",
    )
    return parser.parse_args()


def section_present(markdown: str, section: str) -> bool:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    return bool(pattern.search(markdown))


def section_body(markdown: str, section: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(section)}\s*$(.*?)(^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
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

    if args.strict and verdict == "ship":
        review_text = "\n".join(
            [
                evidence_body,
                section_body(markdown, "Risks / Blockers"),
                section_body(markdown, "Assumptions"),
            ]
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
