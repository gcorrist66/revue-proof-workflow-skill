# Vega / v3ga Patterns for revüe

Use this reference when improving revüe itself or shaping a revüe-style workflow platform.

## What Vega actually is

Vega (v3ga) is a fault-tolerant AI agent orchestration tool: a YAML DSL (`team.vega.yaml`) or a Go
library, with Erlang-style supervision. `vega serve team.vega.yaml` exposes a chat UI and a REST/SSE
API. In the UI, each tool call renders as a collapsible panel showing arguments, results, and
execution time. The streaming API emits typed events: `text_delta`, `tool_start`, `tool_end`
(with `duration_ms`), `error`, `done`.

Two ideas from Vega matter most for revüe: **declare the work in a spec**, and **make every step
observable with timing**.

## Borrow

- **Declarative run spec.** Model a review as a small YAML spec (`examples/sample-run.revue.yaml`)
  with mode, inputs, proof required, gates, and board — close enough to `team.vega.yaml` that
  `vega validate` / `vega run` could consume it. See `references/run-contract.md`.
- **Typed, timed trace.** Record each step (`intake`, `board`, `prove`, `verdict`) with a duration,
  mirroring Vega's `tool_end.duration_ms`. This is the `trace` field in `revue.review.v1`.
- **Observable tool calls.** Every claim in a review should be a panel: what was done, the result,
  and what it proves — never an unsupported summary.
- **Validate before run.** Vega has `validate` as a first-class command. revüe treats validation
  (`scripts/validate-run.py`, `scripts/validate-evidence.py`) as a gate, not an afterthought.

## Do not borrow by default

- Erlang-style supervision trees and process restarts.
- Long-running `serve` daemons and persistent agent runtimes.
- SSE streaming infrastructure and the Go library surface.
- Automatic tool/MCP downloads.

These are runtime concerns. revüe stays a proof-first skill that *produces and validates* specs;
Vega remains the optional executor if the user genuinely wants agents to run the work.

## Where the other sources fit

- **Panely** → the review board itself: named panelists, shared inputs, non-negotiables. See
  `references/review-board.md`.
- **HiveRunner** → the run contract: one schema-versioned payload/result and a dry-run gate. See
  `references/run-contract.md`.
- **Vega** → the declarative spec and the observable, timed trace (this file).

## revüe board roles

The board in `references/review-board.md` supersedes the earlier flat role table. Keep the mental
model: creative/critique, aggressive, conservative, proof, implementation, stakeholder, and a
final synthesis verdict — run in one pass, each lane cited.
