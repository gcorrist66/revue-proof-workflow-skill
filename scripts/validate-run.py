#!/usr/bin/env python3
"""Validate a revüe run artifact (revue.review.v1) — stdlib only, no dependencies.

Checks required fields, verdict validity, evidence completeness, mode-specific scorecard,
and (with --strict) the dry-run and ship-consistency rules from references/run-contract.md.
"""

from __future__ import annotations

import argparse
import json
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
        help="Enforce dry-run gate rules and ship-vs-scorecard/gate consistency.",
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

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        failures.append("evidence must be a non-empty list")
    else:
        if not any(e.get("category") == "limitation" for e in evidence):
            failures.append("evidence must include at least one 'limitation' entry")

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
        dry_run = data.get("dryRun", True)
        gates = data.get("gates") or []
        if dry_run:
            for gate in gates:
                if isinstance(gate, dict) and gate.get("executed"):
                    failures.append(f"dryRun is true but gate marked executed: {gate.get('name')}")
        if verdict_value == "ship":
            if any(row.get("status") == "fail" for row in scorecard):
                failures.append("ship verdict invalid while a scorecard check is 'fail'")
            unresolved = [g for g in gates if isinstance(g, str)] if dry_run else []
            if unresolved:
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
