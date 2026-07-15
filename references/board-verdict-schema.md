# Board Verdict Schema

Use this reference when returning a decision or reviewing work.

## Verdicts

`ship`

- Required proof exists.
- Remaining risk is low or already accepted.
- No missing approval blocks the next step.
- The exact requested deliverable format exists.

`ship with changes`

- Core direction is sound.
- Listed changes are specific and bounded.
- No unresolved blocker prevents completion after those changes.

`caution`

- Work may proceed only with explicit acceptance of uncertainty.
- Evidence is partial, assumptions are material, or stakeholder preference could change the result.
- A useful substitute exists, but the exact requested deliverable is not verified.

`block`

- Required proof is missing.
- A hard boundary or approval gate is unresolved.
- The result would be misleading, unsafe, externally risky, or materially incomplete.

## Review Output

Lead with the decision:

```text
Verdict: caution
Reason: The mockup is visually directionally correct, but no editable source file exists yet.
Required proof: Figma source link or exported editable package.
Next action: Create the editable source, then rerun review.
```
