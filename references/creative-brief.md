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

Use `assets/intake-template.md`. Four fields are required and block generation until every one is
filled in:

1. **Deliverable + format** — the exact artifact and file format the stakeholder will receive. "A
   landing page" is not a deliverable; "single-file HTML/CSS landing page, desktop + mobile" is.
2. **Sources** — every input the brief is built from, plus one explicit yes/no: has the agent actually
   read the target handoff page, brief doc, or prior artifact — not just the request text? A "no"
   blocks the brief; go read it first, then answer again.
3. **Design system lock** — the color, type, spacing, and logo rules this deliverable must not violate.
   See `references/design-system-lock.md`. Reference an existing lock file, or define one now if this
   is the first creative-production run for the project.
4. **Hard NOs** — literal forbidden elements, words, colors, or moves, one per line:
   `HARD NO: <exact pattern> — <why>`. If genuinely none apply, write "None confirmed" — an empty
   section is a gap, not a green light.

## Completeness check (blocks, does not warn)

Before generating anything, check all four fields against the brief. If any is missing, stop — do not
start on the parts that are ready and drip-feed questions about the rest. Collect every gap into one
batched request and send it once.

```markdown
Brief incomplete — need before I can start:
- Deliverable + format: not specified — what exact file/format will [stakeholder] receive?
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
`deliverable`, `format`, `sources`, `handoffPageRead: true`, `designSystemLock`, or `hardNos`, and
reports every missing field in one failure line — the same batching this gate asks the agent to do by
hand. Run it before presenting concepts, not after they are already built.

## Relationship to the rest of revüe

- Feeds `references/options-and-refine.md` — the brief is what every generated concept is checked
  against.
- Feeds `references/design-system-lock.md` and `references/output-audit.md` — the lock captured here is
  what the finished deliverable is audited against before `ship`.
- A pure review never needs a brief — use the mode's existing intake
  (`references/design-handoff.md` §Required Intake, `references/inspection-checklists.md`) instead.
