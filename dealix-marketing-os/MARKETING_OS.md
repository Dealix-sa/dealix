# Dealix Marketing OS — الوثيقة المعمارية الكاملة

## ما هذه الوثيقة — What This Document Is

هذه الوثيقة المرجعية لنظام Dealix 24/7 Persuasion Draft Factory. تصف كل مكون في النظام بالتفصيل: المقارنة مع Spam Machines، الـ 9 Agents، الـ Pipeline اليومي، نظام التقييم، قرارات Tier، نظام الـ Draft Factory، قواعد الإنتاج، التعلم من الردود، وتقرير الفاوندر اليومي.

This is the reference document for the Dealix 24/7 Persuasion Draft Factory. It describes every component in detail: the comparison with Spam Machines, the 9 Agents, the daily Pipeline, the scoring system, Tier decisions, Draft Factory output rules, production controls, response learning, and the daily founder report.

---

## 1. Spam Machine مقابل Persuasion Intelligence Machine

| المعيار | Spam Machine | Persuasion Intelligence Machine |
|---|---|---|
| الحجم اليومي | مئات أو آلاف رسائل | 8–20 مسودة مُخصصة |
| التخصيص | اسم الشركة فقط (mail merge) | ملاحظة تشغيلية خاصة بكل شركة |
| فهم السياق | لا يوجد | بحث موثق لكل شركة قبل كتابة أي مسودة |
| فرضية الألم | غائبة | مُصاغة بناء على بيانات قطاعية حقيقية |
| اختيار العرض | ثابت للجميع | مُختار حسب القطاع والألم والـ buyer |
| الموافقة قبل الإرسال | لا — يرسل تلقائياً | نعم — الفاوندر يوافق على كل مسودة |
| التعلم | لا يوجد | يتعلم من كل رد ويحدّث الـ playbook |
| المخاطر القانونية | عالية | مُدارة — compliance gate إلزامي |
| أثر السمعة | تراجع سريع | بناء تدريجي محكوم |
| معدل الردود المتوقع | أقل من 1% | مستهدف 3–8% على المسودات المُعتمدة |

---

## 2. الـ 9 Agents — التفصيل الكامل

### Agent 1 — Market Scanner

**الدور:** يعمل يومياً الساعة 12:00 AM لجمع قائمة شركات B2B جديدة تطابق معايير Dealix. يبحث في المصادر العامة: أدلة الأعمال، نتائج LinkedIn العامة، الأخبار التجارية، إعلانات التوظيف المفتوحة.

**المدخلات:** `config/markets.yml` — قائمة القطاعات والمناطق والكلمات المفتاحية.

**المخرجات:** قائمة شركات بالحقول: `company_name`, `sector`, `region`, `source_url`, `signal_type`, `scan_date`.

**القيود الصارمة:**
- لا أتمتة لـ LinkedIn scraping
- لا استخدام APIs خارجية مدفوعة دون إذن
- لا بيانات شخصية — أسماء شركات وقطاعات فقط

**مرجع:** [`agents/market-scanner.md`](agents/market-scanner.md)

---

### Agent 2 — Company Researcher

**الدور:** يعمل الساعة 2:00 AM على كل شركة في قائمة Market Scanner. يجمع context تشغيلي عام: حجم الشركة، طبيعة العمل، إشارات التوظيف، مشاريع معلنة، أي معلومات تشغيلية متاحة للعموم.

**المدخلات:** قائمة شركات من Market Scanner.

**المخرجات:** `company_brief` موثق لكل شركة يتضمن: القطاع، الحجم التقريبي، طبيعة العمليات، إشارات النمو، مصادر البيانات.

**شروط الإكمال:** يجب توثيق مصدر لكل معلومة. إذا لم تكتمل المعلومات الأساسية، الشركة تنتقل لـ `needs_more_research`.

**مرجع:** [`agents/company-researcher.md`](agents/company-researcher.md)

---

### Agent 3 — Pain Hypothesis

**الدور:** يعمل الساعة 4:00 AM. يقرأ الـ `company_brief` ويصيغ فرضية ألم تشغيلي محتملة — ليس تأكيداً، بل استنتاج مبني على أنماط القطاع ومعطيات الشركة.

**المدخلات:** `company_brief` + أنماط الألم حسب القطاع من `config/persuasion.yml`.

**المخرجات:** `pain_hypothesis` محدد بلغة نسبية ("غالبًا"، "في مثل هذا النوع من العمل").

**قاعدة صياغة الألم:** جملة واحدة. نسبية وليست قاطعة. مربوطة بعملية تشغيلية محددة — ليست مشكلة عامة.

**مرجع:** [`agents/pain-hypothesis.md`](agents/pain-hypothesis.md)

---

### Agent 4 — Offer Router

**الدور:** يعمل الساعة 5:00 AM. يقرأ `pain_hypothesis` + `company_brief` ويختار العرض الأنسب من `config/offers.yml`. يحدد `primary_offer` و`entry_offer` لكل شركة.

**المدخلات:** `pain_hypothesis`, `company_brief`, `config/offers.yml`.

**المخرجات:** `selected_offer` + `entry_offer` + مبرر قصير للاختيار.

**قيد صارم:** عرض واحد فقط per company per outreach sequence. لا cross-selling في المسودة الأولى.

**مرجع:** [`agents/offer-router.md`](agents/offer-router.md)

---

### Agent 5 — Buyer Mapper

**الدور:** يعمل الساعة 5:30 AM. يحدد المسمى الوظيفي الأنسب للتواصل في كل شركة بناء على القطاع والعرض المختار.

**المدخلات:** `company_brief`, `selected_offer`, `config/buyer-personas.yml`.

**المخرجات:** `buyer_title` + `buyer_persona_type` + نصيحة اللهجة.

**إذا لم يُحدد الـ buyer:** الحالة = `buyer_not_identified` — المسودة لا تُكتب حتى يُحدد.

**مرجع:** [`agents/buyer-mapper.md`](agents/buyer-mapper.md)

---

### Agent 6 — Persuasion Angle

**الدور:** يعمل الساعة 6:00 AM. يختار زاوية الإقناع الأنسب من 5 زوايا متاحة بناء على خصائص الشركة والـ buyer.

**الـ 5 زوايا:**

| الزاوية | متى تُستخدم |
|---|---|
| `pain_first` | الشركة ثقيلة العمليات مع إشارات ألم واضحة |
| `audit_first` | القطاع واضح لكن الألم غير مؤكد |
| `governance_first` | مؤسسة كبيرة أو حكومية |
| `founder_builder` | شركة متوسطة النمو |
| `executive_value` | CEO أو C-suite أو شركة قابضة |

**مرجع:** [`agents/persuasion-angle.md`](agents/persuasion-angle.md)

---

### Agent 7 — Draft Writer

**الدور:** يعمل الساعة 7:00 AM. يكتب مسودات المحتوى لكل شركة حسب Tier.

**مخرجات حسب Tier:**

| Tier | عدد المسودات | أنواع المحتوى |
|---|---|---|
| Tier A (85+) | 8 مسودات | Cold email AR + Cold email EN + Follow-up 1 AR + Follow-up 1 EN + Follow-up 2 AR + Follow-up 2 EN + LinkedIn message + Executive summary one-pager |
| Tier B (70–84) | 4 مسودات | Cold email AR + Cold email EN + Follow-up 1 AR + Follow-up 1 EN |
| Nurture (55–69) | 2 مسودات | Cold email AR + Cold email EN |

**قاعدة الطول:** Cold email = 150–220 كلمة. Follow-up = 80–120 كلمة. LinkedIn = 100–150 كلمة.

**مرجع:** [`agents/draft-writer.md`](agents/draft-writer.md)

---

### Agent 8 — Draft Quality Gate

**الدور:** يعمل الساعة 8:00 AM. يقيّم كل مسودة من 100 نقطة. يرفض ما دون 82 ويكتب نسخة مُحسّنة.

**معايير التقييم:**

| المعيار | الوزن |
|---|---|
| التخصيص — ملاحظة خاصة بالشركة | 25 |
| الصلة — الألم والعرض يتطابقان | 25 |
| الوضوح — رسالة واضحة وخطوة تالية | 15 |
| القيمة التجارية — هل يرى المستلم قيمة؟ | 15 |
| المصداقية — هل تبدو حقيقية وموثوقة؟ | 10 |
| الامتثال — خط opt-out، لا ادعاءات زائفة | 10 |

**الإجراء عند الرفض:** يكتب revised draft مرة واحدة. إذا فشل مرتين، الحالة = `manual_review_required`.

**مرجع:** [`agents/draft-quality-gate.md`](agents/draft-quality-gate.md)

---

### Agent 9 — Reply Learning Agent

**الدور:** يعمل الساعة 10:00 PM. يصنف الردود الواردة ويستخرج أنماط التعلم لتحديث الـ playbook.

**تصنيف الردود:**

| التصنيف | التعريف | الإجراء |
|---|---|---|
| `positive_meeting` | طلب اجتماع أو محادثة | إشعار فوري للفاوندر |
| `positive_interest` | اهتمام دون طلب اجتماع | وضع في nurture track |
| `soft_decline` | رفض مؤدب | أرشفة، لا متابعة |
| `hard_decline` | رفض صريح أو طلب إيقاف | إضافة لـ suppression list |
| `bounce` | رسالة مرتدة | فحص الدومين، تحديث |
| `no_reply` | لا رد بعد 7 أيام | تفعيل follow-up إذا لم يُرسل |

**مرجع:** [`agents/reply-learning-agent.md`](agents/reply-learning-agent.md)

---

## 3. Pipeline اليومي الكامل

```
00:00  →  Market Scanner
           يبحث في: أدلة الأعمال، إشارات التوظيف، الأخبار التجارية
           المخرج: 50–100 شركة جديدة في pipeline

02:00  →  Company Researcher
           يجمع company_brief لكل شركة
           المخرج: 20–40 brief مكتمل + X حالة needs_more_research

04:00  →  Pain Hypothesis Agent
           يصيغ فرضية الألم لكل brief مكتمل
           المخرج: pain_hypothesis لكل شركة

05:00  →  Offer Router
           يختار primary_offer + entry_offer
           المخرج: selected_offer per company

05:30  →  Buyer Mapper
           يحدد buyer_title + persona
           المخرج: buyer_profile per company

06:00  →  Fit Scoring (مُدمج مع Persuasion Angle)
           يحسب score من 100 ويصنف Tier
           يختار persuasion_angle
           المخرج: tier + angle per company

07:00  →  Draft Writer
           يكتب المسودات حسب Tier
           Tier A: 8 مسودات | Tier B: 4 | Nurture: 2

08:00  →  Draft Quality Gate
           يقيّم من 100، يرفض < 82، يكتب revised
           المخرج: approved_drafts في review_queue

09:00  →  Review Queue جاهزة
           الفاوندر يجد مسوداته منظمة حسب الأولوية

09:00–22:00  →  الفاوندر
               يراجع، يوافق، يرسل، يتابع المحادثات

22:00  →  Reply Learning Agent
           يصنف الردود الواردة
           يحدث patterns في playbook
           يُعد Daily Founder Marketing Report
```

---

## 4. نظام Fit Score من 100 نقطة

نظام التقييم موثق بالتفصيل في [`config/scoring.yml`](config/scoring.yml). ملخص المعايير:

| المعيار | الوزن |
|---|---|
| العمليات ثقيلة ومعقدة | 20 |
| صيانة أو أعمال ميدانية | 20 |
| تقارير دورية متكررة | 15 |
| متعدد الفروع أو المواقع | 10 |
| يمكن تحديد الـ buyer | 10 |
| إشارة نمو عامة | 10 |
| أنظمة بيانات أو API محتملة | 10 |
| تطابق خبرة الفاوندر | 5 |
| **المجموع** | **100** |

### قرارات الـ Tier

| الـ Tier | الحد الأدنى | القرار |
|---|---|---|
| **Tier A** | 85+ | مسودات كاملة — 8 قطع محتوى |
| **Tier B** | 70–84 | مسودات جيدة — 4 قطع محتوى |
| **Nurture** | 55–69 | رسالة خفيفة — 2 قطعة محتوى |
| **Archive** | أقل من 55 | لا مسودة — أرشفة |

### بوابات البحث الإلزامية

قبل كتابة أي مسودة، يجب إكمال:
- فهم الشركة `company_understood`
- تحديد القطاع `sector_identified`
- فرضية workflow `workflow_hypothesized`
- فرضية الألم `pain_hypothesized`
- تحديد الـ buyer `buyer_title_identified`
- اختيار العرض `offer_selected`
- تحديد الـ CTA `cta_defined`

إذا أي شرط ناقص: الحالة = `needs_more_research` — لا مسودة.

---

## 5. Draft Factory — 8 نسخ لكل شركة Tier A

لكل شركة تصل Tier A، يُنتج النظام:

| رقم | نوع المسودة | اللغة | الطول |
|---|---|---|---|
| 1 | Cold Email — رسالة بارد رئيسية | العربي | 150–220 كلمة |
| 2 | Cold Email — رسالة بارد رئيسية | الإنجليزي | 150–220 كلمة |
| 3 | Follow-up 1 — أول متابعة | العربي | 80–120 كلمة |
| 4 | Follow-up 1 — أول متابعة | الإنجليزي | 80–120 كلمة |
| 5 | Follow-up 2 — ثاني متابعة | العربي | 80–120 كلمة |
| 6 | Follow-up 2 — ثاني متابعة | الإنجليزي | 80–120 كلمة |
| 7 | LinkedIn Message | الإنجليزي أو العربي حسب الـ buyer | 100–150 كلمة |
| 8 | Executive One-Pager — ملخص تنفيذي للمشروع | PDF-ready, bilingual | 300–400 كلمة |

---

## 6. Production Rules — مستويات الإنتاج والإرسال

### حدود الإنتاج اليومية

النظام ينتج مسودات بلا حدود خلال الليل. الحد يطبّق على **الإرسال** فقط — ويحكمه الفاوندر.

### جدول الإرسال التدريجي (Ramp)

تفاصيل الجدول في [`config/gmail-ramp.yml`](config/gmail-ramp.yml). المبدأ:

| الأسبوع | الحد اليومي الأقصى |
|---|---|
| 1 | 20 رسالة |
| 2 | 40 رسالة |
| 3 | 80 رسالة |
| 4 | 150 رسالة |
| 5+ | 250 رسالة |

### قاعدة الأولوية

الفاوندر يرسل دائماً بالترتيب: Tier A أولاً → Tier B → Nurture.
لا يُرسل Nurture إذا لم يُراجع Tier A بالكامل.

### نافذة الإرسال المفضلة (GMT+3)

- الصباح: 8:00 – 10:00
- الظهر: 13:00 – 15:00
- تجنّب: مساء الجمعة، عطلة نهاية الأسبوع، الإجازات الرسمية السعودية

---

## 7. نظام التعلم من الردود

بعد كل دورة إرسال، يجمع Reply Learning Agent:

**ما يتتبعه النظام:**
- نوع كل رد (positive meeting / interest / decline / bounce / no-reply)
- الـ angle التي أعطت ردوداً إيجابية أكثر
- القطاعات التي تستجيب أفضل
- أنواع الـ opener التي تعمل
- الـ CTA التي تحوّل

**ما يحدّثه:**
- ترتيب أولوية الـ angles في `config/persuasion.yml`
- توصيات A/B testing للأسبوع التالي
- قائمة suppression للشركات التي رفضت

**ما لا يغيّره تلقائياً:**
- لا يغيّر قواعد الامتثال
- لا يرفع حدود الإرسال دون موافقة
- لا يعيد التواصل مع من أبدى رفضاً صريحاً

---

## 8. Daily Founder Marketing Report — تقرير الفاوندر اليومي

يُعدّ Reply Learning Agent هذا التقرير كل يوم بحلول الساعة 22:15.

### هيكل التقرير

```
DEALIX DAILY MARKETING REPORT — [Date]
========================================

1. PIPELINE TODAY
   - Companies scanned: XX
   - Research completed: XX
   - Tier A: XX | Tier B: XX | Nurture: XX | Archive: XX
   - Drafts produced: XX | Passed quality gate: XX

2. YOUR REVIEW QUEUE
   - Tier A waiting: XX drafts
   - Tier B waiting: XX drafts
   - Time estimate to review all: ~XX minutes

3. SENT TODAY
   - Emails sent: XX / [daily limit]
   - Remaining capacity: XX

4. REPLIES TODAY
   - Positive meetings: XX (NAMES)
   - Positive interest: XX
   - Soft declines: XX
   - Hard declines/opt-outs: XX
   - Bounces: XX

5. LEARNING THIS WEEK
   - Best performing angle: [angle_name]
   - Best sector response rate: [sector]
   - Recommended A/B test next week: [suggestion]

6. HEALTH CHECK
   - Domain reputation: [good/warning/issue]
   - Bounce rate: X.X%
   - Spam complaint rate: X.X%

7. TOMORROW'S PRIORITY
   - [Top 3 companies to review and send]
```

---

## وثائق ذات صلة

- [`README.md`](README.md) — دليل تشغيل النظام
- [`FOUNDER_REVIEW_RULES.md`](FOUNDER_REVIEW_RULES.md) — قواعد مراجعة الفاوندر
- [`config/scoring.yml`](config/scoring.yml) — نظام Fit Score التفصيلي
- [`config/persuasion.yml`](config/persuasion.yml) — قواعد الإقناع
- [`config/compliance.yml`](config/compliance.yml) — بوابة الامتثال
- [`../docs/05_governance_os/APPROVAL_POLICY.md`](../docs/05_governance_os/APPROVAL_POLICY.md) — سياسة الموافقات
- [`../docs/04_data_os/ALLOWED_USE_POLICY.md`](../docs/04_data_os/ALLOWED_USE_POLICY.md) — سياسة استخدام البيانات

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value*
