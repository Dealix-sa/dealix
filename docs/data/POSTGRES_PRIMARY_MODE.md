# Postgres Primary Mode (roadmap)

Today: CSV + JSON inside `DEALIX_PRIVATE_OPS` is the **primary** store.
This is intentional — CSV is debuggable, portable, and forces every
read to go through `api/internal/runtime_reader.py`.

Tomorrow: Postgres becomes the primary; CSV becomes the export.

## Phases

1. **CSV primary** (today).
2. **Shadow Postgres** — every write hits CSV + Postgres; reads stay on CSV.
3. **Postgres primary** — reads switch to Postgres; CSV becomes an export
   produced by a worker.
4. **CSV export only** — Postgres is the only writable; CSV is a snapshot.

## First migration tables (when we get to phase 2)

* `lead_intelligence` (mirrors `intelligence/lead_intelligence_base.csv`)
* `outreach_queue`
* `approval_queue`
* `approval_decisions`
* `proposal_queue`
* `cash_collected`
* `worker_state`
* `trust_flags`
* `incidents`

## Notes

* Alembic is already present in the repo. New migrations land in
  `alembic/versions/` and are gated by `scripts/check_alembic_single_head.py`.
* The runtime reader will gain a `READER_BACKEND` switch (`csv` | `postgres`)
  in phase 2; until then it always reads CSV.
