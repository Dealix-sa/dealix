# Hermes API Surface

All endpoints under `/api/v1/hermes/*`. Composed in
`api/routers/hermes/composite.py` and mounted by `api/main.py`.

## Kernel

| Method | Path |
|---|---|
| POST | `/signals/capture` |
| POST | `/opportunities/score` |
| POST | `/decisions/create` |
| POST | `/executions/plan` |
| POST | `/outcomes/log` |
| POST | `/assets/build` |
| GET  | `/events` |

## Sovereign

| Method | Path |
|---|---|
| GET  | `/sovereign/console` |
| GET  | `/sovereign/approvals` |
| POST | `/sovereign/approvals/open` |
| POST | `/sovereign/approve?approval_id=&approver=` |
| POST | `/sovereign/deny?approval_id=&denier=&reason=` |
| POST | `/sovereign/kill-switch` |
| POST | `/sovereign/kill-switch/restore?target_type=&target_id=` |

## Trust

| Method | Path |
|---|---|
| GET  | `/trust/agents` |
| POST | `/trust/agents/register` |
| GET  | `/trust/tools` |
| POST | `/trust/tools/register` |
| POST | `/trust/check` |
| POST | `/trust/evidence-pack` |
| GET  | `/trust/audit?actor=&subject_id=` |
| GET  | `/trust/risks` |
| GET  | `/trust/incidents` |
| POST | `/trust/mcp-review` |

## Money

| Method | Path |
|---|---|
| GET  | `/money/dashboard` |
| POST | `/money/revenue-assurance` |

## Growth

| Method | Path |
|---|---|
| GET  | `/growth/campaigns` |
| POST | `/growth/campaigns` |
| GET  | `/growth/leads` |
| POST | `/growth/leads` |
| GET  | `/growth/experiments` |
| POST | `/growth/experiments` |
| GET  | `/growth/dashboard` |

## Products / Partners / Customers / Intelligence / Training / Ventures / Assets / Observability

Each domain exposes the relevant ops (offer readiness, partner fit
scoring, customer health & churn, market radar emit/list, workshop build,
vertical launch + evaluate, asset list + scale/kill + commercial review,
system health + lifecycle events).
