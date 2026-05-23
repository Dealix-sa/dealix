# Postgres Primary Mode

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

Postgres is the primary store for Dealix. The CSV files in the
private ops runtime are the operational tier. They are not the system
of record. This document clarifies the responsibilities of each
layer and the rules that prevent drift.

## Why Postgres is primary

Postgres holds the durable, query-friendly, transactionally consistent
data that the platform depends on:

- Account, contact, deal, contract, invoice, payment.
- User, role, permission, session.
- Customer artifacts (assets, files, proof entries).
- Application-level state that must survive restarts and replays.

Postgres is the source of truth for the things that have business
meaning beyond a worker pass. It is the only store with rollback,
multi-row transactions, foreign keys, and migrations. The Alembic
migration files in `alembic/versions/` define the schema; the
`scripts/verify_dealix_ready.py` and related verifiers assert the
database posture.

The environment surface is `DEALIX_PRIMARY_STORE`. The Founder
Console exposes it via `GET /api/v1/internal/data/summary`:

```
{"primary_store": "postgres", "dq_score": null, ...}
```

## Why CSVs are operational

The CSV tier is the operational layer that workers read and write
between runs. It exists for three reasons:

1. **Plain-text auditability.** Operators and the founder can read a
   CSV without a database client.
2. **Append-only safety.** The audit ledger and the suppression list
   are append-only by file convention; no schema migration can drop
   a column accidentally.
3. **Boundary.** The private ops runtime is outside the repo,
   outside the application database, and outside any third-party
   service. It is a deliberate trust boundary.

The CSVs are bootstrapped by
`scripts/bootstrap_private_ops_runtime.py` and live at
`/opt/dealix-ops-private` (or `$PRIVATE_OPS`). The full schema is in
`docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`.

## Responsibilities

| Layer                  | Responsible for                                                                    | Not responsible for                                       |
| ---------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Postgres               | Business-critical state, joins, durable rollbacks, schema invariants, identity.    | Approvals queue tail, audit append-only writes.           |
| Private ops CSVs       | Queues, approvals, audit, suppression, scorecards, worker state.                    | Joins, multi-row transactions, foreign keys.              |
| Application config     | Static configuration; environment variables.                                       | Operating state, customer data.                           |
| Object storage         | Large blobs (attachments, exports).                                                | Operating state, audit.                                   |

## Read path

| Surface                                  | Reads from         |
| ---------------------------------------- | ------------------ |
| Customer-facing API                      | Postgres            |
| Founder Console business endpoints       | Postgres            |
| Founder Console operating endpoints      | Private ops CSVs    |
| Workers                                  | Both, as needed     |
| Verifiers                                | Both, as needed     |

The Founder Console operating endpoints (approvals, audit, trust
flags, worker state, finance unit economics, distribution scorecards)
read from the private ops runtime via
`api/internal/runtime_reader.py`. When the runtime is unset, reads
return empty structures with `data_source: "no-runtime"` so the UI
degrades gracefully.

## Write path

The write path is asymmetric:

- Business writes go to Postgres via the application code.
- Operating writes go to private ops CSVs via the Founder Console
  internal router or the worker orchestrator.
- The audit ledger (`trust/approval_decisions.csv`) is written by
  the router only.
- The suppression list (`outreach/suppression_list.csv`) is written
  by the Trust Guardian only.
- Workers may write to their own assigned directories per the
  `allowed_write_targets` in `registries/agent_registry.yaml`.

A worker never writes business data directly to Postgres. Business
state changes go through the application, which is audit-aware.

## Synchronization

| Direction          | Mechanism                                                       | Cadence       |
| ------------------ | --------------------------------------------------------------- | ------------- |
| Postgres → CSV     | Snapshot workers export aggregates to scorecards.                | Hourly/Daily.  |
| CSV → Postgres     | None for audit/suppression; deal updates go through the app.    | n/a            |

Snapshot workers are read-only on Postgres and write-only to specific
runtime directories. They write through the same `allowed_write_targets`
discipline.

## Backups

Postgres backups are owned by the platform team. The cadence and
recovery strategy are documented in
`docs/security/BACKUP_AND_RESTORE_OS.md`. The private ops runtime is
backed up on the same cadence, but separately, because the trust
boundary is real.

## Schema and migrations

Postgres schema changes flow through Alembic. The migration policy
is documented in `docs/ops/ALEMBIC_MIGRATION_POLICY.md`. CSV schema
changes flow through the bootstrap script; new columns are appended
on the right, never inserted, so existing readers remain compatible.

## Why not move audit and suppression into Postgres?

This is a deliberate choice. Three reasons:

1. The audit ledger is the trust artifact. Keeping it as a file
   outside the application database means a compromise of the
   application does not silently overwrite history.
2. The suppression list is operationally sensitive. The file lives
   in the private ops runtime under a separate mount, with separate
   backups.
3. CSV writers are simpler. The router's `_audit_event` function is
   trivial; we want trivial code in the trust path.

If we ever revisit this decision, the migration must keep the
append-only and out-of-application properties intact.

## What the data summary endpoint will show

`GET /api/v1/internal/data/summary` returns:

| Field                  | Source                                |
| ---------------------- | ------------------------------------- |
| `primary_store`        | `DEALIX_PRIMARY_STORE` env (default `postgres`). |
| `dq_score`             | `data/dq_score.csv` (when present).   |
| `pipelines_failed_24h` | `data/pipeline_failures.csv`.         |
| `last_dq_run`          | `data/dq_run_log.csv`.                |

The DQ scoring system is documented in `DATA_QUALITY_SYSTEM.md`.

## Discipline

1. Business state goes in Postgres.
2. Operating state goes in private ops CSVs.
3. The two never overwrite each other.
4. The trust boundary is a real folder, not a convention.
5. Migrations are documented and reversible.
