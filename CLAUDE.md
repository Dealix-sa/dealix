# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.
This file is the canonical reference for **architecture, conventions, and hard
guardrails**. For Cursor-cloud operational command lists see `AGENTS.md`.

---

## 1. What Dealix is

**Dealix** is a Saudi B2B Revenue Engine — an AI-driven revenue, growth, and
compliance platform for Saudi Arabian enterprises. It is **not** a CRM, **not** a
chatbot, **not** a sales-automation tool.

Three layers:

1. **Lead Engine** — acquire Saudi B2B leads, enrich them, score against ICP,
   suppress duplicates. PDPL-compliant by design (lawful basis, consent, opt-out).
2. **Service Engine** — productized AI services exposed under `/api/v1/...`.
3. **Trust Engine** — PDPL Art. 5/13/14/18/21 wiring, ZATCA Phase 2 e-invoicing,
   decision audit trail. This is the defensible moat.

**Stack:** Python 3.11/3.12 · FastAPI 0.115 · Pydantic v2 + pydantic-settings ·
SQLAlchemy 2.0 async · PostgreSQL 16 (+ pgvector) · Redis 7 · Alembic · Next.js 15
frontend. Deploys on Railway via Docker.

The codebase is **Arabic-first bilingual** — Arabic is the primary business
language; English is secondary. Arabic text in code/docstrings is expected (ruff
`RUF001/2/3` are intentionally disabled).

---

## 2. The Prime Operating Rule

> **AI explores, analyzes, and recommends.**
> **Deterministic workflows execute.**
> **Humans approve critical moves.**

No agent makes an external commitment on its own. No critical output leaves the
system without being **structured, evidence-backed, policy-evaluated**, and (where
required) **human-approved**. Treat this as a hard architectural invariant — do not
write code that lets an agent send, commit, or publish without passing the Trust
Plane.

---

## 3. THE 11 NON-NEGOTIABLES — read this first

These are binding rules enforced in code by passing tests. **If any user request or
in-progress work violates one, refuse and propose a safe alternative. Never improvise
around them.**

1. **No scraping systems.**
2. **No cold WhatsApp automation.**
3. **No LinkedIn automation.**
4. **No fake / un-sourced claims.**
5. **No guaranteed sales outcomes.** (No "guarantee" language in customer-facing copy.)
6. **No PII in logs.**
7. **No source-less knowledge answers.**
8. **No external action without approval.**
9. **No agent without identity.**
10. **No project without Proof Pack.**
11. **No project without Capital Asset.**

**Where they are enforced:**

- `auto_client_acquisition/safe_send_gateway/doctrine.py` —
  `enforce_doctrine_non_negotiables()` raises `ValueError` on violation (checks
  scraping, cold WhatsApp, LinkedIn automation, bulk outreach, guaranteed-sales
  claims, fake proof, external-send-without-approval flags).
- `dealix/commercial_ops/doctrine.py` — `NON_NEGOTIABLE_RULES` (bilingual AR/EN)
  plus the **SOAEN checklist** (Source · Owner · Approval · Evidence · Next Action).
- `tests/test_doctrine_guardrails.py` — verifies clean inputs pass and every
  violation flag is caught. This test must stay green.
- `dealix/masters/constitution.md` — the canonical doctrine document the 11 rules
  derive from (Articles on classifications, external commitments, no-overclaim).

The doctrine verifier has been hardened repeatedly (negation handling,
word-order, base-form "guarantee" detection). If you touch doctrine code, run
`tests/test_doctrine_guardrails.py` and expect strict matching.

Also hardcoded: the **`NEVER_AUTO_EXECUTE`** list (pricing commits, contract
changes, NDAs, payment terms, regulator comms, sensitive data exports) — these
**cannot** bypass human approval regardless of any other signal.

---

## 4. The five mandatory planes

Every feature lives in exactly one plane. Crossing planes happens via **contracts**,
never via shared memory or direct cross-plane calls.

| Plane | Responsibility | Owns |
|---|---|---|
| **Decision** | Agents: reasoning, synthesis, recommendation, evidence assembly | `auto_client_acquisition/`, `autonomous_growth/`, `core/agents/` |
| **Execution** | Durable workflows, retries, compensation, external commitments | `auto_client_acquisition/pipeline.py`, `dealix/execution/` |
| **Trust** | Policy, approval, audit, tool verification, evidence packs | `dealix/trust/` |
| **Data** | Operational source of truth, metrics, lineage | `db/`, `integrations/` |
| **Operating** | Repo governance, CI/CD, releases, SDLC security | `.github/`, `Dockerfile`, `Makefile` |

---

## 5. Repository structure

```
dealix/
├── api/                      FastAPI app — entry point, routers, middleware
│   ├── main.py               App factory, router registration, lifespan hook
│   ├── routers/              161 routers; flat files + domains/ aggregators
│   │   └── domains/          8 domain aggregators (admin, sales, customers,
│   │                         agents, compliance, analytics, webhooks, deprecated)
│   ├── middleware/           AuditLog, ETag, RateLimit, RequestID, SecurityHeaders, APIKey
│   ├── schemas/              Pydantic request/response models
│   ├── security/             API-key validation, rate limiting
│   └── dependencies.py, deps.py   FastAPI DI
│
├── core/                     Shared utilities (cross-plane primitives)
│   ├── agents/               Agent base classes
│   ├── llm/                  Multi-LLM router with fallback chain
│   ├── config/               settings.py — Pydantic settings (.env loader)
│   ├── memory/, nlp/, queue/, tasks/, prompts/
│   └── logging.py, errors.py, utils.py
│
├── dealix/                   Revenue OS platform — governance & contracts core
│   ├── execution/            GovernedPipeline (wraps the acquisition pipeline)
│   ├── trust/                Trust Plane — policy.py, approval.py, audit.py,
│   │                         tool_verification.py  (NON-BYPASSABLE)
│   ├── contracts/            DecisionOutput contract + JSON schemas
│   ├── classifications/      Approval/Reversibility/Sensitivity enums + NEVER_AUTO_EXECUTE
│   ├── governance/           Policy registry, approval matrix, draft gate
│   ├── commercial_ops/       doctrine.py — NON_NEGOTIABLE_RULES + SOAEN checklist
│   ├── masters/              constitution.md + 12 master documents
│   ├── registers/            YAML registers (no_overclaim, compliance_saudi, radar)
│   ├── business_now/, transformation/, marketing_factory/, revenue_ops_autopilot/
│   ├── payments/, observability/, analytics/, reliability/, intelligence/
│   └── caching/, connectors/, config/, docs/, execution_assurance/
│
├── auto_client_acquisition/  Decision Plane — Phase 8 acquisition + the OS modules
│   ├── pipeline.py           AcquisitionPipeline (intake → ICP → pain → qualify → ...)
│   ├── data_os/ governance_os/ proof_os/ value_os/ capital_os/
│   ├── adoption_os/ friction_log/ client_os/ sales_os/   ← the 9 canonical OS modules
│   ├── safe_send_gateway/    doctrine.py — enforce_doctrine_non_negotiables()
│   └── revenue_memory/       isolated_pg_event_store.py (dedicated worker thread)
│
├── autonomous_growth/        Phase 9 growth agents + orchestrator
├── integrations/             External adapters — hubspot, whatsapp, zatca, pdpl,
│                             calendar, email, saudi_market, arabic_templates
├── platform_core/            Enterprise foundation — multi-tenant loop, RBAC, stores
│
├── db/                       Data Plane
│   ├── models.py             SQLAlchemy 2.0 async models (multi-tenant + soft-delete)
│   ├── models_revenue_events.py   Event-sourcing models
│   ├── session.py            Async session factory — get_db(), get_session(), init_db()
│   └── migrations/           ★ Canonical Alembic dir (alembic.ini script_location)
│       └── versions/         Migration revision files
│
├── scripts/                  ~180 operational scripts (mostly read-only diagnostics)
├── tests/                    507 test files — unit/, integration/, e2e/, governance/,
│                             load/, playwright/  + conftest.py
├── frontend/                 Next.js 15 dashboard (App Router, /[locale]/ routing)
├── docs/                     Architecture, ops, business, compliance docs
├── alembic/                  Legacy/secondary alembic scaffolding (not canonical)
├── migrations/               Secondary migration dir (not canonical — see db/migrations/)
└── .claude/agents/           5 Dealix sub-agent charters
```

---

## 6. The canonical OS module layout

Revenue logic is organized into **OS modules** under `auto_client_acquisition/`.
There are 9 canonical ones:

| Module | Purpose |
|---|---|
| `data_os` | Data quality scoring, PII detection, source passport, normalization |
| `governance_os` | Policy check, approval matrix, draft gate, workflow inventory (YAML + loader) |
| `proof_os` | Proof architecture, proof ledger, proof-to-market engine |
| `value_os` | Value capture, value engine, scoring |
| `capital_os` | Capital allocation / capital-asset registration |
| `adoption_os` | Client adoption readiness & tracking |
| `friction_log` | Friction detection and resolution logging |
| `client_os` | Client maturity models, success metrics |
| `sales_os` | ICP scoring, qualification, proposal generation, client-risk scoring |

**Convention:** each OS module is a flat Python package — a handful of focused
`.py` files plus `__init__.py` that exports the public API. When adding new revenue
logic, follow this pattern; do not create deep nested hierarchies.

---

## 7. Cross-cutting patterns

### GovernedPipeline — `dealix/execution/`
Wraps `auto_client_acquisition.pipeline.AcquisitionPipeline` non-invasively. It:
1. runs the underlying pipeline (pain extraction → ICP match → qualification → proposal),
2. lifts outputs into `DecisionOutput` contracts,
3. runs each `NextAction` through the `PolicyEvaluator`,
4. emits audit-log entries,
5. creates `ApprovalRequest`s for escalated actions.

Result: `GovernedPipelineResult` with `decisions`, `policy_results`,
`approval_requests`, `audit_trail`. **Use this for any Phase 8 customization** —
don't call the bare pipeline when governance is required.

### Trust Plane — `dealix/trust/` (NON-BYPASSABLE)
- `policy.py` — `PolicyEvaluator` returns `PolicyDecision` = `ALLOW` / `DENY` / `ESCALATE`.
- `approval.py` — `ApprovalCenter`, `ApprovalRequest` (TTL, multi-approver).
- `audit.py` — `AuditSink` contract; every step is audited.
- `tool_verification.py` — pre-execution tool safety checks.

### DecisionOutput contract — `dealix/contracts/decision.py`
Every critical agent output is a validated Pydantic `DecisionOutput` carrying:
- **Approval class A0–A3** — who must approve.
- **Reversibility class R0–R3** — how hard to undo.
- **Sensitivity class S0–S3** — data/impact risk.
- Evidence list, NextActions, PolicyRequirements, trace IDs.

**High-stakes validator:** A2+/R3/S3 decisions **cannot be constructed without
evidence** — a Pydantic validator enforces it. Don't try to bypass this; supply real
evidence with sources.

### No-overclaim register — `dealix/registers/no_overclaim.yaml`
Every public product claim must have a matching entry with status (`Production` /
`Partial` / `Pilot` / `Planned`) and evidence path. CI enforces this gate.

---

## 8. FastAPI app

- **Entry point:** `api/main.py` — app factory + `lifespan` async context manager.
- **Routers:** registered via 8 domain aggregators in `api/routers/domains/`
  (admin, agents, analytics, compliance, customers, deprecated, sales, webhooks)
  plus direct imports of feature routers. ~161 router files total.
- **Middleware stack** (outermost → innermost): `CORSMiddleware` →
  `SecurityHeadersMiddleware` → `RateLimitHeadersMiddleware` → `ETagMiddleware` →
  `AuditLogMiddleware` → `RequestIDMiddleware` → `APIKeyMiddleware`.
- **Lifespan:** configures logging; calls `init_db()` (`create_all`) **for dev/test
  only** — production schema is owned by Alembic.
- **Public endpoints (no auth):** `/health`, `/healthz`,
  `/api/v1/public/demo-request`, `/api/v1/pricing/plans`, `/api/v1/checkout`,
  `/api/v1/webhooks/moyasar`.
- Admin endpoints expect the `X-Admin-API-Key` header.

---

## 9. Database & migrations

- **Models:** `db/models.py` (+ `db/models_revenue_events.py` for event sourcing).
  Multi-tenant — most tables carry a `tenant_id` FK. Soft-delete via a
  `deleted_at` column; filter active rows with `.where(Model.deleted_at.is_(None))`.
- **Sessions:** `db/session.py` — `async_session_factory()`, `get_db()` (FastAPI
  dependency, auto-commit), `get_session()` (standalone context manager),
  `init_db()` (dev/test schema bootstrap only).
- **Revenue memory:** `auto_client_acquisition/revenue_memory/isolated_pg_event_store.py`
  runs a **dedicated worker thread + separate async engine** on the same
  `DATABASE_URL`. This means two async pools to the same DB when active — budget
  connections accordingly.

### Alembic single-head rule (CI gate)
- Canonical migration dir: **`db/migrations/`** (`alembic.ini` →
  `script_location = db/migrations`). Revisions live in `db/migrations/versions/`.
  (`alembic/` and root `migrations/` are non-canonical scaffolding.)
- The migration graph includes merge revisions. **CI enforces a single Alembic
  head** via `python scripts/check_alembic_single_head.py`.
- Before adding a migration, run `alembic heads`. If more than one head appears,
  create a merge revision — see `docs/ops/ALEMBIC_MIGRATION_POLICY.md`.
- Production applies migrations with `alembic upgrade head` (Railway `release`
  phase); dev/test auto-create tables on startup.

---

## 10. Development workflows

Common commands (full list in `Makefile`, run `make help`):

| Task | Command |
|---|---|
| One-time dev setup | `make setup` (dev deps + pre-commit + `.env` from template) |
| Run API (reload) | `make run` → `uvicorn api.main:app --reload` (port 8000, `/docs`) |
| Start infra | `docker compose up -d postgres redis` |
| Full stack | `make docker-up` (app + postgres + pgbouncer + redis + mongo) |
| Frontend dev | `cd frontend && npm run dev` (port 3000) |
| Full test suite | `APP_ENV=test pytest -v` (507 files, ~15–20 min) |
| Lint | `make lint` → `ruff check .` + `black --check .` |
| Auto-format | `make format` |
| Type check | `make type-check` → `mypy core auto_client_acquisition autonomous_growth integrations api` |
| Security scan | `make security` (bandit + detect-secrets) |

**Quick regression bundle** (fast feedback — same set CI runs):

```bash
APP_ENV=test pytest tests/test_pg_event_store.py tests/test_model_router.py \
  tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py \
  tests/test_isolated_pg_event_store.py tests/test_doctrine_guardrails.py \
  -q --no-cov
```

**Lint note:** ruff/black have large pre-existing drift. Lint is **not** an API
correctness gate — don't reformat unrelated files to "fix" lint. Keep your own
changes clean.

**Hello-world smoke test** — submit a lead through the governed pipeline:

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"company":"Test Co","name":"Test","email":"test@example.sa",
       "phone":"+966501234567","sector":"technology","region":"Saudi Arabia",
       "budget":50000,"message":"Test message"}'
```

---

## 11. Conventions

- **Python:** start modules with `from __future__ import annotations`. Target 3.11.
  ruff line-length 100; ruff lint selects E/W/F/I/B/C4/UP/N/S/SIM/RUF (see
  `pyproject.toml` for the intentional ignore list — Arabic-unicode rules are off).
- **Bilingual:** docstrings and customer-facing strings are AR + EN. Arabic is the
  primary business language; do not strip or "fix" Arabic text.
- **Config:** `.env`-only via Pydantic settings (`core/config/settings.py`). Every
  secret is a `SecretStr`. Never hardcode secrets; never log PII (non-negotiable #6).
  `DATABASE_URL` auto-normalizes `postgres://` → `postgresql+asyncpg://`.
- **Environment flag:** `ENVIRONMENT` / `APP_ENV` ∈ `development | staging |
  production | test`. Keep `development` locally; tests force `APP_ENV=test`.
- **Tests:** files `test_*.py`, classes `Test*`, functions `test_*`.
  `asyncio_mode = "auto"` (no need to mark async tests). Markers: `unit`,
  `integration`, `slow`, `llm`. `tests/conftest.py` provides `mock_router`,
  `mock_llm_response`, `async_client`, and sample lead payloads — LLM calls are
  mocked by default; don't make real LLM calls in tests.
- **Optional dependencies:** the app degrades gracefully when env keys are missing.
  Optional imports use `try/except` (hence `F401` is ignored). Keep that pattern.
- **No-overclaim:** any new public claim needs a `no_overclaim.yaml` entry.

---

## 12. CI gates that must pass

`.github/workflows/ci.yml` (runs on push/PR to `main`) — **blocking gates**:

1. **Compile check** — `python3 -m compileall api auto_client_acquisition`.
2. **Alembic single head** — `scripts/check_alembic_single_head.py`.
3. **Service Readiness Matrix verify** — `scripts/verify_service_readiness_matrix.py`
   (blocks fake "Live" status + forbidden marketing claims).
4. **Quick regression bundle** — the pytest set above.
5. **Service Readiness JSON export** — regenerates
   `landing/assets/data/service-readiness.json`; CI fails if committed JSON is stale
   (`git diff --exit-code`).
6. **SEO audit** — `scripts/seo_audit.py`; fails if `docs/SEO_AUDIT_REPORT.json` is
   stale or required-gap ≠ 0.
7. **Tests with coverage gate.**

If you change the service-readiness YAML or SEO inputs, **re-run the export scripts
and commit the regenerated JSON** or CI will fail on drift.

There are 38 workflow files total (`codeql.yml`, `playwright_smoke.yml`,
`railway_deploy.yml`, plus many scheduled founder/ops jobs). `ci.yml` is the one
that gates code PRs.

**Pre-commit hooks** (`.pre-commit-config.yaml`): trailing-whitespace,
end-of-file-fixer, check-yaml/json, check-large-files, check-merge-conflict, `ruff`
+ `ruff-format`, `mypy`, `bandit`, `gitleaks`, plus local hooks
`verify-service-readiness-matrix` and `export-service-readiness-json`. Install with
`make pre-commit-install`. Do not bypass hooks with `--no-verify`.

---

## 13. Sub-agents available

Five Dealix sub-agents are defined in `.claude/agents/` — use them when the task fits:

| Agent | Use for |
|---|---|
| `dealix-engineer` | Python code, FastAPI routers, tests, DB migrations, cron scripts |
| `dealix-delivery` | The 7-day Revenue Intelligence Sprint per customer (Source Passport → DQ → scoring → draft → governance review → Proof Pack → capital asset). Never sends external messages |
| `dealix-sales` | Lead qualification, proposal rendering, warm-list outreach drafts. Queues drafts for founder approval — never sends |
| `dealix-pm` | Single point of accountability for the 90-day commercial activation plan; coordinates the other agents |
| `dealix-content` | Bilingual AR+EN docs, SOPs, case studies, templates, LinkedIn posts. Never writes code |

All sub-agents honor the 11 non-negotiables and never send external communications.

---

## 14. Deployment

- **Platform:** Railway, Docker-based. Any Docker-capable host works (see
  `DEPLOYMENT.md`).
- **`Procfile`:** `release: alembic upgrade head || true` ·
  `web: uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 2`.
- **`railway.json` / `railway.toml`:** Dockerfile builder, healthcheck `/healthz`
  (300s), predeploy `scripts/railway_predeploy.sh`, restart ON_FAILURE max 3.
- **Production env minimums:** `APP_SECRET_KEY`, `DATABASE_URL`, Moyasar keys when
  billing is enabled (see `DEPLOYMENT.md` / `docs/ops/PRODUCTION_ENV_TEMPLATE.md`).
- **Never enable auto external sends in any environment.** WhatsApp/LinkedIn live
  sends stay disabled; the system only queues drafts for human approval.

---

## 15. Known-resolved gotchas — do NOT re-diagnose as bugs

- **`api/.../auth.py` 204 + logout:** `/logout` and `/logout/all` use
  `response_model=None` deliberately (FastAPI 0.115.x). Correct as-is.
- **`api/middleware/http_stack.py`:** server-fingerprint removal uses
  `del response.headers[key]` — `.pop()` is not available on `MutableHeaders`.
  Correct as-is.
- **`frontend/src/lib/`:** `utils.ts`, `hooks/useAuth.tsx`, `api.ts` exist. The
  root `.gitignore` has a Python `lib/` pattern that can block them — use
  `git add -f` if needed. Not a missing-file bug.
- **ruff/black drift:** large and pre-existing; not an API correctness gate.

---

## 16. Key files & docs index

| Topic | Path |
|---|---|
| Cursor-cloud operational commands | `AGENTS.md` |
| Project overview | `README.md` / `README.ar.md` |
| Binding doctrine | `dealix/masters/constitution.md` |
| 12 master documents | `dealix/masters/` + `dealix/registers/` |
| API map | `docs/architecture/API_MAP.md` |
| Master architecture blueprint | `docs/blueprint/master-architecture.md` |
| Alembic migration policy | `docs/ops/ALEMBIC_MIGRATION_POLICY.md` |
| Provider adapters | `docs/architecture/PROVIDER_ADAPTERS.md` |
| Deployment | `DEPLOYMENT.md` |
| No-overclaim register | `dealix/registers/no_overclaim.yaml` |
| Saudi compliance register | `dealix/registers/compliance_saudi.yaml` |
| Doctrine guardrail tests | `tests/test_doctrine_guardrails.py` |

---

## Working agreement for AI assistants

- **Honor the 11 non-negotiables.** Refuse + propose a safe alternative if a request
  violates one. Never improvise around them.
- **Route critical actions through the Trust Plane.** Never let an agent send,
  commit, or publish externally without policy evaluation and (where required)
  approval.
- **Keep changes scoped.** Don't reformat unrelated files; lint drift is pre-existing.
- **Run the quick regression bundle** before reporting backend work complete.
- **After changing service-readiness/SEO inputs,** re-run the export scripts and
  commit regenerated JSON, or CI fails on drift.
- **Don't bypass hooks** (`--no-verify`) or weaken doctrine/policy checks to make a
  problem go away — fix the root cause.
