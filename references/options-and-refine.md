# Options + Reject-Refine (Pillar 2)

Use this for every creative-production run, right after the brief gate
(`references/creative-brief.md`) passes. It replaces "generate one direction and see if they like it"
with real optionality and a feedback loop that actually converges.

## The rule

Creative generation returns **2–3 distinct, lock-compliant concepts** — never one, never more than
three (past three, the stakeholder is triaging instead of deciding). Each concept must:

- Solve the brief a genuinely different way — name the axis it differs on (structure, tone, hero
  mechanic, information order). Two concepts that differ only in color are not distinct.
- Pass the design-system lock and Hard NOs before it is ever shown. Check each concept against
  `references/design-system-lock.md` first; a concept that fails the lock gets regenerated, not
  presented with a caveat.
- Trace to the brief. Every concept states which brief input or constraint it is optimizing for.

Apply `references/anti-generic-review.md` to the option set itself: if two of the three concepts are
interchangeable safe defaults, that is a finding, not a pass.

## Output block

```markdown
Concepts (brief: <one line>):

1. **<name>** — axis: <what makes this different> — optimizes for: <brief input>
   Lock check: pass — colors/type/Hard NOs all within lock.
2. **<name>** — axis: <...> — optimizes for: <...>
   Lock check: pass.
3. **<name>** — axis: <...> — optimizes for: <...>
   Lock check: pass.
```

## Rejection: keep / kill / change

A rejection is not "try again." The reviewer must answer, per rejected concept:

- **Keep** — the specific elements that worked and must survive into the next round.
- **Kill** — the specific elements to drop entirely.
- **Change** — what to do instead, with direction (not just "make it better").

```markdown
Concept 2 feedback:
- Keep: the pricing-forward hero, the single-CTA close.
- Kill: the testimonial carousel — reads as filler, not proof.
- Change: lead with the loss-aversion line from Concept 1 instead of the generic "book now" headline.
```

Vague rejections ("doesn't feel right", "make it pop") do not count as feedback — ask the reviewer to
pin at least one keep, kill, or change before generating the next round.

## Fold feedback into the brief before the next round

Do not carry rejection feedback only in the conversation. Before generating round 2, update the working
brief (the intake artifact, or the run's `brief` object) with what changed: add killed elements to Hard
NOs if they should never come back, add kept elements as new constraints, and turn "change" direction
into a concrete brief input. The next round of concepts is generated from the *updated* brief, not from
memory of what was said.

## Round budget

Target convergence in **≤ 3 rounds**, matching `references/converge.md`'s pass budget: (1) first 2–3
concepts, (2) refine from keep/kill/change, (3) final pick. If round 3 still produces a reject with no
new keep/kill/change (the same objection twice), stop generating and say so plainly: "This will not
converge without a decision on <specific open question> — regenerating will not change the outcome."

## Self-enforcement

`scripts/validate-run.py` fails a `"produces": "creative-production"` run if `options` has fewer than 2
or more than 3 entries, if any entry's `lockCompliant` is not `true`, or if two entries share the same
`distinctionAxis` — the concepts must actually be different, not just labeled differently.

## Relationship to the rest of revüe

- Requires a passed `references/creative-brief.md` gate first — options generated against an incomplete
  brief are ungrounded.
- Uses `references/design-system-lock.md` for the per-concept lock check.
- The final chosen concept goes through `references/output-audit.md` before a `ship` verdict.
