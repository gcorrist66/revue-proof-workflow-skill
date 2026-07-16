# revüe board review — worked example (implementation-review)

A short, fully-worked example so an agent can imitate the pattern. Fictional but realistic.

## Outcome

Reviewed PR #482 ("add /export endpoint") to decide if it is safe to merge.

## Mode

implementation-review · review board run

## Verdict

Verdict: ship with changes  (face: soft smile, aqua check)

Reason: The endpoint works and tests pass, but it runs an unbounded query with no pagination and
lacks an auth check on the new route — both are specific, bounded fixes.

## Evidence

- Verified (source): read `routes/export.py` and `tests/test_export.py` this session.
- Verified (action): ran `pytest tests/test_export.py` → `12 passed` (exit code 0), captured output.
- Verified (result): `GET /export` returns 200 with a CSV body on the happy path (curl, this session).
- Verified (result): the handler calls `Order.objects.all()` with no `limit`/pagination.
- Not verified (limitation): did not load-test; behavior at 100k+ rows is unmeasured.

## Scorecard

| Check | Status | Evidence |
| --- | --- | --- |
| Builds / runs | pass | pytest 12 passed, exit 0 |
| Tests cover the change | partial | happy path only; no auth or large-data test |
| Security | fail | new route has no auth decorator |
| Performance | fail | unbounded query, no pagination |

## Assumptions

- The export is intended for authenticated admins only. (If public-by-design, the auth finding changes.)

## Risks / Blockers

- No auth on `/export` — data exposure risk.
- Unbounded query — memory/timeout risk on large tenants.

## Decisions Needed

1. Is `/export` admin-only? 2. Acceptable max export size / pagination approach?

## Next Action

Add the auth decorator and paginate the query; add an auth test and a large-dataset test; re-run revüe.

Self-check: 4 observations cited; evidence captured this session (pytest output, curl); exact target
(the PR) inspected; ship blocked by two `fail` scorecard rows, so verdict is `ship with changes`, not `ship`.
