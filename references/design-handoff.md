# Design Handoff Mode

Use this reference for Figma, Canva, landing-page mockups, brand design, client-facing visual packages, and any task where the reviewer expects an editable design artifact.

## Required Intake

- Stakeholder: who will review or use the file.
- Requested format: Figma link, `.fig`, Canva design, SVG, PNG, PDF, HTML, or another format.
- Editability expectation: native layers, editable text, reusable components, or visual-only.
- Required states: desktop, mobile, tablet, hover, sticky elements, modals, forms, or other variants.
- Brand constraints: colors, typography, logo, imagery, tone, and "keep/change" direction.
- Implementation audience: developer, client, designer, marina owner, or internal team.

## Shippability Checklist

A design handoff can be `ship` only when evidence proves:

- Exact requested format exists.
- File can be opened by the intended stakeholder.
- Text and major layout elements are editable if editability was requested.
- Desktop/mobile or required states are present.
- Preview image or screenshot matches the intended design.
- Share link, source file path, or package path is provided.
- Any substitute format is explicitly approved or labeled as interim.

If the requested format is Figma and only SVG/PNG/package files exist, use `caution` unless the user explicitly accepts an import package as the final handoff.

## Scorecard

Include this scorecard for design handoffs. Use `pass`, `partial`, `fail`, or `not applicable`.

| Check | Status | Evidence |
| --- | --- | --- |
| Exact requested format |  |  |
| Source editability |  |  |
| Desktop/mobile states |  |  |
| Preview fidelity |  |  |
| Brand fit |  |  |
| Stakeholder access |  |  |
| Developer clarity |  |  |

Scoring rule:

- `ship`: all required checks are `pass`.
- `ship with changes`: only minor non-blocking checks are `partial`.
- `caution`: any required check is `partial` or unverified, but a usable interim exists.
- `block`: a required check is `fail` and no usable interim exists.

For Figma requests, `Exact requested format` is `pass` only with a native Figma file, `.fig`, or accessible Figma share link. An SVG import package is `partial`.

## Stakeholder Test

Ask:

- Can the recipient open it?
- Can the recipient understand the design without a live walkthrough?
- Can a developer tell what to build?
- Can a designer edit the source?
- Is the missing proof obvious in the handoff?

If the answer to any required question is no, call out the gap under Risks / Blockers.

## Stakeholder Summary

When a named person or non-technical reviewer is involved, add a short stakeholder summary:

- What is ready.
- What they can review.
- What is not final yet.
- What decision or action is needed from them.

Keep it plain. Do not include internal validation language unless it helps them make a decision.

## Design Evidence

Good evidence includes:

- Native design URL or source file path.
- Preview PNG/PDF dimensions.
- Screenshot of imported/opened source.
- File inspection output.
- List of frames/artboards/states.
- Notes on what is editable versus flattened.

Avoid claiming "editable" from a visual preview alone. Prove editability from source structure, imported file behavior, or tool inspection.
