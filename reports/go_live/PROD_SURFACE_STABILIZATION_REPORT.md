# Production Surface Stabilization Report

## Date: 2026-06-23
## Branch: fix/startup-prod-surface-stabilization

## What Was Broken
1. `.env.example` missing critical outbound safety flags (EXTERNAL_SEND_ENABLED, OUTBOUND_MODE, EMAIL_SEND_ENABLED, WHATSAPP_SEND_ENABLED, SMS_SEND_ENABLED)
2. `docker-compose.prod.yml` had dead `frontend` service referencing deleted `frontend/Dockerfile`
3. Caddy upstream pointed to `frontend:3000` (dead service) instead of `web:3000`
4. No BASE_URL / DEALIX_API_BASE in .env.example
5. No docs for Railway production runbook or environment variables reference

## What Was Fixed
1. Added outbound safety section to `.env.example` with all 6 flags set to false/draft_only
2. Added BASE_URL and DEALIX_API_BASE to `.env.example`
3. Removed dead `frontend` service from `docker-compose.prod.yml`
4. Updated Caddy `DEALIX_FRONTEND_UPSTREAM` to `web:3000`
5. Updated Caddy `depends_on` to reference `web` instead of `frontend`
6. Created `docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md`
7. Created `docs/ops/ENVIRONMENT_VARIABLES_REFERENCE.md`
8. Created `reports/go_live/FRONTEND_SURFACE_DECISION.md`

## Validation Results
- Backend boot: API_BOOT_OK (with safe env)
- Frontend verify: PASS (typecheck + build)
- Docker Compose config: VALID (with POSTGRES_PASSWORD set)
- compileall: PASS (no errors)
- Outbound safety: all flags default to false in .env.example and .env.production.example

## apps/web Is Canonical Frontend
- frontend/ was deleted on main (commit 62991222)
- apps/web/ has working Next.js app with Dockerfile
- Build and typecheck pass

## Not Included
- Backend endpoint additions (Phase 2)
- Frontend page additions (Phase 3)
- Database migrations (Phase 4)
- Company/brand docs (Phase 5)
- Product catalog (Phase 6)

## Next PR Recommendation
Phase 2: Backend production readiness (healthz, readyz, outbound safety endpoints)