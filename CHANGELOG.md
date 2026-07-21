# Changelog

## Unreleased

### Added

- **Custom AI Service intake (ladder Rung 4):** new bilingual `/custom-ai` page (`frontend/src/app/[locale]/custom-ai/`) and governed endpoint `POST /api/v1/public/custom-ai-request` that records bespoke AI-project requests as leads for founder review (honeypot + consent gate + transactional confirmation).
- **Founder daily call sheet:** `scripts/dealix_call_sheet.py` turns the warm-contact list into an ICP-scored, qualified, rung-recommended bilingual call sheet — warm contacts only, manual dialing, no automation.
- **Launch master plan:** `docs/LAUNCH_MASTER_PLAN.md` — comprehensive bilingual 30/60/90 plan (objectives, website + funnel, visual identity, sales/lead engine, readiness gates, obstacles & resolutions, KPI scorecard, risk register).
- **Brand & GTM collateral:** `docs/brand/VISUAL_IDENTITY.md` (Navy + Gold guide), sector one-pagers (`docs/sectors/`), launch-week content calendar (`docs/launch/`), Custom AI proposal template (`sales/custom_ai/`), founder sales playbook (`sales/playbook/`), and first-10 warm outreach drafts (`data/templates/`).
- Tests for the new surfaces: `tests/test_custom_ai_request.py`, `tests/test_call_sheet.py`.
- Added a repository gap audit: `docs/architecture/REPO_GAP_AUDIT.md`.
- Added a production readiness checklist: `docs/ops/PRODUCTION_READINESS_CHECKLIST.md`.
- Added an environment contract checker: `scripts/check_env_contract.py`.
- Added an OpenAPI export utility: `scripts/export_openapi.py`.
- Added repository operating commands: `make env-check`, `make openapi-export`, and `make prod-verify`.

### Changed

- **Security:** upgraded `next` 15.1.3 → 15.5.19 in `frontend/` to remediate CVE-2025-66478.
- Services page "Custom AI" CTA now routes to the new `/custom-ai` intake; added a "Custom AI" link to the public site navigation.
- `dealix-pm` agent now treats the in-repo `docs/LAUNCH_MASTER_PLAN.md` as the canonical 90-day plan.
- Refreshed `README.md` to match the actual `Dealix-sa/dealix` repository and current operating workflow.
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
