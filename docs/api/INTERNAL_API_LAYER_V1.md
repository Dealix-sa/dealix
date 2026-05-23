# Internal API Layer v1

## Purpose

Expose safe internal APIs for the Founder Console so every page in the
UI reads from (and writes through) a documented endpoint rather than
talking to the database or external services directly.

This is the contract between `apps/web` and the FastAPI backend for
Founder Console v2.

## Principles

- Read endpoints can summarise operating data.
- Write endpoints must pass the Trust Plane.
- A2 / A3 actions require explicit founder approval.
- Every action writes an audit event.
- The frontend never writes directly to the database — it goes through
  the internal API.
- The internal API is mounted under `/api/v1/internal/*` and is reserved
  for the Founder Console; it is not part of the public OpenAPI surface
  for customers.

## Endpoint Groups

| Prefix | Purpose |
| --- | --- |
| `/api/v1/internal/ceo` | CEO morning brief / one top action |
| `/api/v1/internal/sales` | Sales funnel + cockpit counters |
| `/api/v1/internal/approvals` | Pending approvals + decision actions |
| `/api/v1/internal/workers` | Worker health + heartbeats |
| `/api/v1/internal/trust` | Trust flags + policy outcomes |
| `/api/v1/internal/finance` | Cash, MRR, pipeline, follow-ups |
| `/api/v1/internal/distribution` | Channel + sector scorecards |
| `/api/v1/internal/delivery` | Delivery queue (sprints, packs) |
| `/api/v1/internal/retention` | Retention queue (renewals, churn risk) |
| `/api/v1/internal/proof` | Proof library (case studies, evidence) |

## Endpoint Contract Rule

Every internal endpoint must define, in code and in this document:

- **input** — request body / query params
- **output** — JSON shape (typed in `apps/web/lib/dealix-runtime.ts`)
- **data source** — which worker or table provides the truth
- **trust class** — A1 (read), A2 (write, requires approval), or A3
  (sensitive, never automated)
- **audit behavior** — what is persisted on success / failure

## Current Endpoints (v1)

| Method | Path | Trust | Audit | Source |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/internal/ceo/summary` | A1 | none | `ceo_summary_worker` |
| GET | `/api/v1/internal/sales/funnel` | A1 | none | `revenue_runtime` |
| GET | `/api/v1/internal/approvals` | A1 | none | `approval_queue` |
| POST | `/api/v1/internal/approvals/{id}/approve` | A2 | written | `approval_queue` |
| POST | `/api/v1/internal/approvals/{id}/reject` | A2 | written | `approval_queue` |
| POST | `/api/v1/internal/approvals/{id}/request-edit` | A2 | written | `approval_queue` |
| GET | `/api/v1/internal/workers/health` | A1 | none | `worker_health_logs` |
| GET | `/api/v1/internal/trust/flags` | A1 | none | `trust_flag_log` |
| GET | `/api/v1/internal/finance/summary` | A1 | none | `finance_runtime` |
| GET | `/api/v1/internal/distribution/summary` | A1 | none | `channel_sector_scorecards` |
| GET | `/api/v1/internal/delivery/queue` | A1 | none | `delivery_queue` |
| GET | `/api/v1/internal/retention/queue` | A1 | none | `retention_queue` |
| GET | `/api/v1/internal/proof/library` | A1 | none | `proof_library` |

## Versioning

- This document and the matching router (`api/routers/internal/founder_console.py`)
  are version `v1`.
- Breaking changes require a `v2` router and a coordinated UI release.
- Adding new read endpoints is non-breaking and can ship in `v1.x`.

## Not Yet Wired (planned)

- Authentication on internal endpoints (founder-only session token).
- Real source-of-truth wiring (workers, queues, tables) per the runtime
  source-of-truth map.
- Audit persistence to `approval_decisions` ledger.
