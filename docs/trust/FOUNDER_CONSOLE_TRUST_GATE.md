# Founder Console — Trust Gate

The Founder Console (`apps/web/app/*`) is the only place where humans
approve external-impact actions. Every page that exposes a decision is
backed by the internal API and the audit log.

## Flow

1. The founder opens `/approvals`.
2. The page calls `/api/v1/internal/approvals` (read-only).
3. The founder chooses Approve / Reject / Needs Edit / Escalate.
4. The action client posts to the corresponding `/api/v1/internal/approvals/{id}/*`.
5. The internal router runs `policy_adapter.evaluate(...)`.
6. The decision and the matched rule are appended to
   `${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv`.
7. `external_action_allowed` is set to `true` only when:
   - decision == "approved"
   - approval class != "A3"
   - policy decision allows external action

## A3 protection

The A3 class is hard-coded: even an "approved" decision will not set
`external_action_allowed: true`. A3 actions remain founder-only and
manual.

## Auth

The internal API requires `X-Dealix-Internal-Token` in production. In
local dev with the env var unset, requests are allowed and the trust gate
labels the system as `auth_mode: open_dev` — never claim production
readiness in this mode.
