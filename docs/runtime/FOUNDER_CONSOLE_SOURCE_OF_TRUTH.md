# Founder Console Source of Truth

## Purpose

Map every founder page to its source of truth so a number on screen can
always be traced back to a documented worker, queue, or table — never a
hard-coded UI constant.

## Pages

| Page | Source | Endpoint |
| --- | --- | --- |
| `/ceo` | CEO summary worker | `/api/v1/internal/ceo/summary` |
| `/sales-cockpit` | revenue runtime | `/api/v1/internal/sales/funnel` |
| `/approvals` | approval queue | `/api/v1/internal/approvals` |
| `/workers` | worker health logs | `/api/v1/internal/workers/health` |
| `/trust` | trust flags | `/api/v1/internal/trust/flags` |
| `/finance` | finance runtime | `/api/v1/internal/finance/summary` |
| `/distribution` | channel/sector scorecards | `/api/v1/internal/distribution/summary` |
| `/delivery` | delivery queue | `/api/v1/internal/delivery/queue` |
| `/retention` | retention queue | `/api/v1/internal/retention/queue` |
| `/proof` | proof library | `/api/v1/internal/proof/library` |

## Rule

A frontend number must come from a source of truth, not hard-coded UI.

If a page needs to surface a value that is not yet wired to a worker:

1. The endpoint still returns the field, with a safe zero / placeholder
   value.
2. The endpoint declares the planned source in its response (`source`
   field).
3. The Founder Console renders a "not yet wired" badge so Sami does not
   mistake placeholder zeros for real measurements.

## Wiring Status

| Endpoint | Source Wired? | Notes |
| --- | --- | --- |
| `/api/v1/internal/ceo/summary` | no | top action is static until CEO worker lands |
| `/api/v1/internal/sales/funnel` | no | funnel counters return 0 |
| `/api/v1/internal/approvals` | no | returns empty list |
| `/api/v1/internal/workers/health` | no | returns empty list |
| `/api/v1/internal/trust/flags` | no | returns empty list |
| `/api/v1/internal/finance/summary` | no | returns 0 / 0 / 0 |
| `/api/v1/internal/distribution/summary` | no | returns 0 / 0 / 0 |
| `/api/v1/internal/delivery/queue` | no | returns empty list |
| `/api/v1/internal/retention/queue` | no | returns empty list |
| `/api/v1/internal/proof/library` | no | returns empty list |

Wiring is tracked in the next runtime PRs. Production gate F6 (Runtime
Ready) cannot pass until every row in this table reads "yes".
