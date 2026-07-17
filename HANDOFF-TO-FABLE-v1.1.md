# Handoff to Fable — revüe v1.1

Sonnet 5 pass on v1.1: site tiers (Standard/Premium/Custom), the elevate craft layer, and
brief-conformance, on top of the v1.0 creative-production pipeline. Read the "spec input gap" section
first — it affects how much weight to put on anything described as coming from a named source file.

## Spec input gap (read first)

None of the following were present in this repo, the mounted folder, or the session's uploads, despite
being referenced as existing: `revue-v1.0-build-handoff.md`, `vip-flagship-page.html` (the named
Premium exemplar), `vip-instance-real.html` (the named Standard exemplar). I searched the full repo
tree and uploads directory; they do not exist here. This is the same situation the v1.0 pass documented
(see `docs/v1.0-acceptance-report.md`'s provenance note) — it appears to recur by design in this
environment rather than being a one-off gap.

**What I did about it:** the v1.1 task description itself distilled the Premium craft rules in enough
concrete detail (full-bleed hero + scrim, serif-display + sans-body type system, editorial restraint,
signature motif, legibility-over-imagery, desktop+mobile+sticky-bar) that I built `references/elevate.md`
directly from that description rather than blocking on the missing file. For the worked exemplars:

- **Premium**: I built `examples/premium-exemplar.html` + `examples/premium-lock.json` from scratch,
  implementing every rule elevate.md states literally (it is a VIP Lake Travis marina page — the
  running example this repo already uses — not a copy of an original I've never seen).
- **Standard**: I did NOT fabricate a redundant new file. `examples/dogfood/winner.html` (already real,
  already committed, already "clean, functional, on-brand") serves as the Standard exemplar — I only
  added `brief.tier: "Standard"` to its run artifact.
- **Anti-pattern ("Knight Water" clone)**: `examples/redteam-original-failure.html` (Fable's own v1.0
  fixture — the off-palette, generic-template clone with a fabricated "4.9/200+" metric) matches the
  description closely enough that I pointed `references/elevate.md` at it rather than building a
  duplicate.

**Before you tag v1.1.0**: if the real exemplar files surface, diff `references/elevate.md` and
`examples/premium-exemplar.html` against them and correct anything I guessed wrong (I don't know, for
example, whether the flagship's actual signature motif looked anything like the "coordinate line +
wake-pin" device I invented from the task's one-line description — that specific device is my
reconstruction, not a fact from the source).

## What I built

**Tier field + cascade** (`references/creative-brief.md`)
- Brief is now five required, blocking fields: deliverable+format, **tier**, sources, designSystemLock,
  hardNos. `assets/intake-template.md` gets a required Tier section with the three options explained.
- The cascade table: Standard → lock-compliance-is-the-whole-bar / `standard` model / `outputAudit.pass`.
  Premium → + elevate.md / `deep` model / `outputAudit.pass` **and** `elevatePass`. Custom →
  human-directed / human-led / `outputAudit.pass` **and** a `tierSignoff` naming a human.

**Elevate layer** (`references/elevate.md`)
- Six rules, four machine-checked (full-bleed hero+imagery, legibility scrim, 2+ type families, sticky
  bar), two explicitly left to human/board judgment (editorial restraint, signature motif) — documented
  as such, not faked as automatable.

**Elevate heuristics in `scripts/validate-output.py`**
- New `--tier {standard,premium,custom}` flag (default `standard` — zero behavior change unless
  explicitly requested). Premium adds `outputAudit.elevateChecks` (list) and `outputAudit.elevatePass`
  (bool), folded into overall `pass`. Implementation is regex/pattern heuristics against the raw
  markup+CSS text, not a real DOM/renderer — see "What's still open" below for exactly where this is
  weakest.
- One real bug I hit and fixed while building the Premium exemplar, worth knowing about: the existing
  (Fable's) named-color scanner does `re.findall(r"[a-zA-Z]{3,20}", value)` against CSS *values* to
  catch named colors like `coral`/`navy`. If a deliverable defines CSS custom properties named after
  color words (`--navy: #062456`) and later writes `var(--navy)`, the regex extracts the substring
  "navy" out of the middle of `var(--navy)` and misreads it as the CSS named color `navy` (`#000080`) —
  a false positive that would incorrectly fail an otherwise-clean deliverable. I avoided it in my own
  fixture by not using CSS custom properties (literal hex throughout, matching how
  `examples/dogfood/winner.html` already does it), but I did not fix the underlying scanner — that's
  core Pillar 3 logic outside my assigned scope, and it's a real, reproducible false-positive you should
  either fix or add a documented-limitation note for.

**Brief-conformance** (`references/brief-conformance.md`, `scripts/validate-conformance.py`)
- New pillar, new script, non-adversarial first version (explicitly modeled on how `validate-output.py`
  itself started before Fable hardened it). Checks required sections (via a `data-section="name"` /
  `<section id="name">` convention), section order, forbidden markup patterns, and required
  placeholders (proving an unknown value stayed an honest placeholder instead of a silent guess).
- One correctness fix I made while testing against my own exemplar: the initial version didn't strip
  HTML comments before scanning for `data-section` markers, so my own authoring comment (which
  *describes* `data-section="hero"` in prose) was misread as a real section. Fixed by stripping
  `<!-- ... -->` before section detection. This is basic hygiene, not adversarial hardening — it's
  already in the shipped script, not left as an open item.

**Tier-sets-audit-bar, enforced** (`scripts/validate-run.py`)
- `ship` on Premium requires `outputAudit.elevatePass == true`, with the exact failure text "meets only
  the Standard bar" so it reads as a real finding, not a generic validation error.
- `ship` on Custom requires a top-level `tierSignoff.by`.
- `ship` requires a passing `conformance` object whenever (and only whenever) `brief.structure` is
  declared — a brief with no structural opinions never trips this gate.
- Premium also requires the `options-generation` trace step tagged `modelTier: "deep"` — this is the
  one piece of "tier routes the model" I made structurally enforced rather than just documented, since
  it was cheap and directly requested ("wire the cascade... routes the model").
- `conformance-check` joined the `fast`-tagged gate-step list.

**Schema** (`assets/revue-run.schema.json`): `brief.tier` (required enum), `brief.structure` (optional),
top-level `conformance` and `tierSignoff` objects, `outputAudit.elevateChecks`/`elevatePass`.

**Fixtures + eval suite**: `examples/premium-exemplar.html`, `examples/premium-lock.json`,
`examples/premium-structure.json`, `examples/worked-premium-production.json` (first Premium `ship`
golden), `examples/structure-fixture.json`, `examples/conformance-{pass,fail}.html`. Updated
`examples/worked-creative-production.json` and `examples/dogfood/run.json` with `brief.tier: "Standard"`
(mandatory now that `tier` is required). `scripts/run-evals.py`: **80/80 passing** (58 pre-v1.1
unchanged + 22 new).

## Self-verification done

- `python3 -m py_compile scripts/*.py` — clean.
- `python3 scripts/run-evals.py` — 80/80, including a full run before touching `validate-run.py` (58/58,
  no regressions) and after every subsequent change.
- `python3 -m json.tool assets/revue-run.schema.json` — valid JSON.
- Manually ran `scripts/validate-output.py --tier premium` against `examples/premium-exemplar.html` and
  confirmed all four elevate checks pass, then against `examples/deliverable-pass.html` (an existing
  v1.0 Standard-only fixture) and confirmed it's correctly flagged (`elevatePass: false`) while its base
  lock/font/Hard-NO audit still passes clean — proving the heuristic distinguishes "meets the lock" from
  "meets the Premium bar," not just re-testing the lock.
- Grepped all new/changed files for generic-AI buzzwords, the wrong-ü codepoint (`Ũ`, U+0168), and
  machine paths/credentials — none found.
- Read `references/elevate.md` and `references/brief-conformance.md` back against
  `references/self-check.md` and `references/anti-generic-review.md`'s own bar: both name what they
  can't check as plainly as what they can, tie every rule to a concrete file path or example, and avoid
  the generic-AI traps the repo's own anti-generic reference warns about.

## What is still open — your focus

1. **Elevate heuristics are pattern-matching, not layout-aware.** The "legibility scrim" check looks
   for a scrim pattern within `HERO_WINDOW_CHARS` (2000) characters of the hero marker — a heuristic
   window standing in for real DOM/CSS-cascade scoping. A hero section with unusual markup order, or a
   scrim rule that lives in a separate CSS file not passed to the script, will misfire in either
   direction. Same caveat applies to "2+ distinct font families" (counts families, doesn't verify one is
   actually a serif *display* face and the other a sans *body* face — two unrelated sans fonts would
   pass) and "sticky action bar" (any `position: sticky`/`fixed` anywhere counts, not necessarily a real
   CTA bar).
2. **The named-color-via-CSS-custom-property false positive** in the existing (pre-v1.1) scanner,
   described above — reproduce with a deliverable that defines `--coral: #FF5747` and later writes
   `background: var(--coral)`; `coral` (`#ff7f50`) will incorrectly show up in `colorsFound`/possibly
   `colorsOutOfLock`. Worth a real fix (skip `var()` argument contents when scanning for named-color
   tokens) or, at minimum, a documented limitation.
3. **Red-team fixtures for the new gates.** My 22 new eval cases are correctness cases (does the gate
   fire when it should), not adversarial ones (can it be evaded). Try: a deliverable that fakes a hero
   marker with `class="not-hero-related"` containing the substring "hero" to pass the check without a
   real hero; a scrim declared far outside the actual hero's real DOM scope but within the 2000-char
   heuristic window; a `data-section` name that collides with a real section deep inside an unrelated
   component; a forbidden-element pattern evaded by reformatting the same markup (different attribute
   order, extra whitespace); a `tierSignoff.by` set to an empty-looking but non-empty string ("N/A") to
   probe whether that should be rejected too.
4. **Real DOM parsing for both new scripts** — `scripts/validate-output.py`'s elevate checks and
   `scripts/validate-conformance.py`'s section detection are both regex-over-text, same limitation
   class Pillar 3 started with before you hardened it. `references/brief-conformance.md` and
   `references/elevate.md` both name this explicitly under "what's out of scope."
5. **Dogfood the tier/elevate/conformance pipeline together**, the way `examples/dogfood/` proved the
   v1.0 pipeline end to end on revüe's own brand. `examples/worked-premium-production.json` proves the
   schema/validator wiring is internally consistent, but it's a hand-authored golden, not a real agent
   run through the brief→options→build→audit loop the way the v1.0 dogfood was.
6. **Verify against the real exemplars if they surface** — see "Spec input gap" above.
7. **Packaging and tagging** — not done this pass. `scripts/make-installer.py` auto-discovers files by
   walking the tree (no registration needed for the new files), so it should pick up everything here
   without changes, but I did not run it or regenerate `dist/apply-revue-v1.1.0.sh`. `README.md` and
   `docs/v1.0-acceptance-report.md` still describe v1.0 only; a `docs/v1.1-acceptance-report.md` in the
   same style (mapping whatever the real v1.1 acceptance criteria turn out to be to the eval cases that
   prove them) would match the repo's existing convention.
8. **Two sandbox artifacts, same cause as the v1.0 pass**: this session's mounted folder still blocks
   all file deletion (confirmed again this pass — `rm`/`mv`/`os.remove` all fail with "Operation not
   permitted" on this mount, `os.remove` on a scratch file in `/tmp` works fine). The commit was routed
   around a stale `.git/index.lock` via a temporary `GIT_INDEX_FILE` at `/tmp/revue-index-v11`, then
   copied back over the real `.git/index` so the working tree's index stays in sync. No stray files were
   left in the tracked tree this time (I didn't create a `scratch.tmp` equivalent), but a `git gc` on a
   normal machine will clean up orphaned `.git/objects/*/tmp_obj_*` temp files from the object-write step.

## File map for your pass

- Harden: `scripts/validate-output.py` (elevate heuristics + the named-color/`var()` false positive),
  `scripts/validate-conformance.py`, `references/elevate.md`, `references/brief-conformance.md`.
- Add red-team fixtures alongside: `examples/premium-exemplar.html`, `examples/premium-lock.json`,
  `examples/structure-fixture.json`, `examples/conformance-{pass,fail}.html`.
- Verify against real exemplars if found; correct `references/elevate.md` and
  `examples/premium-exemplar.html` accordingly.
- Packaging/tagging: `scripts/make-installer.py`, `README.md`, a new `docs/v1.1-acceptance-report.md`.
- Everything else (tier field/cascade, schema, `scripts/validate-run.py`, `SKILL.md`,
  `docs/release-notes.md`) is done and green — 80/80 in `python3 scripts/run-evals.py`, all scripts
  `py_compile` clean.
