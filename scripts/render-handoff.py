#!/usr/bin/env python3
"""Render a revüe handoff Markdown skeleton."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone


VALID_VERDICTS = ("ship", "ship with changes", "caution", "block", "pending")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a revüe handoff.")
    parser.add_argument("--title", default="revüe Handoff")
    parser.add_argument("--outcome", default="")
    parser.add_argument("--verdict", default="pending", choices=VALID_VERDICTS)
    parser.add_argument("--reason", default="")
    parser.add_argument("--next-action", default="")
    return parser.parse_args()


def section(name: str, value: str = "") -> str:
    body = value.strip()
    return f"## {name}\n\n{body}\n"


def main() -> int:
    args = parse_args()
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    parts = [
        f"# {args.title.strip()}\n",
        f"Generated: {generated_at}\n",
        section("Outcome", args.outcome),
        section("Verdict", f"Verdict: {args.verdict}\n\nReason: {args.reason.strip()}"),
        section("Evidence"),
        section("Assumptions"),
        section("Risks / Blockers"),
        section("Decisions Needed"),
        section("Next Action", args.next_action),
    ]
    print("\n".join(parts).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
