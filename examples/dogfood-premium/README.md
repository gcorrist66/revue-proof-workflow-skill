# Dogfood: the v1.1 Premium pipeline run on revüe's own launch page

This directory is a complete, real end-to-end run of the v1.1 tier pipeline — brief with
`tier: "Premium"`, a declared structure spec, production against the lock, and every new gate firing
in sequence on real work. The deliverable is a Premium launch page for the tier system itself, so the
page had to pass the same gates it describes.

## The run, in order

1. **Brief declared Premium** with a structure spec (`structure.json`: hero → tiers → proof → cta,
   no bespoke masthead, `[LAUNCH_DATE]` must stay a visible placeholder) and a lock (`lock.json`)
   that adds Fraunces to the revüe palette, because Premium requires a serif display face
   (`references/elevate.md`).
2. **Three distinct concepts** were generated at the `deep` model tier (Premium routes generation
   there — `references/model-routing.md`), culled by keep/kill/change.
3. **The tier gate caught the exact target failure.** `winner-draft-1.html` is clean, fully on-brand,
   and structurally conforming — the brand audit passes it and the conformance check passes it. It is
   also exactly the failure v1.1 exists to stop: a page declared Premium that ships clean-template.
   `validate-output.py --tier premium` failed it on **all four** elevate rules: no full-bleed hero,
   no legibility scrim, no display type system, no sticky action bar. Only the tier bar caught it.
4. **Rebuilt to earn the tier.** `winner.html` adds the full-bleed hero (in-lock SVG gradient imagery,
   cover + viewport height), the navy legibility scrim, the Fraunces-display/Quicksand-body pairing on
   headings, and a bottom-anchored sticky bar with the CTA. The Premium audit passes all four checks;
   the conformance check confirms section order, no banned masthead, and `[LAUNCH_DATE]` honestly
   visible.
5. **Verdict: `ship with changes`,** not `ship` — this environment cannot render the page, and elevate
   rules 3–5 (restraint, motif, scrim sufficiency) are judgment calls the script does not decide. The
   one bounded fix is owner-tagged in `pathToShip`. The eval suite proves both directions from this
   artifact: flipped to `ship` it validates (a genuinely Premium output may ship), and flipped to
   `ship` while carrying draft 1's audit it is rejected as meeting only the Standard bar.

## Verify it yourself

```bash
python3 scripts/validate-output.py examples/dogfood-premium/winner-draft-1.html --lock examples/dogfood-premium/lock.json --tier premium   # exit 1: all four elevate checks fail
python3 scripts/validate-conformance.py examples/dogfood-premium/winner-draft-1.html --structure examples/dogfood-premium/structure.json  # exit 0: structure alone can't catch a tier failure
python3 scripts/validate-output.py examples/dogfood-premium/winner.html --lock examples/dogfood-premium/lock.json --tier premium          # exit 0
python3 scripts/validate-conformance.py examples/dogfood-premium/winner.html --structure examples/dogfood-premium/structure.json          # exit 0
python3 scripts/validate-run.py examples/dogfood-premium/run.json --strict                                                                # exit 0
```
