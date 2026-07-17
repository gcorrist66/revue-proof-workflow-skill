# Product Hunt draft

## Name

revüe — Proof Workflow

## Tagline

On-brand AI work that has to prove it is ready to ship

## Short description

revüe is an open AI review skill for teams that need more than a confident draft. It inspects the
real artifact, separates proof from assumptions, audits design and marketing output against a brand
lock, rejects unapproved claims, and returns one verdict: `ship`, `ship with changes`, `caution`, or
`block`.

The workflow includes Standard, Premium, and Custom craft bars, 108 automated eval cases, 12
adversarial red-team fixtures, and CI on every push. Its validators are Python standard-library only,
require no network or credentials, and operate on local files. revüe is MIT-licensed and works in
Claude Code, Codex, and Cowork.

Built by Corriston Consulting to answer a practical question: how do you get the speed of generative
AI without quietly lowering the bar for client-ready work?

## First / maker comment

I built revüe after seeing the same failure pattern in AI-assisted creative work: the first draft
looks finished before it is proven.

A polished page can still be off-brand. A persuasive metric can still be invented. A “Premium”
layout can still be a generic template with nicer spacing. And an AI reviewer can still say “looks
good” without inspecting the source.

revüe turns those failure modes into gates:

- Evidence must name its source and freshness.
- Brand colors, fonts, claims, hard noes, and structure can be locked and audited.
- Premium work has to clear an additional craft bar; clean-template output does not qualify.
- A `ship` verdict is invalid when an audit fails.
- Every non-ship verdict has an owner-tagged path to ship.

The repo includes 108 eval cases and active red-team fixtures that try to evade the gates with hidden
colors, obfuscated banned copy, fabricated metrics, and hand-flipped audit results.

It is open under MIT. I would especially value feedback on two things: where the gates feel too strict,
and which real-world failure mode deserves the next regression test.

## Gallery

1. `images/product-hunt-01-logo.png`
   - Caption: **Proof over vibes.** An open review workflow for client-ready AI work.
2. `images/product-hunt-02-evals.png`
   - Caption: **108 eval cases.** Golden paths, regression guards, and adversarial fixtures run in CI.
3. `images/product-hunt-03-verdicts.png`
   - Caption: **One verdict, a short path forward.** Ship, ship with changes, caution, or block.
4. `images/product-hunt-04-vip-before-after.png`
   - Caption: **Premium has to be earned.** The clean template is rejected; the rebuilt VIP exemplar clears the additional craft gate.

## Launch-day replies to prepare

**Does it prevent hallucinations?**

> It does not claim to prevent every model hallucination. It prevents unapproved claims from receiving a `ship` verdict when the brand/claim lock and audit are in use, and it forces missing proof to stay visible.

**Is this an agent or a prompt?**

> It is a portable Agent Skill with references, schemas, local validators, examples, and an eval suite. The instruction layer guides the review; deterministic scripts enforce the gates that should not depend on model judgment.

**Who is it for?**

> Consultants, agencies, internal creative teams, and developers who use AI to produce stakeholder-facing work and need a repeatable readiness decision before it leaves the building.

