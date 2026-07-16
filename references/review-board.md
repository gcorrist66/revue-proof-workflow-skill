# Review Board

Use this reference for any stakeholder-facing work — design, product shaping, client delivery,
or a proof review. It replaces a single generic "look it over" pass with a small board of named
panelists who share the same inputs and the same non-negotiables, then converge on one verdict.

This is revüe's version of the Panely panelist model (multi-perspective review), run inside one
pass rather than as several live agents.

## How the board works

1. Every panelist reads the **same shared inputs** (below). No panelist reviews from memory or vibes.
2. Every panelist is bound by the **same non-negotiables** (below). These travel with every role.
3. Each panelist returns findings in its own lane — they are not allowed to blur into one another.
4. A final **Synthesis** step reconciles them into a single `ship` / `ship with changes` /
   `caution` / `block` verdict with evidence.

Run all panelists in one pass for most work. Only split into separate runs when the work is large
enough that each lane needs its own artifact.

## Shared inputs (every panelist must read)

State these explicitly at the top of the review so each lane is working from the same source of truth:

- The exact request and the intended outcome, in one sentence.
- The stakeholder / audience, and whether they can use the result without a live walkthrough.
- The actual artifacts under review: files, links, screenshots, repo, prior handoff. Not descriptions of them.
- The requested deliverable format and the proof required before it can be called done.
- The brand / style / tone constraints and any hard "do not" boundaries.

If any shared input is missing, that is itself a finding — record it under the gap, do not proceed as if it exists.

## Non-negotiables (travel with every panelist)

These bind every lane. A panelist that violates one has failed regardless of how good its output looks.

- **Honesty rule.** Only real facts stated as facts. Everything unverified is a clearly-labeled
  placeholder or assumption. No fabricated metrics, logos, testimonials, quotes, or capabilities.
- **Evidence rule.** No claim of "done," "works," or "editable" without concrete proof (path, URL,
  screenshot, command output, source inspection). "Looks good" is not evidence.
- **Exact-deliverable rule.** A substitute is not the requested deliverable. A PNG is not a Figma
  file; a draft is not a sent email; a preview deploy is not production. Label substitutes as interim.
- **Anti-generic rule.** If the output could belong to any other client, brand, or project, it has
  failed. Tie every direction to a specific reason: user preference, brand constraint, audience need,
  or observed evidence.
- **Approval-gate rule.** Nothing external, paid, destructive, or public happens without an explicit
  gate. When approval is missing, stop at a validated draft.

## The panelists

Each lane answers one question and stays in it. Adapt the named roles to the mode, but keep the lanes distinct.

| Panelist | Question it owns | Fails if |
| --- | --- | --- |
| Critique & Refinement | What are the genuine strengths to protect, and the specific weaknesses to fix — by area, citing what is actually there? | It gives vague praise, or prescribes "make it cleaner" instead of an actionable punch-list. |
| Aggressive | What is the boldest, sharper-POV version that still clears the bar and the non-negotiables? | It confuses louder/hypey with sharper, or breaks a non-negotiable to look bold. |
| Conservative | What is the most credible, lowest-objection version that a cautious stakeholder could not reject? | It becomes generic or templated in the name of safety. |
| Proof | What actually proves this exists and works, in the exact requested format? | It accepts a substitute or an untested preview as proof. |
| Stakeholder | Can the named recipient use / decide from this without a live explanation? | It reviews for the maker, not the recipient. |
| Synthesis | Across all lanes: the highest-leverage moves, and the single verdict with reasons. | It lists everything equally instead of forcing priority and a decision. |

For a design or client review, run Critique + Aggressive + Conservative + Proof + Stakeholder, then
Synthesis. For implementation or QA review, swap Aggressive/Conservative for an Implementation lane
(can someone build/operate this from the handoff?) and keep Proof, Stakeholder, Synthesis.

## Output block

Keep each lane short and cited. Use this shape:

```markdown
Shared inputs: <one line each: request, stakeholder, artifacts, deliverable+proof, constraints>
Non-negotiable check: <any rule breached, or "all clear">

Critique: strengths worth protecting → …; weaknesses by area (hero/hierarchy/moat/proof/copy/mobile) → …; punch-list → …
Aggressive: sharper direction → …; where the line was held so it stays credible → …
Conservative: lowest-objection direction → …; what keeps it non-generic → …
Proof: exact format present? → …; evidence → …; not verified → …
Stakeholder: can the recipient use/decide without a walkthrough? → …; gaps → …

Synthesis:
- Do these first (ranked): …
- Highest-leverage single move: …
- Verdict: ship / ship with changes / caution / block — because …
```

## Relationship to the rest of revüe

- The **non-negotiables** are the enforcement layer for `references/evidence-schema.md` and
  `references/anti-generic-review.md` — the same rules, applied per lane.
- The **Synthesis verdict** uses `references/board-verdict-schema.md`.
- When a review run is captured as a structured artifact, each panelist lane becomes an entry in the
  run contract (`references/run-contract.md`) so the board's output is inspectable, not just prose.
