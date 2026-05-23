# Ultimate Internal API

Router file: `api/routers/internal/founder_console.py`.
Helpers: `api/internal/runtime_reader.py`,
`api/internal/policy_adapter.py`, `api/internal/agent_registry_reader.py`,
`api/internal/auth.py`.

## Endpoint catalogue

```
GET  /api/v1/internal/ceo/summary
GET  /api/v1/internal/sales/funnel
GET  /api/v1/internal/approvals
POST /api/v1/internal/approvals/{id}/approve
POST /api/v1/internal/approvals/{id}/reject
POST /api/v1/internal/approvals/{id}/request-edit
POST /api/v1/internal/approvals/{id}/escalate
GET  /api/v1/internal/workers/health
GET  /api/v1/internal/trust/flags
GET  /api/v1/internal/finance/summary
GET  /api/v1/internal/distribution/summary
GET  /api/v1/internal/delivery/queue
GET  /api/v1/internal/retention/queue
GET  /api/v1/internal/proof/library
GET  /api/v1/internal/audit/events
GET  /api/v1/internal/control/summary
GET  /api/v1/internal/control/policies
GET  /api/v1/internal/control/agents
POST /api/v1/internal/control/agents/{id}/disable
POST /api/v1/internal/control/agents/{id}/enable
GET  /api/v1/internal/control/scorecard
GET  /api/v1/internal/control/risks
GET  /api/v1/internal/evals/status
GET  /api/v1/internal/product/productization
GET  /api/v1/internal/security/status
```

## Auth

Production must set `DEALIX_INTERNAL_TOKEN` and present the header
`X-Dealix-Internal-Token`. Local dev with the env var unset is allowed
but the auth gate logs a warning and the system refuses to call itself
production-ready (see `docs/security/INTERNAL_API_AUTH_GATE.md`).
