# Founder Console Trust Gate

The Founder Console (`apps/web/app/...`) only mutates state through the
internal API. It never performs an external send. Every mutation:

1. Calls `/api/v1/internal/...` with `X-Dealix-Internal-Token` header.
2. Triggers `evaluate_action(...)` in `api/internal/policy_adapter.py`.
3. Appends to `trust/approval_decisions.csv` in the private ops tree.
4. Updates UI on the next render (no client-side cache).

If the policy adapter returns `allowed=false`, the endpoint returns
HTTP 400 with a list of `block_reasons`. The UI surfaces this verbatim.
