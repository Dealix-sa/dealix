# Postgres Primary Mode

Dealix runs Postgres as the primary durable store. Postgres holds the transactional state that the operating CSVs in `$PRIVATE_OPS` mirror. When Postgres is the truth, the CSVs are derived; when the CSVs are the truth, Postgres is the index.

**Source of truth:** Postgres schema in `db/migrations/` + `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
**Owner:** Engineering Lead
**Trust gate:** A2 — schema changes require founder approval and migration review.

## What lives in Postgres

| Domain | Tables |
|--------|--------|
| Identity | `users`, `roles`, `tenants` |
| Revenue | `signals`, `opportunities`, `proposals`, `contracts`, `invoices` |
| Finance | `payments`, `recognitions`, `cost_ledger` |
| Delivery | `engagements`, `milestones`, `deliverables` |
| Customer Success | `health_scores`, `risks`, `working_sessions` |
| Agents | `agent_runs`, `tool_calls`, `eval_results` |
| Trust | `approval_decisions`, `policy_events`, `audit_log` |
| Proof | `consents`, `proof_artifacts` |

## Why Postgres as primary

- ACID guarantees.
- Mature ecosystem for backup, restore, replication.
- Row-level security available for tenant isolation.
- Auditable: every write logged with `created_at`, `created_by`, `updated_at`, `updated_by`.

## CSV mirror

Some surfaces — early prototype tools, founder-side ad-hoc reads, partner exports — operate on CSVs in `$PRIVATE_OPS`. The contract:

- **Writes** go to Postgres first. A change-data-capture process projects to CSV.
- **Reads** prefer Postgres for transactional accuracy and CSV for analyst convenience.
- **Reconciliation** nightly: any CSV row missing in Postgres or vice versa triggers an alert.

## Schema discipline

- Migrations are forward-only with reversible escape hatches.
- Every table has `created_at`, `updated_at`, `created_by`, `updated_by`.
- Every table has a primary key that is a stable identifier, not an auto-increment that exposes volume.
- Soft-delete preferred over hard-delete; deletion is a compliance event (`docs/04_data_os/DATA_RETENTION_POLICY.md`).

## Tenancy

Row-level security enforces tenant isolation. Cross-tenant queries require a named, audited service-account path and explicit founder approval.

## Backup and restore

- Continuous WAL archive.
- Point-in-time recovery target: 5 minutes.
- Daily full backup retained 30 days; weekly retained 1 year.
- Restore drills quarterly.

## Failure modes

- **Schema-mirror drift:** CSV column added without Postgres column. Detection: nightly diff. Recovery: schema patch.
- **RLS bypass:** a query crosses tenants. Detection: query log audit. Recovery: deny path; root cause filed.
- **Backup failure:** a backup is missed. Detection: backup monitor. Recovery: replay from WAL; investigate.

## Recovery path

If Postgres is unavailable, the runtime fails closed for write paths. Read paths can serve cached CSV snapshots in degraded mode with a banner. No actions dispatch on degraded read.

## Metrics

- Primary write latency (p50, p99).
- CSV mirror lag (seconds).
- Restore-drill success rate.
- RLS bypass incidents (target: 0).

## Disclaimer

Postgres reliability is engineered, not absolute. Dealix does not guarantee zero downtime. Estimated value is not Verified value.
