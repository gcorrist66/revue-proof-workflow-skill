# X thread — technical

**1/9**

I built an open AI review skill that audits its own design output against a brand lock—and refuses to
mark off-brand or unapproved claims as shipped.

It is called revüe. MIT. 108 eval cases. Thread on how the gate works 🧵

**2/9**

The core split: model judgment vs deterministic rules.

The model can critique hierarchy, synthesize evidence, and propose fixes.

Local validators check what should not depend on taste: colors, fonts, claims, hard noes, structure,
and audit consistency.

**3/9**

A run ends with one verdict:

ship / ship with changes / caution / block

But `ship` is not just prose. In strict mode it is invalid if required evidence is thin, the output
audit is missing, or a listed violation contradicts `pass: true`.

**4/9**

The brand lock can define approved colors, typography, claims, banned patterns, and required
structure.

The validator catches more than obvious hex codes: CSS variables, near-miss HSL/RGB values, encoded
SVG assets, and off-lock fonts are in the regression suite.

**5/9**

Fabrication is handled as a ship gate, not a request to “be careful.”

If a metric or claim is not approved by the lock, the artifact cannot pass the audit. Missing proof
stays visible; it does not get polished into certainty.

**6/9**

Premium is a separate gate.

A page can be clean, on-palette, and structurally valid—but still be a generic template. Premium work
must clear an additional craft profile. “Premium” is a bar, not a label.

**7/9**

The 108-case suite includes 12 red-team fixtures that actively try to cheat:

- obfuscated banned copy
- hidden heroes
- forged audit flags
- fabricated metrics
- structure evasions
- colors buried in encoded assets

CI runs it on every push.

**8/9**

The validators are Python stdlib only. No network. No credentials. Local files in, evidence + verdict
out.

That keeps the trust boundary small and makes failures reproducible.

**9/9**

Repo + install instructions:

https://github.com/gcorrist66/revue-proof-workflow-skill

I want bypass reports more than compliments. If you can make bad work pass, open an issue with the
smallest fixture that proves it.

