---
name: revue-proof-workflow
description: Proof-first review-board workflow for turning ambiguous requests, product ideas, design work, site changes, operational tasks, and delivery reviews into structured revüe handoffs. Runs a small board of reviewer panelists (critique, aggressive, conservative, proof, stakeholder, synthesis) over shared inputs and non-negotiables, then returns a single ship/caution/block verdict with evidence. Use when the user asks to "run this through revüe", "review this", "make this workflow proof-first", "prepare a handoff", "decide ship/caution/block", "run the review board", "look at Panely/HiveRunner/Vega style workflows", needs a design/Figma/client handoff, or wants a practical board-style review with assumptions, exact deliverable proof, risks, approvals, and next actions.
---

# revüe Proof Workflow

Use this skill to convert messy work into a clear, verified handoff. Favor concrete evidence, visible
assumptions, a real review board over a single generic pass, and a direct decision over abstract planning.

## Operating Contract

1. Restate the intended outcome in one sentence.
2. Identify the mode and stage, and whether the run is a **review** of existing work or **creative
   production** (revüe generating something new). Tag `"produces": "creative-production"`
   (`references/run-contract.md`) for the latter.
3. Separate facts from assumptions. Label assumptions explicitly.
4. Define the exact deliverable format and proof required before claiming success.
5. For creative-production work, run the required brief gate (`references/creative-brief.md`,
   `assets/intake-template.md`) before generating anything — including **tier** (`Standard` /
   `Premium` / `Custom`), which sets the craft bar, routes the model, and sets the audit bar. If a
   required field is missing, stop and return one batched request for exactly what's missing — never
   start on the parts that are ready and drip-feed questions about the rest.
6. Surface approval gates before making external, destructive, paid, or public changes.
7. Gather evidence with `references/inspection-checklists.md` for the active mode. Meet the evidence
   floor: at least three concrete, cited observations taken from the actual artifact, each with how and
   when it was captured. If you cannot inspect it, say so and cap the verdict at `caution` or `block`.
8. Run the review board (`references/review-board.md`) for design, product, or stakeholder-facing work:
   shared inputs, shared non-negotiables, distinct panelist lanes, one synthesized verdict.
9. For creative-production work, generate 2–3 distinct, lock-compliant concepts
   (`references/options-and-refine.md`) — never a single default direction. For Premium tier, every
   concept must also be checked against the elevate bar (`references/elevate.md`) before it is shown.
   Fold reject feedback (keep/kill/change) into the brief before generating the next round.
10. For creative-production work, run the output audit (`references/output-audit.md`,
    `scripts/validate-output.py --tier <site tier>`) against the design-system lock
    (`references/design-system-lock.md`) before any `ship` verdict — Premium tier requires
    `elevatePass` too. If the brief declared a structure spec, also run brief-conformance
    (`references/brief-conformance.md`, `scripts/validate-conformance.py`).
11. Route each step to a model tier (`references/model-routing.md`): gates and validators always run
    `fast`; creative generation and board synthesis run `standard`, escalating to `deep` for Premium
    tier; genuinely ambiguous judgment escalates to `deep`; heavy coding escalates to `deep-coding`;
    Custom tier is human-led — the model may draft, but a human signs off (`tierSignoff`) before ship.
12. Produce a final verdict: `ship`, `ship with changes`, `caution`, or `block`. If the verdict would
    change under a stated assumption, name the assumption and give both outcomes.
13. Before presenting, run the self-check (`references/self-check.md`) on your own draft, and run
    `scripts/validate-evidence.py` (or `scripts/validate-run.py`) if a handoff file exists.
14. Converge, don't loop (`references/converge.md`). Triage every finding into fix / prove / decide;
    do the fix and prove items this pass instead of returning them as blockers; batch the decisions the
    human must make into one minimal block; and pair any non-`ship` verdict with an explicit path to
    ship. Do not re-review an artifact that has not changed since its last verdict — say the verdict
    stands and move to the decision block.

Do not claim verification unless evidence exists. If the evidence is unavailable, say what is missing
and what would prove it. Never write "reviewed", "verified", or "works" about something you did not
directly observe this session.

## Mode Selector

Pick one mode before shaping the work. Infer the mode from the request when possible; do not wait for
the user to name it.

- `design-handoff`: design files, Figma, Canva, mockups, screenshots, brand polish, client-facing design packages. Read `references/design-handoff.md`.
- `product-shaping`: product concepts, platform workflows, feature definitions, roadmap options.
- `implementation-review`: code, local apps, scripts, technical changes, QA findings.
- `client-delivery`: artifacts intended for a named client or stakeholder.
- `platform-build`: revüe/Panely/HiveRunner/Vega-style internal workflow platform work.

Mode triggers:

- Use `design-handoff` for Figma, Canva, landing page mockups, PNG/SVG/PDF visual exports, editable files, design links, client visual review, brand polish, mobile/desktop states, or design source packages.
- Use `implementation-review` for code, repo, tests, build, local server, deploy readiness, bug, script, database, or API work.
- Use `product-shaping` for feature ideas, scope, roadmap, MVP, customer workflow, pricing later, or product strategy.
- Use `client-delivery` when the recipient is named and the task is mainly about presenting a usable artifact.
- Use `platform-build` when working on revüe, Panely, HiveRunner, Vega, or the all-in-one workflow platform.

If the user names a specific stakeholder, apply the stakeholder test: can that person use the result
without a live explanation?

Every mode above runs in one of two tracks: **review** (default) — checking work that already exists —
or **creative production** — revüe designing or building something new. Creative-production work always
starts with the brief gate (`references/creative-brief.md`) regardless of which mode it runs under.

Every creative-production run also carries a **site tier** — `Standard`, `Premium`, or `Custom` — set
in the brief. Tier is orthogonal to mode: a `design-handoff` or `client-delivery` run can be any tier.
See `references/creative-brief.md`'s tier cascade table for what each tier changes.

## Workflow

### 1. Intake

Capture the job in this shape:

- Request: what the user asked for.
- Owner/audience: who needs the result.
- Inputs: files, links, tools, notes, screenshots, repos, or prior artifacts.
- Constraints: brand, style, budget, time, approvals, "do not" boundaries.
- Exact deliverable: file type, link type, share state, or format the stakeholder asked for.
- Success: what must be visibly true and usable by the stakeholder at the end.

Use `assets/intake-template.md` when the user needs a reusable intake artifact. For a repeatable run,
declare it as a spec using `examples/sample-run.revue.yaml`.

For creative-production requests, intake IS the brief gate: fill in `assets/intake-template.md`'s five
required sections (including tier) and do not proceed to Shape until `references/creative-brief.md`'s
completeness check passes. A missing field blocks with one batched request, not a partial start.

### 2. Shape

Turn the request into a working contract:

- Scope in / scope out.
- Main risks.
- Open questions.
- Working recommendation.
- Proof plan.
- Ship threshold: what must exist for `ship` instead of `caution`.

Read `references/workflow-contract.md` when the task is broad, multi-step, or likely to drift.

For creative, product, or client-facing work, read `references/review-board.md` and
`references/anti-generic-review.md`, and reject the first obvious answer before recommending direction.

### 3. Build

Execute only the work inside the contract. Keep changes narrow and reversible. When building product or
design work, preserve the user's style and workflow mentality unless the user explicitly changes direction.

For creative-production work, generate 2–3 distinct, lock-compliant concepts
(`references/options-and-refine.md`) rather than one default direction. When a concept is rejected,
require keep/kill/change feedback and fold it into the brief before generating the next round — never
regenerate from memory of the conversation alone. For Premium tier, generation runs at `deep` model
tier and every concept is also checked against the elevate craft bar (`references/elevate.md`) before
it is shown — a concept that only clears Standard does not get presented as a Premium option.

For revüe itself, prefer practical operator surfaces:

- compact dashboards over marketing pages
- evidence-backed cards over vague summaries
- approvals and blockers near the action that needs them
- persistent handoff artifacts after every meaningful run

When revüe is used for longer work, maintain run state using `assets/run-state-template.json`, or the
structured run artifact in `references/run-contract.md`: current claim, artifacts, evidence, blockers,
trace, and verdict.

### 4. Prove

Follow the mode's procedure in `references/inspection-checklists.md` to gather proof step by step, and
meet the evidence floor before writing a verdict. Collect evidence proportional to risk:

- Local file work: file paths, validation script results, rendered previews, screenshots, or diffs.
- Website/app work: live route, local route, screenshot, browser check, build/test output, console status.
- Data/workflow work: source query, exported artifact, schema check, row counts, or audit trail.
- Strategy/review work: cited inputs, assumption list, risk register, and decision record.

For design handoffs, prove the requested source format, editability, preview fidelity, mobile/desktop
states, and shareability. A PNG/SVG/package is not equivalent to a Figma file unless the user requested
that substitute or the handoff labels it as an interim package.

Use `references/evidence-schema.md` for evidence categories. Use `scripts/validate-evidence.py` to check
a Markdown handoff, or serialize the review as a `revue.review.v1` artifact
(`references/run-contract.md`) and check it with `scripts/validate-run.py`. Validation is a gate, not an
afterthought: a review can always be dry-run validated before any external action.

For creative-production work, run the output audit before any `ship` verdict:
`python3 scripts/validate-output.py <deliverable> --lock <lock.json> --tier <site tier>` checks the
deliverable's actual colors, fonts, and text against the design-system lock
(`references/design-system-lock.md`, `references/output-audit.md`), plus the elevate craft heuristics
for Premium (`references/elevate.md`). `scripts/validate-run.py --strict` refuses a `ship` verdict on a
`"produces": "creative-production"` run unless `outputAudit.pass` is `true`; Premium additionally
requires `outputAudit.elevatePass`, and Custom requires a `tierSignoff` naming a human. If the brief
declared a structure spec, also run `python3 scripts/validate-conformance.py <deliverable> --structure
<structure.json>` (`references/brief-conformance.md`) — required before `ship` whenever declared.

For platform-build work, read `references/vega-patterns.md` before proposing revüe changes. Borrow
patterns such as the review board (Panely), the schema-versioned run contract with a dry-run gate
(HiveRunner), and the declarative spec plus timed trace (Vega); do not copy heavyweight runtime features
unless the user is explicitly building a runtime.

### 5. Handoff

Return the result in this order:

1. Outcome
2. Mode
3. Verdict
4. Evidence
5. Scorecard, when the selected mode defines one
6. Stakeholder summary, when a client/reviewer is involved
7. Assumptions
8. Risks / blockers
9. Decisions needed
10. Next action

Use `assets/handoff-template.md` for manual drafting or `scripts/render-handoff.py` for a deterministic
Markdown skeleton (`--design` includes the scorecard and stakeholder summary).

### 6. Review

When asked to review, run the board (`references/review-board.md`), then the self-check
(`references/self-check.md`) before presenting, and lead with defects or blockers. Then converge
(`references/converge.md`): fix what you can, ask only what you must, and give the path to ship. Use
this verdict scale:

- `ship`: evidence supports release/use in the exact requested deliverable format.
- `ship with changes`: safe enough if listed fixes are made.
- `caution`: material uncertainty remains; proceed only with explicit acceptance.
- `block`: missing proof, unacceptable risk, broken workflow, or required approval is absent.

Read `references/board-verdict-schema.md` for the full decision model.

## Approval Gates

Read `references/approval-gates.md` before actions that could publish, send, deploy, charge, delete,
overwrite, message another person, or alter external systems. If approval is missing, stop at a prepared
draft or preview.

## Model Routing

Read `references/model-routing.md` to pick the model tier for each step: `fast` (Haiku 4.5) for every
gate and validator, `standard` (Sonnet 5) for creative generation and board synthesis, `deep` (Fable 5)
for genuinely ambiguous judgment calls, and `deep-coding` (Opus 4.8) for heavy coding work. Gates and
validators must run `fast` without exception — `scripts/validate-run.py` rejects a run where a known
gate step is tagged anything else. Site tier also routes creative generation specifically: `Standard`
stays `standard`, `Premium` escalates to `deep` (enforced — `scripts/validate-run.py` rejects a Premium
run whose `options-generation` step isn't tagged `deep`), and `Custom` is human-led.

## Resource Map

- `references/converge.md`: converge on ship — fix/prove/decide triage, path to ship, no re-review of unchanged work, pass budget.
- `references/self-check.md`: mandatory pre-verdict gate — evidence floor, freshness, verdict consistency, assumption-dependent verdicts.
- `references/inspection-checklists.md`: per-mode procedure for how to actually gather the evidence.
- `references/review-board.md`: the reviewer panelists, shared inputs, and non-negotiables (Panely model).
- `references/run-contract.md`: schema-versioned run artifact and dry-run gate (HiveRunner model).
- `references/vega-patterns.md`: Vega/v3ga declarative-spec and timed-trace patterns worth borrowing.
- `references/workflow-contract.md`: scope, assumptions, and proof contract.
- `references/anti-generic-review.md`: reject obvious AI-generic first answers before choosing a direction.
- `references/approval-gates.md`: when to pause for approval.
- `references/evidence-schema.md`: what counts as proof.
- `references/board-verdict-schema.md`: ship/caution/block decision rules.
- `references/design-handoff.md`: Figma/design/client handoff proof checklist.
- `references/creative-brief.md`: Pillar 1 — the required, blocking creative brief for any creative-production run, including the tier cascade (Standard/Premium/Custom → craft bar, model routing, audit bar).
- `references/options-and-refine.md`: Pillar 2 — 2–3 distinct lock-compliant concepts, and the keep/kill/change reject-refine loop.
- `references/design-system-lock.md`: Pillar 3 — the machine-checkable color/type/Hard-NO/claims lock format.
- `references/output-audit.md`: Pillar 3 — the evasion-resistant, fail-closed audit of a finished deliverable against the lock before `ship`, plus the Premium elevate heuristics (`--tier premium`).
- `references/elevate.md`: the Premium craft bar — full-bleed hero + legibility scrim, display type system, editorial restraint, repeating signature motif, desktop+mobile+sticky bar. What's machine-checked vs. judged.
- `references/brief-conformance.md`: structure check — required sections present and ordered, forbidden elements absent, required placeholders present — against the brief's declared `structure` spec.
- `references/model-routing.md`: Pillar 4 — fast/standard/deep/deep-coding model tiers and which steps run at each, plus site-tier routing (Standard → standard, Premium → deep, Custom → human-led).
- `assets/intake-template.md`: reusable intake form; now doubles as the required creative brief (five fields, including tier) for creative-production work.
- `assets/run-state-template.json`: lightweight blackboard/run-state artifact.
- `assets/revue-run.schema.json`: JSON schema for the `revue.review.v1` run artifact, including `brief` (with `tier` and optional `structure`), `options`, `designSystemLock`, `outputAudit` (with `elevateChecks`/`elevatePass`), `conformance`, `tierSignoff`, and per-step `modelTier`.
- `assets/verification-matrix-template.md`: proof checklist.
- `assets/handoff-template.md`: final handoff format.
- `assets/stakeholder-summary-template.md`: concise non-technical reviewer note.
- `examples/sample-run.revue.yaml`: declarative run spec (Vega-compatible authoring format).
- `examples/worked-design-handoff.md`: a full worked design review to imitate.
- `examples/worked-implementation-review.md`: a full worked code/QA review to imitate.
- `examples/worked-creative-production.json`: a full worked creative-production run (brief → options → output audit → ship) to imitate — Standard tier.
- `examples/worked-premium-production.json`: the Premium-tier worked exemplar — brief with `tier: "Premium"`, three concepts with only the Premium-bar one kept, `outputAudit.elevatePass: true`, a passing `conformance` result, `ship`. Paired with `examples/premium-exemplar.html` and `examples/premium-lock.json`.
- `examples/dogfood/run.json` + `examples/dogfood/winner.html`: the Standard-tier worked exemplar (clean, functional, on-brand, no elevate layer) — see Pillar 3 dogfood notes below.
- `examples/lock-fixture.json`, `examples/deliverable-pass.html`, `examples/deliverable-fail.html`: fixtures for `scripts/validate-output.py`.
- `examples/structure-fixture.json`, `examples/conformance-pass.html`, `examples/conformance-fail.html`: fixtures for `scripts/validate-conformance.py`.
- `examples/redteam-*.html`: red-team fixtures — deliverables that actively try to sneak past the output audit; the eval suite proves each is rejected. `examples/redteam-original-failure.html` is the exact failure class v1.0 exists to prevent, and doubles as the off-palette anti-pattern `references/elevate.md` points to.
- `examples/dogfood/`: a real end-to-end v1.0 pipeline run on revüe's own brand — brief gate blocked then completed, three concepts, audit-rejected draft, audited winner, `ship with changes` run artifact.
- `scripts/render-handoff.py`: create a Markdown handoff skeleton (`--design` for the design scorecard).
- `scripts/render-stakeholder-summary.py`: create a stakeholder-ready summary.
- `scripts/validate-evidence.py`: check required handoff sections and evidence markers.
- `scripts/validate-run.py`: validate a `revue.review.v1` run artifact against the schema and gate rules, including the brief/options/output-audit gates for creative-production runs and the tier cascade (Premium elevatePass, Custom tierSignoff, brief-conformance).
- `scripts/validate-output.py`: evasion-resistant, fail-closed audit of an HTML/CSS/SVG deliverable against a design-system lock — colors in any syntax, fonts, obfuscated Hard NOs, fabricated-metric claims, and unverifiable content; `--tier premium` adds the elevate craft heuristics; exits non-zero on a violation.
- `scripts/validate-conformance.py`: check a deliverable against the brief's declared structure spec — required sections present and ordered, forbidden elements absent, required placeholders present; exits non-zero on a violation.
- `scripts/make-installer.py`: generate the self-contained `apply-revue-v<version>.sh` installer, which recreates the tree and refuses to finish unless the full eval suite passes inside it.
- `docs/v1.0-acceptance-report.md`: the six v1.0 acceptance criteria, each mapped to the eval case that proves it.
