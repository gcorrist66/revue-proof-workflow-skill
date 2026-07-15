# revŨe Proof Workflow Skill

revŨe is a proof-first workflow skill for turning messy work into clear handoffs with evidence, assumptions, risks, decisions, and a `ship` / `ship with changes` / `caution` / `block` verdict.

Use it when an agent needs to review work before it goes to a client, developer, stakeholder, or public audience.

## What it is good for

- Design and Figma handoffs
- Client-ready review packets
- Website or app implementation QA
- Product/workflow shaping
- Approval-gated actions such as send, publish, deploy, or share
- Funnel checks where visual polish is not enough and proof matters

## Example prompts

```text
Run this through revŨe before I send it to the client.
```

```text
Review this Figma handoff and tell me if it is ship, caution, or block.
```

```text
Take this product idea and turn it into a proof-first workflow with assumptions, risks, and next actions.
```

```text
Run it further down the funnel and tell me what breaks before a stakeholder sees it.
```

## Install in Claude / Claude Code

Copy this folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R revue-proof-workflow ~/.claude/skills/revue-proof-workflow
```

Restart Claude / Claude Code if the skill does not appear immediately.

## Install in Codex

Copy this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R revue-proof-workflow ~/.codex/skills/revue-proof-workflow
```

Restart Codex if needed.

## Package as a ZIP

The ZIP should contain the skill folder as its root:

```text
revue-proof-workflow.zip
└── revue-proof-workflow/
    ├── SKILL.md
    ├── references/
    ├── assets/
    └── scripts/
```

## Validation

The skill includes a validator for generated handoffs:

```bash
python scripts/validate-evidence.py path/to/handoff.md --mode design-handoff --strict
```

## Current status

This is an early public version. It is intended for hands-on testing with real workflows. Expect iteration around examples, evals, and stricter validation rules.

## License

No license has been selected yet. Until a license is added, all rights are reserved by default.
