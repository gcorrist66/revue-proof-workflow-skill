# Model Routing (Pillar 4)

Use this to decide which model tier runs each step of a revüe pass. Cost and latency scale with model
size; the correctness of a mechanical gate does not improve by spending a bigger model on it. Route by
what the step actually requires, not by default.

## Tiers

| Tier | Model | Model string | Use for |
| --- | --- | --- | --- |
| `fast` | Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Deterministic gates, validators, pattern checks, format checks — anything with a correct/incorrect answer a script could mostly do. |
| `standard` | Claude Sonnet 5 | `claude-sonnet-5` | Creative generation, synthesis, board panelist lanes, ordinary code changes — most of the actual work. |
| `deep` | Claude Fable 5 | `claude-fable-5` | Genuinely ambiguous judgment calls, first-of-kind pattern work (new platform-build shaping), synthesis across conflicting stakeholder input where the "right call" is not mechanical. |
| `deep-coding` | Claude Opus 4.8 | `claude-opus-4-8` | Heavy coding: multi-file refactors, new subsystems, schema migrations — anything where a wrong architectural call is expensive to unwind. Carved out of `deep` because coding weight and judgment weight are not the same axis. |

## The rule: gates and validators are always `fast`

Every self-enforcing check in revüe — the brief completeness gate, the design-system lock check, the
output audit, the self-check, and every `scripts/validate-*.py` invocation — is deterministic: it is
checking a rule, not making a judgment call. Tag these steps `fast` without exception. If a "gate" needs
a bigger model to get the right answer, it is not actually a gate yet — tighten the rule instead of
escalating the model.

## Step → tier map

| Step | Tier | Why |
| --- | --- | --- |
| Brief completeness gate (`references/creative-brief.md`) | `fast` | Field-presence check. |
| Design-system lock check (`references/design-system-lock.md`) | `fast` | Pattern/color match against a fixed lock. |
| Options generation (`references/options-and-refine.md`) | `standard` | Real creative judgment, three times over. |
| Reject-refine synthesis (fold keep/kill/change into the brief) | `standard` | Judgment about what feedback implies for the next round. |
| Review board panelist lanes (`references/review-board.md`) | `standard` | Each lane is a judgment call grounded in evidence. |
| Review board synthesis | `standard`, escalate to `deep` if lanes conflict sharply | Reconciling five judgment calls into one verdict. |
| Output audit (`scripts/validate-output.py`, `references/output-audit.md`) | `fast` | Color extraction + pattern scan against a lock file. |
| Self-check (`references/self-check.md`) | `fast` | Checklist against the draft; no new judgment. |
| `validate-run.py` / `validate-evidence.py` / `validate-output.py` invocations | `fast` | Scripts; the model is only invoking them. |
| Platform-build shaping (new revüe/Panely/HiveRunner/Vega pattern decisions) | `deep` | Ambiguous, first-of-kind, expensive to get wrong. |
| Heavy coding build (new subsystem, multi-file refactor, schema migration) | `deep-coding` | Coding weight, not judgment weight. |
| Ordinary implementation (small fix, single-file change, test addition) | `standard` | Bounded, low-ambiguity coding. |

## Escalation, not default-to-biggest

Start at the tier the step maps to. Escalate one tier only when a concrete signal shows up — the
board's lanes genuinely disagree (not just different emphasis), the brief is contradictory in a way no
gate rule resolves, or a `standard`-tier coding attempt has failed twice on the same defect. Do not
escalate because the stakes feel high; escalate because the current tier actually produced a wrong or
stuck answer.

## Recording the tier

Tag every step in the run's `trace` with the tier it ran at (`assets/revue-run.schema.json`):

```json
{ "step": "brief-gate", "modelTier": "fast", "durationMs": 0 },
{ "step": "options-generation", "modelTier": "standard", "durationMs": 0 },
{ "step": "output-audit", "modelTier": "fast", "durationMs": 0 }
```

## Self-enforcement

`scripts/validate-run.py` rejects a run if a known gate/validator step (`brief-gate`,
`design-system-lock-check`, `options-lock-check`, `output-audit`, `self-check`, `validate-run`,
`validate-output`, `validate-evidence`) is tagged with any `modelTier` other than `fast`.

## Relationship to the rest of revüe

- Applies across every mode and every pillar — this is routing, not a new gate of its own.
- The gates it pins to `fast` are exactly the ones defined in `references/creative-brief.md`,
  `references/options-and-refine.md`, `references/design-system-lock.md`,
  `references/output-audit.md`, and `references/self-check.md`.
