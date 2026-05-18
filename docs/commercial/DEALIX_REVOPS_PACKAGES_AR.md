# حزم Dealix التجارية — Revenue Operations + AI Implementation

> **🔑 مصدر التسعير الرسمي / Canonical pricing source.** المصدر الوحيد المعتمد
> للأسعار وسلم العروض هو [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
> (الدرجات 0–5). تمت مواءمة هذا الملف معه؛ عند أي تعارض، يُعتمد ملف سلم العروض.
> The single source of truth for pricing is `docs/OFFER_LADDER_AND_PRICING.md`
> (rungs 0–5). This file has been reconciled to it; on any conflict, the ladder file wins.

**المرجع الشامل لشركة التشغيل (9 أنظمة، أبواب العميل، QA، خارطة بناء):** [DEALIX_AI_OPERATING_COMPANY_AR.md](DEALIX_AI_OPERATING_COMPANY_AR.md)

**مقاييس North Star (تشغيل داخلي):** [NORTH_STAR_METRICS_AR.md](NORTH_STAR_METRICS_AR.md)

**المرجع التشغيلي (Linear):** Issue #232 — تعليق *Commercial Packaging — Realistic Dealix AI Services Model* (تفاصيل النقاش والتعديلات تبقى في Linear؛ **التسعير المعتمد** هو سلم العروض في `docs/OFFER_LADDER_AND_PRICING.md`).

## الموقف التجاري (لا تُباع كـ«AI عام»)

Dealix تُباع كـ **Software + Service + AI Operations** للشركات السعودية B2B: نرتّب البيانات، نحدّد الفرص، نجهّز مسودات آمنة، نوضّح الـ pipeline، ونخرج تقارير تنفيذية مربوطة بـ **Decision Passport** و**Proof** — وليس كاستشارة نماذج لغوية عابرة أو SaaS رخيص بدون مخرجات ملموسة.

**قواعد منتج غير قابلة للمساومة في التسويق والتسليم:**

- لا إرسال بارد (واتساب / LinkedIn automation) — مسودات وموافقة أولاً.
- لا قوائم مشتراة ولا scraping إنتاجي — وفق `source_registry` و`forbidden_sources`.
- أي «Outreach» في العروض = **Draft Pack** فقط حتى موافقة صريحة.

## سياق السوق (مراجع خارجية — لا تُنسَخ كأسعار Dealix)

- وكالات أتمتة AI: نطاقات مشاريع وريتينر واسعة عالمياً (مؤشر اتجاه السوق وليس تعادل سعر مباشر):  
  https://automatenexus.com/blog/ai-automation-agency-pricing-complete-cost-guide-2025  
- تكاليف تنفيذ CRM (Salesforce SMB كمرجع فئة):  
  https://crminfusion.com/2025/12/salesforce-implementation-cost/  
- حجم المنشآت في السعودية (سياق الطلب على التشغيل والبيانات):  
  https://www.spa.gov.sa/en/N2484191  

## الحزم المعتمدة للعرض — سلم العروض القياسي (الدرجات 0–5)

> الأسعار التالية مطابقة لـ `docs/OFFER_LADDER_AND_PRICING.md`. هذه هي الأرقام
> الوحيدة المعتمدة للعرض على العملاء.

| الدرجة | الحزمة | السعر المعتمد (ريال) | المدة المقترحة | ملخص النتيجة للعميل |
|--------|--------|----------------------:|----------------|----------------------|
| 0 | **Free AI Ops Diagnostic** | **مجاني** | فوري + مراجعة يدوية | تقرير تشخيصي صفحة واحدة + 3 أولويات + توصية الخطوة التالية |
| 1 | **7-Day Revenue Proof Sprint** | **499** (دفعة واحدة) | 7 أيام تقويمية | تقرير تشخيصي مفصل، 5 مسودات outreach، Proof Pack يوم 7، تقرير تنفيذي، خطة 30 يوم |
| 2 | **Data-to-Revenue Pack** | **1,500** (مشروع واحد) | 5–7 أيام عمل | تحليل pipeline، خريطة فرص، 10 مسودات استهداف، تقرير ROI basis، playbook مبيعات |
| 3 | **Managed Revenue Ops** | **2,999–4,999 / شهر** | مستمر | تقرير أسبوعي، ≤20 مسودة/شهر، Proof Pack شهري، KPIs، جلسة استراتيجية شهرية |
| 4 | **Executive Command Center** | **7,500–15,000 / شهر** | مستمر | تقرير يومي تنفيذي، رادار سوق، مسودات كاملة، Proof Pack، استراتيجية ربعية |
| 5 | **Agency Partner OS** | مخصص + **rev-share 15–30%** | إعداد 2–4 أسابيع | white-label محدود، تدريب الشريك، co-branded proof packs، dashboard شريك |

> ملاحظة نمط التسليم: الدرجتان 0–1 منتج مُتحقَّق منه؛ الدرجات 3–5 **بقيادة المؤسس /
> شبه-مؤتمتة** اليوم — انظر إفصاح نمط التسليم في ملف سلم العروض.

> العمل التنفيذي المخصّص الأكبر (تكاملات ERP، حوكمة بيانات على نطاق مؤسسي،
> SLA مخصّص) يُعرّف ضمن Rung 5 أو SOW منفصل ولا يُعلن سعراً ثابتاً على الموقع
> العام؛ لا يُعرض إلا مع عميل كبير وجاهزية تنفيذ مؤكدة.

---

## 0) Free AI Ops Diagnostic — مجاني

**يشمل:** مراجعة عيّنة من داتا العميل، تقييم جودة leads/accounts، 3 أولويات، Top 10 فرص أولية، تقرير تشخيصي صفحة واحدة، توصية الخطوة التالية (الترقية إلى Sprint).

**لا يشمل:** تنظيف كامل للداتا، إعداد CRM كامل، حملات، تكاملات عميقة، تنفيذ outreach، وعود ROI.

---

## 1) 7-Day Revenue Proof Sprint — 499 ريال (العرض الافتراضي للبيع الآن)

**يشمل:** تقرير تشخيصي مفصل، تحليل الـ pipeline الحالي، scoring، Top 50 مرتّبة، Top 10 إجراءات فورية، **5 مسودات** outreach جاهزة للموافقة (عربي/إنجليزي حسب الحاجة)، Proof Pack يوم 7، تقرير تنفيذي، خطة 30 يوم.

**لا يشمل:** إرسال فعلي لطرف ثالث، أتمتة LinkedIn، واتساب بارد، شراء قوائم، ضمان تحويل إيرادي رقمي إلا إذا وُثّق في SOW منفصل.

**أصول جاهزة في الريبو:**  
[عرض Markdown](OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md) · [قائمة تسليم](checklists/DELIVERY_LEAD_INTELLIGENCE_SPRINT.md) · [قالب نطاق](templates/SCOPE_SPRINT_SAR.md)

> بوابة سلم العروض (Next.js): `/ar/services` و `/en/services`

---

## 2) Data-to-Revenue Pack — 1,500 ريال

**يشمل:** تحليل pipeline كامل، خريطة فرص مرتّبة، 10 مسودات استهداف مخصّصة، تقرير ROI basis، playbook مبيعات مخصّص.

**لا يشمل:** استخراج بيانات (no scraping)، تكامل مباشر مع أنظمة CRM، ضمان تحويل إيرادي.

---

## 3) Managed Revenue Ops — 2,999–4,999 ريال / شهر

**يشمل:** تقرير أسبوعي تنفيذي، ≤20 مسودة outreach موافق عليها شهرياً، Proof Pack شهري، تقرير KPIs، جلسة استراتيجية شهرية 60 دقيقة.

**لا يشمل:** إرسال تلقائي، أكثر من 20 مسودة/شهر، استشارات قانونية، ضمان صفقات.

**نمط التسليم اليوم:** بقيادة المؤسس / شبه-مؤتمت — تشغيل يدوي شهري.

---

## 4) Executive Command Center — 7,500–15,000 ريال / شهر

**يشمل:** تقرير يومي تنفيذي، رادار سوق أسبوعي، مسودات كاملة شهرياً، Proof Pack كامل، استراتيجية نمو ربعية، وصول أولوية للمؤسس.

**متطلبات الفتح:** ≥ 3 pilots مكتملة + ≥ 1 case study موثق.

**نمط التسليم اليوم:** بقيادة المؤسس / شبه-مؤتمت.

---

## 5) Agency Partner OS — مخصص + rev-share 15–30%

للوكالات بعد إتمام ≥ 3 proof packs واتفاقية شراكة موقعة. العمل التنفيذي المخصّص
الأكبر على نطاق مؤسسي يُعرّف هنا أو ضمن SOW منفصل؛ لا يُعلن سعراً ثابتاً على
الموقع العام، ولا يُعرض إلا مع عميل كبير وجاهزية تنفيذ مؤكدة.

---

## ربط المنتج — أين يدعم الكود الحالي كل عرض؟

هذا القسم يربط **الوعود التجارية** بما هو **موجود فعلياً** في المستودع، ويحدد ما يبقى «تسليم خدمة» أو تطوير لاحقاً — **دون** استخدام تسميات داخلية (مثل إصدارات v10/v11) في واجهة العميل أو الوثائق العامة.

| عنصر تسليم في الحزم | مسار / وحدة في الريبو | ملاحظة |
|----------------------|----------------------|--------|
| استقبال ليدز + جواز قرار + جاهزية العميل | `POST /api/v1/leads`، [`api/routers/leads.py`](../../api/routers/leads.py)، [`AcquisitionPipeline`](../../auto_client_acquisition/pipeline.py) | مسار ليد واحد كامل |
| دفعة ليدز + Tier1 + dedupe في metadata | `POST /api/v1/leads/batch`، نفس الـ router | حد أقصى 50 عنصراً لكل طلب |
| سجل مصادر + سياسات تخزين | `GET /api/v1/revenue-os/catalog`، [`source_registry.py`](../../auto_client_acquisition/revenue_os/source_registry.py) | يشرح المصادر المسموحة والمحظورة |
| اكتشاف محلي (سعودي) | `POST /api/v1/leads/discover/local`، [`saudi_targeting_profile.py`](../../auto_client_acquisition/revenue_os/saudi_targeting_profile.py) | يتطلب مفاتيح خرائط حسب البيئة |
| بذرة تجريبية + استيراد CLI | [`data/seed/saudi_demo_leads.yaml`](../../data/seed/saudi_demo_leads.yaml)، [`scripts/import_seed_leads.py`](../../scripts/import_seed_leads.py) | للمعرض والتجارب فقط — بيانات وهمية |
| مكينة ليدز سعودية (تشغيل) | [`docs/ops/SAUDI_LEAD_MACHINE_AR.md`](../ops/SAUDI_LEAD_MACHINE_AR.md) | مسار التشغيل الآمن |
| تقارير أسبوعية / حزم تنفيذية | سكربتات مثل [`scripts/dealix_weekly_executive_pack.py`](../../scripts/dealix_weekly_executive_pack.py) وعائلة `dealix_*_pack` | تُضبط حسب البيئة؛ قد تتطلب تهيئة مفاتيح |
| مسودات outreach آمنة | سياسات `action_catalog` + بوابات الموافقة — لا قناة خارجية بدون موافقة | التسليم = **مسودات** في العروض القياسية |

**خارطة طريق كود (اختيارية لاحقاً):** وحدة داخلية صغيرة (مثلاً تحت `auto_client_acquisition/` أو `delivery_os/`) تجمع: استيراد CSV العميل → تشغيل dedupe/scoring عبر المسارات الحالية → توليد حزمة Markdown/PDF للتقرير — **دون** إظهار أسماء إصدارات داخلية للعميل.

---

## مسار البيع المقترج

```text
Free Diagnostic → 7-Day Revenue Proof Sprint (499) → Data-to-Revenue Pack (1,500) → Managed Revenue Ops (2,999–4,999/mo) → Executive Command Center (7,500–15,000/mo) → Agency Partner OS (rev-share)
```

## روابط داخلية

- [سلم العروض والتسعير — المصدر الرسمي](../OFFER_LADDER_AND_PRICING.md)  
- [عرض Sprint — صفحة واحدة](OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md)  
- [الخطة الرئيسية للتدشين التجاري](../COMMERCIAL_LAUNCH_MASTER_PLAN.md)  
- [نموذج التشغيل الأعظم](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md)  
- [حلقة تجارية يومية](../ops/DAILY_COMMERCIAL_LOOP_AR.md)
