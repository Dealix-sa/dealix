# Ultimate Internal API

All endpoints listed below are mounted by
`api/routers/internal/founder_console.py` under `/api/v1/internal/`.
Every endpoint is gated by `X-Dealix-Internal-Token` in production.

## Read

```
GET /ceo/summary
GET /sales/funnel
GET /approvals
GET /workers/health
GET /trust/flags
GET /finance/summary
GET /distribution/summary
GET /delivery/queue
GET /retention/queue
GET /proof/library
GET /audit/events
GET /control/summary
GET /control/policies
GET /control/agents
GET /control/scorecard
GET /control/risks
GET /evals/status
GET /product/productization
GET /security/status
GET /sovereign/readiness
```

## Write

```
POST /approvals/{id}/approve
POST /approvals/{id}/reject
POST /approvals/{id}/request-edit
POST /approvals/{id}/escalate
POST /workers/{id}/retry
POST /control/agents/{id}/disable
POST /control/agents/{id}/enable
```

## Source markers

Every response includes a `source` field:

* `private_runtime` — read from CSV/JSON inside `DEALIX_PRIVATE_OPS`.
* `computed` — derived (e.g. control summary).
* `policy_yaml`, `registry_yaml`, `eval_yaml` — read from a YAML file.
* `fallback` — backing store missing or unreadable. UI shows a warning banner.
