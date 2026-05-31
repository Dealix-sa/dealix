# Changelog

## Unreleased

### Added — Commercial Launch Prep (2026-05-28, branch `claude/commercial-launch-prep-a2kJT`)

- Added `docs/LAUNCH_EXECUTION_LOG.md` — append-only launch execution log.
- Added `docs/launch-evidence/2026-05-28/` — 19 raw verdict files + README index from canonical launch gates run at commit `646129d`.
- Added `frontend/.env.local.example` — frontend env contract (was missing per `verify_commercial_fe_be.py`).
- Refreshed `docs/PUBLIC_LAUNCH_CHECKLIST.md` with evidence-backed status per item (✅ proven · 🟡 partial · ⛔ blocker · ⏸ founder action).
- Captured canonical verdict: `DEALIX_OFFICIAL_LAUNCH_VERDICT=FAIL` traced to 3 surgical fixes (frontend `opsAdmin.ts` missing, `paths.py` missing 2 constants, stale-date test) — full root cause in `docs/LAUNCH_EXECUTION_LOG.md` and evidence README.
- 11 non-negotiables doctrine status: 73 passed, 2 failed (doctrine debt), 2 skipped, 1 xfailed.
- Single Alembic head confirmed at `013`.

### Added (prior unreleased)

- Added a repository gap audit: `docs/architecture/REPO_GAP_AUDIT.md`.
- Added a production readiness checklist: `docs/ops/PRODUCTION_READINESS_CHECKLIST.md`.
- Added an environment contract checker: `scripts/check_env_contract.py`.
- Added an OpenAPI export utility: `scripts/export_openapi.py`.
- Added repository operating commands: `make env-check`, `make openapi-export`, and `make prod-verify`.

### Changed

- Refreshed `README.md` to match the actual `VoXc2/dealix` repository and current operating workflow.
- Consolidated CI into a single workflow with backend and web jobs.
- CI now checks the environment template and verifies OpenAPI schema export.
- Cleaned `.env.example` to remove duplicate admin key definitions.

### Fixed

- Fixed stale README quick-start commands.
- Fixed duplicate CI workflow definitions.

---

## [3.0.0] — 2026-04-23

### ✨ Features — Dealix v3.0.0 الإطلاق الكامل

#### Phase 2 — Cost Optimization
- **Prompt caching** (Anthropic): `cache_control: ephemeral` على system prompts ≥ 1024 توكن (توفير 90%)
- **Semantic cache**: Redis-backed + multilingual MiniLM embeddings (threshold 0.95, TTL 24h)
- **Cost tracker**: Postgres `llm_calls` table + ring buffer + MODEL_PRICES
- **Smart routing** (`core/config/models.smart_route`): Groq للتصنيف، DeepSeek للكود، GLM للعربية، Gemini Flash للبحث، Anthropic للحرج
- **Batch mode** (`AcquisitionPipeline.run_batch`): asyncio.Semaphore=8 للـ≥5 عملاء

#### Phase 3 — Security
- **Rate limiting** (slowapi): leads 10/min, sales 30/min, WA 100/min, generic 60/min, global 1000/min
- **API key middleware** مع `hmac.compare_digest`
- **Webhook signatures**: HubSpot v3 + Calendly + n8n HMAC verification
- **scripts/rotate_secrets.sh**: تدوير API_KEYS / HUBSPOT_APP_SECRET / CALENDLY_WEBHOOK_SECRET / N8N_WEBHOOK_SECRET / JWT_SECRET / DEALIX_INTERNAL_TOKEN

#### Phase 4 — Observability
- **OpenTelemetry**: FastAPI + HTTPX + SQLAlchemy instrumentation + custom LLM/agent/tool spans → Langfuse
- **Sentry** مع FastApiIntegration + SqlalchemyIntegration
- `/health/deep` يفحص Postgres + Redis + LLM providers
- `/api/v1/admin/costs` يجمع الإنفاق حسب model/provider/task
- `/api/v1/admin/cache/stats`

#### Phase 5 — Integrations
- **ConnectorFacade** موحّد: timeout/retry/idempotency/policy/audit
- **EnrichSoClient** lead enrichment عبر إيميل
- **HubSpotTwoWay**: upsert_contact + handle_inbound_webhook
- **CalendlyDynamic**: create_single_use_link

#### Phase 6 — Intelligence
- **Arabic NLP**: normalize (hamza/taa/tashkeel/tatweel) + segment + is_arabic
- **Arabic sentiment** (lexicon خليجي + negator detection)
- **Intent classifier** (quote/demo/support/partnership/greeting/compliment/complaint)
- **Lead scorer** heuristic + ML-ready sklearn interface

#### Phase 7 — Dashboard
- Streamlit RTL لوحة: Overview / Leads / Approvals / Evidence / Costs / Audit
- Port 8501، يقرأ من API

#### Phase 8 — CI/CD
- **CodeQL** Python (security-and-quality queries)
- **Docker build** مع Trivy CRITICAL/HIGH + SBOM (SPDX-JSON) + GHCR
- **Release Please** لتوليد إصدارات وchangelog تلقائياً
- **Dependabot** أسبوعي (pip + github-actions + docker)
- **pre-commit**: ruff + mypy + bandit + gitleaks

#### Phase 9 — Infrastructure
- `scripts/infra/ssh_harden.sh`: port 2222 + fail2ban + UFW
- `scripts/infra/ssl_certbot.sh`: Let's Encrypt auto-renew
- `scripts/infra/backup_pg.sh`: pg_dump يومي + استبقاء 14 يوم
- `scripts/infra/uptimerobot_setup.md`
- `scripts/infra/logrotate.conf`

#### Phase 10 — Tests + Docs
- Unit tests: smart_routing، arabic_nlp، lead_scorer، sentiment، webhook_signatures (72 اختبار نجحت)
- Integration tests: connector_facade retry + policy
- docs/COST_OPTIMIZATION.md + SECURITY_GUIDE.md + DASHBOARD.md + API_REFERENCE.md + postman_collection.json

#### Phase 11 — Release
- tests/e2e/test_e2e.py (smoke ضد instance مشغّل)
- tests/load/k6_smoke.js (100 VU لـ2.5 دقيقة)
- tag v3.0.0

### Phase 1 — GitHub Cleanup (sesión سابقة)
- حذف 10 branches dependabot قديمة
- main protected (linear history, no force push, PR review, conversation resolution)
- Dependabot alerts + secret scanning + push protection مفعّلة
- tag v3.0.0 تم تعيينه

---

**Breaking changes:** لا يوجد (هذا أول إصدار رسمي public).
