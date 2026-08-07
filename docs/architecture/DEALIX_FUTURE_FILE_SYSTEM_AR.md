# DEALIX FUTURE FILE SYSTEM — Architecture Guide

## Canonical Folders and Owners

```
dealix/
├── api/                    # Backend team — FastAPI entry + routers
│   ├── main.py             # App factory — NEVER duplicate
│   ├── routers/            # Route handlers
│   │   ├── domains/        # Domain aggregators (admin, sales, customers, agents, compliance, analytics, webhooks, deprecated)
│   │   └── *.py            # Individual routers
│   ├── middleware/         # HTTP middleware stack
│   ├── security/           # Auth, rate limiting, API keys
│   └── schemas/            # Pydantic schemas
├── frontend/               # Frontend team — CANONICAL Next.js app
│   ├── src/app/            # App router pages
│   │   └── [locale]/       # i18n routes
│   ├── src/components/     # React components
│   ├── src/lib/            # Utils, API client, hooks
│   └── package.json        # Single source of deps
├── apps/web/               # ⚠️ DEPRECATED — merge into frontend/ then remove
├── core/                   # Platform team — config, LLM, agents, tasks
├── dealix/                 # Product team — business logic
│   ├── commercial/         # Revenue engine
│   ├── payments/           # Moyasar integration
│   └── hermes/             # Agent registry
├── auto_client_acquisition/ # Growth team
├── autonomous_growth/      # Growth team
├── integrations/           # Integrations team
├── db/                     # Backend team — models + session
├── alembic/                # Backend team — migrations
├── scripts/                # DevOps + Founder — verification + automation
├── tests/                  # QA team — all test categories
├── docs/
│   ├── architecture/       # Tech lead — system design, API ref
│   ├── commercial/         # Founder/GTM — sales, pricing, GTM
│   ├── compliance/         # Legal/Security — PDPL, ZATCA, security
│   ├── ops/                # Operations — runbooks, deployment
│   └── transformation/     # CEO/CTO — strategy, OKRs
├── .github/workflows/      # DevOps — CI/CD
└── docker-compose*.yml     # DevOps — Docker
```

## Where to Put New Files

| What | Where | Naming |
|------|-------|--------|
| New API router | `api/routers/` | `snake_case.py` |
| New domain group | `api/routers/domains/` | `domain_name.py` |
| New middleware | `api/middleware/` | `descriptive_name.py` |
| New business module | `dealix/domain_name/` | Package per domain |
| New frontend page | `frontend/src/app/[locale]/` | Route directory |
| New component | `frontend/src/components/` | `PascalCase.tsx` |
| New test | `tests/test_*.py` | `test_domain_feature.py` |
| New script | `scripts/` | `snake_case.py` or `snake_case.sh` |
| New commercial doc | `docs/commercial/` | `UPPER_SNAKE_AR.md` |
| New compliance doc | `docs/compliance/` | `UPPER_SNAKE_AR.md` |
| New runbook | `docs/ops/` | `UPPER_SNAKE_AR.md` |

## Rules

### NO DUPLICATION
1. Before creating, search: `find . -name "*similar*"`
2. If equivalent exists, update it — don't create parallel
3. Frontend pages go in `frontend/` only — never in `apps/web/`

### NO NEW NUMBERED DOC DIRECTORIES
- Existing numbered dirs (00-44) are historical
- New docs use descriptive names: `FEATURE_DESCRIPTION_AR.md`
- When in doubt, put in `docs/commercial/`, `docs/ops/`, or `docs/compliance/`

### DEPRECATION POLICY
1. Mark deprecated: `_DEPRECATED_` prefix in filename
2. Document migration path in commit message
3. Remove after 30 days if no objections

### NAMING CONVENTIONS
- Python: `snake_case.py`
- React: `PascalCase.tsx`
- Docs Arabic: `UPPER_SNAKE_AR.md`
- Docs English: `UPPER_SNAKE_EN.md`
- Workflows: `kebab-case.yml`
- Scripts: `snake_case.sh` / `snake_case.py`

### PR CHECKLIST FOR NEW FILES
- [ ] No duplicate of existing file
- [ ] In correct canonical folder
- [ ] Naming follows convention
- [ ] Referenced from AGENTS.md if dev-facing
- [ ] Tested or testable
- [ ] No secrets
- [ ] No overclaims without evidence

### AGENT INSTRUCTIONS (Kimi/Claude/Cursor)
1. Read `AGENTS.md` first
2. Read `docs/architecture/DEALIX_FUTURE_FILE_SYSTEM_AR.md` (this file)
3. Search before creating
4. Prefer updating existing files
5. Run `make doctor` after backend changes
6. Run `cd frontend && npm run typecheck` after frontend changes
7. Never commit `.env`, secrets, or archives
8. All changes must be merge-safe (small, reviewable)
