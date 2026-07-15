# Evidence Schema

Use this reference to decide whether a handoff has enough proof.

## Evidence Categories

- Source: file path, URL, screenshot, user-provided text, database query, or external record.
- Action: command run, edit made, review performed, browser interaction, or generated artifact.
- Result: output, screenshot, rendered page, test result, diff, validation report, or measured state.
- Limitation: what the evidence does not prove.

## Minimum Evidence By Work Type

- File artifact: absolute output path and validation result.
- Website/app: local or live URL, build/test result, and screenshot or browser check.
- Design mockup: requested source format, share/file path, preview dimensions, required states, and source-editability note.
- Product strategy: cited inputs, assumptions, risks, and decision record.
- Automation/workflow: trigger, permissions, dry-run or live-run proof, and rollback/stop condition.

## Exact Deliverable Rule

Do not mark a handoff `ship` when the evidence proves only a substitute for what the user requested. Examples:

- Requested Figma file, evidence shows only PNG/SVG: use `caution`.
- Requested live URL, evidence shows only local HTML: use `caution`.
- Requested sent email, evidence shows only draft: use `caution`.
- Requested production deploy, evidence shows only preview deploy: use `caution`.

Use `ship` only when the exact requested deliverable exists or the user explicitly accepted the substitute.

## Evidence Language

Use direct phrasing:

- "Verified by..."
- "Evidence:..."
- "Not verified:..."
- "Blocked because..."

Avoid unsupported phrases:

- "should work"
- "looks good" without inspection details
- "probably"
- "confirmed" without evidence
