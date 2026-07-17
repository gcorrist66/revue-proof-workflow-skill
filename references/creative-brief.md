# Creative Brief Gate (Pillar 1)

Use this before any creative-production work — revüe generating a new design, page, asset, or build,
not reviewing something that already exists. It replaces "start building and hope the constraints
surface later" with a single blocking checkpoint.

## When this applies

Creative production, not review. If the user hands you a finished Figma file, PR, or draft and asks
"is this ready," you are reviewing — skip this gate and go straight to the mode's inspection checklist
(`references/inspection-checklists.md`). If the user asks revüe to design, write, or build something
new — a landing page, a set of options, a coded feature, a campaign asset — this gate runs first,
before any concept work starts. Tag the run `"produces": "creative-production"`
(`references/run-contract.md`) so the validators apply the brief and options gates below.

## Required brief

Use `assets/intake-template.md`. Five fields are required and block generation until every one is
filled in:

1. **Deliverable + format** — the exact artifact and file format the stakeholder will receive. "A
   landing page" is not a deliverable; "single-file HTML/CSS landing page, desktop + mobile" is.
2. **Tier** — `Standard`, `Premium`, or `Custom`. Not a formality: it sets the craft bar, routes the
   model, and sets the audit bar (see "The tier cascade" below). Never default this silently — ask.
3. **Sources** — every input the brief is built from, plus one explicit yes/no: has the agent actually
   read the target handoff page, brief doc, or prior artifact — not just the request text? A "no"
   blocks the brief; go read it first, then answer again.
4. **Design system lock** — the color, type, spacing, and logo rules this deliverable must not violate.
   See `references/design-system-lock.md`. Reference an existing lock file, or define one now if this
   is the first creative-production run for the project.
5. **Hard NOs** — literal forbidden elements, words, colors, or moves, one per line:
   `HARD NO: <exact pattern> — <why>`. If genuinely none apply, write "None confirmed" — an empty
   section is a gap, not a green light.

Optionally, the brief can also declare a **structure spec** (required sections, order, forbidden
elements, required placeholders) — see `references/brief-conformance.md`. This is not one of the five
blocking fields; declare it when the deliverable's structure genuinely matters, skip it when it doesn't.

## The tier cascade

Tier is not just metadata — setting it changes three things at once:

| Tier | Craft bar | Model routing | Audit bar |
| --- | --- | --- | --- |
| `Standard` | Clean, functional, on-brand. The design-system lock is the whole bar. | `fast` for gates, `standard` for generation (`references/model-routing.md`). | `outputAudit.pass == true` (`references/output-audit.md`). |
| `Premium` | Everything Standard requires, plus the elevate layer: full-bleed hero + scrim, display type system, editorial restraint, a repeating signature motif, desktop+mobile+sticky bar (`references/elevate.md`). | `fast` for gates, `deep` for generation — Premium craft calls are the "genuinely ambiguous, expensive to get wrong" judgment `references/model-routing.md` reserves for Fable 5. | `outputAudit.pass == true` **and** `outputAudit.elevatePass == true`. A Premium-declared deliverable that only clears the Standard bar is flagged, not shipped. |
| `Custom` | Set by direct human creative direction in the brief — no prescribed template. The lock and Hard NOs still apply; they are never optional. | Human-led: the model may draft, but final creative judgment and sign-off belong to a human, not an autonomous pass. | `outputAudit.pass == true` **and** a top-level `tierSignoff` naming the human who approved the direction. |

## Completeness check (blocks, does not warn)

Before generating anything, check all five fields against the brief. If any is missing, stop — do not
start on the parts that are ready and drip-feed questions about the rest. Collect every gap into one
batched request and send it once.

```markdown
Brief incomplete — need before I can start:
- Deliverable + format: not specified — what exact file/format will [stakeholder] receive?
- Tier: not specified — Standard, Premium, or Custom? This sets the craft bar and how it gets built.
- Sources: handoff page not confirmed read — should I read [page/link] before drafting, or is there a
  different source of truth?
- Design system lock: no colors/type/spacing supplied — reuse an existing lock, or should I propose one?
- Hard NOs: none stated — anything explicitly off-limits (words, colors, moves, competitors)?
```

List only what is actually missing. Do not re-ask for fields already answered, and do not pad the
request with fields that do not gate generation (Constraints and Success Criteria are useful, but not
blocking).

## Self-enforcement

`scripts/validate-run.py` fails a `"produces": "creative-production"` run if `brief` is missing any of
`deliverable`, `format`, `tier`, `sources`, `handoffPageRead: true`, `designSystemLock`, or `hardNos`,
and reports every missing field in one failure line — the same batching this gate asks the agent to do
by hand. Run it before presenting concepts, not after they are already built. It also enforces the tier
cascade at ship time: `ship` requires `outputAudit.elevatePass` for Premium and `tierSignoff` for
Custom, and (when the brief declares a `structure` spec) a passing `conformance` result
(`references/brief-conformance.md`).

## Relationship to the rest of revüe

- Feeds `references/options-and-refine.md` — the brief is what every generated concept is checked
  against.
- Feeds `references/design-system-lock.md` and `references/output-audit.md` — the lock captured here is
  what the finished deliverable is audited against before `ship`.
- Feeds `references/elevate.md` for Premium-tier work, and `references/brief-conformance.md` when the
  brief declares a structure spec.
- A pure review never needs a brief — use the mode's existing intake
  (`references/design-handoff.md` §Required Intake, `references/inspection-checklists.md`) instead.
