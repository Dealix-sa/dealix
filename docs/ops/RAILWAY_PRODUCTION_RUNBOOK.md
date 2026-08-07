# Railway Production Runbook

## Services
| Service | Purpose | Port | Health Check |
|---------|---------|------|--------------|
| API (FastAPI) | Backend API | 8000 | GET /healthz |
| Web (Next.js) | Frontend | 3000 | GET /healthz |
| Postgres | Database | 5432 | pg_isready |
| Redis | Cache/queue | 6379 | redis-cli ping |
| Caddy | Reverse proxy | 80/443 | - |

## Railway Deployment

### Environment Variables (required)
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
APP_SECRET_KEY=<generate 64-byte hex>
JWT_SECRET_KEY=<generate 64-byte hex>
API_KEYS=<comma-separated client keys>
ADMIN_API_KEYS=<comma-separated admin keys>
CORS_ORIGINS=https://dealix.me,https://www.dealix.me
APP_ENV=production
ENVIRONMENT=production
```

### Outbound Safety Defaults (never change in production without approval)
```
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Deployment Steps
1. Ensure all env vars are set in Railway
2. Deploy API service (Dockerfile at repo root)
3. Deploy Web service (apps/web/Dockerfile)
4. Run `alembic upgrade head` after first deploy
5. Verify /healthz responds 200
6. Verify /api/status returns safe status

## Rollback
- Railway automatically keeps previous deployment
- Click "Rollback" in Railway dashboard if health checks fail

## Smoke Tests
- `curl https://api.dealix.me/healthz` → 200
- `curl https://api.dealix.me/api/status` → JSON with status
- `curl https://dealix.me` → 200 (frontend loads)

## Owner
CTO / Release Engineer