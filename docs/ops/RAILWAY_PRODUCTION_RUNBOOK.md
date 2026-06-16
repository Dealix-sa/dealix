# Railway Production Runbook

## Services
- `dealix` — API + dashboard + webhooks.
- `Postgres` — source of truth.
- `dealix-worker` — daily jobs + outbound queue (future).
- `dealix-cron` — scheduled daily tasks (future).

## Database URL
Use reference variable only:
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```
Do not use `DATABASE_PUBLIC_URL` inside the app.

## Required Variables
```env
APP_ENV=production
ENVIRONMENT=production
APP_URL=https://api.dealix.me
BASE_URL=https://api.dealix.me
DEALIX_API_BASE=https://api.dealix.me
CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me
DATABASE_URL=${{Postgres.DATABASE_URL}}
EXTERNAL_SEND_ENABLED=true
OUTBOUND_MODE=controlled_live
OUTBOUND_REQUIRE_APPROVAL=true
EMAIL_SEND_ENABLED=true
EMAIL_SEND_MODE=live
WHATSAPP_SEND_ENABLED=true
WHATSAPP_ALLOW_LIVE_SEND=true
WHATSAPP_SEND_MODE=template_only
```

## Deployment Steps
1. Push branch to GitHub.
2. Create PR.
3. Wait for CI (fix failures).
4. Merge to main.
5. Railway auto-deploys.
6. Run `alembic upgrade head`.
7. Run `make outbound-env`.
8. Run health checks.

## Monitoring
```bash
railway logs --service dealix
railway variables --service dealix
```

## Rollback
- Revert commit.
- Redeploy via Railway dashboard.
