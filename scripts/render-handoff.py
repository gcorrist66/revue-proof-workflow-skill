#!/usr/bin/env python3
"""Render a revüe handoff Markdown skeleton.

Emits a Mode section, and (with --design) a Scorecard and Stakeholder Summary, so the output
passes scripts/validate-evidence.py --strict (and --mode design-handoff --strict).
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone


VALID_VERDICTS = ("ship", "ship with changes", "caution", "block", "pending")

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
    parser = argparse.ArgumentParser(description="Render a revüe handoff.")
    parser.add_argument("--title", default="revüe Handoff")
    parser.add_argument("--mode", default="", help="Mode id, e.g. design-handoff.")
    parser.add_argument("--outcome", default="")
    parser.add_argument("--verdict", default="pending", choices=VALID_VERDICTS)
    parser.add_argument("--reason", default="")
    parser.add_argument("--next-action", default="")
    parser.add_argument(
        "--design",
        action="store_true",
        help="Include a design-handoff Scorecard and Stakeholder Summary.",
    )
    return parser.parse_args()


def section(name: str, value: str = "") -> str:
    body = value.strip()
    return f"## {name}\n\n{body}\n"


def scorecard_block() -> str:
    rows = "\n".join(f"| {check} |  |  |" for check in DESIGN_SCORECARD_CHECKS)
    return (
        "## Scorecard\n\n"
        "| Check | Status | Evidence |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n"
    )


def main() -> int:
    args = parse_args()
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    parts = [
        f"# {args.title.strip()}\n",
        f"Generated: {generated_at}\n",
        section("Outcome", args.outcome),
        section("Mode", args.mode),
        section("Verdict", f"Verdict: {args.verdict}\n\nReason: {args.reason.strip()}"),
        section("Evidence"),
    ]
    if args.design:
        parts.append(scorecard_block())
        parts.append(section("Stakeholder Summary"))
    parts.extend(
        [
            section("Assumptions"),
            section("Risks / Blockers"),
            section("Decisions Needed"),
            section("Next Action", args.next_action),
        ]
    )
    print("\n".join(parts).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
