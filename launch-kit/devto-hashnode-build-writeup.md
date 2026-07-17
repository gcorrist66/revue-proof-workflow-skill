---
title: "How I Built an AI Review Skill That Refuses to Ship Bad Work"
published: false
description: "Inside revüe: an MIT AI review skill with brand-lock audits, verdict gates, 108 eval cases, and adversarial fixtures."
tags: ai, opensource, python, agents
canonical_url: ""
---

# How I Built an AI Review Skill That Refuses to Ship Bad Work

The fastest way to create AI slop is not to use a bad model. It is to accept a polished first draft as
proof that the work is finished.

That failure shows up everywhere: a landing page uses an almost-correct brand color, a campaign draft
invents a persuasive metric, or a “Premium” design is really a generic template with nicer spacing. An
AI reviewer then compounds the problem with a confident “looks good.”

I built [revüe](https://github.com/gcorrist66/revue-proof-workflow-skill) to put a reproducible gate
between the draft and the decision to ship.

revüe is an MIT-licensed Agent Skill for Claude Code, Codex, and Cowork. It combines a review workflow
with local validators, schemas, worked examples, and 108 automated eval cases. The central design
choice is simple:

> Let the model handle judgment. Make deterministic rules executable.

## The verdict is a contract

A revüe run ends with one of four verdicts:

- `ship`
- `ship with changes`
- `caution`
- `block`

The output is represented as a structured run artifact. In strict validation, `ship` is not accepted
when required proof is missing or an audit fails.

```bash
python3 scripts/validate-run.py path/to/run.json --strict
```

That changes the role of the final answer. The model cannot simply write a reassuring paragraph and
call the work ready. Its decision has to agree with the recorded evidence and audit state.

Every non-ship verdict also needs an owner-tagged path to ship. This prevents a different failure mode:
review systems that produce an impressive list of concerns but never close the work.

## Turn the brand system into a lock

For design and marketing production, revüe uses a design-system lock. The lock can define approved
colors, font families, claims, banned patterns, and structural rules.

A simplified example looks like this:

```json
{
  "colors": ["#062456", "#FF5747", "#25C7C3", "#FFFFFF"],
  "fonts": ["Avenir Next Rounded", "Arial"],
  "claims": ["Weekdays: 15% off"],
  "hardNos": ["lorem ipsum", "click here"]
}
```

The output validator inspects an HTML deliverable against the lock:

```bash
python3 scripts/validate-output.py \
  path/to/deliverable.html \
  path/to/lock.json
```

The important word is *inspects*. Asking a model to remember the approved palette is useful, but it is
not the same as checking the artifact it actually wrote.

## Why the audit needed adversaries

The first version caught obvious violations. The red-team fixtures taught it to catch less obvious
ones.

The current suite includes attacks such as:

- a near-miss color expressed through HSL or modern RGB syntax;
- an off-palette color behind a CSS variable;
- a color embedded in a base64 SVG data URI;
- banned copy split with entities, tags, or zero-width characters;
- an unapproved metric inside an otherwise compliant page;
- a forged audit object with `pass` flipped to `true` over listed failures;
- a hidden hero that tries to satisfy a Premium heuristic; and
- a placeholder hidden while a guessed value is shown instead.

Each discovered bypass becomes a permanent regression test.

```bash
python3 scripts/run-evals.py
```

At v1.2.0 the suite contains 108 cases. CI runs it on every push and pull request.

## Clean is not the same as Premium

One of the most useful failures was not a brand violation. It was a clean template declared as
Premium.

The page used approved colors and passed its structural checks. It still lacked the craft expected of
a flagship experience. That led to a tier model:

- **Standard:** clean, on-brand, and lock-audited.
- **Premium:** everything in Standard plus an additional editorial craft profile.
- **Custom:** a human-directed bar with explicit signoff.

Premium work is checked for machine-observable parts of that profile, including a full-bleed hero,
display/body typography contrast, a repeating signature motif, and a persistent action treatment.
These checks do not replace a designer. They prevent the system from equating compliance with craft.

The repository includes both sides of the test: a Premium-declared clean template that fails and a VIP
Lake Travis exemplar that clears the additional bar.

## Keep the trust boundary small

The validators use only Python's standard library. They need no network connection, API key, or
credential store. They read local artifacts and write local results.

That was deliberate. A review gate is easier to trust when its dependencies and data boundary are
small. It also makes the full suite easy to run in CI or inside the self-contained installer.

This does not mean the whole agent environment is incapable of network access. It means the bundled
deterministic validation layer does not require it.

## Package one workflow across agent runtimes

The root `SKILL.md` contains the portable workflow. Supporting material lives in `references/`,
schemas and templates live in `assets/`, and deterministic checks live in `scripts/`.

Claude Code users can install the repository as a plugin marketplace:

```text
/plugin marketplace add gcorrist66/revue-proof-workflow-skill
/plugin install revue-proof-workflow@revue-proof-workflow
```

Codex users can install the skill manually or with the self-contained installer documented in the
README. The same instruction layer also works in Cowork.

## What I would build next

The honest edge of the project is that no validator catches every future evasion. The useful roadmap
comes from concrete failures:

1. Collect bypass reports as minimal fixtures.
2. Add a failing eval before changing the validator.
3. Make the smallest deterministic fix.
4. Keep judgment-heavy checks visible as judgment, not fake certainty.
5. Publish adoption numbers only when a public counter supports them.

That last point matters because this project is also consulting proof for Corriston Consulting. The
repository should demonstrate the operating principle we sell: AI speed is valuable only when the
quality bar is explicit, testable, and honest about its limits.

## Try it and try to break it

The code, skill, examples, and eval suite are available under MIT:

https://github.com/gcorrist66/revue-proof-workflow-skill

If revüe helps, star the repository. If it lets bad work pass, open an issue with the smallest artifact
that reproduces the bypass. A new failure case is more valuable than a vague feature request.

And if your team needs this kind of proof-first workflow around its own brand system, approval rules,
and client handoffs, that is the consulting work Corriston Consulting is built to do.

