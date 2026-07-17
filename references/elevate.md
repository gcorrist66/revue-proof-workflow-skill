# Elevate: the Premium craft bar

Use this when `brief.tier` is `Premium` (`references/creative-brief.md`). It is a second, additional
bar on top of the design-system lock — the lock says a deliverable didn't break the rules; elevate says
it earned the tier. Standard-tier work does not pull this in. Custom-tier work is human-led and is
judged against the brief's own bespoke direction, not this checklist.

**Provenance note.** This reference was built from the craft bar as distilled in the v1.1 task
description, not by reading the named exemplar file directly — `vip-flagship-page.html` was not
present in this repo or the session's uploads (see `HANDOFF-TO-FABLE-v1.1.md`). The worked exemplar
this pillar ships with, `examples/premium-exemplar.html`, is a reconstruction built to satisfy every
rule below, not a copy of the original.

## The rules

1. **Full-bleed cinematic imagery with a legibility scrim.** The hero is not a colored box with text
   in it — it is imagery that fills the viewport edge to edge. Because of that, every piece of text or
   CTA sitting over it needs a scrim: a gradient, a semi-transparent solid, or a text-shadow strong
   enough that the copy reads instantly regardless of what is directly behind it.
2. **A display type system: serif display + sans body.** Headlines run in a serif display face
   (the exemplar uses Fraunces); body copy, labels, and UI text run in a plain sans (Quicksand/Arial).
   One family for voice, one for function — never the same face doing both jobs, and never more than
   these two doing the talking.
3. **Editorial restraint and negative space.** One message per section. No stacked CTAs, no competing
   badges, no "just add one more trust signal" creep. If a section has three things fighting for
   attention, cut two. Space is not empty — it's what makes the one thing that's there read as
   deliberate instead of default.
4. **A repeating signature motif.** Pick one small, brand-specific device and repeat it as a structural
   element — not decoration reused at random, a device that shows up in the same role every time (the
   exemplar's coordinate line + wake-pin mark appears in the header, the sticky bar, and the footer,
   always in the same spot doing the same job: "you are here, this is us"). A motif used once is an
   accident; used three times in the same role, it's a signature.
5. **Legibility over imagery, always.** Rule 1 restated as a hard boundary: text and CTAs never sit
   directly on a bright or busy region of an image with no backing. If the imagery is too busy for a
   scrim to fix, move the text to a solid panel instead of forcing it over the image.
6. **Desktop + mobile + a sticky action bar.** Premium's required states are one more than Standard's:
   both breakpoints, plus a persistent booking/CTA bar that stays reachable as the page scrolls — the
   reservation ask is never more than one thumb-reach away.

## What's machine-checked vs. judged

`scripts/validate-output.py --tier premium` checks four of these rules by pattern, heuristically:

| Rule | Machine check | What it can't see |
| --- | --- | --- |
| 1. Full-bleed hero + scrim | hero section marker + background image/`<img>` + a scrim pattern (gradient/rgba/`text-shadow`/`overlay`) nearby | whether the scrim is visually *enough* — a technically-present gradient that's too subtle still passes |
| 2. Display type system | 2+ distinct non-generic font families declared | whether they're actually a serif-display/sans-body *pairing*, or just two unrelated fonts |
| 6. Sticky action bar | `position: sticky` or `position: fixed` anywhere | whether it's actually the booking bar, or an unrelated fixed element |

Rules 3, 4, and 5 are **not** machine-checked — restraint, a genuine signature motif, and true
legibility-over-imagery judgment require actually looking at the rendered page. These stay a board/
self-check call (`references/review-board.md`, `references/self-check.md`): note explicitly in the
scorecard or evidence whether they were met, the same way `references/output-audit.md` documents what
its own script can't see.

## Result shape

The four machine-checked rules land in `outputAudit.elevateChecks` (`assets/revue-run.schema.json`),
each `{ "check": ..., "status": "pass" | "fail", "detail": ... }`, folded into a single
`outputAudit.elevatePass` boolean. `elevatePass` is required `true` before a `ship` verdict on any
Premium-tier run — a deliverable that passes the base lock but fails elevate has met only the Standard
bar, and `scripts/validate-run.py --strict` will say exactly that.

## Procedure

```bash
python3 scripts/validate-output.py <deliverable> --lock <lock.json> --tier premium --json
```

Same invocation as the Standard-tier audit, with `--tier premium` added. `--tier standard` (the
default) never runs these checks or adds `elevateChecks` to the result — a Standard-tier deliverable is
not held to a bar it was never asked to clear.

## Worked exemplars

- **Premium**: `examples/premium-exemplar.html` + `examples/premium-lock.json`, wired up end to end in
  `examples/worked-premium-production.json` (a full `ship` run: brief with `tier: "Premium"`, three
  concepts with only the Premium-bar one kept, `elevatePass: true`, conformance pass).
- **Standard**: `examples/dogfood/winner.html` (`examples/dogfood/run.json`, `tier: "Standard"`) — clean,
  functional, on-brand, no elevate layer pulled in. Compare the two directly to see what Premium adds.
- **Anti-pattern**: `examples/redteam-original-failure.html` — the off-palette, generic-template clone
  with a fabricated metric. It fails the base lock audit regardless of tier; it is also the clearest
  illustration of what "meets neither bar" looks like.

## Relationship to the rest of revüe

- Gated by `brief.tier` (`references/creative-brief.md`), which also sets the model tier
  (`references/model-routing.md`: Premium creative generation runs `deep`) and the audit bar (this file).
- Runs inside `scripts/validate-output.py` (`references/output-audit.md`) — no separate elevate script;
  `output-audit` stays the single `fast`-tagged gate step for both the lock and the craft bar.
- Structure (section presence/order) is a separate concern — see `references/brief-conformance.md`.
