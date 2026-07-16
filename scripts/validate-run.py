#!/usr/bin/env python3
"""Validate a revüe run artifact (revue.review.v1) — stdlib only, no dependencies.

v0.4.0: adds an evidence floor (>= 3 entries), an evidence freshness marker, a board minimum
(>= 3 lanes when a board is present), and assumption-dependent verdict support.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VALID_MODES = {
    "design-handoff",
    "product-shaping",
    "implementation-review",
    "client-delivery",
    "platform-build",
}

VALID_VERDICTS = {"ship", "ship with changes", "caution", "block"}
VALID_STATUS = {"pass", "partial", "fail", "not applicable"}

FRESHNESS_PATTERN = re.compile(
    r"(captured|verified by|as of|this session|screenshot|snapshot|observed|inspected|"
    r"run at|dated|today|live|exit code|output)",
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
    parser = argparse.ArgumentParser(description="Validate a revüe run artifact (revue.review.v1).")
    parser.add_argument("run", type=Path, help="Path to a run JSON file.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce dry-run gate rules, ship consistency, evidence freshness, and assumption-dependent verdicts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.run.exists():
        print(f"FAIL: file not found: {args.run}")
        return 2

    try:
        data = json.loads(args.run.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON: {exc}")
        return 2

    failures: list[str] = []

    if data.get("schema") != "revue.review.v1":
        failures.append("schema must be 'revue.review.v1'")

    mode = data.get("mode")
    if mode not in VALID_MODES:
        failures.append(f"mode must be one of {sorted(VALID_MODES)}")

    for field in ("request", "stakeholder"):
        if not str(data.get(field, "")).strip():
            failures.append(f"missing or empty field: {field}")

    inputs = data.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        failures.append("inputs must be a non-empty list")

    # Evidence floor: at least three concrete observations, including one limitation.
    evidence = data.get("evidence")
    if not isinstance(evidence, list) or len(evidence) < 3:
        failures.append("evidence floor: at least 3 evidence entries are required")
    else:
        if not any(e.get("category") == "limitation" for e in evidence):
            failures.append("evidence must include at least one 'limitation' entry")
        if not any(e.get("category") == "source" for e in evidence):
            failures.append("evidence must include at least one 'source' entry")

    # Board minimum when a board is present.
    board = data.get("board")
    if isinstance(board, list) and 0 < len(board) < 3:
        failures.append("board present but has fewer than 3 panelist lanes")

    verdict = data.get("verdict") or {}
    verdict_value = verdict.get("value")
    if verdict_value not in VALID_VERDICTS:
        failures.append(f"verdict.value must be one of {sorted(VALID_VERDICTS)}")
    if not str(verdict.get("reason", "")).strip():
        failures.append("verdict.reason is required")

    scorecard = data.get("scorecard") or []
    for row in scorecard:
        if row.get("status") not in VALID_STATUS:
            failures.append(f"scorecard status must be one of {sorted(VALID_STATUS)}: {row.get('check')!r}")

    if mode == "design-handoff":
        if not scorecard:
            failures.append("design-handoff requires a scorecard")
        else:
            present = {row.get("check") for row in scorecard}
            for check in DESIGN_SCORECARD_CHECKS:
                if check not in present:
                    failures.append(f"design scorecard missing check: {check}")

    if args.strict:
        # Freshness: at least one evidence statement carries a capture/recency marker.
        if isinstance(evidence, list) and not any(
            FRESHNESS_PATTERN.search(str(e.get("statement", ""))) for e in evidence
        ):
            failures.append("evidence lacks a capture/recency marker (how/when it was observed)")

        # Assumption-dependent verdict must name what it flips to.
        if verdict.get("assumptionDependent"):
            flips = verdict.get("flipsTo")
            if flips not in VALID_VERDICTS:
                failures.append("assumptionDependent verdict must set 'flipsTo' to a valid verdict")
            if not str(verdict.get("assumption", "")).strip():
                failures.append("assumptionDependent verdict must name the 'assumption'")

        dry_run = data.get("dryRun", True)
        gates = data.get("gates") or []
        if dry_run:
            for gate in gates:
                if isinstance(gate, dict) and gate.get("executed"):
                    failures.append(f"dryRun is true but gate marked executed: {gate.get('name')}")
        if verdict_value == "ship":
            if any(row.get("status") == "fail" for row in scorecard):
                failures.append("ship verdict invalid while a scorecard check is 'fail'")
            if dry_run and [g for g in gates if isinstance(g, str)]:
                failures.append("ship verdict invalid while gates are unresolved under dryRun")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: revüe run artifact is valid" + (" (strict)" if args.strict else "") + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
