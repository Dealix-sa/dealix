# Offer Router Agent — مواصفات الـ Agent

## الدور — Role

يعمل الساعة 5:00 AM. يقرأ `pain_hypothesis` + `company_brief` لكل شركة ويختار عرضاً واحداً من `config/offers.yml`. يحدد عرضاً رئيسياً `primary_offer` وعرض دخول `entry_offer`.

Runs at 5:00 AM. Reads the `pain_hypothesis` and `company_brief` for each company and selects one offer from `config/offers.yml`. Determines a `primary_offer` and an `entry_offer`.

---

## المبدأ الأساسي — Core Principle

> رسالة واحدة = عرض واحد.
> لا cross-selling في الرسالة الأولى. لا قائمة خدمات. لا تشتيت.

> One message = one offer.
> No cross-selling in the first message. No service list. No distraction.

---

## المدخلات — Inputs

- `pain_hypothesis` — الألم المستنتج وفئته
- `company_brief` — القطاع، الحجم، هيكل العمليات
- `config/offers.yml` — كامل catalog العروض مع `ideal_for` و`pain_triggers`

---

## المخرجات — Outputs

حقل `offer_selection` يُضاف إلى ملف brief:

```json
{
  "offer_selection": {
    "primary_offer": "maintenance_intelligence_os",
    "primary_offer_name_ar": "Maintenance Intelligence OS",
    "entry_offer": "agentic_ai_workflow_audit",
    "entry_offer_name_ar": "تدقيق Agentic AI Workflow",
    "routing_reason": "شركة FM + ألم SLA وتقارير الفنيين = Maintenance Intelligence OS هو الأنسب. Entry: Workflow Audit لتخفيض عائق البداية.",
    "pain_offer_match": "high",
    "alternate_offers": ["project_controls_ai_os"],
    "why_not_alternates": "لا إشارات مشاريع في brief — الـ alternate ليست ذات صلة بالسياق الحالي"
  }
}
```

---

## منطق القرار — Decision Logic

### خطوة 1: تحديد فئة الألم

من `pain_hypothesis.pain_category`، حدد أي نوع من الألم:

| فئة الألم | العروض الأنسب |
|---|---|
| `sla_gap` أو `reporting_chaos` | maintenance_intelligence_os |
| `project_visibility` أو `approval_bottleneck` | project_controls_ai_os |
| `executive_visibility_gap` | executive_ai_command_center |
| `knowledge_gap` أو `compliance_burden` | sovereign_knowledge_rag |
| `lead_leakage` أو `slow_proposals` | revenue_ai_os |
| `ai_adoption_uncertainty` أو `governance_gap` | ai_governance_adoption_pack |
| `hr_bandwidth` أو `manual_cv_screening` | hr_screening_agent |
| `pain_uncertain` أو `multiple` | agentic_ai_workflow_audit (entry only) |

### خطوة 2: تحقق من `ideal_for` في config

هل القطاع مدرج في `ideal_for` للعرض المختار؟ إذا نعم، تطابق كامل. إذا لا، إعادة النظر.

### خطوة 3: Entry Offer دائماً Workflow Audit

`agentic_ai_workflow_audit` هو الـ entry offer الافتراضي لجميع الشركات بسبب:
- سعر منخفض (499 ريال)
- تسليم سريع (7 أيام)
- يُخفض عائق القرار الأول

الاستثناء: إذا الشركة حكومية كبيرة → Entry offer يكون `ai_governance_adoption_pack` أو `sovereign_knowledge_rag`.

---

## ما يمنع اختيار عرض — Disqualifiers

| الحالة | العرض المستبعد |
|---|---|
| لا إشارات مشاريع في brief | project_controls_ai_os |
| شركة صغيرة < 50 موظف | executive_ai_command_center, sovereign_knowledge_rag |
| لا توظيف بكميات كبيرة | hr_screening_agent |
| لا عمليات ميدانية أو صيانة | maintenance_intelligence_os |
| لا بيانات على قنوات المبيعات | revenue_ai_os |

---

## قاعدة العرض الواحد — One Offer Rule

**الرسالة الأولى:** entry_offer فقط (Workflow Audit).
**الـ one-pager والـ follow-up:** primary_offer.

لا رسالة تذكر عرضين في نفس الوقت. إذا الـ buyer طلب المزيد → أنت تحدث المحادثة يدوياً.

---

## Prompt جاهز للاستخدام

```
SYSTEM: You are the Offer Router for Dealix, a B2B AI workflow company.

Your task: Given a company brief and pain hypothesis, select the single most appropriate offer from the Dealix catalog.

COMPANY BRIEF: {company_brief_json}
PAIN HYPOTHESIS: {pain_hypothesis_json}
OFFER CATALOG: {offers_yml_content}

ROUTING LOGIC:
1. Match the pain_category to the offer's pain_triggers
2. Verify the company sector matches the offer's ideal_for list
3. Apply disqualifiers (check company size, operation type, etc.)
4. Always select agentic_ai_workflow_audit as entry_offer (unless large government — then use governance pack)

OUTPUT FORMAT (JSON):
{
  "primary_offer": "offer_key",
  "primary_offer_name_ar": "Arabic name",
  "entry_offer": "offer_key",
  "entry_offer_name_ar": "Arabic name",
  "routing_reason": "one sentence explaining the selection",
  "pain_offer_match": "high/medium/low",
  "alternate_offers": ["list of considered but not selected"],
  "why_not_alternates": "brief reason"
}

RULE: Select exactly ONE primary offer. Never suggest two offers in the same outreach sequence.
```

---

## مرتبط بـ — Related

- [`agents/pain-hypothesis.md`](pain-hypothesis.md) — المرحلة السابقة
- [`agents/buyer-mapper.md`](buyer-mapper.md) — المرحلة التالية
- [`prompts/offer_router.md`](../prompts/offer_router.md) — الـ system prompt مع JSON schema
- [`config/offers.yml`](../config/offers.yml) — catalog العروض الكامل
