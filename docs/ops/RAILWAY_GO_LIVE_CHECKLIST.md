# Railway Go-Live Checklist

This checklist closes the gap between a green repository and a live Railway deployment.

## Current state

The repository can be green while Railway still fails if production service variables are missing. Railway starts Dealix with `APP_ENV=production`, and the API intentionally refuses to boot with placeholder or missing production secrets.

## Required Railway variables for the `dealix` service

Set these in Railway service variables, not in GitHub and not in the repository:

```text
APP_ENV=production
ENVIRONMENT=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_SECRET_KEY=<64 hex chars or strong random string>
JWT_SECRET_KEY=<64 hex chars or strong random string>
API_KEYS=<comma separated service keys>
ADMIN_API_KEYS=<comma separated admin keys>
CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me
APP_URL=https://api.dealix.me
BASE_URL=https://api.dealix.me
DEALIX_API_BASE=https://api.dealix.me
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Generate local secret strings

Run locally; never paste the values into chat:

```bash
python - <<'PY'
import secrets
print('APP_SECRET_KEY=' + secrets.token_hex(32))
print('JWT_SECRET_KEY=' + secrets.token_hex(32))
print('API_KEYS=' + secrets.token_urlsafe(32))
print('ADMIN_API_KEYS=' + secrets.token_urlsafe(32))
PY
```

## Validate before redeploy

From Codespaces/local with the same environment variables loaded:

```bash
make railway-env-check
```

Expected:

```text
RAILWAY_PRODUCTION_ENV=READY
```

## Redeploy

After variables are saved in Railway:

1. Redeploy the `dealix` service.
2. Check Railway logs for `RAILWAY_PRODUCTION_ENV=READY` if the checker is run manually.
3. Confirm the Railway deployment status is success.

## Production smoke

After deployment succeeds:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/api/status
```

Optional readiness check:

```bash
curl -fsS https://api.dealix.me/readyz || true
```

## Safety rule

Do not enable live outbound during beta unless a separate controlled-live PR and policy review are completed.

Keep these safe defaults during beta:

```text
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Launch verdicts

- Green GitHub matrix means the repo is beta-test ready.
- Railway success plus passing `/healthz` means the API is deployment-ready.
- Live customer pilot starts only after production smoke passes and outbound remains draft-only.
