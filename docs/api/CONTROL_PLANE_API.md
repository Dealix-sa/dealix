# Control Plane API

All endpoints under `/api/v1/internal/control/...` require the
`X-Dealix-Internal-Token` header in production. See
`docs/security/INTERNAL_API_AUTH_GATE.md`.

## Read endpoints

| Method | Path |
|---|---|
| GET | `/api/v1/internal/control/summary` |
| GET | `/api/v1/internal/control/policies` |
| GET | `/api/v1/internal/control/agents` |
| GET | `/api/v1/internal/control/scorecard` |
| GET | `/api/v1/internal/control/risks` |

## Write endpoints

| Method | Path | Effect |
|---|---|---|
| POST | `/api/v1/internal/control/agents/{id}/disable` | record incident + return `disabled` |
| POST | `/api/v1/internal/control/agents/{id}/enable` | record incident + return `enabled` |

Both write endpoints append to `<private_ops>/trust/incidents.csv`. They
do not perform external send.
