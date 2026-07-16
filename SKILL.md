---
name: revue-proof-workflow
description: Proof-first review-board workflow for turning ambiguous requests, product ideas, design work, site changes, operational tasks, and delivery reviews into structured revüe handoffs. Runs a small board of reviewer panelists (critique, aggressive, conservative, proof, stakeholder, synthesis) over shared inputs and non-negotiables, then returns a single ship/caution/block verdict with evidence. Use when the user asks to "run this through revüe", "review this", "make this workflow proof-first", "prepare a handoff", "decide ship/caution/block", "run the review board", "look at Panely/HiveRunner/Vega style workflows", needs a design/Figma/client handoff, or wants a practical board-style review with assumptions, exact deliverable proof, risks, approvals, and next actions.
---

# revüe Proof Workflow

Use this skill to convert messy work into a clear, verified handoff. Favor concrete evidence, visible
assumptions, a real review board over a single generic pass, and a direct decision over abstract planning.

## Operating Contract

1. Restate the intended outcome in one sentence.
2. Identify the mode and stage.
3. Separate facts from assumptions. Label assumptions explicitly.
4. Define the exact deliverable format and proof required before claiming success.
5. Surface approval gates before making external, destructive, paid, or public changes.
6. Gather evidence with `references/inspection-checklists.md` for the active mode. Meet the evidence
   floor: at least three concrete, cited observations taken from the actual artifact, each with how and
   when it was captured. If you cannot inspect it, say so and cap the verdict at `caution` or `block`.
7. Run the review board (`references/review-board.md`) for design, product, or stakeholder-facing work:
   shared inputs, shared non-negotiables, distinct panelist lanes, one synthesized verdict.
8. Produce a final verdict: `ship`, `ship with changes`, `caution`, or `block`. If the verdict would
   change under a stated assumption, name the assumption and give both outcomes.
9. Before presenting, run the self-check (`references/self-check.md`) on your own draft, and run
   `scripts/validate-evidence.py` (or `scripts/validate-run.py`) if a handoff file exists.
10. Converge, don't loop (`references/converge.md`). Triage every finding into fix / prove / decide;
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
- `assets/intake-template.md`: reusable intake form.
- `assets/run-state-template.json`: lightweight blackboard/run-state artifact.
- `assets/revue-run.schema.json`: JSON schema for the `revue.review.v1` run artifact.
- `assets/verification-matrix-template.md`: proof checklist.
- `assets/handoff-template.md`: final handoff format.
- `assets/stakeholder-summary-template.md`: concise non-technical reviewer note.
- `examples/sample-run.revue.yaml`: declarative run spec (Vega-compatible authoring format).
- `examples/worked-design-handoff.md`: a full worked design review to imitate.
- `examples/worked-implementation-review.md`: a full worked code/QA review to imitate.
- `scripts/render-handoff.py`: create a Markdown handoff skeleton (`--design` for the design scorecard).
- `scripts/render-stakeholder-summary.py`: create a stakeholder-ready summary.
- `scripts/validate-evidence.py`: check required handoff sections and evidence markers.
- `scripts/validate-run.py`: validate a `revue.review.v1` run artifact against the schema and gate rules.
