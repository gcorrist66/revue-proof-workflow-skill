# Release Notes

## v1.2.0

Simplifies revüe's operating layer without weakening its proof gates.

- Existing-product fixes, copy refinements, backend simplification, and bounded UI polish now route to
  review/remediation. They no longer trigger a creative brief, tier question, or 2–3 concept round.
- Explicit `premium`, `flagship`, or `custom` language sets the creative tier; the workflow does not ask
  the user to repeat a decision already present in the request.
- Model routing is capability-based and vendor-neutral. A run omits routing metadata when the runtime
  cannot confirm that routing occurred.
- Implementation inspection now covers active account context, loading and completion feedback, plain
  score meaning, a visible target, prioritized fixes, and useful empty states.
- User reports are explicitly separated from direct observations; no-artifact reviews name the proof
  still needed instead of pretending a validator ran. P0/P1/P2 priorities make fix order unambiguous.
- `agents/openai.yaml` adds Codex-facing identity, icons, brand color, and a useful default prompt.
- The self-contained installer excludes the tracked empty `deltest.tmp` scratch file.
- Six new contract evals guard the v1.2 behavior. Total: **108 cases**.

The v1.0/v1.1 validators, adversarial fixtures, and creative-production gates remain backward
compatible.

## v1.1.0

Adds site tiers, the Premium craft layer, and brief-conformance on top of the v1.0 creative-production
pipeline. Every new gate is self-enforcing (blocks or caps the verdict, never just advises), and every
pre-v1.1 run artifact stays valid — the new required brief field (`tier`) only gates
`"produces": "creative-production"` runs, exactly like every other v1.0 brief field.

**Provenance note.** The task's named craft exemplars (`vip-flagship-page.html`, `vip-instance-real.html`)
and the referenced `revue-v1.0-build-handoff.md` were not present in this repo or the session's uploads.
The Premium craft rules were built from the task's own distilled description; the worked Premium
exemplar (`examples/premium-exemplar.html`) is a reconstruction built to satisfy every rule, not a copy
of an original. The Standard exemplar reuses the existing, real `examples/dogfood/winner.html` rather
than fabricating a redundant one. See the provenance note in `docs/v1.1-acceptance-report.md`.

- **Tier field and cascade** (`references/creative-brief.md`): the brief now has five required,
  blocking fields — `deliverable + format`, **`tier`** (`Standard` / `Premium` / `Custom`), `sources`,
  `designSystemLock`, `hardNos`. Tier sets three things at once: the craft bar (Standard = lock
  compliance is the whole bar; Premium = lock compliance plus `references/elevate.md`; Custom =
  human-directed, no template), the model tier (Standard/Premium creative generation run `standard`/
  `deep`; Custom is human-led), and the audit bar (Standard/Premium both require `outputAudit.pass`;
  Premium additionally requires `outputAudit.elevatePass`; Custom requires a `tierSignoff` naming a
  human). `assets/intake-template.md` gets a new required Tier section.
- **Elevate layer** (`references/elevate.md`): the Premium craft bar distilled into six rules —
  full-bleed cinematic hero with a legibility scrim, a serif-display + sans-body type system, editorial
  restraint and negative space, a repeating signature motif, legibility-over-imagery, and
  desktop+mobile+sticky-bar. Four of the six are machine-checked (see below); restraint, the signature
  motif, and true legibility judgment stay a human/board call, documented as such rather than faked.
- **Elevate heuristics in `scripts/validate-output.py`** (`--tier {standard,premium,custom}`, default
  `standard`) — **hardened, scope-aware, fail-closed**: the hero is judged by its own section span plus
  the CSS rules whose selectors reference it (comments stripped first), and must carry imagery, a
  full-bleed treatment (`cover`/viewport-relative height), and a scrim in that same scope — a hidden
  hero, a 1px image, or a scrim declared in an unrelated rule all fail. The type system must be a real
  pairing — a serif-generic display stack attached to headings plus a sans-serif body stack; two
  unrelated sans fonts do not pass. The sticky action bar must be a visible, bottom-anchored element
  that actually contains a CTA — a sticky masthead or decorative fixed strip does not pass. Folds into
  `outputAudit.elevateChecks` + `outputAudit.elevatePass`, and into overall `pass`. `--tier standard`
  (the default) never runs these — Standard-tier work isn't held to a bar it wasn't briefed for.
- **Brief-conformance** (`references/brief-conformance.md`, `scripts/validate-conformance.py`): checks
  a deliverable against an optional `brief.structure` spec — required sections present (via a
  `data-section="name"` or `<section id="name">` convention) and, if declared, in order; forbidden
  markup patterns absent; required placeholders present verbatim (proving a not-yet-known value stayed
  an honest placeholder instead of a silent guess). **Hardened and evasion-resistant**: comments are
  stripped before anything counts; a required section faked as an empty stub or hidden with CSS fails
  as a stub; banned markup is matched on normalized and squashed forms plus class/id-token matching
  (quoting, spacing, case, attribute order, and multi-class values don't dodge a ban); and a required
  placeholder must be *visibly* present — one buried in a `display:none` container while a guessed
  value ships is caught by an ancestor-chain scan and named as exactly that dishonesty.
- **Tier-sets-audit-bar, enforced** (`scripts/validate-run.py`): a `ship` verdict on a Premium-tier run
  requires `outputAudit.elevatePass == true` — a deliverable that only clears the Standard bar is
  flagged, not shipped, with that exact wording in the failure. Custom requires a top-level
  `tierSignoff.by` **naming a real human** — placeholder signoffs (`N/A`, `TBD`, `agent`, ...) are
  rejected. When `brief.structure` is declared, `ship` also requires a passing top-level `conformance`
  object. Premium also requires the `options-generation` trace step to be tagged `modelTier: "deep"`
  (`references/model-routing.md`'s tier-routing rule, structurally enforced). `conformance-check` joins
  the steps that must be tagged `fast`. **Forgery-resistant**: `elevatePass` asserted without (or over
  failing) `elevateChecks`, and a `conformance` object whose `pass` was flipped `true` over listed
  violations, are both rejected as internally inconsistent — the scripts are the source of truth.
- Schema (`assets/revue-run.schema.json`): `brief.tier` (required enum) and optional `brief.structure`;
  new top-level `conformance` and `tierSignoff` objects; `outputAudit.elevateChecks`/`elevatePass`.
- New fixtures: `examples/premium-exemplar.html` + `examples/premium-lock.json` +
  `examples/premium-structure.json`, `examples/worked-premium-production.json` (the first Premium-tier
  `ship` golden), `examples/structure-fixture.json`, `examples/conformance-pass.html`,
  `examples/conformance-fail.html`. `examples/worked-creative-production.json` and
  `examples/dogfood/run.json` gain `brief.tier: "Standard"` (now a required field).
- `scripts/run-evals.py`: **102 cases total** — the 58 pre-v1.1 cases unchanged, 22 tier/elevate/
  conformance correctness cases, 15 v1.1 red-team cases, and 7 Premium-dogfood cases.
- **Red-team fixtures for all three v1.1 failure classes**, each proven REJECTED for the targeted
  reason: `examples/redteam-premium-clean-template.html` (declared Premium, ships clean-template — base
  audit clean, all four elevate rules fail, and a `ship` over that audit is rejected as
  Standard-bar-only), `examples/redteam-premium-gamed.html` (actively games the heuristics with a
  hidden hero + 1px image, a sticky top masthead, and a two-sans "type system" — every fake fails),
  `examples/redteam-conformance-evasion.html` (reformatted banned header, empty stub section, hidden
  placeholder over a guessed phone number, reordered sections — all four caught), and the original
  off-palette generic clone re-asserted against the brand audit. Plus run-level forgeries: bare
  `elevatePass`, `elevatePass` over a failing check, flipped `conformance.pass`, and an `N/A`
  tier signoff — all rejected.
- **Premium dogfood run** (`examples/dogfood-premium/`): the v1.1 pipeline end to end on a Premium
  launch page for the tier system itself — brief with `tier: "Premium"` and a structure spec, concepts
  generated at `deep`, and the tier gate catching the exact target failure: a draft that passed the
  brand audit AND the conformance check but failed all four elevate rules, rebuilt to earn the tier.
  The eval suite proves both directions from the same artifact: flipped to `ship` with the real audits
  it validates; flipped to `ship` over the clean-template draft's audit it is rejected.
- **Fixed**: the named-color/`var()` false positive — CSS custom properties named after color words
  (`--navy`, `--coral`) are no longer misread as the CSS named colors `navy`/`coral`, while a real
  color hidden in a `var()` fallback is still caught. Both directions are eval-guarded.
- **Acceptance report** (`docs/v1.1-acceptance-report.md`): each v1.1 guarantee (tier bar, conformance,
  brand) mapped to the eval case(s) that prove it.

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
- **Pillar 3 — design-system lock + evasion-resistant output audit**
  (`references/design-system-lock.md`, `references/output-audit.md`, `scripts/validate-output.py`):
  a machine-checkable color/typography/Hard-NO/claims lock, enforced by a fail-closed audit built to
  be attacked. Colors are caught in every expressible syntax — hex of any length, legacy hash-less
  attribute hex, comma/space/percentage `rgb()`, `hsl()` in any hue unit, named CSS colors, CSS custom
  properties, gradients, SVG attributes, literal colors in scripts, and colors inside base64/percent-
  encoded data URIs and `atob()` payloads; near-miss shades are labeled with the closest lock color
  and still fail. Hard NOs are caught across tag/comment splits, HTML entities, zero-width joins,
  homoglyph swaps (Cyrillic/Greek), and separator respellings. Fonts are checked against the lock's
  typography. Fabricated-metric patterns (star ratings, "200+ clients", "trusted by 500+", star-glyph
  runs, "#1 rated") fail unless explicitly allowlisted in the lock's `claims` — the original
  fabricated-"4.9 / 200+" failure can no longer ship silently. Anything the audit cannot verify
  (external stylesheets/scripts, iframes, binary formats, a deliverable with no detectable colors)
  fails as unverifiable instead of passing unexamined.
- **Anti-evasion gates in `scripts/validate-run.py`**: a run carrying creative-production fields
  cannot dodge the gates by omitting `"produces": "creative-production"`; a forged `outputAudit`
  (pass flipped `true` over listed violations) is rejected as internally inconsistent; option
  distinctness survives case/punctuation paraphrases.
- **Pillar 4 — model routing** (`references/model-routing.md`): introduced the `fast`, `standard`,
  `deep`, and `deep-coding` capability tiers. v1.2 made these labels vendor-neutral. The validator
  rejects a known gate step tagged anything other than `fast`.
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
- `scripts/run-evals.py`: **58 cases total** — the 20 pre-v1.0 cases unchanged, 14 pillar-gate cases
  (creative-production golden, incomplete-brief batching, option count/shape/compliance/distinctness,
  failing/missing output audit before ship, mistagged gate step, unknown model tier, audit smoke
  tests), 19 red-team cases, and 5 dogfood cases.
- **Red-team fixtures** (`examples/redteam-*.html`): nine deliverables that actively try to sneak past
  the output audit, each proven REJECTED for the specific reason the attack targets — led by
  `examples/redteam-original-failure.html`, a faithful reproduction of the failure class this version
  exists to prevent: a generic template-clone landing page with guessed off-palette colors, an
  off-brand font, generic link text, and a fabricated "4.9 / 200+" metric. Plus four red-team run
  artifacts against `validate-run.py` (undeclared creative run, forged audit, paraphrased duplicate
  concept, stringly-typed `handoffPageRead`) and a control proving a lock-approved metric still passes.
- **Dogfood run** (`examples/dogfood/`): the v1.0 pipeline executed end to end on revüe's own brand —
  the brief gate blocked first with one batched request, three distinct concepts were presented and
  culled by keep/kill/change, the audit caught a genuinely guessed hover shade in draft 1 (labeled a
  near-miss), and the fixed winner shipped `ship with changes` with the audit object attached. All
  five steps are locked in as eval cases.
- **Self-contained installer** (`scripts/make-installer.py` → `dist/apply-revue-v1.0.0.sh`):
  regenerates the full tree from embedded base64 and refuses to finish unless the complete eval suite
  passes inside the applied tree. Verified against a clean directory and a fresh clone; a sabotaged
  tree fails the install.
- **Acceptance report** (`docs/v1.0-acceptance-report.md`): each of the six v1.0 acceptance criteria
  mapped to the eval case(s) that prove it.

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
