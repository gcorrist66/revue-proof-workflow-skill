# Release Notes

## v1.0.0

Turned revüe from a reviewer into a guided creative-production skill with a failsafe at every seam.
Adds four pillars on top of the v0.6.0 review engine; every pillar is self-enforcing (blocks or caps
the verdict, never just advises), and every pre-v1.0 run artifact stays valid.

- **Pillar 1 — required creative brief** (`references/creative-brief.md`): before any
  creative-production work, `assets/intake-template.md`'s four sections (deliverable + format,
  sources incl. "handoff page read?", design-system lock, Hard NOs) must be complete. A missing field
  blocks generation and returns one batched request, not a drip of questions.
- **Pillar 2 — options + reject-refine** (`references/options-and-refine.md`): creative generation
  returns 2–3 distinct, lock-compliant concepts, never one default direction. Rejecting a concept
  requires keep/kill/change feedback, which is folded into the brief before the next round —
  convergence target is ≤ 3 rounds, matching `references/converge.md`'s pass budget.
- **Pillar 3 — design-system lock + output audit (scaffolding)**
  (`references/design-system-lock.md`, `references/output-audit.md`, `scripts/validate-output.py`):
  a machine-checkable color/typography/Hard-NO lock, and a first working audit script that extracts
  colors from an HTML/CSS/SVG deliverable and scans for Hard-NO text, exiting non-zero on a violation.
  This is the non-adversarial first pass — evasion resistance (obfuscated text, CSS variables, encoded
  Hard NOs) is explicitly out of scope for v1.0; see `HANDOFF-TO-FABLE.md`.
- **Pillar 4 — model routing** (`references/model-routing.md`): `fast` (Haiku 4.5) for every gate and
  validator, `standard` (Sonnet 5) for creative generation and board synthesis, `deep` (Fable 5) for
  ambiguous judgment, `deep-coding` (Opus 4.8) for heavy coding. `scripts/validate-run.py` rejects a
  run where a known gate step is tagged anything other than `fast`.
- Schema (`assets/revue-run.schema.json`): adds `produces` (`review` | `creative-production`, default
  `review`), `brief`, `designSystemLock`, `options`, `optionFeedback`, `outputAudit`, and per-step
  `modelTier`/`model` on `trace` entries.
- `scripts/validate-run.py`: for `"produces": "creative-production"` runs, requires a complete brief
  (batched into one failure line), 2–3 distinct lock-compliant options, and (under `--strict`, before a
  `ship` verdict) `outputAudit.pass == true`. Runs without `produces`, or tagged `review`, are
  unaffected — every pre-v1.0 golden fixture still validates unchanged.
- `SKILL.md`: Operating Contract now runs the brief gate, options gate, output audit, and model
  routing at the right points in the pipeline; Mode Selector notes the review-vs-creative-production
  track; new Model Routing section; Resource Map updated.
- New fixtures: `examples/worked-creative-production.json` (full brief → options → output-audit →
  `ship` golden, the first `ship`-verdict golden in the suite), `examples/lock-fixture.json`,
  `examples/deliverable-pass.html`, `examples/deliverable-fail.html`.
- `scripts/run-evals.py`: 14 new cases (34 total) — the creative-production golden, plus rejections for
  an incomplete brief, too few/too many options, a non-lock-compliant option, duplicate concepts, a
  failing or missing output audit before ship, a mistagged gate step, and an unknown model tier; plus
  `scripts/validate-output.py` pass/fail smoke tests.

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

## v0.6.0

Made it trustworthy to share: the skill now proves its own guarantees.

- `scripts/run-evals.py`: an eval suite (20 cases) that asserts golden reviews across all modes
  validate and reach the expected verdict, that every failure mode is rejected (dead-end verdict,
  false ship, thin evidence, missing source, missing freshness marker, bad path owner), and that the
  fixed bugs stay fixed (plural "screenshots" accepted; "ship with changes" not misread as "ship").
- `.github/workflows/evals.yml`: CI runs the suite on every push and pull request.
- New golden fixtures span the modes: `examples/worked-product-shaping.json`,
  `examples/worked-client-delivery.json` (joining the design and implementation examples).
- README documents the eval suite and carries the CI status badge.

## Next investigation

For a future version, inspect the local Vega workflow service as a source of patterns worth borrowing
(role clarity, blackboard claims, observable run history). Keep environment-specific paths, service
endpoints, and internal project codenames out of this public repo; record them only in local,
untracked notes.
