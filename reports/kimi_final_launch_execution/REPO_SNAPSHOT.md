# REPO SNAPSHOT — Dealix Launch Readiness Audit

## Git State
- **Branch**: `launch/kimi-final-readiness-20260614`
- **Base commit**: `30b65db692fc` — "Add files via upload (#717)"
- **Total commits**: 575
- **Original branch**: `main`

## Top-Level Architecture Summary

| Layer | Location | Count | Purpose |
|-------|----------|-------|---------|
| **FastAPI Backend** | `api/` | 2,587 Python files | Core API with 172+ routers |
| **Next.js Frontend (Primary)** | `frontend/` | ~300 TS/TSX | Main dashboard + ops surfaces |
| **Next.js Frontend (Legacy)** | `apps/web/` | ~50 TS/TSX | Legacy landing pages |
| **Business Logic** | `dealix/`, `core/`, `auto_client_acquisition/`, `autonomous_growth/` | ~800 Py | Revenue OS, AI agents, pipelines |
| **Tests** | `tests/` | 563 test files | Unit, integration, e2e, playwright |
| **CI/CD** | `.github/workflows/` | 60 workflows | CI, security, deployment, scheduled ops |
| **Documentation** | `docs/` | ~2,754 files | Architecture, commercial, compliance, ops |
| **Scripts** | `scripts/` | 314 Py + 106 Sh | Verification, automation, founder tools |
| **Integrations** | `integrations/` | ~100 files | HubSpot, payments, WhatsApp, etc. |
| **Migrations** | `alembic/`, `supabase/migrations/` | ~50 files | DB schema evolution |

## Key Apps and Services

### Backend (FastAPI)
- **Entry**: `api/main.py` — Factory pattern with lifespan manager
- **Routers**: 172 flat + 8 domain aggregators (admin, sales, customers, agents, compliance, analytics, webhooks, deprecated)
- **Security**: API key middleware, rate limiting, CORS, security headers, audit log
- **Auth**: JWT + API keys (production secret validation on boot)
- **Health**: `/health` endpoint + `/` root discovery
- **Payments**: Moyasar integration (sandbox by default)
- **Hermes**: Agent registry startup hook

### Frontend (Primary: `frontend/`)
- **Framework**: Next.js 15.1.3 + TypeScript + Tailwind
- **Key surfaces**:
  - `/[locale]/` — Public landing (CommercialLaunchHome)
  - `/[locale]/ops/founder` — Founder cockpit (90-min daily)
  - `/[locale]/ops/command-room` — Unified command room
  - `/[locale]/ops/war-room` — Revenue war room
  - `/[locale]/ops/marketing` — Marketing ops
  - `/[locale]/ops/sales` — Sales ops
  - `/[locale]/cloud` — Dealix Cloud UI
  - `/[locale]/business-now` — 8 pillars + commercial strategy
- **API proxy**: `frontend/src/app/api/dealix-proxy/` for admin-gated ops

### Frontend (Legacy: `apps/web/`)
- Same Next.js 15.1.3 version
- Surfaces: control-plane, war-room, pricing, lead-engine, proof-vault, data-room
- **Status**: Appears partially overlapping with `frontend/`

### Docker
- `Dockerfile` — Main app
- `docker-compose.yml` — Dev stack (app + postgres + redis + mongo)
- `docker-compose.prod.yml` — Production
- `Dockerfile.web`, `Dockerfile.worker`, `Dockerfile.company-brain`, `Dockerfile.watchdog`

## Test Counts
- **Total test files**: 563
- **Unit tests**: Majority in `tests/test_*.py`
- **Integration tests**: `tests/integration/`
- **E2E tests**: `tests/e2e/` + `tests/playwright/`
- **Load tests**: `tests/load/` + `locustfile.py`

## Workflow Counts (60 total)
- **Core CI/CD**: `ci.yml`, `deploy.yml`, `railway_deploy.yml`, `deploy-pages.yml`
- **Security**: `security.yml`, `agentic-security-gate.yml`, `codeql.yml`, `repository-hardening.yml`
- **Smoke/Verify**: `production-smoke.yml`, `staging-smoke.yml`, `official-launch-verify.yml`, `local_stack_verify.yml`
- **Founder/Business automation**: ~40 workflows (daily, weekly, scheduled)
- **Performance**: `lighthouse_ci.yml`, `playwright_smoke.yml`

## Env Template Locations
- `.env.example` — 175 lines, primary template
- `.env.railway.example` — Railway-specific
- `apps/web/.env.example` — Frontend web
- `frontend/.env.example` — Frontend dashboard

## Launch Docs and Go/No-Go
- `docs/ops/FOUNDER_GO_LIVE_DAY0_AR.md`
- `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md`
- `docs/DEALIX_LAUNCH_CLOSURE_VERDICT.md`
- `docs/DAY_1_LAUNCH_KIT.md`
- `docs/DEALIX_100_PERCENT_LAUNCH_PLAN.md`
- `scripts/verify_dealix_commercial_go_live.sh`
- `scripts/verify_commercial_launch_ready.py`

## Critical Observations
- **Duplication risk**: Two frontend directories (`frontend/` vs `apps/web/`)
- **Doc overload**: 2,754 doc files with 44 numbered directories having duplicates
- **Workflow overload**: 60 workflows, many founder-automation (may be noisy)
- **Archive files**: `.zip` and `.tar.xz` files in repo root (should not be committed)
- **Secret scanning**: `.gitleaks.toml`, `.secrets.baseline`, `pre-commit-config.yaml` present
