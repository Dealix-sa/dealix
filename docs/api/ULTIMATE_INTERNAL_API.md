# Ultimate Internal API

Mounted under `/api/v1/internal`. Defined in
`api/routers/internal/founder_console.py`. Token-gated via
`api/internal/auth.py`.

## Read endpoints

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
```

## Write endpoints

```
POST /approvals/{id}/approve
POST /approvals/{id}/reject
POST /approvals/{id}/request-edit
POST /approvals/{id}/escalate
POST /workers/{id}/retry
POST /control/agents/{id}/disable
POST /control/agents/{id}/enable
```

Every write appends to the private ops audit/state CSV; none of them
send anything externally.
