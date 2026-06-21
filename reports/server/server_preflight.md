# Server Preflight

**Status:** FAIL

## Environment
- [x] APP_SECRET_KEY (cryptographic signing)
- [x] DATABASE_URL (PostgreSQL connection)
- [x] REDIS_URL (cache / queue, optional) — not set
- [x] MOYASAR_SECRET_KEY (payments sandbox/live, optional) — not set
- [x] HUBSPOT_ACCESS_TOKEN (CRM sync, optional) — not set

## Alembic
- [ ] /home/codespace/.python/current/bin/python3: No module named alembic.__main__; 'alembic' is a package and cannot be directly executed
