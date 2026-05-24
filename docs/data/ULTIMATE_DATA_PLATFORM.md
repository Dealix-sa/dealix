# Ultimate Data Platform — منصة البيانات الشاملة

Status: v1
Owner: Founder

## 1. Purpose — الغرض

A single data platform that ingests structured artifacts, shadows them safely, promotes to primary storage, and exposes them to analytics — without ever exposing restricted data to LLM prompts.

منصة بيانات واحدة تستوعب الملفات المُهيكلة، تظللها بأمان، ترفعها إلى التخزين الأساسي، وتعرضها للتحليل دون كشف أي بيانات حساسة لمُحفّزات النماذج.

## 2. Tiers — الأطوار

```
+------------+     +-------------------+     +---------------------+     +------------+
|   CSV      | --> |  Shadow Postgres  | --> |  Primary Postgres   | --> | Warehouse  |
| ingest dir |     | (read-only mirror)|     | (read/write, RLS)   |     | (analytics)|
+------------+     +-------------------+     +---------------------+     +------------+
```

Promotion is policy-gated. CSV is the audit floor. Primary Postgres is the operating store. Warehouse is the analytics store.

## 3. CSV Ingest — استيعاب CSV

- Drop location: `/opt/dealix-ops-private/<domain>/inbox/`.
- Naming: `<domain>__<stream>__<YYYYMMDDTHHMMSS>.csv`.
- Schema: every file ships with a `.schema.json` next to it.
- Validation: hash, schema-conformance, row-count, max-size, sensitive-column scan.
- On accept: file is moved to `received/`. On reject: moved to `quarantine/` with reason.

## 4. Shadow Postgres — قاعدة الظل

- Mirrors accepted CSVs into typed tables.
- Read-only from the application. Used to validate transforms before promotion.
- Retention: 30 days rolling, then archived to cold storage with hash.

## 5. Promotion to Primary — الترقية

- Promotion is a job, not a click.
- Each promotion:
  1. Diff vs. primary.
  2. Lint and constraint checks.
  3. Founder approval (A2) for any column added or type changed.
  4. Audit entry with diff hash.
  5. Atomic write inside a transaction.
- Rollback path: PITR + audit log replay.

## 6. Primary Postgres — القاعدة الأساسية

- The operating store for the company.
- Row Level Security per data tier.
- No agent has direct write access; agents write only through allowed services.
- Backups: daily snapshot + PITR; restore drill monthly.
- See `docs/data/POSTGRES_PRIMARY_MODE.md`.

## 7. Warehouse — المستودع

- ELT from primary; never from agents or CSV directly.
- Used for scorecards, DORA, AI cost, maturity reporting.
- Restricted columns are tokenized in the warehouse.
- Access is scoped to Control Plane queries and offline analysts.

## 8. Data Tiers — أطوار التصنيف

| Tier | Examples | Agent prompts allowed? |
|---|---|---|
| public | brand assets, public copy | yes |
| internal | ICP rubric, scorecards, drafts | yes |
| confidential | engagement records, pilot results | yes (redacted) |
| restricted | full-fidelity PII, payment data | no |

The agent prompt builder MUST refuse any field marked `restricted`. The Trust Guardian double-checks.

## 9. Lineage — النسب

Every row carries:
- `source_file_hash`
- `ingested_at`
- `promoted_at`
- `producer` (worker id or agent id)
- `policy_version`

Lineage queries are first-class; the Control Plane exposes lineage for any displayed metric.

## 10. Failure Modes — أنماط الفشل

- CSV malformed -> quarantined; audit entry; no promotion.
- Shadow diverges from primary -> promotion blocked; alert.
- Primary unavailable -> writes paused; CSV inbox keeps queuing; nothing is lost.
- Warehouse unavailable -> analytics stale; scorecard shows "stale" banner.

## 11. Non-Negotiables — خطوط حمراء

- No agent writes directly to primary.
- No restricted data is ever in a warehouse plain-text column.
- No CSV is deleted before its hash is in audit.
- No promotion without approval log.

## 12. References — مراجع

- `docs/data/POSTGRES_PRIMARY_MODE.md`
- `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
