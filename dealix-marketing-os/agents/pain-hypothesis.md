# Pain Hypothesis Agent — مواصفات الـ Agent

## الدور — Role

يعمل الساعة 4:00 AM. يقرأ كل `company_brief` مكتمل ويصيغ فرضية ألم تشغيلي محتملة. المهمة ليست تأكيد مشكلة — بل اقتراح ألم منطقي ومُعلَّل بناء على ما هو معروف عن الشركة وقطاعها.

Runs at 4:00 AM. Reads each completed `company_brief` and formulates a probable operational pain hypothesis. The task is not to confirm a problem exists — it is to propose a logical, reasoned pain based on what is known about the company and its sector.

---

## المبدأ الأساسي — Core Principle

> الألم فرضية، ليست حقيقة. كل صياغة تعكس هذا الفارق.

> Pain is a hypothesis, not a fact. Every formulation reflects this distinction.

لا يقول النظام "أنتم تعانون من X". يقول "في هذا النوع من العمل، التحدي الشائع هو X".

---

## المدخلات — Inputs

- `company_brief` مكتمل من Company Researcher
- `config/offers.yml` — أنماط الألم المرتبطة بكل قطاع
- `config/persuasion.yml` — أمثلة صياغة الألم المقبولة

---

## المخرجات — Outputs

حقل `pain_hypothesis` يُضاف إلى ملف brief:

```json
{
  "pain_hypothesis": {
    "primary_pain": "ربط تقارير الفنيين بمؤشرات الأداء يدوياً يستهلك وقتاً وقد يُأخر رؤية الإدارة",
    "pain_category": "operational_reporting_gap",
    "confidence": "medium",
    "reasoning": "شركة FM متعددة المواقع مع فرق ميدانية — هذا النمط يصاحبه عادة عبء تقارير يدوية",
    "sector_pattern_basis": "facilities_management",
    "specific_to_company": false,
    "language_ar": "غالبًا في شركات الصيانة المتعددة المواقع، الوقت الضائع في تجميع تقارير الفنيين وترجمتها لملخصات الإدارة هو ألم حقيقي يصعب حله بالأدوات التقليدية.",
    "language_en": "In multi-site maintenance operations, the time lost compiling technician reports into management summaries is typically a real operational constraint.",
    "avoid_saying": "لديكم مشكلة في التقارير"
  }
}
```

---

## أنواع الآلام حسب القطاع — Pain Types by Sector

### Facilities Management

| الألم | النمط | الكلمات المفتاحية |
|---|---|---|
| تقارير الفنيين غير منظمة | reporting_chaos | technician reports, work orders, inconsistent |
| اختراقات SLA تُكتشف متأخرة | sla_gap | SLA breach, reactive, late escalation |
| أعطال متكررة غير مُتتبعة | repeat_failures | recurrence, root cause, preventive |
| تقرير الإدارة يأخذ ساعات | manual_reporting | weekly report, compilation, Excel |

### Contracting / Construction

| الألم | النمط | الكلمات المفتاحية |
|---|---|---|
| تحديثات المشاريع متأخرة | project_visibility | weekly update, status report, delays |
| المخاطر تظهر متأخرة | risk_blindspot | risk register, late escalation |
| الموافقات تُعطّل التسليم | approval_bottleneck | change request, approval chain |
| بيانات متعددة الأشكال | data_fragmentation | P6, Excel, Word, multi-format |

### Oil & Gas / Energy

| الألم | النمط | الكلمات المفتاحية |
|---|---|---|
| ثقل التقارير التشغيلية | operational_reporting | shift reports, compliance reports |
| إدارة المعرفة المشتتة | knowledge_gap | procedures, SOPs, policy retrieval |
| مخاطر الامتثال | compliance_burden | HSE, regulatory, audit trail |

### B2B Services

| الألم | النمط | الكلمات المفتاحية |
|---|---|---|
| تسرب العملاء المحتملين | lead_leakage | follow-up, CRM, lost leads |
| بطء إعداد العروض | slow_proposals | proposal, quote, template |
| عدم اتساق المتابعة | followup_inconsistency | CRM discipline, pipeline |

---

## قواعد الصياغة — Formulation Rules

### ما يجب أن تتضمنه الفرضية

1. **كلمة نسبية** — "غالبًا"، "عادةً"، "في مثل هذا النوع"، "قد يكون"
2. **مرتبطة بالشركة** — ليس ألماً عاماً، بل ألم يناسب خصائص هذه الشركة تحديداً
3. **تشغيلية** — ليست ألم تقنياً، بل ألم العمليات والناس
4. **واحدة** — ألم واحد فقط، ليس قائمة مشاكل

### ما يجب تجنبه

- "أنتم تعانون من..." — يفترض ما هو غير مؤكد
- "نعلم أن شركتكم..." — ادعاء معرفة خاصة
- قائمة مشاكل — لا أكثر من ألم واحد في الرسالة الأولى
- ألم تقني بحت — "نظامكم قديم" / "بنيتكم التحتية ضعيفة"

---

## مستويات الثقة — Confidence Levels

| المستوى | التعريف | متى يُستخدم |
|---|---|---|
| `high` | الشركة تُظهر إشارات مباشرة على هذا الألم | إعلان وظيفة مرتبط مباشرة، أو ذُكر في مصدر عام |
| `medium` | الألم شائع جداً في هذا النوع من الشركات | قطاع واضح + حجم + هيكل تشغيلي يُشير للألم |
| `low` | استنتاج من قطاع فقط — بلا إشارة خاصة بالشركة | عندما لا تتوفر معلومات كافية |

إذا الثقة `low`: يُوصى بزاوية `audit_first` بدلاً من `pain_first`.

---

## Prompt جاهز للاستخدام

```
SYSTEM: You are the Pain Hypothesis Agent for Dealix.

Your task: Given a company_brief, formulate ONE operational pain hypothesis for this company.

COMPANY BRIEF: {company_brief_json}
SECTOR PAIN PATTERNS: {sector_pain_patterns_from_config}

INSTRUCTIONS:
1. Identify the company's most likely operational pain based on:
   - Their sector
   - Their company size and structure
   - Their growth signals
   - Any specific signals from the brief

2. Formulate the pain hypothesis in BOTH Arabic and English.
   - Use hedging language: "غالبًا", "في مثل هذا النوع من العمل", "usually in operations like this..."
   - Mention ONE pain only — not a list.
   - Make it operational and specific to their type of work.
   - Never say "you have a problem" — say "this type of operation often faces..."

3. Assign a confidence level: high / medium / low

OUTPUT FORMAT (JSON):
{
  "primary_pain": "brief description",
  "pain_category": "one of the sector pain types",
  "confidence": "high/medium/low",
  "reasoning": "why this pain fits this company",
  "language_ar": "Arabic formulation — ready to use in outreach",
  "language_en": "English formulation — ready to use in outreach",
  "avoid_saying": "what NOT to say about this pain"
}

NEVER: state pain as fact. NEVER: list multiple pains. NEVER: use aggressive or presumptuous framing.
```

---

## مرتبط بـ — Related

- [`agents/company-researcher.md`](company-researcher.md) — المرحلة السابقة
- [`agents/offer-router.md`](offer-router.md) — المرحلة التالية
- [`prompts/pain_hypothesis.md`](../prompts/pain_hypothesis.md) — الـ system prompt الكامل
- [`config/persuasion.yml`](../config/persuasion.yml) — قواعد صياغة الألم
