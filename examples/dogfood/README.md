# Dogfood: revüe's v1.0 pipeline run on revüe's own brand

This directory is a complete, real end-to-end run of the v1.0 creative-production pipeline, using the
repo's own brand (`docs/brand.md`, `assets/logo-revue.svg`) as the high-specificity design source. It
exists to prove the gates fire in sequence on real work, not just in eval fixtures.

## The run, in order

1. **Brief gate blocked first.** `run-incomplete-brief.json` is the run as it stood before the brief
   was complete. `scripts/validate-run.py --strict` rejects it with **one batched line** naming every
   missing field (sources, handoffPageRead, designSystemLock, hardNos) — not a drip of questions.
2. **Brief completed, lock written.** `revue-lock.json` copies the six hex values verbatim from
   `docs/brand.md` and adds three Hard NOs — including `revue proof`, which forbids flattening the
   ü in display copy.
3. **Three distinct concepts** were presented (verdict-states hero / gate-pipeline hero /
   before-after split), each with its own `distinctionAxis`, all lock-compliant. Feedback was
   keep/kill/change: keep A's spine, fold B's gate strip in, kill C as a generic trope.
4. **The audit caught real drift.** `winner-draft-1.html` is the first build of the winner. Its CTA
   hover was "just darkened coral" — `#e64435`, a guessed shade. The output audit rejected it and
   labeled it a near-miss of `#e5484d`. This is precisely the failure class v1.0 exists to stop:
   a color the source never specified, invented mid-build.
5. **Fixed and audited clean.** `winner.html` replaces the guessed hover with lock navy. The audit
   passes: 6 colors found, all in lock; fonts in lock; no Hard-NO hits; no unverified claims. The
   audit object is attached verbatim to `run.json` as `outputAudit`.
6. **Verdict: `ship with changes`,** not `ship` — this environment cannot render the page in a real
   browser, so preview fidelity is `partial` and the one bounded fix (human opens it and confirms both
   breakpoints) is owner-tagged in `pathToShip`. Claiming `ship` without that proof would be exactly
   the overclaim revüe blocks.

## Verify it yourself

```bash
python3 scripts/validate-run.py examples/dogfood/run-incomplete-brief.json --strict   # exit 1, batched
python3 scripts/validate-output.py examples/dogfood/winner-draft-1.html --lock examples/dogfood/revue-lock.json  # exit 1, near-miss
python3 scripts/validate-output.py examples/dogfood/winner.html --lock examples/dogfood/revue-lock.json          # exit 0
python3 scripts/validate-run.py examples/dogfood/run.json --strict                    # exit 0
```
