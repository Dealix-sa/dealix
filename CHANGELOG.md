# Changelog

## [Unreleased] — 2026-05-24 — Holistic Founder Execution Pass

### 🎯 Strategic / Commercial
- **NEW** `docs/commercial/MARKET_INTELLIGENCE_2026_MAY_UPDATE_AR.md` — monthly executive intel brief:
  - PDPL enforcement live (48 SDAIA decisions, SAR 5M fines per breach, marketing-without-consent explicitly cited)
  - Saudi AI market sizing (Vision 2030 → $50B GDP target; Sales & Marketing AI $580M segment, fastest at 38.4% CAGR)
  - Pricing benchmark confirms Dealix's 5-rung ladder is intentionally below SAR 25K–150K market floor for SME entry
  - WhatsApp 2026 portfolio limits + explicit opt-in mandate
  - Competitive landscape: PACT Revenu (CRM only), SAP/SAS/IBM (enterprise tier), no local player combines PDPL-first + Trust Plane + Capital Asset Registry
  - 3 founder-only decisions ranked
- **UPDATED** `MARKET_INTELLIGENCE_MASTER_INDEX_AR.md` adds "Monthly Updates" section pinned to the top
- **NEW** `docs/commercial/MARKET_INTELLIGENCE_PDPL_ENFORCEMENT_2026_AR.md` (via dealix-content)
- **PDPL Pass** advanced from 1/6 → 6/6 sections complete in `FOUNDER_PDPL_COMPLIANCE_PASS_AR.md` (via dealix-content)
- **AEO objection registry** extended with 5 PDPL-enforcement-specific objections in `objection_engine_registry.yaml` (via dealix-content)

### 🛠 Operational / Data
- **NEW** `data/war_room_today.json` regenerated (15 targets) via `scripts/commercial_war_room_sync.py`
- **NEW** `data/founder_briefs/DAILY_PACK_2026-05-24.md` + `commercial_2026-05-24.md` + `commercial_value_map_2026-05-24.{json,md}` + `value_plan_2026-05-24.json` + `index.json`
- **NEW** `data/sales/war_room_ranking_2026-05-24.md` — transparent proxy ranking + schema gap flag
- **NEW** `data/sales/approval_queue/2026-05-24/SKIP_*.md` (8 files) — doctrine-correct skips: targets lack `relationship_basis`/`consent_on_file` (PDPL safety, no cold outreach)

### 🚦 Doctrine / Governance
- `FOUNDER_STRONGEST_PLAN_VERDICT` flipped FAIL → **PASS** (138/138 tasks satisfied)
- Phase 0-1 gate remains BLOCKED — gated only on real `payment_received` + `proof_pack_delivered` events (founder action, not engineering)
- **NEW** KPI-import placeholder guardrail in `scripts/apply_kpi_founder_commercial.py` (via dealix-engineer)
- **NEW** doctrine test `tests/test_no_cold_outreach_doctrine.py` asserts no send-path bypasses approval_center (via dealix-engineer)

### 📦 Delivery
- Sprint Readiness Audit `docs/delivery/SPRINT_READINESS_AUDIT_2026-05-24_AR.md` (via dealix-delivery)
- Proof Pack template TODO slots filled (via dealix-delivery)
- Retainer Eligibility Checklist `docs/delivery/RETAINER_ELIGIBILITY_CHECKLIST_AR.md` (via dealix-delivery)

### 🔒 Non-Negotiables Enforced
- No live external sends
- No scraping (warm-list only via founder-supplied consented contacts)
- No cold outreach (8/8 candidate targets correctly SKIP'd)
- No invented KPIs (CRM import file remains empty until founder fills it)
- No new features beyond Phase 0-1 unblock (no-build rule honored)

### 🔬 Web Research Sources (codified into May 2026 brief)
- Clyde & Co · Global Privacy Blog · IAPP · SDAIA · MarketsandMarkets · Vision 2030 · Trade.gov · Suffescom · Competenza · GMCS · Meta · Unifonic · PACT Revenu · Expert Market Research

### ✅ Test Suite Status (this pass)
- Canonical regression bundle: **191 passed, 1 skipped** (skip = `test_isolated_pg_event_store.py`, requires live DB — environmental)
- New tests: 11 in `tests/test_apply_kpi_founder_commercial.py` (KPI guardrail) + 3 new doctrine tests in `tests/test_no_cold_outreach_doctrine.py` (send-path gating, send-function allow-list, no-direct-provider-calls outside transports)
- `bash scripts/dealix_capability_verify.sh` → **PASS** (`DEALIX_READY=true`)
- `python3 scripts/check_alembic_single_head.py` → **PASS** (single head 013)
- `python3 scripts/founder_strongest_plan_status.py` → **PASS** (138/138)
- `python3 scripts/market_intelligence_status.py` → **PASS** (21 pillars)
- `bash scripts/revenue_os_master_verify.sh` → PARTIAL (all 14 sub-flags pass; PARTIAL driven by 21 pre-existing ruff style errors — see Honest Debt below)

### 🧾 Honest Debt (NOT addressed this pass, by design)
- **Phase 0-1 gate remains BLOCKED** — only the human founder can unblock by closing one paid 499 SAR Diagnostic (Moyasar `payment_received` + `proof_pack_delivered` events into `data/evidence_events_tracker.csv`)
- **PDPL Pass operational counter** stays at 1/6 because each item in `docs/commercial/operations/founder_pdpl_compliance_pass.yaml` requires the founder to perform the operational step (publish privacy policy, run DSAR test, attach DPA, etc.) — DOCUMENTATION is now complete (6/6), the EXECUTION is the founder's
- **CapitalAsset consent gate gap** (flagged by delivery agent): `auto_client_acquisition/capital_os/capital_ledger.py::CapitalAsset` lacks `consent_on_file` + `publication_status`; `add_asset()` does not block `public_safe` publication without signed consent letter. Fix is ~30 min engineer work BEFORE first paid Diagnostic closes
- **Sprint friction emitters not wired** (flagged by delivery): `FrictionKind.MISSING_PROOF_PACK` and `MISSING_SOURCE_PASSPORT` enums exist but no caller emits them. Fix is ~1hr engineer work
- **`scripts/register_capital_asset.py` CLI does not exist** (flagged by delivery): founder has no fast CLI to register a capital asset post-close meeting. Fix is ~1hr engineer work
- **21 pre-existing ruff style errors** across revenue_os spine (I001/RUF022/UP037/F811/W292/UP012). `ruff check --fix` is a zero-behavior-impact cleanup, deferred to a dedicated PR
- **war_room_today.json contains 15 placeholder targets** ("هدف استراتيجي N"). The `TARGET_FIELDS` schema in `dealix/commercial_ops/targeting_csv.py` does NOT carry `relationship_basis` or `consent_on_file` — flagged by sales agent as a founder schema decision
- **Cross-link gaps** flagged by content agent: `dealix/registers/sdaia_notice_log.yaml`, `dealix/registers/sdaia_contact.yaml`, `docs/sales-kit/dealix_objection_handler.md`, `docs/sales-kit/dealix_security_faq.md` — referenced but not all present; founder/engineer to confirm or migrate

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
