# revüe launch + distribution kit

Consulting-credibility launch assets for revüe. Every public claim in this kit is grounded in the
repository as of v1.2.0: MIT source, 108 eval cases, CI, 12 red-team fixtures, stdlib-only validators,
brand-lock checks, tier gates, and `ship` / `ship with changes` / `caution` / `block` verdicts.

## Copy

- `github-polish.md` — description, topics, social-preview instructions, and README star line.
- `product-hunt.md` — tagline, launch copy, maker comment, and gallery captions.
- `show-hn.md` — title and technical launch body.
- `linkedin-short-post.md` — short consulting-led post.
- `linkedin-article.md` — long-form consulting article.
- `x-technical-thread.md` — audit/verdict mechanics.
- `x-business-thread.md` — agency-quality economics without invented savings claims.
- `devto-hashnode-build-writeup.md` — technical build story with frontmatter.
- `awesome-list-one-liners.md` — PR-ready entries and honest PR context.
- `launch-checklist.md` — one-page sequence and measurement plan.
- `adoption-monitoring.md` — metric definitions, baseline, commands, and weekly scorecard.

## Visuals

- `images/github-social-preview.png` — 1280×640 GitHub social preview.
- `images/product-hunt-01-logo.png` — Product Hunt cover.
- `images/product-hunt-02-evals.png` — eval and red-team proof.
- `images/product-hunt-03-verdicts.png` — verdict system.
- `images/product-hunt-04-vip-before-after.png` — rejected Standard-bar template vs Premium exemplar.

The PNGs are generated from the SVG files in `source/` using `render-assets.mjs`. The social-preview
background was generated once with the image-generation tool, then the exact repository logo and copy
were composited deterministically. Product screenshots come from repository HTML fixtures, not mockups.
