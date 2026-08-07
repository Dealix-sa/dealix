# Dealix Railway Deployment Rules

## Current status (2026-06-30)

- Railway billing past due — founder must pay manually.
- Service source may be `ghcr.io/railwayapp-temp` — must be reconnected to GitHub repo.
- Production variables must be set before redeploy.
- Do not attempt to bypass production secret validation to make Railway boot.

## railway.toml contract

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"
healthcheckPath = "/healthz"
healthcheckTimeout = 300
```

Do not change builder to NIXPACKS. Do not remove healthcheckPath.

## Required Railway service variables

```
APP_ENV=production
ENVIRONMENT=production
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_SECRET_KEY=<64-char hex>
JWT_SECRET_KEY=<64-char hex>
API_KEYS=<comma-separated keys>
ADMIN_API_KEYS=<comma-separated keys>
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

## Generate secrets locally (never commit values)

```bash
python3 - <<'PY'
import secrets
print('APP_SECRET_KEY=' + secrets.token_hex(32))
print('JWT_SECRET_KEY=' + secrets.token_hex(32))
print('API_KEYS=' + secrets.token_urlsafe(32))
print('ADMIN_API_KEYS=' + secrets.token_urlsafe(32))
PY
```

## Validate before redeploy

```bash
make railway-env-check
# Expected: RAILWAY_PRODUCTION_ENV=READY
```

## Recovery procedure

Full runbook: `docs/ops/RAILWAY_RECOVERY_RUNBOOK.md`

Short path:
1. Pay Railway billing.
2. Disconnect `ghcr.io/railwayapp-temp` source if present.
3. Connect GitHub repo `Dealix-sa/dealix`, branch `main`.
4. Set Dockerfile path to `Dockerfile`.
5. Attach Postgres plugin.
6. Set all required service variables above.
7. Redeploy then check `/healthz`.

## Production smoke (after deployment)

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/api/status
```

`/api/status` must show `external_send_enabled: false`.
