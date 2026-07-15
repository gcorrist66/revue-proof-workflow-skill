# v3ga / Vega Patterns for revüe

Use this reference when improving revüe itself or shaping a revüe-style workflow platform.

## Borrow

- **Role clarity:** define who is acting: creative review, proof review, implementation review, stakeholder review, final verdict.
- **Blackboard claims:** before doing multi-step work, record what is in flight; at the end, record artifacts and evidence.
- **Evidence completion rule:** a task is not done until it includes verified paths, URLs, screenshots, command output, excerpts, or other concrete proof.
- **Observable run history:** each run should have a request, mode, artifacts, evidence, blocker list, verdict, and next action.
- **Workflow DSL thinking:** model repeatable work as named steps with inputs and outputs, even if the first version is Markdown rather than code.
- **Specialist review board:** borrow the useful mental model of lead designer, frontend/dev, UX writer, and orchestrator without requiring multiple live agents.
- **Cost/time awareness:** when available, record elapsed time, tool runs, or costs so longer workflows can be improved.

## Do not borrow by default

- Full Erlang-style supervision trees.
- Telegram integration.
- MCP auto-downloads.
- Long-running process orchestration.
- Retry/circuit-breaker architecture.

These are runtime concerns. Add them only if revüe becomes an actual agent runner rather than a proof-first skill/workflow layer.

## revüe board roles

For complex work, simulate these roles in one pass:

| Role | Question |
| --- | --- |
| Creative Review | Does it avoid generic output and fit the desired style? |
| Proof Review | What proves the work exists and works? |
| Implementation Review | Can someone build/use it from this handoff? |
| Stakeholder Review | Can the recipient decide without a live explanation? |
| Final Verdict | Ship, ship with changes, caution, or block? |

## Recommended run record

Use `assets/run-state-template.json` when the work spans multiple steps or might be resumed later.

