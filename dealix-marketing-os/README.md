# Dealix 24/7 Persuasion Draft Factory — نظام المسودات الذكي

## ما هو هذا النظام — What This System Is

### بالعربي

Dealix 24/7 Persuasion Draft Factory هو نظام يعمل طوال اليوم للبحث عن شركات B2B مناسبة في منطقة الخليج، فهم عملياتها، وكتابة مسودات تواصل مُخصصة بالكامل — جاهزة لمراجعة الفاوندر وإرسالها.

النظام **ليس** آلة spam. لا يرسل رسائل تلقائياً، ولا يتصل ببوابات WhatsApp، ولا يشغّل أي أتمتة على LinkedIn. كل مسودة تمر عبر الفاوندر قبل إرسالها.

**الهدف:** بناء محرك إقناع يفهم السوق السعودي وقطاعات الخليج بعمق، ويكتب رسائل تبدو وكأنها جاءت من شخص يعرف تفاصيل عمل الشركة — لأن النظام بالفعل درس هذه التفاصيل.

### In English

Dealix 24/7 Persuasion Draft Factory is a system that runs around the clock to research suitable B2B companies across the GCC, understand their operations, and write fully personalized outreach drafts — ready for the founder's review and sending.

The system is **not** a spam machine. It sends nothing automatically. No WhatsApp gateway automation, no LinkedIn automation, no bulk outreach. Every draft passes through the founder before it reaches any recipient.

**The goal:** Build a persuasion intelligence layer that understands the Saudi market and GCC sectors deeply enough to write messages that read as if they came from someone who studied the company — because the system actually did.

---

## الفرق الجوهري — The Core Distinction

| آلة الـ Spam | محرك الإقناع الذكي |
|---|---|
| ترسل لمئات يومياً | تكتب 8–20 مسودة مُخصصة يومياً |
| فتح بعام افتراضي | كل رسالة تبدأ بملاحظة خاصة بالشركة |
| تعد بنتائج | تعرض فرص مُثبتة بأدلة |
| تعمل بدون موافقة | كل مسودة تنتظر موافقة الفاوندر |
| تتجاهل الردود | تتعلم من كل رد وتحدّث الـ playbook |

---

## الـ 9 Agents — Nine Agents and Their Roles

| # | Agent | الدور |
|---|---|---|
| 1 | **Market Scanner** | يبحث يومياً عن شركات جديدة تطابق معايير Dealix من مصادر عامة |
| 2 | **Company Researcher** | يجمع بيانات كل شركة: القطاع، الحجم، نشاطات التوظيف، الإشارات العامة |
| 3 | **Pain Hypothesis** | يستنتج الألم التشغيلي المحتمل بناء على ما هو معروف عن الشركة والقطاع |
| 4 | **Offer Router** | يختار العرض الأنسب من catalog Dealix بناء على القطاع والألم |
| 5 | **Buyer Mapper** | يحدد المسمى الوظيفي الأنسب للتواصل في كل شركة |
| 6 | **Persuasion Angle** | يختار زاوية الإقناع الصحيحة من 5 زوايا متاحة |
| 7 | **Draft Writer** | يكتب 8 نسخ محتوى لكل شركة Tier A، 4 لـ Tier B |
| 8 | **Draft Quality Gate** | يقيّم كل مسودة من 100 ويرفض ما دون 82 |
| 9 | **Reply Learning Agent** | يصنف الردود الواردة ويحدّث الـ playbook بناء على الأنماط |

---

## Pipeline اليومي — Daily Pipeline

```
12:00 AM  →  Market Scanner يبحث عن شركات جديدة (مصادر عامة)
02:00 AM  →  Company Researcher يجمع بيانات الشركات الجديدة
04:00 AM  →  Pain Hypothesis يصيغ فرضية الألم لكل شركة
05:00 AM  →  Offer Router يختار العرض المناسب
05:30 AM  →  Buyer Mapper يحدد الـ buyer title
06:00 AM  →  Persuasion Angle يختار الزاوية
07:00 AM  →  Draft Writer يكتب المسودات
08:00 AM  →  Quality Gate يراجع ويصفّي
09:00 AM  →  Review Queue جاهزة للفاوندر
09:00 AM – 10:00 PM  →  الفاوندر يراجع، يوافق، ويرسل
10:00 PM  →  Reply Learning Agent يصنف الردود الواردة
```

---

## القاعدة الذهبية — The Golden Rule

> **النظام يبحث، يفهم، يكتب.**
> **الفاوندر يوافق، يرسل، يبيع.**

لا مسودة تصل لأحد دون أن يقرأها الفاوندر ويوافق عليها.

> **The system researches, understands, and writes.**
> **The founder approves, sends, and sells.**

No draft reaches a recipient without the founder reading and approving it.

---

## كيف تشغّل النظام — How to Run the System

### المتطلبات الأساسية

1. إعداد ملفات الـ config:
   - [`config/markets.yml`](config/markets.yml) — تعريف الأسواق والقطاعات المستهدفة
   - [`config/offers.yml`](config/offers.yml) — catalog العروض
   - [`config/scoring.yml`](config/scoring.yml) — نظام التقييم
   - [`config/persuasion.yml`](config/persuasion.yml) — قواعد الإقناع
   - [`config/gmail-ramp.yml`](config/gmail-ramp.yml) — جدول الإرسال التدريجي
   - [`config/compliance.yml`](config/compliance.yml) — بوابة الامتثال
   - [`config/buyer-personas.yml`](config/buyer-personas.yml) — personas المشترين

2. مراجعة [`FOUNDER_REVIEW_RULES.md`](FOUNDER_REVIEW_RULES.md) وحفظ قواعد المراجعة اليومية.

3. إعداد Gmail domain مع SPF + DKIM + DMARC (راجع [`config/gmail-ramp.yml`](config/gmail-ramp.yml)).

4. تشغيل agents من مجلد [`agents/`](agents/) حسب الترتيب.

### الإرسال اليومي المتوقع حسب المرحلة

| الأسبوع | الإرسال اليومي الأقصى |
|---|---|
| 1 | 20 رسالة |
| 2 | 40 رسالة |
| 3 | 80 رسالة |
| 4 | 150 رسالة |
| 5+ | 250 رسالة |

---

## مخرجات يومية متوقعة — Expected Daily Outputs

| المخرج | الكمية اليومية |
|---|---|
| شركات ممسوحة | 50–100 شركة |
| شركات مكتملة البحث | 20–40 شركة |
| Tier A (مسودات كاملة) | 5–10 شركات |
| Tier B (مسودات مختصرة) | 10–20 شركة |
| مسودات جاهزة للمراجعة | 60–120 مسودة |
| مسودات اجتازت Quality Gate | 40–90 مسودة |
| رسائل يوافق عليها الفاوندر | حسب قرار الفاوندر |

---

## بنية الملفات — File Structure

```
dealix-marketing-os/
├── README.md                    ← هذا الملف
├── MARKETING_OS.md              ← الوثيقة المعمارية الكاملة
├── FOUNDER_REVIEW_RULES.md      ← قواعد مراجعة الفاوندر
├── config/
│   ├── markets.yml              ← الأسواق والقطاعات المستهدفة
│   ├── offers.yml               ← catalog العروض
│   ├── scoring.yml              ← نظام Fit Score
│   ├── persuasion.yml           ← محرك الإقناع
│   ├── gmail-ramp.yml           ← جدول الإرسال التدريجي
│   ├── compliance.yml           ← بوابة الامتثال
│   └── buyer-personas.yml       ← personas المشترين
├── agents/
│   ├── market-scanner.md
│   ├── company-researcher.md
│   ├── pain-hypothesis.md
│   ├── offer-router.md
│   ├── buyer-mapper.md
│   ├── persuasion-angle.md
│   ├── draft-writer.md
│   ├── draft-quality-gate.md
│   └── reply-learning-agent.md
└── prompts/
    ├── market_scan.md
    ├── company_research.md
    ├── pain_hypothesis.md
    ├── offer_router.md
    ├── buyer_mapper.md
    ├── persuasion_angle.md
    ├── cold_email_draft.md
    ├── followup_draft.md
    ├── quality_gate.md
    └── reply_classifier.md
```

---

## وثائق ذات صلة — Related Documents

- [`MARKETING_OS.md`](MARKETING_OS.md) — المعمارية الكاملة للنظام
- [`FOUNDER_REVIEW_RULES.md`](FOUNDER_REVIEW_RULES.md) — ما الذي يفعله الفاوندر فقط
- [`../docs/05_governance_os/APPROVAL_POLICY.md`](../docs/05_governance_os/APPROVAL_POLICY.md) — سياسة الموافقات
- [`../docs/04_data_os/ALLOWED_USE_POLICY.md`](../docs/04_data_os/ALLOWED_USE_POLICY.md) — سياسة استخدام البيانات
- [`../docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`](../docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md) — حدود قناة WhatsApp

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value*
