# revüe Brand Notes

## Name

Use `revüe` for the public-facing product name.

Pronunciation: `reh-view`, like `review`.

## Logo direction

Lowercase wordmark with the `ü` as the hero character:

- `r`, `e`, `v`, and final `e`: deep navy.
- `ü`: coral, larger than the other letters.
- Two dots over the `ü`: eyes.
- Bottom curve of the `ü`: a smile.
- Check badge: aqua circle with a white check, on a white halo ring, perched on the top-right
  shoulder of the final `e` (it overlaps the corner of the `e`, not floating beside it).

## Expression system

The mark is also a verdict indicator. The same coral ü changes mouth, and the badge changes color
and symbol, to signal the review outcome:

- `ship`: full smile, aqua check badge — `assets/logo-state-ship.svg`
- `ship with changes`: soft smile, aqua check — `assets/logo-state-changes.svg`
- `caution`: flat mouth, amber `!` badge — `assets/logo-state-caution.svg`
- `block`: frown, red `x` badge — `assets/logo-state-block.svg`

The face stays coral in every state so the brand reads consistently; the badge carries the
color-coding. See `assets/logo-states.png` for all four, and `references/board-verdict-schema.md`
for the verdict definitions.

## Colors

- Navy: `#062456`
- Coral: `#FF5747`
- Aqua: `#25C7C3`
- Amber (caution badge): `#F2A64D`
- Red (block badge): `#E5484D`
- White: `#FFFFFF`

## Typography

The wordmark is set in a rounded geometric sans. The packaged SVGs use a fallback stack
(Avenir Next Rounded → Nunito → Quicksand → Arial Rounded MT Bold → Arial). Avenir Next Rounded is
a licensed font: it renders locally on macOS, but do NOT outline it into this public repo. For a
distributable, portable wordmark, lock the type to a libre rounded typeface (for example Quicksand,
Baloo 2, or Fredoka) and outline that to vector paths.

## Usage

- `assets/logo-revue.svg` — full wordmark.
- `assets/logo-mark.svg` — favicon, avatar, or square app icon.

## Trademark / brand note

The MIT license covers the skill source code and packaged workflow files. The `revüe` name, logo, and
brand assets should not be used to present a separate product or service as the official revüe project
without permission.
