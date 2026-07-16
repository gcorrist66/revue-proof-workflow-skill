# Self-Check (run before every verdict)

This is the gate that makes revüe work without an expert driving it. Run it on your OWN draft before
you present any review. If a check fails, fix the draft or lower the verdict — do not ship the review.

If a handoff file exists, also run `scripts/validate-evidence.py` (or `scripts/validate-run.py` for a
JSON artifact). If you cannot run a script, apply every check below by hand and say you did.

## 1. Evidence floor

- You must have at least **three concrete, quotable observations** taken from the actual artifact
  (exact text, counts, file paths, prices, command output, screen captures). Not descriptions of what
  it probably contains — things you actually saw.
- If you cannot produce three, you have not reviewed it. The verdict cannot exceed `caution`, and you
  must say what you could not inspect.

## 2. Freshness guard

- State how and when each key observation was captured, and whether it is **live or a prior snapshot**.
- Second-hand, stale, or assumed evidence caps the verdict at `caution`. Never write "reviewed",
  "verified", or "works" about something you did not directly observe this session.

## 3. Exact-deliverable check

- Does the evidence prove the **exact requested format**, or only a substitute? A PNG is not a Figma
  file; a draft is not a sent email; a preview deploy is not production.
- If only a substitute is proven, the verdict is `caution` unless the user explicitly accepted it.

## 4. Verdict consistency

- `ship` is invalid if any scorecard row is `fail`, any required proof is missing, or any approval gate
  is unresolved. Use `caution` or `block` instead.
- The evidence section must include at least one **limitation** — what the review does not prove.

## 5. Assumption-dependent verdict

- If the verdict would **change under a stated assumption** (for example "mobile is out of scope this
  round"), you must name the assumption and give both outcomes:
  `caution now; ship with changes if <assumption> is confirmed`.
- Never let an unconfirmed assumption silently decide the verdict.

## 6. Non-negotiables (from the review board)

- Honesty: only real facts as facts; everything else a labeled placeholder or assumption.
- Anti-generic: if the review or direction could apply to any other client, it has failed.
- Approval-gate: nothing external, paid, destructive, or public without an explicit gate.

## Report line

End the review with one line confirming the gate ran, e.g.:

```text
Self-check: 3+ observations cited; evidence captured this session (snapshot); exact-format proven; no ship-vs-scorecard conflict; verdict is assumption-dependent on mobile scope.
```
