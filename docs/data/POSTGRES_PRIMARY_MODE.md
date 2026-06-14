# Postgres Primary Mode

> Move Dealix runtime from CSV bootstrap to Postgres as the single
> source of truth.

## Purpose

CSV worked well enough to start the company. It does not survive
multi-process workers, concurrent founder + worker writes, or audit
guarantees. Postgres Primary Mode promotes Postgres from "backup we
might use" to "the only place runtime state lives".

## Position in the Operating Layer

This is the Data Layer of Operating Layer v1. Founder Console v5
surfaces, every worker, and every audit consumer must read from
Postgres once this mode is on.

## First Tables

The minimum set that powers `/ceo`, `/approvals`, `/sales-cockpit`,
`/workers`, `/trust`, and `/finance`:

| Table | Purpose |
|-------|---------|
| `approval_queue` | Pending approvals visible in `/approvals` |
| `approval_decisions` | Founder decisions with reason + evidence |
| `lead_intelligence` | Enriched leads, scored and routed |
| `outreach_queue` | Drafted outreach awaiting approval / sent |
| `conversation_log` | All inbound + outbound messages with route labels |
| `proposal_queue` | Proposals drafted / approved / sent / accepted |
| `payment_capture_queue` | Payment / PO follow-ups in flight |
| `worker_state` | Last run, status, failures, queue depth per worker |
| `trust_flags` | Open trust flags emitted by Guardian / Policy |
| `audit_events` | Append-only audit log for every layer |

All tables have:

- A surrogate id (UUID).
- `created_at`, `updated_at` (timestamptz, default `now()`).
- A `version` integer for optimistic concurrency on mutable rows.
- An immutable `source` column noting the worker / agent that wrote it.
- A `payload jsonb` column for structured detail where appropriate.

## Migration Strategy

### Phase 1 — Shadow Write

- Every writer continues to write CSV.
- Every writer **also** writes to Postgres in the same transaction.
- A consistency worker compares the two daily and reports drift.

### Phase 2 — API Reads Postgres

- Founder Console v5 surfaces flip to read Postgres.
- CSV reads remain available as a fallback for one release.
- `/workers` shows which surfaces have flipped.

### Phase 3 — CSV Export

- CSV writes are removed from the runtime path.
- A scheduled export worker produces CSV daily for reporting / sharing.
- CSV is no longer trusted as a source.

### Phase 4 — Event Sourcing

- Every mutation also writes an event row.
- Replay tooling reconstructs state for audit / disaster recovery.
- Snapshots are taken nightly.

## Migration Order

Migrate first the tables that power founder surfaces, in this order:

1. `approval_queue` + `approval_decisions` — unlock `/approvals`.
2. `worker_state` — unlock `/workers`.
3. `audit_events` — unlock cross-surface trust.
4. `trust_flags` — unlock `/trust`.
5. `outreach_queue` + `conversation_log` + `lead_intelligence` —
   unlock `/sales-cockpit`.
6. `proposal_queue` + `payment_capture_queue` — unlock `/finance`.

`/ceo` lights up gradually as each of the above flips.

## Operational Requirements

- **Migrations:** Alembic only. No ad-hoc schema changes.
- **Backups:** nightly + WAL streaming. Tested restore drill monthly.
- **Connection pooling:** PgBouncer in transaction mode.
- **RLS:** off in v1 (single-tenant); revisit for partner access.
- **Schema review:** every migration PR requires the founder's sign-off
  plus one engineer review.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Drift between CSV and Postgres (Phase 1) | Daily consistency worker | Block Phase 2 flip until clean |
| Migration partial failure | Alembic exit code + post-migration verifier | Rollback, never patch live |
| Read fallback to CSV silently | API health check | Surface a `degraded` badge in `/workers` |
| Audit gap | Audit verifier finds missing events | Open incident, freeze writes for that table |

## Rule

> Migrate first the tables that power founder surfaces. Everything
> else waits.

We do not migrate prettier tables first. We migrate the tables that
turn `/ceo`, `/approvals`, `/workers`, `/trust`, and `/finance` from
"showing data" to "showing truth".

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`WORKER_ORCHESTRATOR_V1`](../runtime/WORKER_ORCHESTRATOR_V1.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
