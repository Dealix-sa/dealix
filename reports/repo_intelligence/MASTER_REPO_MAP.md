# Dealix MASTER_REPO_MAP.md

**Date:** 2026-06-23
**Branch:** feat/repo-archaeology-startup-map
**Remote:** origin https://github.com/Dealix-sa/dealix.git

## Repo shape

- Files (depth <=3): 7,772
- Directories (depth <=3): 1,579
- Python files total: ~15,460
- Test files: 638
- Markdown docs: ~3,700
- Frontend apps: `apps/web` (bare Next.js) + `frontend` (rich Next.js dashboard) + `frontend/dealix-app` + `frontend/founder-dashboard`
- Backend: FastAPI in `api/main.py`
- DB: SQLAlchemy models in `db/`, **alembic/versions/ is empty** (no migrations)
- CI/CD: 70+ workflows in `.github/workflows/`, Dockerfiles, Railway configs

## Stack

- Python 3.11/3.12
- FastAPI 0.115+
- SQLAlchemy async + asyncpg
- PostgreSQL, Redis, MongoDB
- Next.js 15 + React 19
- Tailwind 4 (`apps/web`) and Tailwind 3 (`frontend`)
- pydantic-settings for env
- pytest
- Railway deployment

## Major folder classification

### Keep (core startup system)
- `api/` — FastAPI backend + routers
- `app/` — outbound policy gate and lightweight modules
- `auto_client_acquisition/` — revenue, email, WhatsApp, lead pipeline
- `brand/` — logo, colors, visual identity
- `business/` — product docs, proposals, contracts, playbooks
- `clients/` — client delivery templates + workbench
- `company/` — company operating packs
- `core/` — config, logging, errors, utils
- `data/` — templates, seeds
- `db/` — SQLAlchemy models
- `dealix/` — core dealix modules and registers
- `docs/` — operations, strategy, launch plans
- `frontend/` — rich Next.js dashboard and public pages
- `apps/web/` — lightweight enterprise web app
- `integrations/` — email, WhatsApp, third-party connectors
- `ledgers/` — CSV operating ledgers
- `scripts/` — revenue, command room, launch runners
- `templates/` — outreach and contract templates
- `tests/` — test suite (638 test files)
- `workflows/` — sales and delivery workflows
- `.github/`, `alembic/`, `docker-compose.yml`, `railway.toml`

### Merge or supersede (useful but scattered)
- `business_autopilot/` — older automation templates
- `autonomous_growth/` — content/SEO engine
- `transformation_os/`, `intelligence_os/`, `self_evolving_os/`, `platform_core/`, `learning_flywheel/`, `founder_os/`, `executive/`, `mcp_server/`, `observability/`, `qa/`, `readiness/`, `continuous_improvement/`, `design-skills/`, `token-optimizer/`, `simulations/`

### Generated or ignore
- `.venv/`, `.pytest_cache/`, `node_modules/`, `outbox/`, `reports/` (except templates), `dealix.egg-info/`

### Dangerous / needs review before any live send
- `auto_client_acquisition/email/gmail_send.py` — Gmail OAuth send
- `auto_client_acquisition/whatsapp_safe_send.py` — WhatsApp safe send with gates
- `integrations/email.py` — email provider integration
- `integrations/whatsapp.py` — WhatsApp provider integration
- `api/routers/email_send.py` — email send API
- `api/routers/whatsapp_client_os.py` — WhatsApp client API
- `app/outbound/policy_gate.py` — new policy gate (GOOD)

### Archive candidates (superseded or marketing experiments)
- `patches/`, `landing/`, `sales/custom_ai/`, `sales/packages/`, `sales/service_pages/`, `presentations/`, `demos/`, `projects/`

## Existing startup assets to preserve

1. **Brand system** — `brand/` already has logo, colors, hero imagery, visual identity guide.
2. **Revenue machine** — `scripts/revenue/run_daily_revenue_machine.py` and related scripts.
3. **Command room** — `scripts/command_room/build_command_room.py` generates HTML dashboard.
4. **Safety tests** — `tests/test_no_auto_send.py`, `tests/test_no_guaranteed_revenue_claims.py`.
5. **Outbound policy gate** — `app/outbound/policy_gate.py` has correct controlled-live conditions.
6. **Client delivery templates** — `clients/_TEMPLATE/` and `_PROJECT_WORKBENCH/`.
7. **Service ladder** — `docs/COMPANY_SERVICE_LADDER.md`.
8. **Trust registers** — `dealix/registers/no_overclaim.yaml`, `dealix/registers/compliance_saudi.yaml`.
9. **Founder operating docs** — `README_FOUNDER_EXECUTION.md`, `docs/DAILY_OPERATING_GUIDE_AR.md`, `docs/DEALIX_OPERATING_CONSTITUTION.md`.
10. **Frontend dashboard** — `frontend/src/app/[locale]/` has many pages incl. ops, founder, dashboard, command-room, trust, clients.

## Startup layer gap analysis

| Product | Status | Existing file |
|---|---|---|
| Revenue Command Room OS | exists | `business/products/REVENUE_COMMAND_ROOM_OS.md` |
| Company Brain OS | missing | — |
| WhatsApp / Inbox Follow-up OS | missing | reuse `auto_client_acquisition/whatsapp_client_os/` |
| AI Trust & Compliance OS | missing | reuse `dealix/registers/`, `auto_client_acquisition/compliance_os/` |
| Client Delivery OS | exists | `company/delivery/CLIENT_DELIVERY_OS.md` |
| Controlled Live Outbound OS | exists | `business/products/CONTROLLED_LIVE_OUTBOUND_OS.md` |
| Company Diagnosis Sprint | missing | — |
| Daily CEO Decision Desk | missing | — |
| Offer Intelligence OS | missing | — |
| Market & Competitor Watch OS | missing | — |

## Makefile target status

- `production-check`: exists
- `company-day`: exists
- `command-room`: exists
- `full-revenue-day`: exists
- `outbound-dry`: MISSING
- `revenue-day`: exists
- `brain-day`: MISSING
- `client-intake`: MISSING

## Open PR / issue summary

- Open PRs: 50 (11 open, 39 draft)
- Non-dependabot open PRs include many Claude-generated drafts from 2026-06-07/08/11/17/21, mostly superseded by later work or stalled.
- Fetched issues: 75 total, including security Next.js upgrades and daily revenue machine failure reports from early May.
- Recent action runs show a mix of Global AI Transformation, CI, Agent Team Audit, Docker Build, CodeQL, Security, No-Crash Launch Guard workflows.

## Launch blockers

1. **No alembic migrations.** `alembic/versions/` empty.
2. **Two competing frontends.** Need to pick `frontend/` as primary dashboard/public site.
3. **50 open PRs / many drafts.** Need triage before they block `main`.
4. **Generated artifacts not fully gitignored.** `outbox/`, `reports/company_launch/`, etc. must not be committed.
5. **Server preflight needs DATABASE_URL + APP_SECRET_KEY.** Local runs fail without docker compose or `.env`.
6. **No `brain-day`, `client-intake`, `outbound-dry` targets yet.** Required by startup OS plan.
7. **Many duplicate/superseded modules** in `auto_client_acquisition/` could confuse new contributors.

## Recommended next PR sequence

1. **feat/release-stabilization-foundation** — stabilize existing code, add tests, fix build, gitignore generated outputs
2. **feat/startup-source-of-truth** — consolidate brand/company/product docs into one catalog
3. **feat/public-startup-website** — use `frontend/` to create homepage, product pages, diagnostic CTA
4. **feat/revenue-command-room-os** — reuse existing revenue scripts, make `full-revenue-day` deterministic
5. **feat/company-brain-os** — add daily decision, future radar, board memo
6. **feat/client-delivery-os** — create `clients/_template/` from existing `_TEMPLATE/` and `_PROJECT_WORKBENCH/`
7. **feat/ai-trust-compliance-os** — consolidate trust pack
8. **feat/controlled-live-outbound-os** — add dry/live policy gate, suppression, rate limits
9. **feat/production-railway-readiness** — migrations, healthchecks, env examples
10. **feat/gtm-machine** — sector playbooks, outreach cadence
11. **feat/founder-backoffice** — add missing dashboard views
12. **feat/go-live-pack** — final decision documents

## Exact next command

```bash
cd /c/Users/samim/dealix-inspect
.venv/Scripts/python scripts/run_company_launch_day.py
```

Then open PR from `feat/release-stabilization-startup-foundation`.
