# MASTER HOLISTIC EXECUTION PLAN — Dealix (الخطة الشاملة من A إلى Z)

> الجمهور: المؤسس (CEO/CTO/COO) + الفِرَق الفرعية (Engineering / Content / Delivery / Sales) + المستثمر.
> الفرع: `claude/gracious-faraday-AYRy8` — التاريخ: 2026-05-24.
> النوع: خطة تنفيذية مرجعية موحَّدة (Master Holistic Plan). تُعتبر **العقد التشغيلي** بين الأدوار، فوق أي خطة جزئية أخرى في `docs/transformation/` أو `docs/commercial/`.

---

## 0) Executive Summary — خلاصة تنفيذية بسطر

Dealix تبيع **Governed AI Operations للقطاع السعودي B2B** — قدرة تشغيلية + إثبات قابل للتدقيق، عبر سُلَّم خماسي (Free Diagnostic → 499 Sprint → 1,500 Pack → 2,999–4,999/mo Managed Ops → 5K–25K Custom Setup) مع مسار Enterprise (25K–50K) بطيء. الهدف 90 يوماً: **8–15K SAR MRR + 30–40K SAR one-time = ~40–55K SAR تراكمي**.

**الـ 11 non-negotiables تُفرض بالكود** عبر اختبارات `tests/test_no_*.py` + `tests/test_doctrine_guardrails.py` + `tests/test_output_requires_governance_status.py` + `tests/test_proof_pack_required.py`. لا استثناء.

---

## 1) Holistic Gap Analysis — تحليل الفجوات الشمولي

### 1.1 ما هو **موجود فعلاً** (Strong)

| الطبقة | الموقع | الحالة |
|---|---|---|
| `data_os` | `auto_client_acquisition/data_os/` | ✅ source_passport + dq score + pii_classifier + dedupe + normalization |
| `governance_os` | `auto_client_acquisition/governance_os/` | ✅ approval_matrix + claim_safety + draft_gate + workflow_control_registry + runtime_decision |
| `proof_os` | `auto_client_acquisition/proof_os/` | ✅ proof_pack + proof_score (14 sections) |
| `value_os` | `auto_client_acquisition/value_os/` | ✅ value_ledger (4 tiers) + monthly_report |
| `capital_os` | `auto_client_acquisition/capital_os/` | ✅ capital_ledger + 8 asset types |
| `adoption_os` | `auto_client_acquisition/adoption_os/` | ✅ adoption_score + retainer_readiness + friction_log + client_roles |
| `friction_log` | `auto_client_acquisition/friction_log/` | ✅ emit + aggregate + sanitizer |
| `client_os` | `auto_client_acquisition/client_os/` | ✅ badges + status |
| `sales_os` | `auto_client_acquisition/sales_os/` | ✅ qualification + proposal_renderer + icp_score + decision_tree + scope_renderer |
| `delivery_os` | `auto_client_acquisition/delivery_os/` | ✅ control_tower + framework + readiness_gates + service_catalog |
| `executive_command_center` | `auto_client_acquisition/executive_command_center/` | ✅ 14 panels (builder + customer_safe_renderer) + router |
| `intelligence_os` | `auto_client_acquisition/intelligence_os/` | ✅ benchmark_engine + capability_index + capital_allocator + decision_engine + venture_signal |
| `strategy_os` | `auto_client_acquisition/strategy_os/` | ✅ ai_readiness + use_case_scoring |
| `agent_os` | `auto_client_acquisition/agent_os/` | ✅ agent_card + agent_registry + lifecycle + autonomy_levels + tool_permissions |
| `approval_center` | `auto_client_acquisition/approval_center/` | ✅ external send gating |
| `decision_passport` | `auto_client_acquisition/decision_passport/` | ✅ v2 schema |
| `case_study_engine` | `auto_client_acquisition/case_study_engine/` | ✅ builder |
| `customer_brain` | `auto_client_acquisition/customer_brain/` | ✅ context_pack + builder |
| Doctrine tests | `tests/test_no_*.py` + `tests/test_doctrine_guardrails.py` | ✅ 8 forbid + 1 guardrail |
| 117+ routers في `api/routers/` (decision_passport, executive_command_center, partnership_os, business_now, revenue_os, leads, ...) | ✅ |
| 525 ملف اختبار في `tests/` | ✅ |

### 1.2 ما هو **ناقص حقيقياً** (Gaps to Close)

| # | الفجوة | الأثر | الأولوية |
|---|---|---|---|
| G-1 | **AI Layers Orchestrator** — لا يوجد ملف واحد يربط الـ 9 طبقات (lead_scoring + account_scoring + content_generation + decision_passport + compliance_reasoning + proof_curation + customer_health + growth_signals + executive_intelligence) في pipeline واحد قابل للاستدعاء | عالٍ — تشتت | P0 |
| G-2 | **compliance_reasoning** كطبقة AI مستقلة (تفسير PDPL/ZATCA/SAMA/NCA على أي إجراء قبل تنفيذه + إرجاع reasoning chain) | عالٍ — مخاطرة قانونية | P0 |
| G-3 | **proof_curation** — منطق اختيار أفضل proof artifacts لكل عميل/قطاع/مرحلة بيع، حالياً يدوي | متوسط | P1 |
| G-4 | **growth_signals layer** — تجميع warm signals (founder-supplied فقط) + ربطها بـ account_scoring + venture_signal | متوسط | P1 |
| G-5 | **AI Layers HTTP Router** — لا توجد نقطة API موحَّدة (`/api/v1/ai-layers/...`) تكشف الـ 9 طبقات | متوسط | P1 |
| G-6 | **Master Plan AR** الحالي — أكثر من 12 خطة جزئية متفرقة بدون عقد موحَّد | عالٍ (تشتيت تنفيذي) | P0 — يُحَل بهذا الملف |
| G-7 | **Revenue Intelligence Sprint Engine** — السكربتات موجودة لكن لا يوجد orchestrator يحرك العميل من Day 1 → Day 7 تلقائياً مع حواجز الحوكمة | عالٍ — وقت المؤسس | P1 |
| G-8 | **Partnerships Orchestrator** — `partnership_os.py` موجود لكن lifecycle غير مكتمل (lead → MoU → first-deal → revenue-share) | متوسط | P1 |
| G-9 | **Executive Daily Brief** — موجود `dealix_pm_daily.py` لكن غير مدمج مع الـ 9 طبقات | متوسط | P2 |
| G-10 | **Holistic e2e smoke test** — لا يوجد اختبار e2e واحد يمر بكل الطبقات | عالٍ (ضمان جودة) | P0 |
| G-11 | **AI Layers Doctrine Card** — وثيقة واحدة تشرح كل طبقة + مدخلاتها + مخرجاتها + الحواجز | متوسط | P1 |

### 1.3 ما يجعل المنتج **قابل للبيع غداً صباحاً**

1. **Free Diagnostic مدفوع بـ AI Layer واحد** (مذكور G-1) يُنتج تقريراً بصفحتين + Proof Pack snapshot — العميل يرى القيمة قبل أن يدفع.
2. **Sprint Engine** (G-7) يُسلِّم 7-Day Revenue Intelligence Sprint بأقل من 5 ساعات من وقت المؤسس.
3. **Compliance Reasoning** (G-2) — يجيب "هل هذا الإجراء يحترم PDPL/ZATCA/SAMA/NCA؟" قبل أي قرار، مع سلسلة استدلال موثَّقة.
4. **AI Layers Router** (G-5) — يُعطي المؤسس + العميل واجهة API واحدة بدلاً من 117 router.
5. **Master Plan AR موحَّد** (G-6) — يُغلق التشتت التنفيذي.

---

## 2) الاستراتيجية التنفيذية — CEO/CTO/COO Cadence

### 2.1 CEO Cadence (أسبوعي + شهري + ربعي)

| الإيقاع | المدة | المُخرَج | المسار |
|---|---|---|---|
| Daily | 25 دقيقة | Daily Brief + 4 إجراءات | `scripts/dealix_pm_daily.py` |
| Weekly | 60 دقيقة | OKR review + KPI snapshot | `scripts/run_executive_weekly_checklist.sh` |
| Monthly | 90 دقيقة | Board pack + Value Ledger report + Capital Asset registry | `scripts/founder_weekly_metrics_bundle.py --write` |
| Quarterly | نصف يوم | OKR re-set + Doctrine review + 90-day plan rotation | RFC في `docs/transformation/rfcs/` |

### 2.2 CTO Cadence

| الإيقاع | المُخرَج |
|---|---|
| Daily | CI green على main + `tests/test_no_*.py` PASS |
| Weekly | `scripts/run_cto_weekly_anchor.sh` (12 pillar verify + commercial registry) |
| Monthly | Reliability drill log + observability contracts review |
| Quarterly | Architecture review + dependency hygiene + SLO recalibration |

### 2.3 COO Cadence

| الإيقاع | المُخرَج |
|---|---|
| Daily | Approval Center clean ≤ 24h + Friction Log sweep |
| Weekly | Delivery Control Tower + Sprint pipeline state |
| Monthly | Unit economics review (CAC, payback, NRR) |
| Quarterly | Org operating system tune-up |

### 2.4 OKRs (90-Day)

- **O1 (Revenue):** ≥ 1 paid invoice in Moyasar live mode بنهاية اليوم 30 + ≥ 5 paid customers بنهاية اليوم 90.
  - KR1: warm-list outreach generates ≥ 20 founder-approved drafts بنهاية اليوم 7.
  - KR2: ≥ 8 free diagnostics delivered with proof_pack_lite بنهاية اليوم 30.
  - KR3: ≥ 5 sprints sold بنهاية اليوم 60.
  - KR4: ≥ 1 retainer active بنهاية اليوم 90.
- **O2 (Trust):** صفر انتهاك للـ 11 non-negotiables في audit trail.
  - KR1: كل output يحمل `governance_decision`.
  - KR2: كل engagement مدفوع له Proof Pack score ≥ 70 + ≥ 1 capital asset.
  - KR3: كل external send مرَّ بالـ approval_center.
- **O3 (Capability):** بناء الـ 9 طبقات AI وربطها في orchestrator.
  - KR1: AI Layers module مكتمل + tests خضراء.
  - KR2: `/api/v1/ai-layers/...` router live.
  - KR3: e2e smoke test يمر بكل الطبقات.
- **O4 (Sovereignty):** PDPL/ZATCA/SAMA/NCA reasoning مفعَّل قبل أي إجراء خارجي.

---

## 3) الاستراتيجية التجارية — GTM, Pricing, Partnerships

### 3.1 السلَّم الخماسي (مُفصَّل)

| Rung | Offer | Price (SAR) | Lead time | What inside |
|---|---|---|---|---|
| 0 | Free AI Ops Diagnostic | 0 | 24h | تقرير صفحتين + 5 توصيات + Proof Pack lite (proof_pack/draft_only) |
| 1 | 7-Day Revenue Intelligence Sprint | 499 | 7 أيام | Source Passport + DQ score + Top 10 account scoring + 5 bilingual drafts + Proof Pack (≥ 70) + 1 capital asset |
| 2 | Data-to-Revenue Pack | 1,500 | 14 يوم | كل Sprint + PII handling + CRM import + Customer brain context_pack |
| 3 | Managed Revenue Ops | 2,999–4,999/mo | شهري | Retainer + weekly cadence + Executive Command Center access + adoption tracking |
| 4 | Custom AI Service Setup | 5,000–25,000 + 1,000/mo | 4–8 أسابيع | Custom agent + integration + governance review + 12-month retainer |
| Enterprise | AI Governance Review | 25K–50K | 6–12 أسبوع | PDPL/SAMA/NCA audit + Trust Pack + procurement response kit |

### 3.2 GTM Motions

1. **Founder-led Warm-list Outreach** (لا scraping, لا cold WhatsApp/LinkedIn). تجهيز 20 draft → founder review → external send عبر `approval_center`.
2. **LinkedIn content cadence** — منشور أسبوعي بلغتين (`docs/content/LINKEDIN_POST_NNN.md`).
3. **Sector reports** كـ trust signal (`docs/sector-reports/*.md`).
4. **Partnerships** (G-8) — وكالات تسويق B2B + متخصصو data engineering + شركاء قانونيون. revenue share 20–30%.
5. **Inbound funnel** — `/dealix-diagnostic` + `/risk-score` + `/proof-pack` + `/partners`.

### 3.3 Retention

- Adoption score ≥ 70 + retainer_readiness eligibility → upsell to Managed Ops.
- Monthly value ledger report (تلقائي عبر `value_os.monthly_report.generate`).
- Quarterly business review (QBR) — يُولِّد proof_pack + capital asset جديد.

---

## 4) البنية التقنية — Architecture, AI Layers, Observability

### 4.1 الـ OS Modules الكاملة (موجودة)

```
auto_client_acquisition/
├── data_os/              # ✅ source passport + DQ + PII + normalization
├── governance_os/        # ✅ approval matrix + claim safety + draft gate
├── proof_os/             # ✅ 14-section proof pack
├── value_os/             # ✅ 4-tier value ledger
├── capital_os/           # ✅ 8 asset types
├── adoption_os/          # ✅ score + retainer readiness + friction
├── friction_log/         # ✅ emit + aggregate + sanitize
├── client_os/            # ✅ badges + status
├── sales_os/             # ✅ qualify + proposal renderer
├── delivery_os/          # ✅ control tower + framework
├── executive_command_center/  # ✅ 14 panels
├── intelligence_os/      # ✅ benchmark + capability + decision
├── strategy_os/          # ✅ AI readiness + use case scoring
├── agent_os/             # ✅ agent card + registry + lifecycle
├── approval_center/      # ✅ external send gating
├── decision_passport/    # ✅ v2 schema
├── case_study_engine/    # ✅ builder
├── customer_brain/       # ✅ context_pack
├── compliance_os/        # ✅ rules + lawful basis
└── ... (90+ OS modules total)
```

### 4.2 الـ 9 AI Layers — التصميم الموحَّد (الجديد)

سيُبنى **module جديد** `auto_client_acquisition/ai_layers/` يربط الـ 9 طبقات في pipeline واحد قابل للاستدعاء:

```
auto_client_acquisition/ai_layers/
├── __init__.py             # public API: run_layer(name, ctx) + run_pipeline(ctx)
├── schemas.py              # LayerContext + LayerResult + governance envelope
├── lead_scoring.py         # wraps crm_v10/lead_scoring.py + config/lead_scoring.yaml
├── account_scoring.py      # wraps revenue_os/account_scoring.py
├── content_generation.py   # draft generator wrapping draft_gate + claim_safety
├── decision_passport.py    # wraps decision_passport/ builder
├── compliance_reasoning.py # NEW: PDPL/ZATCA/SAMA/NCA reasoning chain
├── proof_curation.py       # NEW: chooses best proof artifacts for context
├── customer_health.py      # wraps crm_v10/customer_health.py
├── growth_signals.py       # NEW: warm signals from founder inputs only
├── executive_intelligence.py # wraps executive_command_center/builder.py
└── orchestrator.py         # runs the full pipeline + emits governance envelope
```

كل طبقة:
1. تأخذ `LayerContext` (customer_id, payload, source_refs).
2. تنفِّذ `governance_os.decide(action="ai_layer_run", context=...)` قبل التشغيل.
3. تُرجع `LayerResult` مع `governance_decision` (المطلوب لكل output).
4. تُكتب إلى `value_os` / `friction_log` / `capital_os` حسب الحاجة.

### 4.3 Observability

- **Metrics:** `dealix/observability/cost_tracker.py` (موجود) — تتبع تكلفة كل layer.
- **Tracing:** `dealix/observability/otel.py` (موجود) — span per layer.
- **Logs:** `dealix/observability/sentry.py` (موجود) — لا PII (PDPL-safe).
- **Audit:** كل governance_decision + value event + capital asset يُكتب في JSONL store (env override: `DEALIX_*_PATH`).

### 4.4 Reliability

- **SLOs:** `docs/SLO.md` — availability 99.5%, p95 latency < 2s للـ AI layer.
- **On-call:** `docs/ON_CALL.md` — founder + designated engineer.
- **Runbooks:** `docs/SECURITY_RUNBOOK.md` + `docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md`.
- **Drills:** `docs/transformation/evidence/reliability_drill_log.template.txt` (شهري).

---

## 5) الحوكمة والامتثال — PDPL, ZATCA, SAMA, NCA

| إطار | المتطلب | المسار في الكود |
|---|---|---|
| **PDPL** | تصنيف PII قبل أي معالجة + lawful_basis لكل غرض + consent ledger | `data_os/pii_classifier.py` + `governance_os/lawful_basis.py` + `consent_table.py` |
| **ZATCA** | فاتورة e-invoice متوافقة لكل دفعة + QR code + UUID | `dealix/payments/` + Moyasar live cutover gate |
| **SAMA** | لا تخزين بيانات مالية حساسة بدون tokenization + audit trail قابل للتصدير | `auditability_os/` + `evidence_control_plane_os/` |
| **NCA** | تصنيف بيانات (عام/داخلي/سري/سري للغاية) + sovereignty (Saudi region) | `sovereignty_os/` + `compliance_saudi.yaml` |

كل قرار AI Layer يمر بـ `compliance_reasoning.py` (الجديد) الذي يُرجع:

```python
ComplianceReasoning(
    frameworks=["PDPL", "ZATCA", "SAMA", "NCA"],
    decision="ALLOW" | "REQUIRES_APPROVAL" | "BLOCK",
    chain=[...steps...],
    citations=[...source_refs...],
)
```

---

## 6) خط الإيرادات (7 Revenue Streams)

1. **Free Diagnostic** (lead gen) → conversion to Sprint.
2. **499 SAR Sprint** (transactional).
3. **1,500 SAR Pack** (transactional).
4. **2,999–4,999/mo Managed Ops** (recurring).
5. **5K–25K + 1K/mo Custom Setup** (project + retainer).
6. **25K–50K Enterprise Governance Review** (project, slow track).
7. **Partner revenue share** (20–30% on referred deals).

---

## 7) Reliability & On-Call

- **SLO targets:**
  - API availability ≥ 99.5%
  - p95 latency `/api/v1/leads` < 2s
  - p95 latency `/api/v1/ai-layers/*` < 5s
  - data loss tolerance: 0 (Postgres + JSONL backup)
- **Incident runbook:** `docs/SECURITY_RUNBOOK.md`.
- **Backups:** Railway Postgres + JSONL stores under `var/` checked-in nightly to S3 (founder action).

---

## 8) Delivery Control Tower

موجود في `auto_client_acquisition/delivery_os/control_tower.py`. تُضاف ربط مع `ai_layers/orchestrator.py` للسماح بقياس time-per-sprint.

---

## 9) Executive Command Center (lubrication)

موجود (`auto_client_acquisition/executive_command_center/` — 14 panels). سيُضاف panel رقم 15 = `ai_layers_state` يُلخِّص حالة الـ 9 طبقات لكل عميل.

---

## 10) Execution Timeline — 90 Days

### Days 0–30 (Foundation)
- ✅ AI Layers module (G-1, G-2, G-3, G-4, G-5).
- ✅ Holistic e2e test (G-10).
- ✅ AI Layers Doctrine Card (G-11).
- ✅ Master plan published (G-6 — هذا الملف).
- 5 free diagnostics delivered.
- 1 paid sprint sold + delivered.

### Days 30–60 (Activation)
- Sprint Engine (G-7) — orchestrator يحرك Day 1 → Day 7.
- Partnerships Orchestrator (G-8).
- 5 paid sprints sold.
- LinkedIn content cadence (1/week).
- 1 retainer eligible customer.

### Days 60–90 (Scale)
- 8–15K SAR MRR active.
- 30–40K SAR one-time cumulative.
- Enterprise Governance Review opportunity in pipeline.
- Wave 16 gate: ≥ 1 paid invoice + ≥ 1 Proof Pack ≥ 70 + ≥ 1 case-safe summary + 0 doctrine violations.

---

## 11) Doctrine Lock (المُحَرَّر النهائي)

**Non-negotiables (تُفرض بالاختبارات):**

1. No scraping systems.
2. No cold WhatsApp automation.
3. No LinkedIn automation.
4. No fake / un-sourced claims.
5. No guaranteed sales outcomes.
6. No PII in logs.
7. No source-less knowledge answers.
8. No external action without approval.
9. No agent without identity.
10. No project without Proof Pack.
11. No project without Capital Asset.

**Decision rules:**
- إذا الإيرادات < 25K SAR بنهاية يوم 60 → نقف عن بناء عروض جديدة، نضاعف المبيعات.
- إذا وقت المؤسس / sprint > 5 ساعات بعد العميل الخامس → نوقف بيع جديد ونحوِّل أعمال Sprint engine للأولوية.
- إذا أي non-negotiable كان سيُنتَهَك → نرفض ونقترح بديل آمن.

---

## 12) Acceptance Criteria (هذه الخطة تُعتبر منجَزة عندما)

- [x] هذا الملف يوجد في `docs/transformation/MASTER_HOLISTIC_EXECUTION_PLAN_AR.md`.
- [ ] `auto_client_acquisition/ai_layers/` module مكتمل + tests خضراء.
- [ ] `compliance_reasoning.py` + `proof_curation.py` + `growth_signals.py` موجودة.
- [ ] `api/routers/ai_layers.py` مُسجَّل في `api/main.py`.
- [ ] `tests/test_ai_layers_orchestrator.py` + `tests/test_compliance_reasoning.py` + `tests/test_proof_curation.py` + `tests/test_growth_signals.py` + `tests/test_ai_layers_e2e.py` تَمُرّ.
- [ ] AI Layers Doctrine Card في `docs/transformation/AI_LAYERS_DOCTRINE_CARD_AR.md`.
- [ ] Sprint Engine playbook في `docs/03_commercial_mvp/SPRINT_ENGINE_PLAYBOOK_AR.md`.
- [ ] Sales motion architecture في `docs/sales-kit/FOUNDER_LED_SALES_ARCHITECTURE_AR.md`.
- [ ] PR draft مفتوح على فرع `claude/gracious-faraday-AYRy8`.
- [ ] جميع doctrine guard tests خضراء.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
