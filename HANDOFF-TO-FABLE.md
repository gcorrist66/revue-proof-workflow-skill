# Handoff to Fable — revüe v1.0

> **Resolved (Fable pass, v1.0.0).** Every open item below was completed: Pillar 3 was hardened into
> the evasion-resistant, fail-closed audit (`scripts/validate-output.py`), nine red-team fixtures plus
> four red-team run artifacts were added and proven rejected (58/58 evals), the six acceptance
> criteria were verified against the finishing task's own enumeration (the referenced
> `revue-v1.0-build-handoff.md` never surfaced — see `docs/v1.0-acceptance-report.md` for the
> provenance note and the criterion→eval map), the pipeline was dogfooded end to end on revüe's own
> brand (`examples/dogfood/`), and the installer was rebuilt (`scripts/make-installer.py`) and tested
> against a fresh clone with the eval suite gating the install. This file is kept as history of the
> Sonnet pass.

This is the Sonnet 5 pass on v1.0. Scope was Pillars 1, 2, and 4, plus shared scaffolding for Pillar 3,
plus the schema/validator/SKILL.md wiring and eval suite. Read this before touching anything —
particularly the "spec input gap" section, since it affects how much you can trust the acceptance
criteria below.

## Spec input gap (read first)

`revue-v1.0-build-handoff.md` was **not present** in the repo, in the mounted folder, or in the
session's uploads — I searched the full repo tree and the uploads directory and it does not exist.
Neither did a Panely prompt file or a model-tier mapping file. I proceeded from the detailed pillar
descriptions, schema fields, model-tier mapping, and acceptance standards given directly in the task
instructions, which were specific enough to build against (exact model strings, exact schema field
names, exact standards). Where the task said "if the Panely file is absent, use the reconstructed lock
format in the spec and note the assumption," I did that for the Hard-NO field format
(`HARD NO: <pattern> — <why>`, one per line) — this is my own reconstruction, not copied from a real
Panely artifact.

**What this means for you:** I do not have the actual "six acceptance criteria" the task description
referenced as being in the missing build-handoff file. I built to the spec embedded in my task prompt
and to this repo's existing conventions, and I self-verified against what I could infer (see
"Self-verification done" below). Before you tag v1.0.0, either locate the real
`revue-v1.0-build-handoff.md` (check with the user/repo owner — it may exist outside this session's
reach) and diff my work against its actual acceptance criteria, or treat the criteria implicit in the
original task message as authoritative and confirm each one explicitly. Don't assume my build matches
an acceptance list you haven't seen.

## What I built

**Pillar 1 — required creative brief**
- `references/creative-brief.md`: when it applies (creative-production vs. review), the four required
  brief fields, the blocking completeness check with a single batched-request output format, and the
  self-enforcement tie to `validate-run.py`.
- `assets/intake-template.md`: added four required, blocking sections (Deliverable & Format, Sources
  incl. "Handoff page read?", Design System Lock, Hard NOs) ahead of the existing general fields.

**Pillar 2 — options + reject-refine**
- `references/options-and-refine.md`: the 2–3-distinct-concepts rule, the lock-check-before-presenting
  rule, the keep/kill/change rejection format, folding feedback into the brief before the next round,
  a ≤3-round budget borrowed from `references/converge.md`, and self-enforcement.

**Pillar 4 — model routing**
- `references/model-routing.md`: fast = Haiku 4.5 (`claude-haiku-4-5-20251001`), standard = Sonnet 5
  (`claude-sonnet-5`), deep = Fable 5 (`claude-fable-5`), deep-coding = Opus 4.8 (`claude-opus-4-8`); a
  full step→tier map; the "gates and validators are always fast" rule; and self-enforcement.

**Pillar 3 — scaffolding only (first working version, not hardened)**
- `references/design-system-lock.md`: the lock's fields, the machine-checkable JSON format, the brief
  authoring format, and an explicit "what v1.0 does not cover" section.
- `references/output-audit.md`: when the audit runs, the procedure, the `outputAudit` result shape, the
  ship-gate rule, and the same explicit non-coverage section.
- `scripts/validate-output.py`: stdlib-only. Extracts hex colors (`#abc`/`#aabbcc`/`#aabbccdd`, plus
  `rgb()`/`rgba()` normalized to hex) from an HTML/CSS/SVG file, compares against a JSON lock's
  `colors` list, scans raw text for literal `hardNos[].pattern` (case-insensitive substring), and exits
  non-zero on any violation. `--json` prints the `outputAudit` object directly.

**Schema + validators**
- `assets/revue-run.schema.json`: added `produces` (`review` | `creative-production`, default
  `review`), `brief`, `designSystemLock`, `options`, `optionFeedback`, `outputAudit`, and
  `trace[].modelTier` / `trace[].model`.
- `scripts/validate-run.py`: for `"produces": "creative-production"` runs — brief completeness (one
  batched failure line naming every missing field), options count (2–3) and shape, `lockCompliant ==
  true` on every option, distinct `distinctionAxis` values, and (under `--strict`, before a `ship`
  verdict) `outputAudit.pass == true`. Also validates `trace[].modelTier` against the known enum and
  requires known gate/validator step names to be tagged `fast`. **Design decision, not in any spec I
  could see:** all of this is gated behind `data.get("produces", "review") == "creative-production"` so
  that every pre-v1.0 run artifact (no `produces` field) is completely unaffected — this is what kept
  the full pre-existing eval suite green. If the real build-handoff spec says otherwise (e.g., these
  checks should be unconditional), you'll need to revisit this gating.

**SKILL.md**
- Operating Contract expanded from 10 to 14 numbered steps, inserting the brief gate, options
  generation, output audit, and model routing at the points in the pipeline where they actually run.
- Mode Selector gets a short paragraph on the review-vs-creative-production track.
- Workflow §1/§3/§4 (Intake/Build/Prove) each get a paragraph pointing at the relevant new pillar.
- New `## Model Routing` section.
- Resource Map updated with all six new/changed files.

**docs/release-notes.md** — full v1.0.0 entry.

## Self-verification done

- `python3 -m py_compile scripts/*.py` — clean.
- `python3 scripts/run-evals.py` — **34/34 passing** (20 pre-existing + 14 new). New cases: the
  creative-production golden (`examples/worked-creative-production.json`, the suite's first `ship`-
  verdict golden), plus rejections for an incomplete brief (batched), too few options, too many
  options, a non-lock-compliant option, duplicate concepts, a failing output audit before ship, a
  missing output audit before ship, a mistagged gate step, and an unknown model tier; plus
  `validate-output.py` pass/fail smoke tests against `examples/lock-fixture.json`,
  `examples/deliverable-pass.html`, `examples/deliverable-fail.html`.
- Confirmed every pre-existing golden fixture still validates and reaches its original expected verdict
  (ran the full suite before touching `validate-run.py`, then again after — no regressions).
- Grepped all new/changed files for the generic-AI buzzwords `references/anti-generic-review.md` warns
  against ("transform," "unlock," "elevate," "seamless," "leverage," etc.) — none found.
- Grepped for `Ũ` (the wrong ü) — none found; the brand name is `revüe` (U+00FC) throughout.
- Grepped all new/changed files for machine paths, credentials, and internal codenames — none found.
- Read every new reference doc back against `references/self-check.md` and
  `references/anti-generic-review.md`'s own bar: each ties to concrete file paths, real examples
  (VIP Marina scenario, real hex codes, real model strings), and states its own limitations rather than
  overclaiming (see the "v1.0 note" callouts in the Pillar 3 docs).

## What is still open — your focus

1. **Pillar 3 hardening (evasion resistance).** `scripts/validate-output.py` is intentionally the
   non-adversarial first pass. It does NOT catch: colors via CSS variables, `hsl()`, named CSS colors
   (`rebeccapurple`), or JS-set colors; Hard NOs that are split across tags, obfuscated, base64-encoded,
   or hidden in alt-text/image content; anything outside HTML/CSS/SVG (no PDF, no raster pixel
   sampling). Both `references/design-system-lock.md` and `references/output-audit.md` name these gaps
   explicitly under "what v1.0 does not cover" — that's your build list.
2. **Red-team eval fixtures.** The 14 new eval cases I added are correctness cases (does the gate fire
   when it should), not adversarial cases (can the gate be evaded). Add fixtures that try to sneak a
   violation past `validate-output.py` (e.g., an out-of-lock color set via a CSS variable, a Hard-NO
   phrase split with an inline comment or zero-width character) and past the brief/options gates in
   `validate-run.py` (e.g., `handoffPageRead: "yes"` (string not bool), a `lockCompliant: true` on a
   concept whose `distinctionAxis` is a near-duplicate paraphrase rather than an exact string match —
   the current distinctness check is an exact-string dedupe, not a semantic one).
3. **Verify the six acceptance criteria.** I don't have them (see "Spec input gap" above). Get the real
   `revue-v1.0-build-handoff.md` if it exists, or get explicit confirmation of what the six criteria are,
   before you sign off — don't infer them from my file list.
4. **Packaging the installer.** README.md still says "Early and actively iterating (v0.6.0)" — I left
   it untouched since the task assigned packaging/tagging to you. Bump it, and check whether the
   install instructions (`cp -R revue-proof-workflow ...`) need updating for any new top-level files.
5. **Tag v1.0.0.** Not done — I only committed locally, per instructions, and did not push.
6. **Two sandbox artifacts you should clean up on a real machine** (I could not remove them — this
   session's mounted folder blocks all file deletion, confirmed by testing `rm`/`mv`/`os.remove` on a
   throwaway file; only creates and overwrites succeed):
   - `scratch.tmp` at the repo root — an empty file from my own delete-permission test. It is **not**
     staged or committed (I ran `git reset -- scratch.tmp` before committing), but it exists on disk and
     needs a plain `rm scratch.tmp` from a normal shell.
   - A stale `.git/index.lock` (created by an earlier read-only `git status` call in this session,
     which normally self-cleans but couldn't unlink it here) plus a handful of orphaned
     `.git/objects/*/tmp_obj_*` temp files left over from `git add`'s object-writing step in this
     restricted environment. Neither affects repo integrity (git tolerates orphaned loose-object temp
     files and I committed via a temp index at `/tmp/revue-index` to route around the stale lock rather
     than remove it), but a `git gc` and `rm .git/index.lock` on a normal machine will tidy them up.

## File map for your pass

- Harden: `scripts/validate-output.py`, `references/design-system-lock.md`, `references/output-audit.md`.
- Add red-team fixtures alongside: `examples/deliverable-pass.html`, `examples/deliverable-fail.html`,
  `examples/lock-fixture.json`, `examples/worked-creative-production.json`.
- Acceptance-criteria verification and packaging: repo root (`README.md`, `docs/release-notes.md`), and
  whatever `revue-v1.0-build-handoff.md` turns out to actually say.
- Everything else (Pillars 1, 2, 4, schema, `SKILL.md`, `scripts/validate-run.py`,
  `scripts/run-evals.py`) is done and green — 34/34 in `python3 scripts/run-evals.py`, all scripts
  `py_compile` clean.
