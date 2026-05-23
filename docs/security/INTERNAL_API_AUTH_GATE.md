# Internal API Auth Gate

Every internal Dealix API requires the `DEALIX_INTERNAL_TOKEN` header. The token gates all internal control surfaces — the Founder Console, the runtime orchestrator admin endpoints, the agent registry CRUD, the policy reload endpoint.

**Source of truth:** middleware in `api/middleware/internal_auth.py` (or equivalent) + this doc
**Owner:** Engineering Lead
**Trust gate:** A2 — token rotation and middleware changes require founder approval.

## How it works

1. Every internal endpoint registers under a route prefix protected by the auth middleware.
2. The middleware reads the `DEALIX_INTERNAL_TOKEN` header.
3. The token is compared against the active key in the secrets store using constant-time comparison.
4. The token's identity (which named human or service issued it) is resolved.
5. A token tied to a deactivated identity is rejected.
6. The request is logged with `identity_id`, `endpoint`, `outcome`.

A missing, malformed, or rejected token returns 401 without revealing why.

## Token issuance

- Tokens are scoped to identity and lifetime.
- A human token's max lifetime is 90 days.
- A service-account token's max lifetime is 30 days, rotated by the secrets store automation.
- Founder may issue an emergency short-lived token (max 24 hours) for incident response.

## Token scopes (illustrative)

| Scope | Endpoints |
|-------|-----------|
| `founder` | All internal endpoints |
| `engineering_lead` | All except policy_change and key_rotation |
| `agent_dispatch` | Orchestrator dispatch only |
| `read_audit` | Audit-log read only |
| `read_kpi` | KPI tree read only |

Scope is enforced at the endpoint level. A scope expansion is an A2 change.

## What it does not do

- It does not authenticate end customers — those use customer-facing auth.
- It does not authorise business decisions — those use the Founder Console and approval class.
- It does not log message bodies — only metadata, to limit PII risk.

## OWASP / NIST posture

- **A01:2021 Broken access control.** Centralised middleware closes the most common bypass.
- **LLM06 Sensitive information disclosure.** Token is hashed in logs; never printed.
- **LLM10 Model theft.** Inference endpoints are internal-only; the token gates them.

## Failure modes

- **Token leak:** a token appears in a log, repo, or screenshot. Detection: log scan + repo scan. Recovery: immediate rotation; audit replay; root cause.
- **Bypass:** an endpoint omits the middleware. Detection: route audit. Recovery: middleware added; access reviewed.
- **Stale token:** an active token tied to a deactivated identity is accepted. Detection: nightly job. Recovery: revoke; review middleware.

## Recovery path

If token integrity is in doubt, the founder triggers an emergency rotation of every active token. Internal operation pauses for the rotation window (target: under 30 minutes).

## Metrics

- Active token count by scope.
- Token age distribution.
- 401 rate (sustained spikes indicate attack or misconfiguration).
- Bypass incidents (target: 0).

## Disclaimer

Auth reduces unauthorised access risk; it does not eliminate it. Estimated value is not Verified value.
