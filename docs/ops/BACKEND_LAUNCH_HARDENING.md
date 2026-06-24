# Dealix Backend Launch Hardening

## الهدف

تجهيز backend لإطلاق تجاري فعلي مع أمان افتراضي وتشغيل مستقر.

## Launch baseline

- API boots with safe env.
- health endpoint remains stable.
- DB config uses DATABASE_URL from Railway Postgres in production.
- communication flags are false by default.
- No secrets are committed.
- Commercial scripts run without external APIs.

## Required checks before launch

```bash
python scripts/commercial/commercial_readiness_check.py
python scripts/ops/backend_launch_cleanliness_check.py
python -m compileall -q api app core db dealix scripts
python -m pytest -q tests/test_commercial_pack.py
```

## Environment contract

Required production variables:

- APP_ENV=production
- ENVIRONMENT=production
- APP_SECRET_KEY
- JWT_SECRET_KEY
- DATABASE_URL
- CORS_ORIGINS
- APP_URL
- BASE_URL
- DEALIX_API_BASE

Safe defaults:

- EXTERNAL_SEND_ENABLED=false
- EMAIL_SEND_ENABLED=false
- WHATSAPP_SEND_ENABLED=false
- WHATSAPP_ALLOW_LIVE_SEND=false
- SMS_SEND_ENABLED=false
- OUTBOUND_MODE=draft_only

## Database policy

- Additive migrations only for launch.
- Keep models and migrations aligned.
- Use Alembic for production changes.
- Review every migration before production.

## API policy

- Sensitive operations require auth.
- AI recommendations require human review.
- Records need owner, source, status, and audit trail.
- Errors must not leak secrets.

## Railway policy

- Use healthcheck.
- Use Postgres private reference for DATABASE_URL.
- Run migration steps only after review.
- Keep safe defaults.
