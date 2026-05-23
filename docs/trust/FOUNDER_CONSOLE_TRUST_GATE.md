# Founder Console Trust Gate

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Founder Console is the only sanctioned origin for mutations in
Dealix. This document explains how it enforces the trust plane,
which endpoints exist, what they evaluate, and how an unauthorized
request is rejected.

## Surface and identity

The console exposes the prefix `/api/v1/internal/*` via
`api/routers/founder_console_internal.py`. Every endpoint requires
the `x-dealix-internal-token` header. The header is validated by
`api/internal/auth.py`:

| Mode               | Trigger                                  | Behavior                                                          |
| ------------------ | ---------------------------------------- | ----------------------------------------------------------------- |
| `enforced`         | `DEALIX_INTERNAL_TOKEN` is set            | Header must match exactly; missing or mismatched returns HTTP 401. |
| `dev_unprotected`  | `DEALIX_INTERNAL_TOKEN` is unset          | Console renders but every response carries `auth_mode` flag.       |

The `dev_unprotected` mode is intentional. It allows the console UI to
boot in local development without surfacing a fake security claim.
Production deployments must set the token. The
`INTERNAL_API_AUTH_GATE.md` document under `docs/security/` is the
operational guide for rotating the token.

## How the gate evaluates a request

Each state-changing endpoint follows the same pattern:

1. The endpoint depends on `require_internal_token`. If the header is
   missing or wrong, FastAPI returns HTTP 401 before any business
   logic runs.
2. The endpoint calls `evaluate_action()` from the policy adapter
   when its action is policy-guarded. The current set is:
   - `POST /approvals/{id}/approve` → `evaluate_action("approval_approve", ...)`
   - other endpoints route through worker logic that consults the
     adapter as needed.
3. If the policy decision returns `allowed=False`, the endpoint raises
   HTTP 409 with the rule id and reason as detail.
4. If the call proceeds, the endpoint calls `_audit_event(...)`,
   which writes a row to `trust/approval_decisions.csv` and returns
   the audit id.
5. The response envelope includes `auth_mode`, `fetched_at`, and the
   `audit_id` for any mutation.

The envelope is built by `_envelope()` in the router. Every response
carries this same shape so the UI can render uniform diagnostics.

## Endpoint families

The console groups endpoints into nine families. The table below
summarizes the families and the trust posture of each.

| Family             | Read endpoints                                   | Write endpoints                                                                       | Trust posture                                                                    |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| CEO summary        | `/ceo/summary`                                   | none                                                                                  | Read-only; no policy gate.                                                       |
| Sales funnel       | `/sales/funnel`                                  | none                                                                                  | Read-only.                                                                       |
| Approvals          | `/approvals`                                     | `/approvals/{id}/approve`, `/reject`, `/request-edit`, `/escalate`                    | Approve is policy-gated; all four record audit rows.                             |
| Workers            | `/workers/health`                                | `/workers/{id}/retry`                                                                 | Retry records `worker_retry` audit at `risk: low`.                               |
| Trust              | `/trust/flags`, `/audit/events`                  | none                                                                                  | Read-only.                                                                       |
| Finance            | `/finance/summary`, `/finance-ops/summary`       | none                                                                                  | Read-only.                                                                       |
| Distribution       | `/distribution/summary`                          | none                                                                                  | Read-only.                                                                       |
| Control            | `/control/summary`, `/policies`, `/agents`, `/scorecard`                  | `/control/agents/{id}/disable`, `/enable`, `/scorecard/refresh`, `/risks/{id}/accept` | Disable is `risk: high`; enable is `risk: medium`; risk accept is `risk: high`.  |
| Proof, marketing, product, customer success, sovereign, security, brand, growth, data, evals, experiments | several read endpoints  | a small number of draft endpoints (campaign, experiment) at `risk: low`               | All writes audited; no external send.                                            |

## Where the policy adapter is invoked

The router currently calls the adapter explicitly on
`approve`. Other endpoints rely on the policy adapter being invoked
by the downstream worker before any external action is taken. The
`evaluate_action()` call is cheap (cached YAML load); calling it more
often is preferable to calling it less.

The action keys that map onto policy rules are listed in
`POLICY_AS_CODE_V1.md`. New endpoints must declare their action key in
both the router and the policy file. A new action without a policy
rule is a silent gap; the verifier
`scripts/verify_policy_as_code.py` catches this.

## How an unauthorized request looks

A request without the header:

```
HTTP/1.1 401 Unauthorized
{"detail": "invalid_or_missing_internal_token"}
```

A request the policy refuses:

```
HTTP/1.1 409 Conflict
{
  "detail": {
    "rule": "no_a3_auto",
    "reason": "A3_disabled_in_dealix"
  }
}
```

A request that passes both gates:

```
HTTP/1.1 200 OK
{
  "data": {"ok": true, "approval_id": "apr_123"},
  "auth_mode": "enforced",
  "fetched_at": "2026-05-23T08:00:00+00:00",
  "audit_id": "...",
  "message": "approval_recorded"
}
```

## The audit ledger

Every write endpoint calls `_audit_event(actor, action, target,
payload, risk)`. The function appends a row to
`trust/approval_decisions.csv` in the private ops runtime. The
columns are documented in `AUDIT_EVENT_MODEL.md`. The function
returns the event dictionary so the response can include the
`audit_id`.

Notable points:

- The ledger is append-only by convention. The router never
  edits or deletes a row.
- The ledger lives outside the repo. The repo only describes the
  schema and the writer.
- If the runtime directory is unset (no `PRIVATE_OPS`), the function
  still returns the event dict so the response is consistent; the
  audit is simply not persisted. Production must always have the
  runtime mounted.

## Failure modes the gate intentionally surfaces

| Failure                          | What the gate does                                                            |
| -------------------------------- | ----------------------------------------------------------------------------- |
| Missing token in production      | Returns 401 with a stable detail string. No silent passthrough.               |
| Policy denial                    | Returns 409 with the rule and the reason; UI surfaces both verbatim.          |
| Worker write to a banned path    | The worker orchestrator rejects the write at scheduling time.                 |
| Runtime directory missing        | Read endpoints return `data_source: "no-runtime"`; writes still audit-emit.   |
| Approval over a suppressed target| Drafted by Distribution Operator, refused at the policy layer before queueing. |

## What the console will not do

The console will never:

- Send an email, post to LinkedIn, fill a contact form, publish a
  proof asset, sign a contract, capture a payment, or commit a price
  externally without an audit row carrying a founder approval and a
  policy-allowed evaluation.
- Read or write outside the private ops runtime tree.
- Expose tokens, secrets, or internal identifiers in any response.

These are not aspirational claims. They are encoded in policy, in
agent registry, in eval gate, and in the router code itself. The
trust gate is the runtime expression of all four.
