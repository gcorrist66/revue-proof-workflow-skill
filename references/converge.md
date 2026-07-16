# Converge Mode (get it to ship, don't loop on caution)

A review that returns `caution` over and over is failing. The job is to move work to `ship`, not to
keep grading it. Converge mode is the default posture for any review: fix what you can, ask only what
you must, and always show the path from the current verdict to `ship`.

## The rule that breaks the loop

**A non-`ship` verdict is incomplete without a path to ship.** Every `caution`, `block`, or
`ship with changes` must be paired with the exact, ordered list of changes that would clear it, each
tagged with an owner. If you can state the blocker, you can state the fix.

## Do not re-review unchanged work

Before reviewing, check whether the artifact changed since the last verdict (compare an
`inputsFingerprint`: frame count + names, file hash, commit SHA, or a one-line state description).

- If nothing changed: **do not re-run the board.** Say "unchanged since last run; verdict stands at X"
  and jump straight to the decision block and path to ship. Re-grading identical work wastes passes.
- Only run the full board on work that actually changed.

## Triage every finding (fix / decide / prove)

Sort each finding into exactly one bucket. This is what stops the loop — most findings are not blockers.

- **FIX** — the agent can resolve it with no outside input (consolidate duplicate frames, name frames,
  strengthen a CTA, label placeholder copy, add a missing section, tidy hierarchy). **Do these this
  pass.** Never return a fixable defect as a blocker.
- **PROVE** — the agent can resolve it by gathering evidence (run the build, open the layers panel,
  screenshot a state). **Do these this pass.**
- **DECIDE** — only the human/client can settle it (which pricing is correct, is mobile in scope, are
  real testimonials available). Batch these into one decision block.

## Output shape for a converge run

1. **Changed since last run?** yes/no (+ fingerprint). If no, short-circuit as above.
2. **Fixed this pass** — what the agent changed, with evidence.
3. **Decisions needed** — the *minimal* set the human must answer, ideally 2–3, never drip. Each with
   the two possible outcomes where useful.
4. **Path to ship** — ordered, each item `[agent]` or `[human]`, and the verdict it unlocks:
   ```
   Current: caution
   [agent] consolidate to one desktop frame        → clears "no final frame"
   [agent] label placeholder testimonials          → clears honesty flag
   [human] confirm boat lineup + pricing           → clears lineup conflict
   [human] confirm mobile in scope                 → if in scope, [agent] builds mobile frame
   Target after decisions answered: ship with changes → ship on client approval
   ```
5. **Verdict** — with the assumption-dependent note if it applies.

## Pass budget

- Target convergence in **≤ 3 passes**: (1) fix + decide block, (2) apply decisions + build, (3) confirm ship.
- **Loop guard:** if the same blocker appears in two consecutive runs, stop and say so plainly:
  "This will not clear until <decision> is made — re-running will not change the verdict." Do not burn a
  third identical review.

## Prompt that triggers it

The user does not need special syntax, but these phrasings force converge posture: "get this to ship",
"fix what you can and only ask what you can't", "converge", "what's the path to ship". Treat any
repeated review of the same artifact as an implicit request to converge, not to re-grade.
