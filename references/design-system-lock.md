# Design System Lock (Pillar 3 — hardened)

Use this to define the fixed visual rules a creative-production deliverable must not violate. This is
what `references/creative-brief.md` asks the user to supply and what `references/output-audit.md`
checks the finished deliverable against.

The lock is enforced by an evasion-resistant audit (`scripts/validate-output.py`): colors in any CSS
form (hex, rgb, hsl, named, custom properties, gradients, SVG attributes, data-URI payloads) are
normalized and matched exactly against the palette; Hard NOs are caught even when split across tags,
entity-encoded, zero-width-joined, or respelled with homoglyphs; fonts are checked against the
typography list; and quantitative marketing claims must be allowlisted or they fail.

## Lock fields

- **Colors** — exact hex values that are in-lock. Anything else the deliverable can express is a
  violation, including near-miss shades (reported with the closest lock color — still failures).
  Include neutrals (white, black) explicitly if they are allowed — they are not assumed.
- **Typography** — allowed font-family names (the CSS `font-family` value, not just the display name).
  Generic families (`serif`, `sans-serif`, `system-ui`, ...) are always allowed as fallbacks.
- **Claims** — quantitative marketing claims that are approved to ship, each backed by a real source
  named in the brief. Any detected metric-like claim ("4.9 / 5", "200+ clients", "trusted by 500+")
  not matching this list fails the audit. Omit the field (or leave it empty) to forbid all
  quantitative claims.
- **Spacing/grid** — described in the brief; not machine-checked in v1.0 (no reliable stdlib way to
  parse computed layout from static HTML/CSS/SVG alone).
- **Logo usage** — notes on allowed logo files/marks; not machine-checked in v1.0.
- **Hard NOs** — forbidden strings, each with why. Matched against every recoverable text form of the
  deliverable (raw, entity-decoded, tag-stripped, separator-squashed, homoglyph-folded).

## Machine-checkable format

`scripts/validate-output.py` reads a lock as JSON:

```json
{
  "colors": ["#062456", "#FF5747", "#25C7C3", "#FFFFFF"],
  "typography": ["Quicksand", "Arial"],
  "hardNos": [
    { "pattern": "lorem ipsum", "why": "placeholder text must never ship" },
    { "pattern": "click here", "why": "brand voice: never generic link text" }
  ],
  "claims": ["4.8 / 5 rating from 132 reviews"]
}
```

`claims` is optional — leave it out to forbid all quantitative marketing claims.

Save it alongside the run (for example `examples/<project>-lock.json`) and reference its path from the
brief's Design System Lock field and the run's top-level `designSystemLock` object.

## Authoring format (in the brief)

When capturing a lock for the first time in `assets/intake-template.md`, write it as:

```markdown
## Design System Lock (required, blocks build)

Colors: #062456 (navy), #FF5747 (coral), #25C7C3 (aqua), #FFFFFF (white)
Typography: Quicksand, fallback Arial
Spacing/grid: 8px base unit, 1200px max content width
Logo usage: assets/logo-revue.svg only, minimum 32px height

## Hard NOs (required, blocks build)

HARD NO: lorem ipsum — placeholder text must never ship
HARD NO: click here — brand voice: never generic link text
```

Convert this into the JSON lock file before running the output audit — `scripts/validate-output.py`
does not parse the Markdown authoring format directly in v1.0.

## What "in lock" means

- A color is in-lock only if, after normalization from whatever syntax it was written in (hex of any
  length, rgb/rgba, hsl/hsla, named color, attribute hex, data-URI payload), its `#rrggbb` value
  exactly matches an entry in `colors`. No tolerance band — a near-miss shade is reported with the
  closest lock color and still fails.
- A Hard NO is hit if its `pattern` appears in any recoverable text form of the deliverable: raw,
  entity-decoded, tag/comment-stripped, whitespace/separator-squashed, casefolded, zero-width-stripped,
  and homoglyph-folded. Splitting, encoding, or respelling the phrase does not evade the match.
- A quantitative claim is in-lock only if it matches an entry in `claims`. No `claims` list means no
  quantitative claims ship.
- A font is in-lock if it is in `typography` or is a CSS generic family.

## Relationship to the rest of revüe

- Captured in `references/creative-brief.md`, checked per-concept in
  `references/options-and-refine.md`, enforced on the finished deliverable in
  `references/output-audit.md` via `scripts/validate-output.py`.
