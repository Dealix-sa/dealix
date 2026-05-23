# Frontend API Contract

## Purpose
Define the backend endpoints required by each page in the Dealix Founder
Frontend (`apps/web`). The frontend never bypasses Trust. Every
external-impact action routes through `/api/v1/approvals`.

## Conventions
- All endpoints under `/api/v1/`.
- Read endpoints: `GET`. Decision endpoints: `POST`.
- Auth: founder console requires `X-Admin-API-Key` (see `api/security.py`).

## CEO Command Center (`/ceo`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Snapshot | GET | `/api/v1/business-now/snapshot` | exists |
| Founder dashboard | GET | `/api/v1/founder/dashboard` | exists |
| Command center summary | GET | `/api/v1/command-center` | exists |
| Worker health | GET | `/api/v1/observability/workers` | partial — see Gaps |
| Top CEO action | GET | `/api/v1/ceo/top-action` | **gap** |

## Sales Cockpit (`/sales-cockpit`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Sales summary | GET | `/api/v1/sales` | exists |
| Revenue pipeline | GET | `/api/v1/revenue-pipeline` | exists |
| Follow-ups | GET | `/api/v1/sales/follow-ups` | **gap** |
| Payment capture | GET | `/api/v1/payment-ops` | exists |

## Approval Center (`/approvals`)
| Panel | Method | Path | Status |
|---|---|---|---|
| List approvals | GET | `/api/v1/approvals` | exists |
| Approve | POST | `/api/v1/approvals/{id}/approve` | exists |
| Reject | POST | `/api/v1/approvals/{id}/reject` | exists |
| Request edit | POST | `/api/v1/approvals/{id}/request-edit` | **gap** |

## Distribution (`/distribution`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Channels | GET | `/api/v1/expansion-engine/channels` | partial |
| Sectors | GET | `/api/v1/expansion-engine/sectors` | partial |
| Experiments | GET | `/api/v1/growth/experiments` | exists |

## Workers (`/workers`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Worker list | GET | `/api/v1/observability/workers` | partial — see Gaps |
| Agent mesh | GET | `/api/v1/agent-mesh` | exists |

## Trust (`/trust`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Audit flags | GET | `/api/v1/safety/flags` | partial |
| Agent governance | GET | `/api/v1/agent-governance` | exists |
| Policy evaluate | POST | `/api/v1/safety/evaluate` | exists |

## Finance (`/finance`)
| Panel | Method | Path | Status |
|---|---|---|---|
| Finance summary | GET | `/api/v1/finance` | exists |
| Revenue metrics | GET | `/api/v1/revenue-metrics` | exists |
| MRR | GET | `/api/v1/finance/mrr` | **gap** |
| Runway | GET | `/api/v1/finance/runway` | **gap** |

## Gaps (tracked)
1. `GET /api/v1/ceo/top-action` — derived top action (no dedicated endpoint yet)
2. `GET /api/v1/sales/follow-ups` — exposed under different prefix today
3. `POST /api/v1/approvals/{id}/request-edit` — only approve/reject implemented
4. `GET /api/v1/observability/workers` — current observability is event-based, not roster
5. `GET /api/v1/finance/mrr` and `/runway` — finance_os returns combined snapshot
6. `GET /api/v1/expansion-engine/channels` and `/sectors` — current router returns aggregates

## Rule
- Frontend **never** bypasses Trust. Every external-impact action goes through `/api/v1/approvals`.
- New endpoints required by this contract are added under existing routers, not in new top-level routes.
- If a panel lacks an endpoint, the page renders mock data **and** logs a `// TODO: live wire` comment naming the missing path.
