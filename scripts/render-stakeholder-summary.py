#!/usr/bin/env python3
"""Render a concise revüe stakeholder summary."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a stakeholder-ready revüe summary.")
    parser.add_argument("--title", default="Stakeholder Summary")
    parser.add_argument("--ready", default="")
    parser.add_argument("--review", default="")
    parser.add_argument("--not-final", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--next-step", default="")
    return parser.parse_args()


def section(name: str, value: str) -> str:
    return f"## {name}\n\n{value.strip()}\n"


def main() -> int:
    args = parse_args()
    parts = [
        f"# {args.title.strip()}\n",
        section("What is ready", args.ready),
        section("What to review", args.review),
        section("What is not final yet", args.not_final),
        section("Decision needed", args.decision),
        section("Next step", args.next_step),
    ]
    print("\n".join(parts).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
