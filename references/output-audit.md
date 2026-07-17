# Output Audit (Pillar 3 — hardened)

Use this to check a finished creative-production deliverable against its design-system lock before any
`ship` verdict. This is the proof step for `references/design-system-lock.md` — the lock says what is
allowed, the audit proves the actual deliverable stayed inside it.

The audit is **fail-closed**: every color the deliverable can express must map exactly to the lock's
palette, every font must map to the lock's typography, Hard-NO text must not appear in any recoverable
form, and every quantitative marketing claim must be explicitly approved. Anything the audit cannot
verify — an external stylesheet, a binary file, a deliverable with no detectable colors — is a
failure, not a pass. A gate that can be gamed has failed; this one is built to be attacked.

## When it runs

After the deliverable exists, before the verdict is written — for every `"produces": "creative-
production"` run, whenever the verdict under consideration is `ship`. Run it once per deliverable
revision; re-run after any fix.

## Procedure

```bash
python3 scripts/validate-output.py <deliverable> [more files...] --lock <lock.json> --json
```

Add `--tier premium` when `brief.tier` is `Premium` to also run the elevate heuristics
(`references/elevate.md`) and fold them into `pass`. `--tier standard` (the default) never adds them —
Standard-tier work is not held to a bar it wasn't briefed for.

Pass every file the deliverable is made of (the HTML plus any local CSS). The audit:

1. Extracts every color the deliverable can express: hex (`#abc`, `#aabbcc`, `#aabbccdd`, and legacy
   hash-less attribute hex like `bgcolor="112233"`), `rgb()`/`rgba()` in comma, modern space, and
   percentage syntax, `hsl()`/`hsla()` in any hue unit, named CSS colors in style positions
   (including CSS custom-property definitions and literal color assignments inside scripts), SVG
   presentation attributes, gradients, entity-encoded values, and colors inside base64/percent-encoded
   data URIs and `atob("...")` payloads. Anything not exactly in the lock's `colors` is a violation;
   near-misses are labeled with the closest lock color, and they still fail.
2. Extracts every `font-family` (CSS declarations, `font` shorthand, SVG attributes). Any non-generic
   family not in the lock's `typography` is a violation.
3. Scans every recoverable text form for Hard NOs: raw text, entity-decoded text, tag- and
   comment-stripped visible text, and a separator-squashed form — after Unicode compatibility
   normalization, zero-width and combining-character stripping, casefolding, and homoglyph folding
   (Cyrillic/Greek lookalikes). Splitting a Hard NO across tags, hiding it in alt-text, encoding it,
   or respelling it with lookalike characters does not evade the scan.
4. Scans visible text for fabricated-metric patterns — star ratings ("4.9 / 5", "rated 4.9"),
   social-proof counts ("200+ happy clients"), "trusted by N", star-glyph runs, percent claims about
   customers/uptime/satisfaction, "#1 rated". Any such claim not matched by the lock's `claims`
   allowlist is a violation. No allowlist means no quantitative claims may ship.
5. Fails as *unverifiable* anything it cannot see through: external stylesheets/`@import`, external
   scripts, iframes, binary formats (PDF/PNG/JPEG/zip), or a deliverable with no detectable colors.
6. Exits `0` with no violations, `1` with at least one, `2` on usage errors.

## Result shape (`outputAudit`)

```json
{
  "deliverablePath": "outputs/vip-marina-landing.html",
  "lockPath": "examples/lock-fixture.json",
  "colorsFound": ["#062456", "#ff5747", "#111111"],
  "colorsOutOfLock": ["#111111"],
  "nearMisses": {},
  "fontsFound": ["Arial", "Quicksand"],
  "fontsOutOfLock": [],
  "hardNoHits": [],
  "unverifiedClaims": ["4.9 / 5", "200+ happy clients"],
  "unverifiable": [],
  "pass": false
}
```

Attach this object to the run as `outputAudit` (`assets/revue-run.schema.json`).

## Gate rule

A `ship` verdict on a `"produces": "creative-production"` run is invalid unless `outputAudit.pass` is
`true`. `scripts/validate-run.py --strict` enforces this, the same way it already blocks `ship` over a
failing scorecard row. `ship with changes` may carry a failing audit as a listed, bounded fix.

## Approving a real metric

If the deliverable legitimately carries a number ("4.8 / 5 from 132 reviews" backed by an actual
review page), put the claim in the lock's `claims` list with its source noted in the brief. The audit
approves a detected claim only when it matches an allowlisted entry. This is deliberate: the original
failure this pillar exists to prevent was a fabricated "4.9 / 200+" metric that shipped unchecked —
under this audit, an unapproved metric can never ride along silently.

## What remains out of scope (and why it still can't ship a lie)

- **Raster pixel sampling** — an embedded photo/logo PNG is noted in the audit output but its pixels
  are not color-checked. Raster payloads are flagged as notes; SVG and text payloads inside data URIs
  ARE decoded and audited.
- **JS execution** — styles computed by running code are not resolved; literal color values inside
  scripts ARE scanned, and external scripts fail the audit as unverifiable.
- **PDF parsing** — a PDF deliverable fails as unverifiable rather than passing unexamined.

Each gap fails closed: the audit refuses to pass what it cannot read, rather than passing it.

## Evasion coverage is proven, not claimed

`scripts/run-evals.py` includes red-team fixtures (`examples/redteam-*.html`) that actively try to
sneak past this audit — CSS-variable colors, hsl near-misses, homoglyph Hard NOs, data-URI payloads,
the original generic-clone-with-fabricated-metric failure — and asserts each one is REJECTED. If the
suite is green, the evasion coverage above is live, not aspirational.

## Relationship to the rest of revüe

- Reads the lock defined in `references/design-system-lock.md`.
- Gates the `ship` verdict alongside `references/board-verdict-schema.md` and
  `references/self-check.md`.
- Runs at `fast` tier (`references/model-routing.md`) — it is a script invocation, not a judgment call.
- For Premium-tier work, also runs the elevate heuristics (`references/elevate.md`) via `--tier
  premium`; `outputAudit.elevatePass` is required `true` before `ship`. Structure (section presence and
  order) is a separate check — see `references/brief-conformance.md`.
