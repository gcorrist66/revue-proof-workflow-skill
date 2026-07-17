# Inspection Checklists (how to gather the evidence)

The rest of revüe tells you what a good review contains. This tells you how to actually gather the
proof, step by step, so the review is grounded and not guessed. Run the checklist for the active mode
before writing the verdict. Aim for the evidence floor in `references/self-check.md` (three concrete
observations minimum).

User-reported behavior is a source input, not a directly observed result. Label it `reported by user`
until reproduced. When no inspectable artifact exists, list the exact test that would verify it and do
not imply a validator or browser check ran.

## design-handoff

1. List **every frame/artboard and its exact name**. Unnamed frames are a developer-clarity finding.
2. Identify which **states exist** (desktop / tablet / mobile / hover / modal) and name the ones that
   are missing. "No mobile frame" is a proof, not an assumption.
3. For each key section (hero, offer, pricing, proof, CTA), **quote the actual text** you can see.
4. Confirm the **exact requested format** (native Figma vs. PNG/SVG export) and note editability from
   the layers/inspect panel — not from a preview image.
5. Record **prices, counts, and names** verbatim; cross-check them across frames for inconsistencies.
6. Note the **share/permission state**: can the named stakeholder actually open it?

## implementation-review

1. Actually **run or build** it. Capture the command, exit code, and output.
2. Run the tests; cite pass/fail counts. Name what you did **not** run and why.
3. List the **files changed** and the risky ones (auth, migrations, external calls).
4. Note console/log errors verbatim. "No errors observed" requires having looked.
5. For product interfaces, test **context, status, meaning, target, action, and empty state**:
   - the active client/company/account is unmistakable on the page;
   - slow actions acknowledge the click immediately and show progress, completion, and failure;
   - scores and labels use plain language and explain what they mean;
   - the user knows the target to aim for;
   - findings say what to fix first and how to improve;
   - an empty report explains why it is empty and what to do next.
6. Exercise account, tenant, or workspace switching when present. Confirm the selected context changes
   visibly before and after loading, and that actions cannot accidentally run against the prior context.
7. Measure slow interactions when possible. Record the observed duration and the product's stated goal
   or baseline; do not invent a universal performance threshold. Regardless of duration, any noticeable
   wait needs immediate in-page feedback.

## product-shaping

1. Cite the **source inputs** (user quotes, data, prior artifacts) — not general knowledge.
2. Separate **facts from assumptions** explicitly; mark each assumption's confidence.
3. State the **ship threshold**: what must be true for `ship` instead of `caution`.

## client-delivery

1. Apply the **stakeholder test**: can the named recipient open it and decide without a walkthrough?
2. Check for **missing links, attachments, or access** the recipient would need.
3. Flag any **unsupported claim** the recipient might take as fact.

## platform-build

1. Read the relevant reference (`review-board.md`, `run-contract.md`, `vega-patterns.md`) first.
2. Borrow **patterns, not runtimes**; record which source each borrowed idea came from.

## If you cannot inspect

If a required inspection is blocked (no access, can't open the file, can't run the build), do not
invent the result. Record it as a limitation, cap the verdict at `caution` or `block`, and state the
exact access or step that would unblock it.
