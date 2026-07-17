# The AI work was fast. Proving it was ready took a system.

**How Corriston Consulting turned a review discipline into an open, audited AI skill for premium client work**

Generative AI made the first draft dramatically cheaper.

It did not make the final decision safer.

That gap is where many AI projects lose credibility. A landing page appears polished, a deck reads
confidently, or a campaign concept feels complete. The team sees speed. The client eventually sees
the problems: a color that is almost right, a font that does not belong, an unsupported claim, a
generic template wearing premium language, or a recommendation that cannot show its evidence.

In an AI-slop era, producing more is not the differentiator. Proving that the work deserves to leave
the building is.

That is why we built revüe.

## A review board, not a confidence machine

revüe is an open, MIT-licensed Agent Skill for Claude Code, Codex, and Cowork. It treats review as a
small operating system rather than a final prompt asking, “Does this look good?”

The workflow starts with the intended outcome and the real artifact. It separates observed facts
from assumptions, requires source-aware evidence, checks approval boundaries, and synthesizes one
verdict:

- `ship`
- `ship with changes`
- `caution`
- `block`

The verdict is not the end of the review. Every non-ship result carries an owner-tagged path to ship.
The goal is convergence, not an endless loop of commentary.

That sounds procedural because it is. Client-ready work benefits from a procedure that survives the
enthusiasm of a good-looking draft.

## On-brand is a testable claim

“On-brand” is often used as an aesthetic opinion. We wanted to make part of it testable.

revüe can work from a design-system lock: approved colors, typography, claims, hard noes, and required
structure. Local validators inspect the generated artifact against that lock. If the audit fails, is
missing, or contradicts its own findings, the run cannot honestly receive a `ship` verdict.

This does not mean software can replace design judgment. It means software can reliably catch the
things that should never depend on taste:

- an off-palette color hidden behind a CSS variable;
- an off-lock font;
- banned or placeholder copy;
- an unapproved metric;
- a required section that is missing or out of order; or
- an audit result that has been hand-flipped from fail to pass.

The model still does the work that requires judgment. The validator handles the rules that should be
deterministic.

## Premium cannot be a label

One of the more useful failures came from work that was technically clean.

The page used the approved palette. The structure was valid. The copy was acceptable. It also looked
like a clean template. Calling it “Premium” did not make it premium.

That led to a second, additional craft gate. revüe distinguishes Standard, Premium, and Custom work.
A Premium declaration must earn its bar through an editorial display system, stronger visual
hierarchy, a signature motif, appropriate responsive states, and other explicit craft requirements.

The repository includes a VIP Lake Travis example that shows both sides. A clean-template version is
rejected as Standard-bar-only. The rebuilt flagship version clears the brand, conformance, and
Premium gates.

This matters beyond one marina page. When a consultancy produces related landing pages or campaign
assets at scale, a tier system makes quality repeatable. It gives the team a shared definition of
“good enough for this job” without pretending every engagement needs the same level of craft.

## Trust comes from the failure cases

The interesting number in the repository is not a vanity adoption metric. We do not have one to
claim yet.

The current proof is 108 automated eval cases.

They cover golden workflows, regression guards, rejection cases, and adversarial fixtures. Twelve
red-team HTML files actively try to evade the rules with techniques such as near-miss colors, encoded
assets, obfuscated hard noes, fabricated metrics, hidden page elements, and forged audit results.

CI runs the suite on every push. The validators use Python's standard library, operate on local files,
and need no network or credential access.

That is not a guarantee that no future bypass exists. It is a visible, reproducible commitment to turn
each discovered failure into a permanent test.

## Why make a consulting tool open?

Because “we use AI” is not consulting credibility.

Clients cannot inspect a claim about expertise. They can inspect a repository. They can run the tests,
read the failure cases, challenge the rules, and see how the system handles uncertainty.

For Corriston Consulting, adoption is useful proof only when it is real. We will publish stars,
installs, contributors, or downstream use as those metrics accrue, with dates and sources. Until then,
the honest claim is narrower: we built a skill people can use, inspect, and test today, and we use its
discipline to make AI-assisted client work more defensible.

Open source also improves the consulting work. External scrutiny exposes brittle assumptions.
Different teams bring different brand locks and failure modes. The public artifact creates a sharper
conversation than another AI capabilities deck.

## The result: speed with a visible standard

The result is not “AI replaces the agency.”

It is a better production system:

- AI accelerates exploration and assembly.
- A brand lock protects non-negotiables.
- A tier defines the craft bar.
- An evidence floor keeps missing proof visible.
- Automated gates reject known failure modes.
- A single verdict gives the team a decision.
- An owner-tagged path closes the remaining gap.

That combination lets a consulting team pursue faster, cheaper production without making an
unmeasured promise about savings or sacrificing the thing the client actually buys: confidence in the
result.

## Try the workflow—or build the operating system around it

revüe is available under MIT at:

https://github.com/gcorrist66/revue-proof-workflow-skill

If it is useful, star the repository. If it misses a failure mode, open an issue with the smallest
reproducible example.

And if your organization is already generating plenty of AI output but still relies on heroic manual
review to make it client-ready, Corriston Consulting can help design the locks, gates, tier system, and
handoffs around your actual workflow.

The deliverable is not another prompt library. It is a credible path from draft to ship.

