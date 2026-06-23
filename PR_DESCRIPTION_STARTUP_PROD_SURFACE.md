# Stabilize Startup Production Surfaces

## What Was Broken
1. `.env.example` missing outbound safety flags (EXTERNAL_SEND_ENABLED, OUTBOUND_MODE, EMAIL_SEND_ENABLED, WHATSAPP_SEND_ENABLED, SMS_SEND_ENABLED)
2. `docker-compose.prod.yml` had dead `frontend` service referencing deleted `frontend/Dockerfile`
3. Caddy upstream pointed to dead `frontend` service instead of canonical `web` service
4. Missing BASE_URL / DEALIX_API_BASE in .env.example
5. Missing Railway production runbook and environment variables reference docs

## What Was Fixed
- Added complete outbound safety section to `.env.example` with all 6 flags defaulting to false/draft_only
- Added BASE_URL and DEALIX_API_BASE to `.env.example`
- Removed dead `frontend` service from `docker-compose.prod.yml`
- Updated Caddy upstream to `web:3000` (canonical frontend)
- Updated Caddy depends_on to reference `web` instead of `frontend`
- Created `docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md`
- Created `docs/ops/ENVIRONMENT_VARIABLES_REFERENCE.md`
- Created `reports/go_live/FRONTEND_SURFACE_DECISION.md`
- Created `reports/go_live/PROD_SURFACE_STABILIZATION_REPORT.md`

## Why apps/web Is Canonical
`frontend/` was deleted on main in commit 62991222. `apps/web/` is the active Next.js app with Dockerfile, working build, login/signup pages, PostHog analytics, and Sentry integration.

## Validation Results
- Backend boot: API_BOOT_OK
- Frontend verify (typecheck + build): PASS
- Docker Compose config: VALID (with POSTGRES_PASSWORD set)
- compileall: PASS (no errors)
- Outbound safety: all flags default to false

## Not Included
- Backend endpoint additions (Phase 2)
- Frontend page additions (Phase 3)
- Database migrations (Phase 4)
- Company/brand docs (Phase 5)

## Next PR Recommendation
Phase 2: Backend production readiness (healthz, readyz, outbound safety endpoints)