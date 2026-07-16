# Run Contract

Use this reference when a revüe review should produce a structured, inspectable artifact — not just
prose. It borrows the HiveRunner external-runner contract: a schema-versioned payload in, a
schema-versioned result out, and a dry-run gate that validates the handoff before anything executes.

A run contract lets a revüe review be validated, stored, diffed, or handed to an executor (for
example a Vega workflow) without rewriting it.

## Principle

- One stable **input** shape describes the work to review.
- One stable **result** shape describes the verdict and its evidence.
- **Dry-run first.** A run can always be validated without taking any external, paid, or destructive
  action. `dryRun: true` means "check the handoff, do not execute gates." This is the contract-level
  version of the approval gate.

## Result artifact — `revue.review.v1`

A completed review serializes to this shape (`assets/revue-run.schema.json` is the machine-checkable
version; `scripts/validate-run.py` checks a file against it):

```json
{
  "schema": "revue.review.v1",
  "runId": "vip-marina-figma-2026-07-16",
  "mode": "design-handoff",
  "dryRun": true,
  "request": "Decide if the VIP Marina landing concept is ready to send to the client.",
  "stakeholder": "Client (marina owner)",
  "inputs": [
    { "type": "figma", "ref": "figma.com/design/…", "note": "3 desktop frames, page 1E1E1E" }
  ],
  "constraints": { "brand": "navy/coral/aqua", "format_requested": "figma" },
  "proofRequired": ["exact requested format", "mobile states", "editable source"],
  "gates": ["send-to-client"],
  "board": [
    { "panelist": "critique", "findings": "…", "evidence": ["…"] },
    { "panelist": "aggressive", "findings": "…", "evidence": ["…"] },
    { "panelist": "conservative", "findings": "…", "evidence": ["…"] },
    { "panelist": "proof", "findings": "…", "evidence": ["…"] },
    { "panelist": "stakeholder", "findings": "…", "evidence": ["…"] }
  ],
  "evidence": [
    { "category": "source", "statement": "Native Figma file, page 1E1E1E, 3 desktop frames.", "verified": true },
    { "category": "limitation", "statement": "Layer-level editability inspected visually only.", "verified": false }
  ],
  "scorecard": [
    { "check": "Exact requested format", "status": "pass", "evidence": "Native Figma file" },
    { "check": "Desktop/mobile states", "status": "fail", "evidence": "No mobile frame exists" }
  ],
  "verdict": {
    "value": "caution",
    "reason": "Strong concept, but no mobile state and inconsistent boat lineup across frames.",
    "requiredProof": "Named final desktop frame plus a matching mobile frame.",
    "nextAction": "Pick one final frame, confirm lineup + pricing, build mobile, re-run."
  },
  "trace": [
    { "step": "intake", "durationMs": 0 },
    { "step": "board", "durationMs": 0 },
    { "step": "verdict", "durationMs": 0 }
  ]
}
```

### Required fields

- `schema` must equal `revue.review.v1`.
- `mode` must be one of the SKILL mode ids.
- `request`, `stakeholder`, `inputs` (non-empty), `verdict` are required.
- `verdict.value` must be one of `ship`, `ship with changes`, `caution`, `block`.
- `evidence` must be non-empty and include at least one `limitation` entry (what the review does not prove).
- If `mode` is `design-handoff`, `scorecard` is required and must cover the checks in
  `references/design-handoff.md`.

### Dry-run and gate rules

- With `dryRun: true`, no gate in `gates` may be marked executed. The review stops at a validated draft.
- `verdict.value: ship` is invalid while any `scorecard` entry is `fail`, or while any listed `gate`
  is unresolved. Use `caution` or `block` instead. (`scripts/validate-run.py --strict` enforces this.)

## Authoring spec — `.revue.yaml`

For repeatable work, the run is declared up front as a small YAML spec (see
`examples/sample-run.revue.yaml`). It is intentionally close to a Vega `team.vega.yaml` so the same
run can be validated by `vega validate` and, if desired, executed by `vega run` — revüe stays the
proof-and-review layer, Vega stays the optional executor.

```yaml
schema: revue.run.v1
mode: design-handoff
request: "Decide if the VIP Marina landing concept is ready to send to the client."
stakeholder: "Client (marina owner)"
inputs:
  - type: figma
    ref: "figma.com/design/…"
constraints:
  brand: "navy/coral/aqua"
  format_requested: figma
proof_required:
  - exact requested format
  - mobile states
  - editable source
gates:
  - send-to-client
board: [critique, aggressive, conservative, proof, stakeholder, synthesis]
verdict_scale: [ship, ship with changes, caution, block]
```

## Why this shape

- **HiveRunner** proved that many different executors (Codex, Claude, Gemini, HERMES) can sit behind
  one payload/result schema with a `DRY_RUN` validation path. revüe borrows the schema-and-dry-run
  discipline, not the process management.
- **Vega** proved that a declarative YAML team plus a typed, timed event stream makes a run
  inspectable. revüe borrows the declarative spec and the `trace` timing, not the runtime.
- The result: a review that can be checked before it is trusted, and handed off without being redescribed.
