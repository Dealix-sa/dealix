# Dealix Transformation OS — وثيقة التموضع الرئيسية

> **الفكرة:** Dealix لا يبيع "بوتات" ولا "داشبوردات" منفصلة. Dealix يبني **أنظمة
> تشغيل أعمال AI-native للمؤسسات** تحوّل العمليات اليومية إلى workflows قابلة
> للقياس، مرتبطة بالمبيعات والتقارير والحوكمة وتجربة العميل والأتمتة.

هذه الطبقة **محكومة بالكامل**: كل نظام عرض حقيقي في الكتالوج الموحّد
(`auto_client_acquisition/service_catalog/registry.py`)، يمر على اختبارات الدكترين
وCI، ويُسعَّر كنطاق تقديري فقط. **ليست سايلو منفصل** — تندمج في المعمارية ذات
الطبقات الخمس عبر العقود.

---

## 1. الأنظمة العشرة ↔ service_id

| النظام | `service_id` | الإعداد (تقديري) | الشهري (تقديري) | الطبقة (A/B/C) |
|---|---|---|---|---|
| AI Business Command Center | `ai_command_center_os` | 35k–120k | 8k–35k | A + B |
| WhatsApp Revenue OS | `whatsapp_revenue_os` | 12k–45k | 3k–15k | A |
| Brand Intelligence OS | `brand_intelligence_os` | 15k–60k | 4k–18k | B |
| AI Agent Workforce OS | `ai_agent_workforce_os` | 40k–180k | 12k–60k | A + C |
| Client Experience OS | `client_experience_os` | 20k–80k | 6k–25k | B |
| Operations Automation OS | `operations_automation_os` | 25k–120k | 7k–35k | B |
| Executive Reporting OS | `executive_reporting_os` | 18k–75k | 5k–20k | A |
| Trust & AI Governance OS | `trust_governance_os` | 30k–150k | 10k–50k | C |
| Growth Engine OS | `growth_engine_os` | 25k–100k | 8k–30k | A |
| Custom Enterprise System | `custom_enterprise_system` | 100k–500k+ | 25k+ | A + B + C |

الأرقام **نطاقات تقديرية** (`is_estimate=True`) تُحدَّد بعد **جلسة تشخيص مدفوعة**؛
لا إيراد قبل `invoice_paid` (دكترين `no_revenue_before_paid`). مرجع الطبقات
A/B/C: [ENTERPRISE_OFFER_POSITIONING_AR.md](../strategic/ENTERPRISE_OFFER_POSITIONING_AR.md).

---

## 2. السلسلة الذهبية (عقد المنتج لكل نظام)

```text
إشارة → Lead → Decision Passport → إجراء معتمد → تسليم → Proof → توسعة → تعلّم
```

كل نظام تحوّل يُسلَّم عبر نفس مراحل [DELIVERY](03_enterprise_package.md):
تشخيص → نموذج أولي → بناء → Pilot مقيّد → Proof → توسعة مشروطة بالإثبات.

---

## 3. الحوكمة (غير قابلة للتجاوز)

- كل إرسال خارجي **مسودة تتطلب موافقة** — لا تنفيذ تلقائي (NO_LIVE_SEND).
- **Growth Engine OS** = مسودات معتمدة فقط: لا واتساب بارد، لا أتمتة LinkedIn،
  لا إرسال جماعي، لا scraping (الـ `hard_gates` تفرض ذلك في الكود + اختبار).
- **AI Agent Workforce OS** = وكلاء بأدوار وحدود وصلاحيات وبوابات موافقة بشرية
  للإجراءات الحساسة + سجل تدقيق.
- لا أرقام مخترعة (`no_invented_crm_kpi`)؛ كل سعر يُقرأ من الكتالوج (Article 11).
- لا "نضمن/guaranteed" في أي مكان (مفروض باختبار).

كل ذلك مفروض عبر: `tests/test_transformation_systems_catalog.py`،
`tests/test_service_catalog.py`، واختبارات الدكترين.

---

## 4. كيف يُولَّد العرض

مولّد عروض محكوم (مسودة + موافقة، بدون حفظ في قاعدة بيانات):

- الكود: `dealix/commercial/transformation_proposal.py`
- الـ API (admin-gated):
  - `POST /api/v1/commercial/transformation-proposal/generate`
  - `POST /api/v1/commercial/transformation-proposal/generate/markdown`
  - `POST /api/v1/commercial/roi/estimate` (تقدير ROI كنطاق — ليس وعدًا)
- يقرأ الأسعار من الكتالوج، يُخرج markdown ثنائي اللغة، الحالة الافتراضية
  `approval_required`، ويرفض لغة الضمان في المدخلات.

---

## 5. ملاحظة على مصفوفة الجاهزية (decoupled)

`docs/registry/SERVICE_READINESS_MATRIX.yaml` تصنيف منفصل (٣٢ قدرة) مقفول بعدد
محدد في الاختبارات. الأنظمة العشرة **لا تُضاف إليها في هذا الإصدار** عمدًا؛ مصدر
الحقيقة للعروض هو الكتالوج + خريطة الربط التجاري (`/api/v1/commercial-map`).
توسعة المصفوفة بحزمة `transformation` مُدرجة في خارطة الطريق.

---

## Executive summary (EN)

Dealix Transformation OS positions Dealix as a company that builds **AI-native
business operating systems** for enterprises — not isolated bots or dashboards.
Ten transformation systems are modeled as **governed catalog offerings** with
estimate-only price ranges, doctrine-enforced guardrails (approval-first, no cold
outreach, no automation, no scraping, no guarantees), and a governed proposal +
ROI generator that reads pricing from the canonical registry. Every system maps to
the A/B/C enterprise tiers and the golden chain. The Service Readiness Matrix is
intentionally decoupled and addressed in the roadmap.

---

## مراجع

- [ENTERPRISE_OFFER_POSITIONING_AR.md](../strategic/ENTERPRISE_OFFER_POSITIONING_AR.md)
- [DEALIX_ROLE_SERVICE_LADDER_AR.md](../strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md)
- [GTM_PLAYBOOK_SERVICE_LADDER_AR.md](../strategic/GTM_PLAYBOOK_SERVICE_LADDER_AR.md)
- [enterprise_package/](enterprise_package/) — MSA · DPA · ROI · Multi-stakeholder · Pilot · Procurement · Trust
- [TRANSFORMATION_OS_ROADMAP_AR.md](TRANSFORMATION_OS_ROADMAP_AR.md)
- `dealix/registers/no_overclaim.yaml` (claim: `transformation_os_catalog`)
