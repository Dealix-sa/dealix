# Control Plane API

All endpoints below live under `/api/v1/internal/`. They are gated by
`DEALIX_INTERNAL_TOKEN` in production (header
`X-Dealix-Internal-Token`).

## Read endpoints

| Path | Description |
|---|---|
| `GET /control/summary` | Policies, agents, risks, scorecard summary |
| `GET /control/policies` | Approval classes + rule ids |
| `GET /control/agents` | Full agent registry + enabled state |
| `GET /control/scorecard` | Live operating scorecard payload |
| `GET /control/risks` | Open trust flags |
| `GET /evals/status` | Eval gate suite totals |
| `GET /security/status` | Security controls + production token flag |

## Mutating endpoints

| Path | Effect |
|---|---|
| `POST /control/agents/{id}/disable` | Disable an agent (audited) |
| `POST /control/agents/{id}/enable` | Enable an agent (audited) |
| `POST /approvals/{id}/approve` | Approve an approval row (audited) |
| `POST /approvals/{id}/reject` | Reject (audited) |
| `POST /approvals/{id}/request-edit` | Send back for edit (audited) |
| `POST /approvals/{id}/escalate` | Escalate (audited) |

Every mutating endpoint appends a row to
`${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv`.
