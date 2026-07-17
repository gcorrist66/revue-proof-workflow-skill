# Show HN draft

## Title

Show HN: revüe – an open AI review skill that audits its own output

## Body

I built an open AI review skill that audits its own design output against a brand lock and refuses to
mark off-brand or fabricated work as shipped.

Repo: https://github.com/gcorrist66/revue-proof-workflow-skill

The technical hook is that the parts that should be deterministic are not left to model judgment.
revüe can take a lock containing approved colors, fonts, claims, hard noes, and structure, then run
local Python validators against the produced artifact. A `ship` verdict is rejected if the audit is
missing, inconsistent, or failing.

It also separates a clean brand pass from a Premium craft pass. A generic clean template can be
on-palette and structurally valid, but it still fails Premium if it lacks the additional editorial
craft layer. That distinction came from a real failure mode: “on-brand” was being confused with
“high-end.”

The repo currently has 108 eval cases. Twelve red-team HTML fixtures actively try to evade the gates:
CSS variables, near-miss colors, base64 data URIs, obfuscated banned copy, unapproved metrics, hidden
heroes, forged audit results, and reformatted structure violations. CI runs the suite on every push.

The validators are stdlib-only Python, need no network or credentials, and operate on local files.
The skill itself is MIT-licensed and works in Claude Code, Codex, and Cowork.

Claude Code install:

```text
/plugin marketplace add gcorrist66/revue-proof-workflow-skill
/plugin install revue-proof-workflow@revue-proof-workflow
```

I run Corriston Consulting, so there is a commercial motive in the open: I want the repository to
show that our AI consulting is built around repeatable proof, not prompt theater. I am not claiming
user or adoption numbers yet. The current proof is the source, fixtures, and reproducible eval suite.

I would appreciate technical criticism, especially on bypasses the audit does not yet catch and on
where the line between deterministic validation and model judgment should sit.

