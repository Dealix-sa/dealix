# Postgres Primary Mode (roadmap)

Today the Founder Console reads CSVs under `$DEALIX_PRIVATE_OPS`. The
roadmap moves the same domains to Postgres in four steps:

1. **CSV primary** (current). Schema lives in
   `scripts/bootstrap_private_ops_runtime.py`.
2. **Shadow Postgres**. Add SQLAlchemy models that mirror each CSV's
   columns; have the workers double-write. No reader change.
3. **Postgres primary**. Switch the runtime reader to read from Postgres
   first, CSV as fallback for offline/dev.
4. **CSV export**. Keep a CSV export job for audit/portability.

Migrations are NOT auto-generated here because the existing repo has
two migration trees (`alembic/` and `migrations/`). Pick one and write
a focused migration when the schema is locked. Do **not** introduce
broken migrations.
