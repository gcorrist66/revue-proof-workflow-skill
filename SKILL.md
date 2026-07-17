---
name: revue-proof-workflow
description: Proof-first review and delivery workflow for designs, product changes, code, client work, and operational tasks. Use when the user asks to run work through revüe, review readiness, improve something to ship, prepare a handoff, assess a design or implementation, or decide ship / ship with changes / caution / block with evidence and next actions.
---

# revüe Proof Workflow

Turn ambiguous work into a verified decision and a short path to ship. Inspect the real artifact, fix
what the user authorized, and make assumptions and missing proof visible.

## Start here

1. State the intended outcome in one sentence.
2. Pick a mode and track from the tables below. Infer them from the request.
3. Separate observed facts from assumptions.
4. Define the exact deliverable and what would prove success.
5. Check approval boundaries before publishing, sending, deploying, deleting, charging, or changing an
   external system. Read `references/approval-gates.md` when any boundary is near.
6. Inspect the actual artifact using `references/inspection-checklists.md`. Gather at least three
   concrete observations, including the source and one limitation, and say how or when each was observed.
7. For design, product, or stakeholder-facing work, use the reviewer lanes in
   `references/review-board.md`, then synthesize one verdict. Do not expose repetitive panelist prose
   when a concise synthesis is enough.
8. If the user asked for changes, make the safe in-scope fixes before reporting blockers. If the user
   asked only for a review or diagnosis, do not mutate the artifact.
9. Validate the result with the relevant script and run `references/self-check.md`.
10. Return one verdict and the shortest credible path to ship.

Never call something reviewed, verified, working, or shipped unless it was directly observed this
session. When proof is unavailable, name the missing proof and cap the verdict at `caution` or `block`.

## Mode selector

| Mode | Use for |
| --- | --- |
| `design-handoff` | Figma, Canva, mockups, visual systems, brand polish, editable design packages. Read `references/design-handoff.md`. |
| `implementation-review` | Code, apps, sites, APIs, databases, QA, bugs, deploy readiness, and scoped UI changes to an existing product. |
| `product-shaping` | Product concepts, scope, workflows, MVPs, roadmap choices, and product strategy. |
| `client-delivery` | Work whose main purpose is a usable artifact or message for a named client or stakeholder. |
| `platform-build` | revüe/Panely/HiveRunner/Vega-style workflow platform work. Read `references/vega-patterns.md`. |

When a stakeholder is named, apply this test: can that person understand and use the result without a
live explanation?

## Track selector

Choose one track. The distinction controls whether the creative brief, concept options, and output
audit apply.

### Review / remediation (default)

Use this for existing work: review it, diagnose it, refine it, fix a bug, improve copy, simplify a
backend, polish an established interface, or implement a bounded change inside an existing system.

A request such as "make this existing dashboard feel more premium" remains review/remediation unless
the user asks for new visual directions or a new design system. Do not force a tier question or 2–3
concepts onto routine implementation work.

### Creative production

Use this only when revüe is producing a net-new visual or brand direction: a new site concept, campaign
asset, identity, design system, or genuinely open-ended creative direction. Tag a structured run with
`"produces": "creative-production"`.

Before generating, read `references/creative-brief.md` and complete the brief gate. Then:

1. Lock sources, design-system rules, hard NOs, exact format, and tier.
2. Generate 2–3 distinct lock-compliant directions using `references/options-and-refine.md`.
3. Fold keep / kill / change feedback into the brief before another round.
4. Audit the selected output with `scripts/validate-output.py` and, when declared, validate structure
   with `scripts/validate-conformance.py`.

Only after the creative-production track is selected, explicit language such as "premium", "flagship",
or "custom" can set the tier; do not re-ask for a choice the user has already made. If a required brief
field is missing, request every missing field once in one batch. See `references/creative-brief.md`.

## Workflow

### 1. Intake and shape

Capture:

- request and intended outcome
- owner or audience
- actual inputs and source of truth
- constraints and hard boundaries
- exact deliverable
- proof required for `ship`

For broad or drift-prone work, read `references/workflow-contract.md`. Use
`assets/intake-template.md` when a reusable brief is useful.

### 2. Inspect

Follow the active mode in `references/inspection-checklists.md`. Evidence must be specific enough that
another person could reproduce the finding.

Treat user-reported behavior as a source input, not direct verification. Label it "reported by user"
until reproduced. It can justify investigation and a cautious verdict, but not a claim that the reviewer
observed the behavior.

For product interfaces, always check:

- **Context:** Is the active client, company, account, environment, or record unmistakable on the page?
- **System status:** Does every action that takes noticeable time show immediate progress, disabled
  controls, completion, and failure feedback?
- **Meaning:** Are scores and labels explained in plain language?
- **Target:** Does the user know the number or condition to aim for?
- **Action:** Does the page show what to fix first and how that change improves the result?
- **Empty state:** Does an empty report explain why it is empty and the next useful action?

### 3. Build or remediate

Act only when the request authorizes changes. Keep changes narrow, reversible, and consistent with the
existing product or brand. Preserve the user's working style unless they ask for a new direction.

For creative-production work, read `references/anti-generic-review.md` and reject the first obvious
template answer. For existing-product remediation, prefer clarity, hierarchy, and feedback over adding
decorative surface area.

### 4. Prove

Collect proof proportional to risk:

- files/code: diff, exact paths, lint, tests, build, rendered output
- site/app: route, browser behavior, responsive states, loading/error states, console status
- data/workflow: source query, schema check, counts, exported artifact, audit trail
- strategy/review: cited inputs, assumptions, risks, and decision record

Use `references/evidence-schema.md`. For Markdown handoffs run:

```bash
python3 scripts/validate-evidence.py path/to/handoff.md --strict
```

For structured run artifacts run:

```bash
python3 scripts/validate-run.py path/to/run.json --strict
```

For creative output run:

```bash
python3 scripts/validate-output.py path/to/deliverable --lock path/to/lock.json --tier standard
python3 scripts/validate-conformance.py path/to/deliverable --structure path/to/structure.json
```

Read `references/output-audit.md`, `references/design-system-lock.md`, and
`references/brief-conformance.md` before using those gates.

If the task provides only a scenario and no artifact, link, repo, or handoff file, do not invent a
validation run. Review the scenario as reported evidence, name the inspection that would verify it,
and state that no file validator applied.

### 5. Converge

Read `references/converge.md`. Classify every finding as:

- **fix:** the agent can safely resolve it now
- **prove:** the agent can verify it now
- **decide:** a human choice or approval is genuinely required

Do the fix and prove items in the current pass. Batch the decide items. Do not re-review unchanged work;
state that the prior verdict stands and move to the outstanding decision or proof.

Prioritize findings when order matters:

- `P0`: safety, wrong-context action, data loss/exposure, or a core path that cannot be completed
- `P1`: material usability, correctness, trust, or conversion problem
- `P2`: polish or efficiency improvement that does not block the core path

### 6. Handoff

Lead with the outcome, then include only what the recipient needs:

1. mode and verdict
2. evidence and scorecard when useful
3. assumptions and material risks
4. decisions that only a human can make
5. next action or owner-tagged path to ship

Use `assets/handoff-template.md` or `scripts/render-handoff.py` for a durable handoff. Use
`assets/stakeholder-summary-template.md` when the audience is non-technical.

## Verdicts

- `ship`: the exact requested result exists and the required proof passed.
- `ship with changes`: usable after specific bounded fixes; name the fixes and owners.
- `caution`: material uncertainty remains; name what would resolve it.
- `block`: required proof, safety, approval, or a usable artifact is absent.

If an assumption changes the verdict, name the assumption and both outcomes. Every non-`ship` verdict
must include a path to ship or a decision block. Read `references/board-verdict-schema.md`.

## Model routing

Use the capability tiers in `references/model-routing.md` only when the runtime supports routing. The
tiers are vendor-neutral run metadata, not hard-coded model names. Validators and scripts are
deterministic; creative synthesis and complex coding need progressively more reasoning. Never claim a
specific model ran unless the runtime confirms it.

## Key resources

- `references/inspection-checklists.md`: mode-specific evidence gathering, including interface clarity.
- `references/review-board.md`: reviewer lanes and synthesis rules.
- `references/converge.md`: fix / prove / decide and path-to-ship rules.
- `references/self-check.md`: mandatory pre-verdict consistency check.
- `references/creative-brief.md`: creative-production gate and tier cascade.
- `references/options-and-refine.md`: 2–3 concepts and keep / kill / change loop.
- `references/output-audit.md`: deliverable audit and known limits.
- `references/run-contract.md`: structured `revue.review.v1` artifact.
- `assets/revue-run.schema.json`: run artifact schema.
- `scripts/run-evals.py`: complete regression and adversarial suite.
