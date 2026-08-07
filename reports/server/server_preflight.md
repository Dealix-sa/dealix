# Server Preflight

**Status:** PASS

## Environment
- [x] APP_SECRET_KEY (cryptographic signing)
- [x] DATABASE_URL (PostgreSQL connection)
- [x] REDIS_URL (cache / queue, optional) — not set
- [x] MOYASAR_SECRET_KEY (payments sandbox/live, optional) — not set
- [x] HUBSPOT_ACCESS_TOKEN (CRM sync, optional) — not set

## Alembic
- [x] OK: single Alembic head (20260610_015_simplify_product_for_launch)
