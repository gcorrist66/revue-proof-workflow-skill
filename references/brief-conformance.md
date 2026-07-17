# Brief Conformance (structure check)

Use this to check a finished creative-production deliverable against the **structure** the brief
actually promised — independent of the design-system lock. The lock (`references/design-system-lock.md`)
proves the deliverable stayed inside its colors, fonts, and Hard NOs. This proves it has the sections
the brief required, in the order the brief required, without the elements the brief banned, and with
the placeholders the brief said were still open — not silently guessed values standing in for them.

**v1.1 note:** this is the first working conformance check, non-adversarial scope. It matches literally
(exact strings, a documented section-marking convention) rather than resisting evasion. Hardening
(fuzzy section detection, obfuscation-resistant forbidden-element matching) is Fable's pass, the same
way `scripts/validate-output.py` started as a scaffold before it was hardened.

## When it runs

Only when the brief declares a `structure` spec — not every brief needs one. A simple one-section page
has nothing to check structural order against. Declare `brief.structure` when the brief has opinions
about section presence, order, banned elements, or placeholders that must stay visible. When declared,
the check is required before a `ship` verdict, the same way the output audit is.

## The structure spec

Add a `structure` object to the brief (`assets/revue-run.schema.json`):

```json
{
  "requiredSections": ["hero", "offer", "proof", "cta"],
  "sectionOrder": true,
  "forbiddenElements": [
    { "pattern": "class=\"custom-header\"", "why": "brief specifies the default masthead only" }
  ],
  "requiredPlaceholders": ["[CLIENT_PHONE]"]
}
```

- **`requiredSections`** — section names the deliverable must contain.
- **`sectionOrder`** — if `true`, required sections must appear in this relative order (sections not
  in the list are ignored for ordering purposes).
- **`forbiddenElements`** — literal markup patterns that must not appear, each with why. This is the
  structural equivalent of a Hard NO — a brief that says "no carousel, no custom header" writes it here.
- **`requiredPlaceholders`** — literal strings that must appear verbatim when the brief doesn't yet
  have a real value for something (a phone number, a launch date, a client name). Their presence
  proves the builder left the gap honestly visible instead of inventing a plausible-looking value —
  the same Honesty rule `references/review-board.md` already enforces, applied to structure.

## Section-marking convention

`scripts/validate-conformance.py` recognizes a section by `data-section="name"` anywhere in the
markup, or by `<section id="name">`. Mark every section the brief cares about with one of these —
a deliverable that doesn't use the convention shows zero sections found, which is itself a real,
actionable finding (the deliverable's structure cannot be verified, so it cannot conform).

```html
<section data-section="hero">…</section>
<section id="offer">…</section>
```

## Procedure

```bash
python3 scripts/validate-conformance.py <deliverable> --structure <structure.json> --json
```

1. Collect every `data-section`/`<section id>` name, in document order.
2. Compare against `requiredSections` — anything missing is a violation.
3. If `sectionOrder` is `true`, check every required-section pair keeps its declared relative order.
4. Scan the raw markup for each `forbiddenElements[].pattern` — a literal match is a violation.
5. Scan for each `requiredPlaceholders` string — its absence is a violation (it was likely replaced
   with a guess instead of staying an honest placeholder).
6. Exit `0` with no violations, `1` with at least one, `2` on usage errors.

## Result shape (`conformance`)

```json
{
  "deliverablePath": "outputs/vip-marina-landing.html",
  "structurePath": "examples/structure-fixture.json",
  "sectionsFound": ["hero", "offer", "cta"],
  "missingSections": ["proof"],
  "orderViolations": [],
  "forbiddenHits": [],
  "missingPlaceholders": ["[CLIENT_PHONE]"],
  "pass": false
}
```

Attach this object to the run as `conformance` (`assets/revue-run.schema.json`).

## Gate rule

A `ship` verdict on a `"produces": "creative-production"` run whose brief declares a `structure` spec
is invalid unless `conformance.pass` is `true`. `scripts/validate-run.py --strict` enforces this the
same way it enforces `outputAudit.pass`. If the brief never declared a `structure` spec, this gate does
not apply — there is nothing to conform to.

## What v1.1 does not cover

- Real DOM parsing — a deliverable that nests or reorders markup in ways a regex can't see may confuse
  section detection. The `data-section` convention exists specifically to avoid needing a parser.
- Evasion resistance on `forbiddenElements` — a banned pattern split across tags, whitespace-varied, or
  written a different but equivalent way (a different class name doing the same visual job) is not
  caught. `scripts/validate-output.py`'s Hard-NO scanning shows the hardened version of this same idea;
  this pillar starts where that one started.
- Semantic placeholder matching — only the exact declared placeholder string is checked. A close but
  not identical placeholder (`[Client Phone]` vs. `[CLIENT_PHONE]`) is treated as missing.

## Relationship to the rest of revüe

- Declared in the brief alongside the design-system lock (`references/creative-brief.md`,
  `references/design-system-lock.md`).
- Runs at `fast` tier (`references/model-routing.md`) — deterministic pattern matching, not judgment.
- For Premium-tier work, `references/elevate.md`'s craft requirements are a separate, additional bar —
  conformance checks structure the brief specified; elevate checks craft the tier requires.
