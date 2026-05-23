# Postgres Primary Mode

Today's runtime reader works on CSVs under `${DEALIX_PRIVATE_OPS}`.
Moving to Postgres is a 5-step migration:

1. **CSV primary** (current). Workers + Founder Console read/write CSVs.
2. **Shadow Postgres**. Every CSV write also inserts to Postgres. Reads
   still come from CSV; we compare nightly.
3. **Postgres primary**. Reads switch to Postgres; CSVs become a debug
   dump.
4. **CSV export**. Daily export job materialises CSVs from Postgres so
   the founder can grep locally.
5. **Event-sourced audit log**. `approval_decisions` becomes an
   append-only `decision_events` table with a hash chain.

## First tables

`approval_queue, approval_decisions, lead_intelligence, outreach_queue,
conversation_log, proposal_queue, payment_capture_queue, worker_state,
trust_flags, audit_events, agent_registry, policy_results, eval_results`.

## Migration mechanics

Add SQLAlchemy models under `db/models/` and Alembic migrations under
`alembic/versions/`, mirroring the CSV headers in
`api.internal.runtime_reader.RUNTIME_FILES`. Do not create migrations
until the founder asks for them — the current state intentionally keeps
CSV as the source of truth.
