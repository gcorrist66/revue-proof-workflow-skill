# Design System Lock (Pillar 3 — scaffolding)

Use this to define the fixed visual rules a creative-production deliverable must not violate. This is
what `references/creative-brief.md` asks the user to supply and what `references/output-audit.md`
checks the finished deliverable against.

**v1.0 note:** this is the first working lock, not the hardened version. It does exact matching —
literal hex values and literal Hard-NO strings. It does not yet catch near-miss colors, obfuscated or
encoded Hard-NO text, or CSS variables/computed colors. See `HANDOFF-TO-FABLE.md` for what evasion
resistance still needs to be built.

## Lock fields

- **Colors** — exact hex values that are in-lock. Anything else found in the deliverable is a
  violation. Include neutrals (white, black) explicitly if they are allowed — they are not assumed.
- **Typography** — allowed font-family names (the CSS `font-family` value, not just the display name).
- **Spacing/grid** — described in the brief; not machine-checked in v1.0 (no reliable stdlib way to
  parse computed layout from static HTML/CSS/SVG alone).
- **Logo usage** — notes on allowed logo files/marks; not machine-checked in v1.0.
- **Hard NOs** — literal forbidden strings, each with why. Checked as a case-insensitive substring match
  against the deliverable's raw text.

## Machine-checkable format

`scripts/validate-output.py` reads a lock as JSON:

```json
{
  "colors": ["#062456", "#FF5747", "#25C7C3", "#FFFFFF"],
  "typography": ["Quicksand", "Arial"],
  "hardNos": [
    { "pattern": "lorem ipsum", "why": "placeholder text must never ship" },
    { "pattern": "click here", "why": "brand voice: never generic link text" }
  ]
}
```

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

- A color is in-lock only if its hex value (case-insensitive, 3-digit hex expanded to 6) exactly
  matches an entry in `colors`. No tolerance band.
- A Hard NO is hit if its `pattern` string appears anywhere in the deliverable's raw text, case-
  insensitive substring match. No regex, no fuzzy matching, no encoding-awareness in v1.0.

## Relationship to the rest of revüe

- Captured in `references/creative-brief.md`, checked per-concept in
  `references/options-and-refine.md`, enforced on the finished deliverable in
  `references/output-audit.md` via `scripts/validate-output.py`.
