#!/usr/bin/env python3
"""Validate a revüe run artifact (revue.review.v1) — stdlib only, no dependencies.

v0.4.0: adds an evidence floor (>= 3 entries), an evidence freshness marker, a board minimum
(>= 3 lanes when a board is present), and assumption-dependent verdict support.

v1.0.0: adds the creative-production gates. Runs tagged "produces": "creative-production" must carry
a complete brief (references/creative-brief.md), 2-3 distinct lock-compliant options
(references/options-and-refine.md), and (before a 'ship' verdict, under --strict) a passing output
audit (references/output-audit.md). Also validates that every trace step's modelTier is a known value,
and that known gate/validator steps are tagged 'fast' (references/model-routing.md). Runs without a
'produces' field, or tagged 'review', are unaffected — this keeps every pre-v1.0 run artifact valid.

v1.1.0: brief.tier (Standard/Premium/Custom) joins the batched brief-completeness check. Before a
'ship' verdict (--strict): a Premium-tier run requires outputAudit.elevatePass == true — a deliverable
that only clears the Standard bar is flagged, not shipped; a Custom-tier run requires a top-level
tierSignoff naming a human. When the brief declares a 'structure' spec (references/brief-conformance.md),
a 'ship' verdict also requires a passing top-level 'conformance' object. 'conformance-check' joins the
fast-tagged gate steps.
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

VALID_PRODUCES = {"review", "creative-production"}
VALID_MODEL_TIERS = {"fast", "standard", "deep", "deep-coding"}
VALID_SITE_TIERS = {"Standard", "Premium", "Custom"}

# Step names that are self-enforcing gates/validators — references/model-routing.md requires these
# run at the 'fast' tier whenever a modelTier is recorded for them.
GATE_STEPS = {
    "brief-gate",
    "design-system-lock-check",
    "options-lock-check",
    "output-audit",
    "conformance-check",
    "self-check",
    "validate-run",
    "validate-output",
    "validate-evidence",
}


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

    # v1.0.0: creative-production gates (brief completeness + options rule). A run with no 'produces'
    # field, or 'produces': 'review', is unaffected — this is what keeps pre-v1.0 runs valid.
    produces = data.get("produces", "review")
    if produces not in VALID_PRODUCES:
        failures.append(f"produces must be one of {sorted(VALID_PRODUCES)}")

    # Anti-evasion: a run cannot dodge the creative-production gates by simply not declaring itself.
    # If the run carries creative-production fields, it must be tagged as one.
    if produces != "creative-production":
        creative_fields = [f for f in ("brief", "options", "optionFeedback", "outputAudit", "designSystemLock") if f in data]
        if creative_fields:
            failures.append(
                "creative-production fields present ("
                + ", ".join(creative_fields)
                + ") but 'produces' is not 'creative-production' — declare the run so its gates apply"
            )

    if produces == "creative-production":
        brief = data.get("brief") or {}
        missing: list[str] = []
        if not str(brief.get("deliverable", "")).strip():
            missing.append("deliverable")
        if not str(brief.get("format", "")).strip():
            missing.append("format")
        if brief.get("tier") not in VALID_SITE_TIERS:
            missing.append(f"tier (must be one of {sorted(VALID_SITE_TIERS)})")
        if not isinstance(brief.get("sources"), list) or not brief.get("sources"):
            missing.append("sources")
        if brief.get("handoffPageRead") is not True:
            missing.append("sources.handoffPageRead (must be true — read the target handoff page first)")
        if not str(brief.get("designSystemLock", "")).strip():
            missing.append("designSystemLock")
        if "hardNos" not in brief or not isinstance(brief.get("hardNos"), list):
            missing.append("hardNos (list required; an empty list is fine if none apply)")
        if missing:
            # One batched failure, not one per field — this is the same batching
            # references/creative-brief.md asks the agent to do by hand.
            failures.append("brief incomplete — missing: " + ", ".join(missing))

        lock = data.get("designSystemLock")
        if not isinstance(lock, dict) or not lock.get("colors"):
            failures.append("designSystemLock: missing or has no 'colors'")

        options = data.get("options")
        if not isinstance(options, list) or not (2 <= len(options) <= 3):
            found = len(options) if isinstance(options, list) else 0
            failures.append(f"creative generation requires 2-3 options (found {found})")
        else:
            bad_shape = any(
                not isinstance(opt, dict)
                or not all(str(opt.get(k, "")).strip() for k in ("id", "summary", "distinctionAxis"))
                for opt in options
            )
            if bad_shape:
                failures.append("each option requires id, summary, and distinctionAxis")
            else:
                if any(opt.get("lockCompliant") is not True for opt in options):
                    failures.append("every presented option must have lockCompliant == true")
                # Normalized dedupe: case/punctuation/whitespace paraphrases are still duplicates.
                axes = [
                    re.sub(r"[^a-z0-9]", "", str(opt.get("distinctionAxis", "")).casefold())
                    for opt in options
                ]
                if len(set(axes)) != len(axes):
                    failures.append("options are not distinct: duplicate distinctionAxis")

    # v1.0.0: gate/validator steps must run at the 'fast' model tier (references/model-routing.md).
    # v1.1.0: Premium tier routes creative generation to 'deep' (the elevate bar is the kind of
    # ambiguous, expensive-to-get-wrong judgment references/model-routing.md reserves for that tier).
    site_tier = (data.get("brief") or {}).get("tier")
    for step in data.get("trace") or []:
        if not isinstance(step, dict):
            continue
        tier = step.get("modelTier")
        if tier is None:
            continue
        if tier not in VALID_MODEL_TIERS:
            failures.append(
                f"trace step {step.get('step')!r} modelTier must be one of {sorted(VALID_MODEL_TIERS)}"
            )
        elif step.get("step") in GATE_STEPS and tier != "fast":
            failures.append(
                f"gate step {step.get('step')!r} must be tagged modelTier 'fast', got {tier!r}"
            )
        elif step.get("step") == "options-generation" and site_tier == "Premium" and tier != "deep":
            failures.append(
                "options-generation must be tagged modelTier 'deep' for Premium tier "
                f"(references/model-routing.md), got {tier!r}"
            )

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
            if produces == "creative-production":
                audit = data.get("outputAudit")
                if not isinstance(audit, dict) or audit.get("pass") is not True:
                    failures.append("ship verdict requires outputAudit.pass == true (references/output-audit.md)")
                elif any(
                    audit.get(k)
                    for k in ("colorsOutOfLock", "hardNoHits", "unverifiedClaims", "fontsOutOfLock", "unverifiable")
                ):
                    # Anti-evasion: a hand-edited audit that flips pass to true while still listing
                    # violations is internally inconsistent. Re-running scripts/validate-output.py is
                    # the source of truth; this catches the cheap forgery.
                    failures.append(
                        "outputAudit is internally inconsistent: pass == true but violations are listed "
                        "— re-run scripts/validate-output.py"
                    )

                # Tier sets the audit bar (references/creative-brief.md cascade). A Premium-declared
                # deliverable that only clears the Standard bar is flagged, not shipped.
                tier = (data.get("brief") or {}).get("tier")
                if tier == "Premium":
                    elevate_pass = isinstance(audit, dict) and audit.get("elevatePass") is True
                    if not elevate_pass:
                        failures.append(
                            "ship verdict requires outputAudit.elevatePass == true for Premium tier "
                            "(references/elevate.md) — this deliverable meets only the Standard bar; "
                            "re-run scripts/validate-output.py --tier premium"
                        )
                elif tier == "Custom":
                    signoff = data.get("tierSignoff")
                    if not isinstance(signoff, dict) or not str(signoff.get("by", "")).strip():
                        failures.append(
                            "ship verdict requires a top-level tierSignoff.by for Custom tier "
                            "(references/creative-brief.md) — Custom is human-led, not autonomously graded"
                        )

                # Brief-conformance (references/brief-conformance.md) is required before ship only when
                # the brief actually declared a structure spec — not every brief needs one.
                if isinstance(brief, dict) and isinstance(brief.get("structure"), dict):
                    conformance = data.get("conformance")
                    if not isinstance(conformance, dict) or conformance.get("pass") is not True:
                        failures.append(
                            "ship verdict requires conformance.pass == true because brief.structure is "
                            "declared (references/brief-conformance.md) — re-run scripts/validate-conformance.py"
                        )

        # Converge: a non-ship verdict must carry a path to ship (or a decision block).
        if verdict_value and verdict_value != "ship":
            if not (data.get("pathToShip") or data.get("decisionsNeeded")):
                failures.append("non-ship verdict requires a non-empty pathToShip or decisionsNeeded")

    # pathToShip items must name an owner (structural, checked always).
    for item in data.get("pathToShip") or []:
        if isinstance(item, dict) and item.get("owner") not in {"agent", "human"}:
            failures.append("pathToShip item owner must be 'agent' or 'human'")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: revüe run artifact is valid" + (" (strict)" if args.strict else "") + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
