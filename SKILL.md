---
name: revue-proof-workflow
description: Proof-first workflow skill for turning ambiguous requests, product ideas, design work, site changes, operational tasks, and delivery reviews into structured revüe handoffs. Use when the user asks to "run this through revüe", "review this", "make this workflow proof-first", "prepare a handoff", "decide ship/caution/block", "look at Panely/HiveRunner style workflows", needs a design/Figma/client handoff, or wants a practical board-style review with assumptions, exact deliverable proof, risks, approvals, and next actions.
---

# revüe Proof Workflow

Use this skill to convert messy work into a clear, verified handoff. Favor concrete evidence, visible assumptions, and a direct decision over abstract planning.

## Operating Contract

1. Restate the intended outcome in one sentence.
2. Identify the mode and stage.
3. Separate facts from assumptions. Label assumptions explicitly.
4. Define the exact deliverable format and proof required before claiming success.
5. Surface approval gates before making external, destructive, paid, or public changes.
6. Produce a final verdict: `ship`, `ship with changes`, `caution`, or `block`.

Do not claim verification unless evidence exists. If the evidence is unavailable, say what is missing and what would prove it.

## Mode Selector

Pick one mode before shaping the work. Infer the mode from the request when possible; do not wait for the user to name it.

- `design-handoff`: design files, Figma, Canva, mockups, screenshots, brand polish, client-facing design packages. Read `references/design-handoff.md`.
- `product-shaping`: product concepts, platform workflows, feature definitions, roadmap options.
- `implementation-review`: code, local apps, scripts, technical changes, QA findings.
- `client-delivery`: artifacts intended for a named client or stakeholder.
- `platform-build`: revüe/Panely/HiveRunner-style internal workflow platform work.

Mode triggers:

- Use `design-handoff` for Figma, Canva, landing page mockups, PNG/SVG/PDF visual exports, editable files, design links, client visual review, brand polish, mobile/desktop states, or design source packages.
- Use `implementation-review` for code, repo, tests, build, local server, deploy readiness, bug, script, database, or API work.
- Use `product-shaping` for feature ideas, scope, roadmap, MVP, customer workflow, pricing later, or product strategy.
- Use `client-delivery` when the recipient is named and the task is mainly about presenting a usable artifact.
- Use `platform-build` when working on revüe, Panely, HiveRunner, or the all-in-one workflow platform.

If the user names a specific stakeholder, apply the stakeholder test: can that person use the result without a live explanation?

## Workflow

### 1. Intake

Capture the job in this shape:

- Request: what the user asked for.
- Owner/audience: who needs the result.
- Inputs: files, links, tools, notes, screenshots, repos, or prior artifacts.
- Constraints: brand, style, budget, time, approvals, "do not" boundaries.
- Exact deliverable: file type, link type, share state, or format the stakeholder asked for.
- Success: what must be visibly true and usable by the stakeholder at the end.

Use `assets/intake-template.md` when the user needs a reusable intake artifact.

### 2. Shape

Turn the request into a working contract:

- Scope in.
- Scope out.
- Main risks.
- Open questions.
- Working recommendation.
- Proof plan.
- Ship threshold: what must exist for `ship` instead of `caution`.

Read `references/workflow-contract.md` when the task is broad, multi-step, or likely to drift.

### 3. Build

Execute only the work inside the contract. Keep changes narrow and reversible. When building product or design work, preserve the user's style and workflow mentality unless the user explicitly changes direction.

For revüe itself, prefer practical operator surfaces:

- compact dashboards over marketing pages
- evidence-backed cards over vague summaries
- approvals and blockers near the action that needs them
- persistent handoff artifacts after every meaningful run

### 4. Prove

Collect evidence proportional to risk:

- Local file work: file paths, validation script results, rendered previews, screenshots, or diffs.
- Website/app work: live route, local route, screenshot, browser check, build/test output, console status.
- Data/workflow work: source query, exported artifact, schema check, row counts, or audit trail.
- Strategy/review work: cited inputs, assumption list, risk register, and decision record.

For design handoffs, prove the requested source format, editability, preview fidelity, mobile/desktop states, and shareability. A PNG/SVG/package is not equivalent to a Figma file unless the user requested that substitute or the handoff labels it as an interim package.

Use `references/evidence-schema.md` for evidence categories. Use `scripts/validate-evidence.py` to check a handoff draft before presenting it.

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

Use `assets/handoff-template.md` for manual drafting or `scripts/render-handoff.py` for a deterministic Markdown skeleton.

### 6. Review

When asked to review, lead with defects or blockers. Use this verdict scale:

- `ship`: evidence supports release/use in the exact requested deliverable format.
- `ship with changes`: safe enough if listed fixes are made.
- `caution`: material uncertainty remains; proceed only with explicit acceptance.
- `block`: missing proof, unacceptable risk, broken workflow, or required approval is absent.

Read `references/board-verdict-schema.md` for the full decision model.

## Approval Gates

Read `references/approval-gates.md` before actions that could publish, send, deploy, charge, delete, overwrite, message another person, or alter external systems. If approval is missing, stop at a prepared draft or preview.

## Resource Map

- `references/workflow-contract.md`: scope, assumptions, and proof contract.
- `references/approval-gates.md`: when to pause for approval.
- `references/evidence-schema.md`: what counts as proof.
- `references/board-verdict-schema.md`: ship/caution/block decision rules.
- `references/design-handoff.md`: Figma/design/client handoff proof checklist.
- `assets/intake-template.md`: reusable intake form.
- `assets/verification-matrix-template.md`: proof checklist.
- `assets/handoff-template.md`: final handoff format.
- `assets/stakeholder-summary-template.md`: concise non-technical reviewer note.
- `scripts/render-handoff.py`: create a Markdown handoff skeleton.
- `scripts/render-stakeholder-summary.py`: create a stakeholder-ready summary.
- `scripts/validate-evidence.py`: check required handoff sections and evidence markers.
