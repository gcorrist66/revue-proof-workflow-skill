# Output Audit (Pillar 3 — scaffolding)

Use this to check a finished creative-production deliverable against its design-system lock before any
`ship` verdict. This is the proof step for `references/design-system-lock.md` — the lock says what is
allowed, the audit proves the actual deliverable stayed inside it.

**v1.0 note:** this is the first working audit, covering the common, non-adversarial case — a real
HTML/CSS/SVG file with literal colors and literal text. It is not yet hardened against an actor
deliberately trying to sneak a violation past it. See `HANDOFF-TO-FABLE.md` for what's still open.

## When it runs

After the deliverable exists, before the verdict is written — for every `"produces": "creative-
production"` run, whenever the verdict under consideration is `ship`. Run it once per deliverable
revision; re-run after any fix.

## Procedure

```bash
python3 scripts/validate-output.py <deliverable-path> --lock <lock.json> --json
```

1. Extract every hex color the deliverable actually contains (`#abc`, `#aabbcc`, `rgb()`/`rgba()`
   normalized to hex).
2. Compare against the lock's `colors` list — anything not in the list is a color-lock violation.
3. Scan the deliverable's raw text for every `hardNos[].pattern` — a match is a Hard-NO violation.
4. Exit `0` with no violations, `1` with at least one.

## Result shape (`outputAudit`)

```json
{
  "deliverablePath": "outputs/vip-marina-landing.html",
  "lockPath": "examples/vip-marina-lock.json",
  "colorsFound": ["#062456", "#ff5747", "#111111"],
  "colorsOutOfLock": ["#111111"],
  "hardNoHits": [],
  "pass": false
}
```

Attach this object to the run as `outputAudit` (`assets/revue-run.schema.json`).

## Gate rule

A `ship` verdict on a `"produces": "creative-production"` run is invalid unless `outputAudit.pass` is
`true`. `scripts/validate-run.py --strict` enforces this, the same way it already blocks `ship` over a
failing scorecard row. `ship with changes` may carry a failing audit as a listed, bounded fix.

## What v1.0 does not cover

- Colors expressed as CSS variables, `hsl()`, named colors (`rebeccapurple`), or colors set/changed via
  JavaScript.
- Hard NOs that are split across tags, obfuscated, base64-encoded, or represented only as image/alt-text
  content.
- Anything outside HTML/CSS/SVG (no PDF parsing, no raster-image color extraction, no PNG/JPEG pixel
  sampling).

These are exactly where an actor motivated to slip a violation past the audit would go first — that
hardening, plus adversarial eval fixtures, is Fable's pass. See `HANDOFF-TO-FABLE.md`.

## Relationship to the rest of revüe

- Reads the lock defined in `references/design-system-lock.md`.
- Gates the `ship` verdict alongside `references/board-verdict-schema.md` and
  `references/self-check.md`.
- Runs at `fast` tier (`references/model-routing.md`) — it is a script invocation, not a judgment call.
