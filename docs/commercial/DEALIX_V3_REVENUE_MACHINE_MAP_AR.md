# Dealix V3 — خريطة "آلة الإيراد" / Revenue Machine Map

> **الحالة:** طبقة تكامل (Integration Layer) فوق المعمارية القائمة — **ليست** حزمة موازية جديدة.
> **Status:** an integration layer over the existing architecture — **not** a new parallel package.

---

## ١) لماذا هذه الوثيقة؟ / Why this document?

الطرح الخارجي (V1 = 13 ملف، V2 = 42 ملف، V3 = حزمة جديدة) كان مبنيًّا على صورة "موقع + خطة".
الواقع في هذا الريبو **متقدّم كثيرًا**: الطبقات السبع المقترحة في V3 **منفّذة فعليًّا** كأنظمة `*_os`
محكومة ومغطّاة باختبارات. لذلك "V3" الصحيح ليس نسخ ملفات، بل:

1. **خريطة صدق** تربط كل طبقة من السبع بمكانها القانوني الحقيقي (endpoint / module / script).
2. **سدّ الفجوة الوحيدة الحقيقية**: التقاط إسناد الزيارة (UTM) عند الإدخال، داخل المسار المحكوم.
3. **سكربت تحقق** يثبت أن الطبقات موصولة فعلاً (فحص، لا وعد).

> The external "V1/V2/V3 ZIP" framing assumed a greenfield site. In reality every one of the
> seven proposed V3 layers already exists as a governed, test-backed `*_os` system. So the real
> "V3" is a **truthful map** + the one genuine micro-gap (inbound UTM attribution) + a
> **verification script** — never a duplicate scaffold.

**أمر التحقق / Verify command:**

```bash
python3 scripts/verify_v3_revenue_machine.py            # DEALIX_V3_REVENUE_MACHINE_VERDICT=PASS
python3 scripts/verify_v3_revenue_machine.py --json     # machine-readable
```

السجل المصدر / source registry: [`dealix/config/v3_revenue_machine.yaml`](../../dealix/config/v3_revenue_machine.yaml)

---

## ٢) الثوابت غير القابلة للتفاوض / Non-negotiables (enforced in code)

كل طبقة أدناه تحترم الثوابت المُنفّذة في
[`auto_client_acquisition/safe_send_gateway/doctrine.py`](../../auto_client_acquisition/safe_send_gateway/doctrine.py)
والمحميّة باختبار [`tests/test_doctrine_guardrails.py`](../../tests/test_doctrine_guardrails.py):

| الكود / code | المعنى |
| --- | --- |
| `no_cold_whatsapp` | لا واتساب بارد / أتمتة واتساب |
| `no_linkedin_automation` | لا أتمتة LinkedIn |
| `no_scraping` | لا جمع ويب غير مصرّح |
| `no_bulk_outreach` | لا تواصل جماعي بلا حوكمة |
| `no_guaranteed_sales_claims` | لا وعود مبيعات مضمونة |
| `no_fake_proof` | لا إثبات مزيّف / أرقام مخترعة |
| `external_action_requires_approval` | كل إرسال خارجي يتطلب موافقة بشرية |

بالإضافة إلى **قوانين Dealix السبعة** ([`docs/00_constitution/DEALIX_LAWS.md`](../00_constitution/DEALIX_LAWS.md)):
Proof · Capital · Governance · Productization · Retainer · Focus · Kill.

---

## ٣) الطبقات السبع → مكانها القانوني / The 7 layers → canonical homes

### الطبقة 1 — التقاط العملاء وإسناد أول لمسة / Lead Capture & First-Touch Attribution

- **API:** `POST /api/v1/leads` (المسار المحكوم الكامل: ICP + BANT + استخراج الألم + Decision Passport + مزامنة HubSpot) · `POST /api/v1/public/leads` · `POST /api/v1/public/risk-score` · `POST /api/v1/public/booking-request`
- **Backend:** [`api/routers/leads.py`](../../api/routers/leads.py) · [`api/routers/revenue_ops_autopilot.py`](../../api/routers/revenue_ops_autopilot.py) · [`dealix/revenue_ops_autopilot/orchestrator.py`](../../dealix/revenue_ops_autopilot/orchestrator.py)
- **🆕 V3:** التقاط الإسناد — [`dealix/revenue_ops_autopilot/attribution.py`](../../dealix/revenue_ops_autopilot/attribution.py) · [`frontend/src/lib/utm.ts`](../../frontend/src/lib/utm.ts) · [`frontend/src/components/analytics/AttributionTracker.tsx`](../../frontend/src/components/analytics/AttributionTracker.tsx)
- **Frontend forms:** `DiagnosticFunnelContent.tsx` · `RiskScoreFunnel.tsx`

> **ماذا أضاف V3 هنا؟** التقاط `utm_*` + معرّفات النقر + المُحيل ومسار الهبوط عند أول زيارة (localStorage)،
> وإرفاقها بالطلب وقت الإرسال. تدخل عبر `attribution` المُعقّمة (allow-list + حدّ طول) إلى **السجل المحكوم**
> نفسه — **لا** كتابة مباشرة لملف `leads.jsonl` ولا التفاف على البوابة.

### الطبقة 2 — سجل CRM مبني على الأحداث / Event-sourced CRM Ledger

- **API:** `GET /api/v1/revenue-os/catalog` · `POST /api/v1/revenue-os/signals/normalize` · `POST /api/v1/revenue-os/anti-waste/check`
- **Modules:** [`auto_client_acquisition/revenue_os/`](../../auto_client_acquisition/revenue_os/) (account_model · account_scoring · source_registry · dedupe · followup_plan) + [`auto_client_acquisition/revenue_memory/`](../../auto_client_acquisition/revenue_memory/) (event_store · projections · timeline · replay · retention)

> البديل المحكوم عن ملفات `accounts.json / opportunities.json / interactions.jsonl` المسطّحة:
> سجل أحداث حقيقي (event-sourced) مع projections وtimeline وretention.

### الطبقة 3 — بنّاء العروض / Offer Builder

- **API:** `…/api/v1/sales-os/*`
- **Modules:** [`auto_client_acquisition/sales_os/`](../../auto_client_acquisition/sales_os/) (proposal_generator · proposal_renderer · scope_renderer · decision_tree · qualification)
- **Config:** [`os/03_OFFERS.yml`](../../os/03_OFFERS.yml) (10 عروض) · [`os/15_PROPOSAL_TEMPLATE.md`](../../os/15_PROPOSAL_TEMPLATE.md)

### الطبقة 4 — محرك دراسات الحالة / Case Study Engine

- **API:** `…/api/v1/case-study-engine/*`
- **Modules:** [`auto_client_acquisition/case_study_engine/builder.py`](../../auto_client_acquisition/case_study_engine/builder.py) · [`auto_client_acquisition/proof_to_market/case_study_exporter.py`](../../auto_client_acquisition/proof_to_market/case_study_exporter.py) · [`dealix/commercial/case_study_generator.py`](../../dealix/commercial/case_study_generator.py)

> مربوط بقيمة مُتحقَّقة (Proof Law): لا دراسة حالة بأرقام مخترعة — اختبار يفرض ذلك.

### الطبقة 5 — التحليلات والمؤشرات / Analytics & KPIs

- **API:** `GET /api/v1/transformation/kpi-snapshot`
- **Modules/Scripts:** [`dealix/analytics/`](../../dealix/analytics/) · [`scripts/founder_weekly_metrics_bundle.py`](../../scripts/founder_weekly_metrics_bundle.py) · [`scripts/apply_kpi_founder_commercial.py`](../../scripts/apply_kpi_founder_commercial.py) · [`scripts/populate_kpi_baselines_platform_signals.py`](../../scripts/populate_kpi_baselines_platform_signals.py)
- **مؤشرات السلسلة:** New Leads → Qualified → Drafts → Replies → Discovery Calls → Proposals → Closed Won.

> قاعدة: **لا أرقام CRM مخترعة في الأتمتة** — تُملأ من المصدر الحقيقي (راجع `AGENTS.md`).

### الطبقة 6 — نظام تسليم العميل / Client Delivery OS

- **API:** `…/api/v1/delivery-os/*`
- **Modules:** [`auto_client_acquisition/delivery_os/`](../../auto_client_acquisition/delivery_os/) (framework · control_tower · qa_review · handoff · readiness_gates · retainer_backlog)
- **Templates:** [`os/16_CLIENT_ONBOARDING_TEMPLATE.md`](../../os/16_CLIENT_ONBOARDING_TEMPLATE.md) · [`os/17_QA_CHECKLIST.md`](../../os/17_QA_CHECKLIST.md) · [`os/18_HANDOVER_TEMPLATE.md`](../../os/18_HANDOVER_TEMPLATE.md)

### الطبقة 7 — الأمن وامتثال الدستور / Security & Doctrine Compliance

- **Enforcement:** [`auto_client_acquisition/safe_send_gateway/`](../../auto_client_acquisition/safe_send_gateway/) (doctrine + middleware) ← اختبار [`tests/test_doctrine_guardrails.py`](../../tests/test_doctrine_guardrails.py)
- **Secrets/CI:** `.gitleaks.toml` · `.secrets.baseline` · `.pre-commit-config.yaml` · workflows: `security.yml` · `codeql.yml` · `production_api_trust_smoke.yml`
- **Constitution:** [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) · [`docs/00_constitution/DEALIX_LAWS.md`](../00_constitution/DEALIX_LAWS.md)

---

## ٤) ما الذي أضافه V3 فعليًّا / What V3 actually added

| البند | الملف | النوع |
| --- | --- | --- |
| تعقيم الإسناد (allow-list + حدّ) | `dealix/revenue_ops_autopilot/attribution.py` | 🆕 backend |
| حقل `attribution` على سجل العميل | `dealix/revenue_ops_autopilot/schemas.py` | تعديل |
| ربط الإسناد بالـ orchestrator + سجل التدقيق | `dealix/revenue_ops_autopilot/orchestrator.py` | تعديل |
| قبول `attribution` في الحمولة العامة | `api/routers/revenue_ops_autopilot.py` | تعديل |
| التقاط UTM (client) | `frontend/src/lib/utm.ts` | 🆕 frontend |
| متتبّع أول لمسة (app-wide) | `frontend/src/components/analytics/AttributionTracker.tsx` | 🆕 frontend |
| ربط النماذج بالإسناد | `DiagnosticFunnelContent.tsx` · `RiskScoreFunnel.tsx` | تعديل |
| سجل الطبقات السبع | `dealix/config/v3_revenue_machine.yaml` | 🆕 registry |
| التحقق + اللقطة | `dealix/commercial_ops/v3_revenue_machine.py` | 🆕 module |
| سكربت التحقق | `scripts/verify_v3_revenue_machine.py` | 🆕 script |
| اختبارات | `tests/test_v3_attribution_capture.py` · `tests/test_v3_revenue_machine.py` | 🆕 tests |
| هذه الخريطة | `docs/commercial/DEALIX_V3_REVENUE_MACHINE_MAP_AR.md` | 🆕 doc |

> الباقي (CRM ledger, offer builder, case studies, KPIs, delivery, security) **كان موجودًا**؛
> دور V3 توثيقه وربطه والتحقق منه — لا إعادة بنائه.

---

## ٥) معادلة آلة الإيراد / The Revenue Machine equation

```
lead in  →  سجِّله (governed record + attribution)  →  قيّمه (lead_score/stage)
         →  أعطِ next action  →  ابنِ offer  →  قِس KPI  →  جهّز التسليم
```

كلها موصولة وقابلة للتحقق عبر `scripts/verify_v3_revenue_machine.py`.
All wired and verifiable — a check, not a promise.
