# Release Notes

## v0.1.0

Initial public-ready package.

- MIT license.
- Initial revüe logo assets.
- Brand notes.
- Proof-first handoff workflow.
- Mode selector for design, product, implementation, client delivery, and platform build work.
- Design/Figma handoff reference.
- Approval-gate reference.
- Evidence schema.
- Board-style verdict model.
- Handoff, intake, verification, and stakeholder-summary templates.
- Handoff validation script.

## v0.2.0 direction

Added v3ga/Vega-inspired workflow guidance:

- Anti-generic review pass.
- Lightweight run-state / blackboard template.
- Vega pattern reference for platform-build work.
- Clear distinction between useful workflow patterns and heavyweight runtime features.

## v0.3.0

Unified the best of Panely, HiveRunner, and Vega into one skill instead of three tools.

- Review board (`references/review-board.md`): reviewer panelists with shared inputs and
  non-negotiables (honesty, evidence, exact-deliverable, anti-generic, approval-gate), converging on
  one verdict. Sourced from the Panely panelist model.
- Run contract (`references/run-contract.md`, `assets/revue-run.schema.json`): schema-versioned
  `revue.review.v1` result artifact and a dry-run validation gate. Sourced from the HiveRunner
  external-runner contract.
- Declarative run spec (`examples/sample-run.revue.yaml`) shaped for Vega `validate`/`run` compatibility.
- `scripts/validate-run.py`: stdlib validator for the run artifact, with strict dry-run/ship rules.
- Rewrote `references/vega-patterns.md` to reflect the real Vega (YAML DSL, typed/timed event stream,
  Erlang-style supervision listed as an explicit "do not borrow").
- Fixed `scripts/render-handoff.py` to emit Mode (and, with `--design`, a Scorecard and Stakeholder
  Summary) so its output passes `validate-evidence.py --strict`.
- Redrawn logo: check badge anchored on the final `e` with a white halo; balanced smiling `ü`;
  matching square app-icon mark.
- Verdict faces: the mark now expresses the outcome — smile (`ship`), soft smile
  (`ship with changes`), flat (`caution`), frown (`block`) — with a color-coded badge. See
  `assets/logo-state-*.svg` and `references/board-verdict-schema.md`.

## v0.4.0

Made the rigor self-enforcing so an average agent gets a good review on the first try.

- `references/self-check.md`: a mandatory pre-verdict gate — evidence floor (>= 3 cited observations),
  freshness guard, exact-deliverable check, verdict consistency, and assumption-dependent verdicts.
- `references/inspection-checklists.md`: per-mode procedure for how to actually gather evidence, not
  just what the output should contain.
- Operating Contract now requires evidence-gathering, the evidence floor, and the self-check before
  any verdict; forbids "reviewed/verified/works" claims about anything not directly observed.
- Validators upgraded: `validate-evidence.py` patterns are stem-tolerant (plurals match) and the
  ship-conflict check is scoped to avoid false positives; both validators now require an evidence
  freshness marker under `--strict`. `validate-run.py` adds an evidence floor (>= 3, incl. a source and
  a limitation), a board minimum, and assumption-dependent verdict support.
- Worked examples for imitation: `examples/worked-design-handoff.md`, `examples/worked-implementation-review.md`.

## v0.5.0

Converge, don't loop. Stops the "caution every run" failure by making revüe a closer, not a grader.

- `references/converge.md`: triage every finding into fix / prove / decide; do the fix and prove items
  in the same pass instead of returning them as blockers; batch the human decisions into one minimal
  block; and pair any non-`ship` verdict with an explicit, owner-tagged path to ship.
- Do not re-review unchanged work: compare an `inputsFingerprint`; if nothing changed, the verdict
  stands and the run jumps to the decision block — no token-burning re-grade. Loop guard: the same
  blocker twice = stop and name the decision that must be made.
- `validate-run.py`: a non-`ship` verdict now fails validation unless it carries a `pathToShip` or
  `decisionsNeeded`; `pathToShip` items must name an owner (`agent` or `human`).
- Schema adds `pathToShip`, `decisionsNeeded`, `changedSinceLastRun`, `inputsFingerprint`,
  `previousVerdict`, and the assumption-dependent verdict fields.
- Worked example: `examples/worked-converge-vip.json` (unchanged-since-last-run short-circuit + path to ship).

## Next investigation

For a future version, inspect the local Vega workflow service as a source of patterns worth borrowing
(role clarity, blackboard claims, observable run history). Keep environment-specific paths, service
endpoints, and internal project codenames out of this public repo; record them only in local,
untracked notes.
