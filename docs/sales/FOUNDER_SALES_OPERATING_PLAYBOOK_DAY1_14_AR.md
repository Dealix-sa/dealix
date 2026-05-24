# Founder Sales Operating Playbook — Day 1-14 (Track A)
## كتيب تشغيل المبيعات للمؤسس — أول أسبوعين

**Owner:** Bassam Assiri (bassam.m.assiri@gmail.com)
**Start date:** 2026-05-24
**End date:** 2026-06-06
**Primary goal:** أول صفقة 499 SAR مغلقة قبل يوم 14
**Secondary goals:** 3 ديمو محجوزة · 10 محادثات Discovery · 1 Proof Pack بيد العميل

---

## كيف تستخدم هذا الملف

هذا الكتيب **يَبني فوق** الأصول الموجودة ولا يستبدلها. عند تعارض، الأصل القانوني يحكم:

| إذا احتجت | افتح أولاً | هذا الملف يضيف |
|-----------|-----------|-----------------|
| ICP و closing flow | `FOUNDER_SALES_PLAYBOOK_AR.md` | تفصيل يوم-بيوم |
| الاعتراضات | `GTM_OBJECTION_MATRIX_AR.md` + `objection_engine_registry.yaml` | 15 اعتراض إضافي × 3 قطاعات |
| سكربت ديمو | `MARKET_INTELLIGENCE_DEMO_SCRIPT_AR.md` (10 دقائق) + `dealix_demo_script_30min.md` (30 دقيقة) | تفصيل لكل tier |
| التأهيل (Score 100) | `CLIENT_SELECTION_DECISION.md` + `QUALIFICATION_SCORE.md` | BANT+ Saudi questionnaire |
| الأسعار | `dealix/config/pricing.yaml` | مخطط 5 درجات للسرد فقط |
| العقد | `PILOT_AGREEMENT_DRAFT.md` + `dealix_pilot_agreement.md` | مخطط Proposal لكل Rung |
| الادعاءات | `dealix/registers/no_overclaim.yaml` | قاعدة التحقق قبل أي وعد |

**قاعدة ثابتة:** كل ادعاء عام (إيميل، عرض، LinkedIn) يجب أن يكون له `id` في `no_overclaim.yaml` بحالة `Production` أو `Partial` صريح. إذا الحالة `Planned` أو `Pilot` فلا يُذكر للعميل.

---

# Part 1 — Qualification Rubric (BANT+ Saudi)
## رُبريك التأهيل — BANT + مكوّنات سعودية

`QUALIFICATION_SCORE.md` يعطي 100 نقطة على 7 معايير. هذا القسم يحوّلها إلى **محادثة فعلية** بالأسئلة السعودية، ويُخرج tier (A/B/C/D) + Rung موصى به.

## 1.1 الأسئلة الـ 12 (5 دقائق)

اطرح بالترتيب. لا تقفز. كل سؤال له **سعر إنصات: 5 ثواني صمت بعد الإجابة**.

### Budget (الميزانية)

**Q1 — الإنفاق الحالي على المبيعات/التسويق**
> "كم تنفقون شهرياً تقريباً على CRM، أدوات المبيعات، أو الوكالة؟ ما أحتاج رقماً دقيقاً — range يكفي."

| الإجابة | الإشارة | Rung الأولي |
|---------|---------|-------------|
| أقل من 1,000 SAR/شهر | لا توجد ميزانية حقيقية | Rung 0 فقط |
| 1,000–5,000 SAR/شهر | SMB ناشئ | Rung 1 → 2 |
| 5,000–15,000 SAR/شهر | mid-market | Rung 2 → 3 |
| 15,000–50,000 SAR/شهر | جاهز للـ retainer | Rung 3 → 4 |
| +50,000 SAR/شهر | enterprise | Rung 4 → 5 |

**Q2 — قرار الإنفاق الجديد**
> "لو شفت قيمة واضحة، ميزانية 499 SAR تحتاج موافقة من حد ثاني؟ 5,000؟ 25,000؟"

→ يكشف **الحد الأقصى للإنفاق بدون تصعيد**.

### Authority (السلطة)

**Q3 — صانع القرار**
> "غيرك مين يتأثر بالقرار؟ CFO؟ COO؟ المالك؟"

| الإجابة | التصنيف |
|---------|---------|
| "أنا أقرر" + المنصب CEO/Founder/Owner | **A (مباشر)** |
| "أنا أقرر تحت 10K" | **B (محدود)** |
| "أحتاج موافقة لكل شي" | **C (gatekeeper)** |
| "أبحث للإدارة" | **D (researcher)** — لا تستثمر وقت ديمو |

**Q4 — العلاقة بـ CEO**
> "متى آخر مرة جلست مع الـ CEO/المالك حول مبيعات؟"

→ إجابة "هذا الأسبوع" = champion قوي. "ما أذكر" = إشارة خطر.

### Need (الحاجة)

**Q5 — الألم بكلماته (لا تقترح)**
> "في ٣ جمل: وش أسوأ شي يحصل في عملية المبيعات عندكم؟"

اكتب الإجابة **حرفياً**. ستستخدمها في الـ proposal الـ Executive Summary.

**Q6 — التكلفة الحالية للألم**
> "تقدر تقدّر: كم lead بيضيع كل أسبوع لأن ما حد رد بسرعة؟ ولو ضربنا في متوسط قيمة الـ deal؟"

→ الرقم هذا = **anchor للعرض**. لو ضايع 10K SAR/أسبوع، عرض 499 SAR يبدو رخيص جداً.

**Q7 — هل جرّبوا قبل**
> "جربتم AI أو أتمتة قبل؟ شنو صار؟"

| الإجابة | الإشارة |
|---------|---------|
| "ما جربنا" | خام — يحتاج تعليم أكثر |
| "جربنا وفشل" | اسأل **لماذا** فشل — هذه ذهب |
| "نستخدم ChatGPT" | tactical, not strategic — فرصة لرفع المستوى |
| "نستخدم HubSpot Breeze" | متطور — بيع تكامل لا استبدال |

### Timeline (التوقيت)

**Q8 — متى يحتاجون النتائج**
> "لو الحل المثالي جاهز اليوم، متى تبغى تبدأ تشوف نتائج؟ هذا الربع؟ الجاي؟"

| الإجابة | Tier |
|---------|------|
| "خلال أسبوعين" | A — اضغط الـ Sprint اليوم |
| "خلال الشهر" | B — Discovery + ديمو هذا الأسبوع |
| "الربع الجاي" | C — Nurture حتى Sept |
| "ما عندنا urgency" | D — لا تستثمر |

**Q9 — Trigger الحالي**
> "ليه تتكلم معاي اليوم تحديداً؟ صار شي جديد؟"

ابحث عن trigger صريح: جولة استثمارية، توسع، فقد عميل كبير، انضمام مدير جديد، تحضير ZATCA/PDPL audit.

### Saudi-specific (سعودي محدد)

**Q10 — PDPL urgency**
> "وش وضع امتثال PDPL عندكم؟ عندكم DPO معيّن؟ أو لسا ما بدأتوا؟"

| الإجابة | المعنى للبيع |
|---------|---------------|
| "عندنا DPO + DPA جاهزة" | متقدم — اربط Dealix كـ governance layer |
| "بدأنا" | فرصة compliance wedge |
| "ما بدأنا" | خاطر عالي — قدّم compliance بريف صريح |
| "PDPL إيش؟" | علّم بهدوء، لا تخوّف |

**Q11 — ZATCA readiness**
> "فواتيركم على ZATCA Phase 2؟ EGS مكامل مع CRM؟"

→ لو نعم: Dealix invoice rendering ينضم بسلاسة. لو لا: لا تتعهد بـ ZATCA حلول — اذكر `zatca_compliance` فقط إذا في `no_overclaim` بحالة Production.

**Q12 — حجم البيانات العربية**
> "كم محادثة عميل بالعربي شهرياً؟ WhatsApp تقريباً؟ بريد؟"

| المحادثات/شهر | Rung مناسب |
|----------------|------------|
| < 50 | Rung 0/1 فقط — لا يبرر retainer |
| 50–500 | Rung 1 → 2 |
| 500–5,000 | Rung 2 → 3 |
| +5,000 | Rung 3 → 4 |

## 1.2 التصنيف النهائي (Tier + Rung)

اجمع `QUALIFICATION_SCORE.md` (100) مع جواب Q1, Q3, Q8:

| Score | Authority | Timeline | **Tier** | **Rung** | **Decision** |
|-------|-----------|----------|----------|----------|--------------|
| 80+ | A | ≤ 2 أسابيع | **A1** | Rung 1 → 2 | اقفل الـ Sprint **اليوم** |
| 80+ | A/B | ≤ شهر | **A2** | Rung 1 | ديمو 30 دقيقة هذا الأسبوع |
| 60–79 | A/B | ≤ ربع | **B** | Rung 0 → 1 | Diagnostic مجاني، ثم Sprint |
| 60–79 | C | أي وقت | **C** | Rung 0 | Nurture — محتوى أسبوعي |
| 40–59 | any | any | **D** | Rung 0 | محادثة واحدة + قاعدة بيانات |
| <40 | any | any | **REJECT** | — | اعتذر بأدب، أحِل لمحتوى عام |

## 1.3 Go / No-Go Checklist

قبل أي ديمو أو عرض، تأكّد:

- [ ] أجاب على 10 من 12 سؤال على الأقل
- [ ] Score ≥ 60
- [ ] حدّد ألم بكلماته (Q5)
- [ ] Authority = A أو B
- [ ] لم يطلب أي ممنوع: cold WhatsApp · scraping · guaranteed sales · auto-send بدون موافقة
- [ ] PDPL stance واضح (Q10)
- [ ] Trigger موجود (Q9)

إذا أقل من 5 صناديق علامة، **توقف** — حوّله إلى Diagnostic مجاني أو Nurture.

---

# Part 2 — 15-Minute Discovery Call Script
## سكربت Discovery — 15 دقيقة

**الهدف:** فلترة + جدولة الديمو، لا بيع.
**القاعدة:** المؤسس يتكلم 30%، العميل 70%.

## 2.1 الجدول الزمني

| الدقائق | المرحلة | المخرج |
|---------|---------|---------|
| 0–1 | Opening | إذن للمتابعة |
| 1–11 | 7 أسئلة تأهيلية | tier + Rung |
| 11–13 | Tier-fit reflection | محاذاة |
| 13–15 | Next step + التزام | ديمو محجوزة أو رفض نظيف |

## 2.2 Opening (1 دقيقة) — عربي

> "السلام عليكم [الاسم]. شاكر للوقت. قبل أبدأ — ٣ أسئلة بسيطة عشان نقدر نوفّر وقت لكلينا:
> أول شي، عندي ١٥ دقيقة فقط الحين — هذي مكالمة تأهيل، مو ديمو. لو ناسبنا، نحجز ديمو ٣٠ دقيقة الأسبوع هذا.
> ثاني شي، أنا بسأل ٧ أسئلة، أكتب الإجابات، ما عندي شي أبيعه الحين.
> ثالث شي، ممكن نسجّل المكالمة (نص فقط) للمراجعة الداخلية؟"

**English opening:**
> "Salam [Name]. Thanks for the time. Quick framing before we start: this is a 15-min qualification call, not a demo. I'll ask 7 questions, take notes, and if there's a fit, we book a 30-min demo this week. Can I capture text notes from the call for internal review?"

## 2.3 الأسئلة السبعة (10 دقائق) — عربي

اختر **7 من 12** من Part 1 بناءً على الـ context. الإصدار القياسي:

1. **(Need)** "في ٣ جمل: وش أسوأ شي في عملية المبيعات عندكم اليوم؟"
2. **(Need quant)** "كم lead بيضيع أسبوعياً لأن ما حد رد بسرعة؟ ولو ضربنا في قيمة الـ deal؟"
3. **(Trigger)** "ليه نتكلم اليوم تحديداً؟ صار شي جديد؟"
4. **(Authority)** "غيرك مين يتأثر بالقرار؟"
5. **(Tooling)** "وش الـ stack الحالي؟ CRM؟ WhatsApp Business؟ HubSpot؟"
6. **(PDPL)** "وضع PDPL/خصوصية البيانات عندكم — DPO معيّن؟"
7. **(Timeline + Budget)** "متى تبغى تشوف نتائج، وميزانية أول خطوة — تحت 500؟ تحت 5K؟"

### English backups (للعملاء الأجانب أو ESL)

1. "In 3 sentences: what's the worst thing in your sales process today?"
2. "How many leads do you estimate slip per week from slow first-response? Avg deal value?"
3. "Why are we talking today specifically? Anything change recently?"
4. "Beyond you, who else weighs in on this decision?"
5. "What's the current stack — CRM, WhatsApp Business, HubSpot, anything?"
6. "On PDPL — do you have a DPO assigned? DPA process?"
7. "Timeline to value, and budget for the first step — sub-500 SAR? Sub-5K?"

## 2.4 Listening Grid (اكتب أثناء الإجابة)

| الإشارة | اسمعها في… |
|---------|------------|
| **Pain magnitude** | Q1, Q2 — يستخدم أرقام؟ يحدد تكلفة؟ |
| **Urgency triggers** | Q3 — جولة؟ مدير جديد؟ فقد عميل؟ |
| **Tooling maturity** | Q5 — يفرّق بين CRM و WhatsApp Business؟ |
| **Budget anchors** | Q7 — يستجيب لـ 5K بدون انكماش؟ |
| **Decision speed** | Q4 + Q7 — قال "أنا أقرر" + timeline قريب |

## 2.5 Closing (2 دقائق)

### السيناريو A — Tier A1 (اقفل اليوم)
> "بصراحة، اللي وصفته — بطء الرد + تكلفة [X SAR/أسبوع] + قرارك أنت — هذا بالضبط ما يحلّه الـ Mini Sprint بـ ٤٩٩ ريال على ٣ أيام. أبغى أرسلك عرض مكتوب خلال ٢٤ ساعة، تراجعه، ولو ناسبك ندفع ٢٥٠ مقدم ونبدأ يوم الأحد. مناسب؟"

### السيناريو B — Tier A2/B (ديمو الأسبوع)
> "اللي وصفته يستحق ديمو ٣٠ دقيقة نشوف فيه المنصة على بياناتك. عندي [اليوم/الوقت] أو [اليوم/الوقت] هذا الأسبوع. أيهم أفضل؟"

### السيناريو C — Tier C/D (Nurture أو رفض نظيف)
> "شكراً للصراحة. حسب اللي قلت، اعتقد إن الـ timing مو الآن. خلّيني أرسل لك ملخص PDPL/Revenue Ops من محتوانا، وإذا تغيّرت الأمور — عندك رقمي."

### السيناريو D — Disqualified (طلب ممنوع)
> "نقدّر اهتمامك. Dealix ما تقدّم [cold WhatsApp / guaranteed sales / scraping]. البديل الآمن: [diagnostic-only / consent-based / evidence-backed]. تحب أرسل لك المسودة البديلة؟"

## 2.6 التوثيق بعد المكالمة (5 دقائق إلزامي)

سجّل في `gtm_conversation_tracker.csv`:
- date · company · score · tier · rung · next_action · next_date · objection_primary

سجّل في `evidence_events_tracker.csv`:
- event_type=`discovery_completed` · company · score

---

# Part 3 — 30-Minute Demo Script (per tier)
## سكربت الديمو ٣٠ دقيقة — حسب الـ tier

`MARKET_INTELLIGENCE_DEMO_SCRIPT_AR.md` يغطي ديمو ١٠ دقائق سريع. `dealix_demo_script_30min.md` يغطي البنية العامة. هذا القسم يفصّل **حسب الـ Rung المستهدف**.

## 3.1 Demo for Mini Sprint (Rung 1 — 499 SAR / 3 days)

**الجمهور:** Tier A1/A2 — pain ≥ 10K SAR/أسبوع، authority = A/B، timeline ≤ شهر.

### Opening (2 دقائق)
> "[الاسم]، قبل أشارك الشاشة — في المكالمة السابقة قلت ‹[اقتباس Q5 حرفياً]›. خلّيني أعكس فهمي: تعاني من [paraphrase] وهذا يكلّفك تقريباً [Q6 رقم] أسبوعياً. صح؟"

**انتظر التأكيد**. لا تكمل قبله.

### Problem reflection (5 دقائق)
- ارسم على شاشة بيضاء: lead in → response gap → loss
- اربط برقمه: "في ٤ أسابيع = [X×4] SAR ضايعة. الـ Sprint بـ ٤٩٩ ريال = ٠.٣% من خسارة شهر واحد."
- اذكر **هل سبب الخسارة معروف؟** غالباً لا — وهذا ما يحلّه الـ Diagnostic داخل الـ Sprint.

### Solution walkthrough (15 دقيقة) — لايف فقط على بيئة آمنة

استخدم checklist `MARKET_INTELLIGENCE_DEMO_SCRIPT_AR.md` (دقائق 3–9):

1. **Decision Passport (5 دقائق)** — `/api/v1/decision-passport/evidence-levels`، أرِه L0–L5. الجملة: «قبل أي رسالة، جواز قرار.»
2. **Approval-first (5 دقائق)** — `/ar/ops/approvals`. أرِه draft → approval → send. اذكر: «لا واتساب بارد في الكود.»
3. **Proof Pack sample (5 دقائق)** — افتح `docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md`. قل: «هذا ما يستلمه بعد ٣ أيام.»

**ممنوع في الـ demo:**
- أي feature ليس في `no_overclaim.yaml` بحالة `Production` أو `Partial` صريح
- أي رقم CRM مخترع
- أي تكامل أحمر (راجع Truth Matrix قبل الديمو)

### Pricing reveal (3 دقائق) — Anchor high, deliver low

> "الـ Diagnostic الكامل من ٤,٩٩٩ ريال. الـ Sprint الموسّع من ٢٥,٠٠٠ ريال. لكن للعملاء الأوائل — وأنت ضمنهم — نقدّم **Mini Sprint بـ ٤٩٩ ريال على ٣ أيام**: تشخيص + ١٠ leads مدققة + Proof Pack مختصر. السبب: نبني case studies سعودية ونحتاج إشارة سوق.
> الدفع: ٢٥٠ مقدم، ٢٤٩ عند تسليم Proof Pack. + ١٥٪ VAT = إجمالي ٥٧٣.٨٥ ريال. فاتورة ZATCA رسمية."

**لا تعتذر عن السعر**. لا تقدّم خصم قبل اعتراض صريح.

### Objection handling (3 دقائق) — أهم ٣

| الاعتراض | الرد (≤30 ثانية) |
|----------|-------------------|
| "السعر مرتفع للـ 499" | "٤٩٩ = ٠.٣% من خسارة شهر واحد ذكرتها أنت. لو الـ Proof Pack ما أثبت ROI، نرجّع المبلغ." |
| "نبي ندرس أكثر" | "ممتاز. عرض مكتوب يصلك خلال ٢٤ ساعة، صالح ١٤ يوم. اقرأه، رجع لي بأسئلة محددة." |
| "نستخدم HubSpot الآن" | "Dealix يكمل HubSpot عبر webhook — ما يستبدله. الـ Sprint نقيس الفجوة، لا نطلب استبدال." |

### Close (2 دقائق)
> "خلاصة: تشوف ناسب؟ لو نعم — أرسل لك العرض المكتوب خلال ٢٤ ساعة، توقّع، ندفع ٢٥٠، نبدأ يوم الأحد. لو لا — قل لي السبب الحقيقي، أحترم رأيك."

**التزام مكتوب:** أرسل `dealix_pilot_agreement.md` معدّل للـ Mini Sprint خلال ٢٤ ساعة. أتبع بـ Calendly link للـ kickoff.

## 3.2 Demo for Data Pack (Rung 2 — 1,500 SAR / 7 days)

**الفرق عن Mini Sprint:** يضيف CSV/CRM ingestion + PII handling.

### تعديل Opening
> "بعد ما شفت في الديمو الأول كيف نشتغل، الـ Data Pack يضيف layer واحد: نأخذ CSV/export من CRM، نشتغل عليه بـ PII handling صريح، ونرجّع لك ١٠٠ lead مع decision passport لكل واحد."

### تعديل Solution walkthrough
- أضف **PII redaction demo**: ملف عيّنة → بعد المعالجة (الأرقام محجوبة)
- أضف **DPA snippet**: افتح ملف الـ DPA الموجود في `docs/sales-kit/`
- أرِه الـ CSV export النهائي

### تعديل Pricing
> "Data Pack: ١,٥٠٠ ريال + ١٥٪ VAT = ١,٧٢٥ ريال. ٧٥٠ مقدم. تسليم ٧ أيام."

### Objections إضافية
- **"خصوصية بياناتنا"** → DPA + PII redaction live demo + sub-processors list
- **"هل تخزن بياناتنا؟"** → Region constraint + retention period (راجع DPA الفعلي)

## 3.3 Demo for Managed Ops (Rung 3 — 2,999/4,999/7,999 SAR/mo)

**الجمهور فقط:** عملاء سبق دفعوا Rung 1 أو 2، Proof Pack ناجح، adoption ≥ 70%.

**القاعدة الذهبية:** لا تعرض Rung 3+ قبل اكتمال Rung 1/2 بنجاح موثّق. (راجع Part 7 — Anti-patterns.)

### Opening
> "بعد Sprint الذي أثبت [نتيجة محددة من الـ Proof Pack]، السؤال: نستمر شهرياً مع حوكمة كاملة، أو ترجع للوضع السابق؟"

### Solution walkthrough (15 دقيقة)
1. **War Room dashboard** — `/ar/ops/founder`، استعراض أسبوعي
2. **Approval queue** — يومي ٩ ص
3. **Monthly Proof Pack** — sample من العميل نفسه
4. **SLA + escalation path** — مكتوب في الـ MSA

### Pricing reveal — Three tiers

| Tier | السعر | الحجم |
|------|-------|-------|
| Starter | 2,999 SAR/mo | حتى 500 محادثة |
| Growth | 4,999 SAR/mo | حتى 2,000 محادثة |
| Scale | 7,999 SAR/mo | حتى 5,000 محادثة |

> "+15% VAT. التزام ٣ شهور. إنهاء بإشعار ٣٠ يوم بعد الـ ٣ شهور."

### Objections إضافية
- **"التزام ٣ شهور طويل"** → "ضمان retainer readiness: لو الـ adoption < 70% بعد شهر، fee الشهر الثاني = ٠. هذا في العقد."
- **"إيش الفرق عن Sprint؟"** → "Sprint = lump-sum project. Retainer = ops ownership شهرياً مع SLA."

## 3.4 Universal demo rules

- **النسبة 60/40:** العميل يتكلم ٦٠٪
- **5-second silence rule:** اسكت بعد كل سؤال
- **No fake numbers:** أي رقم CRM يجب أن يكون من demo account معروف
- **Truth Matrix check:** قبل الديمو افتح `no_overclaim.yaml` وتأكد كل feature ستعرضه = Production
- **Recording:** اطلب إذن صريح، خزّن في drive مع TTL ٩٠ يوم
- **Debrief:** املأ `founder_meeting_debrief_template.yaml` خلال ساعة من نهاية الديمو

---

# Part 4 — Proposal Outline (per Rung)
## مخطط العرض — لكل Rung

كل عرض **bilingual** (عربي + إنجليزي)، PDF نهائي، صالح ١٤ يوم، يحمل توقيع رقمي للمؤسس، فاتورة ZATCA-ready.

## 4.1 الهيكل الموحد (8 أقسام)

```
1. Cover
2. Executive Summary (3 bullets — quantified)
3. Scope (Deliverables + Exclusions)
4. Timeline
5. Pricing (SAR + 15% VAT + payment terms)
6. Trust Signals (PDPL · ZATCA · no_overclaim link)
7. Acceptance (signature block + expiration)
8. Appendix (DPA, sub-processors, references)
```

## 4.2 Rung 1 — Mini Sprint (499 SAR / 3 days)

### Cover
- Dealix logo
- العميل: [Company Name]
- التاريخ: [Issue date]
- صالح حتى: [Issue + 14 days]
- المرجع: SP-[YYYYMMDD]-[3-digit seq]

### Executive Summary (٣ نقاط)
- "خلال ٣ أيام عمل، نحلّل أعلى ١٠ leads حالية ونرجّع Proof Pack يكشف **سبب** ضياعها."
- "Decision Passport لكل lead — L0 إلى L5 — مع evidence و next action."
- "السعر ٤٩٩ ريال = استثمار قياس، لا تعاقد طويل. النتائج خلال ٧٢ ساعة."

### Scope — Deliverables
1. تحليل ١٠ leads (من CSV أو export من CRM يقدّمه العميل)
2. Decision Passport JSON لكل lead
3. تقرير Proof Pack PDF بصفحتين (عربي + إنجليزي)
4. مكالمة ٣٠ دقيقة لمراجعة النتائج
5. توصية واحدة محددة للخطوة التالية

### Scope — Exclusions (NOT included)
- أي إرسال خارجي تلقائي
- تكامل CRM (يأتي في Rung 2+)
- ديمو موسّع للفريق (يأتي في Rung 3+)
- ضمان نتائج عددية (انظر disclaimer)

### Timeline (يوم-بيوم)
| اليوم | المخرج |
|-------|--------|
| Day 0 (Sun) | استلام CSV + توقيع DPA |
| Day 1 (Mon) | معالجة + Decision Passport draft |
| Day 2 (Tue) | Proof Pack draft + مراجعة داخلية |
| Day 3 (Wed) | تسليم نهائي + مكالمة |

### Pricing
| البند | SAR |
|-------|-----|
| Mini Sprint fee | 499.00 |
| VAT 15% | 74.85 |
| **الإجمالي** | **573.85** |

**Payment terms:** 50/50 — 250 SAR مقدم (Moyasar link)، 249 SAR عند تسليم Proof Pack. فاتورة ZATCA Phase 2 صادرة خلال ٢٤ ساعة من كل دفعة.

### Trust Signals
- PDPL: راجع DPA الملحقة + ملف `MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`
- ZATCA: فواتير Phase 2 compliant
- No-overclaim: كل ادعاء في هذا العرض = `Production` في `dealix/registers/no_overclaim.yaml`
- Bilingual disclaimer: «النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.»

### Signature Block
- Bassam Assiri — Founder, Dealix
- [Customer signatory]
- صالح ١٤ يوم من تاريخ الإصدار

## 4.3 Rung 2 — Data Pack (1,500 SAR / 7 days)

نفس هيكل Rung 1 مع تعديلات:

### Executive Summary
- "خلال ٧ أيام عمل، نأخذ CRM export كامل ونحوّله إلى Decision Passport لكل lead."
- "حتى ١٠٠ lead معالج مع PII redaction كامل."
- "DPA موقّعة + sub-processors list + ٩٠ يوم retention."

### Deliverables
1. CSV/export ingestion (حتى 100 سجل)
2. PII redaction (national_id, IBAN, phone middle digits)
3. Decision Passport لكل سجل
4. Proof Pack موسّع (٥ صفحات)
5. توصية roadmap للـ retainer

### Exclusions
- > 100 records (Rung 3+)
- ربط حي مع CRM (Rung 3+)
- تدريب فريق (إضافة منفصلة)

### Pricing
| البند | SAR |
|-------|-----|
| Data Pack fee | 1,500.00 |
| VAT 15% | 225.00 |
| **الإجمالي** | **1,725.00** |

**Payment:** 750 SAR مقدم، 750 SAR عند التسليم.

## 4.4 Rung 3 — Managed Ops (2,999 / 4,999 / 7,999 SAR/mo)

### Cover
- المرجع: MS-[YYYYMM]-[3-digit seq]
- المدة: 3 شهور أولاً، ثم شهرياً
- صالح ١٤ يوم

### Executive Summary
- "Revenue Ops كامل — Approval-first، Decision Passport على كل lead، Proof Pack شهري."
- "SLA: رد على approval queue خلال ٤ ساعات عمل، Proof Pack بنهاية كل شهر."
- "ضمان adoption: لو < 70% بعد الشهر الأول، fee الشهر الثاني = ٠."

### Deliverables (شهرياً)
1. Approval queue management (يومي)
2. Weekly War Room dashboard update
3. Monthly Proof Pack PDF (١٠ صفحات)
4. Quarterly Business Review session
5. Slack channel مشترك (response SLA ٤ ساعات عمل)

### Exclusions
- تطوير custom features (Rung 4)
- اجتماعات تنفيذية أسبوعية (Rung 5)
- ضمان نتائج عددية محددة

### Timeline (أسبوع-بأسبوع، شهر واحد)
| الأسبوع | المخرج |
|---------|--------|
| W1 | Onboarding + access + DPA |
| W2 | Approval queue live + first batch |
| W3 | Mid-month checkpoint |
| W4 | Proof Pack delivery + review |

### Pricing
| Tier | Fee SAR | VAT 15% | Total SAR/mo |
|------|---------|---------|---------------|
| Starter | 2,999 | 449.85 | **3,448.85** |
| Growth | 4,999 | 749.85 | **5,748.85** |
| Scale | 7,999 | 1,199.85 | **9,198.85** |

**Payment:** 1st month مقدم، ثم monthly في اليوم الأول من كل شهر.

## 4.5 Rung 4 — Custom AI (5K-25K SAR + 1K/mo)

### Notes — يحتاج founder approval قبل الإرسال
- Custom scope = founder يكتب SOW يدوياً
- Payment 30/30/40 (kick-off, mid, delivery)
- 4–8 أسابيع، scope-bound
- Monthly retainer 1K SAR للـ maintenance

### Executive Summary template
- "Bespoke build على معمارية Dealix، scope محدد في SOW الملحق."
- "Timeline [N] أسابيع، 3 milestones."
- "Production handover + 90-day support."

### Pricing range
| Type | Range SAR |
|------|-----------|
| Integration build | 5,000–10,000 |
| Custom agent | 10,000–18,000 |
| Multi-channel orchestration | 18,000–25,000 |
| Monthly maintenance | 1,000/mo |

## 4.6 Rung 5 — Executive Command Center (12K-25K SAR/mo)

### Notes — Enterprise tier، يحتاج founder + legal approval
- 6-month minimum
- Custom MSA (لا يستخدم العقد القياسي)
- Quarterly Executive Review مع CEO
- Dedicated Slack + dedicated number
- SLA 1-hour business response

### Executive Summary template
- "Command Center لـ C-suite — dashboards, approvals, weekly proof, quarterly governance review."
- "Dealix يصبح طبقة Revenue Governance رسمية تحت CFO/CRO."
- "6-month engagement, custom SOW."

### Pricing
- 12,000–25,000 SAR/mo حسب الحجم
- Setup fee منفصل: 15K–50K SAR

## 4.7 قاعدة موحدة لجميع العروض

**قبل الإرسال — checklist:**
- [ ] كل ادعاء له id في `no_overclaim.yaml` بحالة Production/Partial
- [ ] لا يوجد ضمان نتائج عددية (revenue, leads, conversion)
- [ ] VAT 15% بسطر منفصل
- [ ] Bilingual disclaimer موجود
- [ ] DPA كملحق
- [ ] صلاحية ١٤ يوم محددة
- [ ] رقم مرجع فريد
- [ ] founder signature (digital)

**ممنوع في أي proposal:**
- "نضمن X SAR إيرادات"
- "زيادة conversion بنسبة Y%"
- "Best in MENA / #1 in Saudi"
- "Free trial" بدون cap واضح

---

# Part 5 — Objection Matrix (15 new × 3 sectors)
## مصفوفة الاعتراضات — ١٥ جديد × ٣ قطاعات

`GTM_OBJECTION_MATRIX_AR.md` و `objection_engine_registry.yaml` يغطيان الأساسيات الست. هذا القسم يضيف ١٥ اعتراض جديد عبر ٣ قطاعات: **Agency · SaaS · Retail/E-commerce**.

**القاعدة:** كل رد ≤ ٣٠ ثانية، يحوّل لسؤال، ما يضع وعد جديد.

## 5.1 الاعتراضات العامة (تنطبق على كل القطاعات) — ٥

### O-001 — "السعر مرتفع للـ ٤٩٩"
**Sector:** all · **Classify:** pricing
**رد:**
> "٤٩٩ = ٠.٣٪ من خسارة شهر واحد لو ضايع lead واحد بـ ١٠K. الـ Proof Pack يكشف كم ضايع. ضمان: لو ما أثبت ROI أرجّع المبلغ. ممكن نشوف Q6 رقم خسارتك مرة ثانية؟"

### O-002 — "نستخدم HubSpot الآن"
**Sector:** all · **Classify:** positioning
**رد:**
> "Dealix يكمل HubSpot عبر webhook، ما يستبدله. HubSpot يخزّن الـ deal، Dealix يثبت ما حدث بين الـ leads. الـ Sprint يقيس الفجوة بدون أي تغيير في HubSpot. تحب أرسل integration spec؟"

### O-003 — "Arabic data خصوصية"
**Sector:** all · **Classify:** compliance
**رد:**
> "PDPL-native by design. DPA موقّعة قبل أي بيانات، PII redaction قبل المعالجة، sub-processors list منشورة، region constraint مكتوب. راجع compliance register: [link]. تحب نراجع DPA معاً قبل العرض؟"

### O-004 — "ما حد سمع عنكم"
**Sector:** all · **Classify:** trust
**رد:**
> "صحيح، نحن في beta. لذلك السعر ٤٩٩ ريال = ٠.٣٪ من خسارة شهر. ضمان إرجاع كامل لو الـ Proof Pack ما أثبت قيمة. الـ logos تأتي بعد العملاء الأوائل — وأنت ضمنهم. الـ trust يأتي من الـ work، لا من اللوقو."

### O-005 — "نبي ندرس أكثر"
**Sector:** all · **Classify:** stall
**رد:**
> "ممتاز. الـ Diagnostic مجاني — صفر ريال، ١٠ دقائق، تأخذ تقرير بدون أي التزام. تدرس معه بدل ما تدرس بدون بيانات. متى مناسب — اليوم العصر أو بكره الصباح؟"

## 5.2 Agency-specific — ٥

### O-101 — "نحن وكالة، Dealix ينافسنا"
**Classify:** wedge_conflict
**رد:**
> "بالعكس — Dealix يحلّ السؤال الذي تسأله العميل: ‹وش حدث بعد الحملة؟›. اشتري Sprint للعميل، تبيعه كـ value-add من الوكالة، نوقّع white-label MSA. صار قيمة إضافية لعقدك، لا تهديد."

### O-102 — "عملاؤنا ما يدفعون لأي AI"
**Classify:** market
**رد:**
> "ما نبيع AI — نبيع Proof: ‹هذي ١٠ leads ضاعت، هذا السبب، هذا الحل›. العميل يدفع للـ proof لا للـ AI. شفت ردة فعل العميل لما تعطيه تقرير بأرقام محددة؟"

### O-103 — "نستخدم Looker/Tableau للتقارير"
**Classify:** tooling
**رد:**
> "Looker/Tableau يعرضون ما حدث. Dealix يثبت **لماذا** lead معين فشل، ويعطي next action. مكمّل، لا منافس. الـ Sprint نقدم البيانات بصيغة تستهلكها Looker مباشرة."

### O-104 — "العميل ما يفهم AI"
**Classify:** education
**رد:**
> "ما يحتاج يفهم. يستلم PDF بصفحتين: ١٠ leads، السبب، التوصية. الـ AI خلف الكواليس. الـ value هو الـ outcome، لا الـ technology. تحب أرسل sample Proof Pack؟"

### O-105 — "Margin ضعيف على re-sell"
**Classify:** economics
**رد:**
> "MSA partner: ٢٠٪ margin مدى الحياة على كل عميل تجلبه. ٤٩٩ × ٢٠٪ = ٩٩.٨٠ على Sprint. retainer ٤,٩٩٩ × ٢٠٪ = ١,٠٠٠/شهر متكرر. تحب نوقّع partner agreement اليوم؟"

## 5.3 SaaS-specific — ٥

### O-201 — "Product-led growth، ما عندنا outbound"
**Classify:** model_fit
**رد:**
> "ممتاز. الـ Sprint يقيس conversion داخل الـ funnel: signup → activated → paid. كم signup ضايع لأن first-message ما وصل في الوقت؟ هذا outbound داخلي. تحب نشوف؟"

### O-202 — "عندنا data team داخلي"
**Classify:** internal_build
**رد:**
> "Data team يبني التحليل. Dealix يبني الـ governance + approval workflow عليه. كم وقت يأخذ data team عشان يبنون approval queue + audit log + DPA layer؟ ٣ أيام بـ ٤٩٩ أرخص."

### O-203 — "نريد API فقط، ما نريد managed service"
**Classify:** delivery_model
**رد:**
> "API متاح من Rung 2. الـ Sprint يثبت أن الـ API يعطي قيمة قبل تطلب integration كبير. لا تشتري API على وعد — اشتري على Proof. ممكن نبدأ بـ Sprint ثم API spec؟"

### O-204 — "نستخدم Mixpanel/Amplitude للـ events"
**Classify:** tooling
**رد:**
> "Mixpanel يقيس behavior. Dealix يقيس decision: من قرر، بأي evidence، متى. مكمّل. الـ Sprint نأخذ Mixpanel export ونرجّع decision layer فوقه. تحب نشوف؟"

### O-205 — "نحن compliant SOC 2، ما نحتاج PDPL وحدها"
**Classify:** compliance
**رد:**
> "SOC 2 يغطي infra. PDPL يغطي data subject rights للسعوديين تحديداً: consent, deletion, region. SOC 2 ≠ PDPL. الـ Sprint نراجع gap analysis مجاناً ضمن الـ ٤٩٩."

## 5.4 Retail / E-commerce-specific — ٥

### O-301 — "نستخدم Salla/Zid، كل شي مربوط"
**Classify:** ecosystem
**رد:**
> "ممتاز — Salla/Zid يجمعون orders. Dealix يثبت ما حدث للـ leads اللي ما اشتروا. أبانديند كارت، DM ما رُد عليه، استفسار WhatsApp ضاع. الـ Sprint نقيس هذا الجزء."

### O-302 — "WhatsApp Business عندنا فيه bot"
**Classify:** tooling
**رد:**
> "Bot يرد على FAQs. Dealix يقرر **متى** ينتقل من bot لإنسان + يثبت سبب الفشل. الـ Sprint نأخذ ١٠ محادثات bot ضايعة ونرجّع تحليل قرار. تحب sample؟"

### O-303 — "موسمنا نوفمبر، الحين slow"
**Classify:** timing
**رد:**
> "بالضبط الوقت المثالي. Sprint الآن = جاهزية كاملة قبل البلاك فرايداي. لو بدأت أكتوبر فقدت ٤ شهور تحضير. ٤٩٩ ريال اليوم = ROI واضح في نوفمبر. تحب نحجز Sprint للأسبوع الجاي؟"

### O-304 — "نبيع لمستهلك B2C، Dealix B2B"
**Classify:** model_fit
**رد:**
> "Dealix أساساً B2B، صحيح. لكن في B2C عالي القيمة (سيارات، عقار، تعليم خاص) الـ lead-to-close مشابه. لو متوسط الـ deal > ٥K SAR والـ sales cycle > أسبوع، نناسب. لو tickets أصغر، نحوّلك لشريك."

### O-305 — "ZATCA Phase 2 لسا ما طبّقناه، مشغولين بيه"
**Classify:** timing + compliance
**رد:**
> "Dealix يدعم ZATCA invoice rendering بعد التسليم. خلال الـ Sprint ما يأثر على workflow ZATCA الحالي. اخلص ZATCA أولاً، الـ Sprint الموازي ٣ أيام فقط. تحب نبدأ بعد ZATCA؟"

## 5.5 توثيق وتغذية راجعة

بعد كل اعتراض جديد (لم يظهر في القائمة):
1. سجّل في `objection_engine_registry.yaml` بنفس schema
2. لو تكرر ≥ ٢ مرات/أسبوع → drafting أصل AEO جديد
3. حدّث `GTM_OBJECTION_MATRIX_AR.md` بـ row جديد

---

# Part 6 — Pipeline Operating Procedure (Daily / Weekly)
## إجراءات تشغيل الـ Pipeline — يومي وأسبوعي

## 6.1 الـ Morning Loop (٩٠ دقيقة، ٨:٠٠ – ٩:٣٠ ص)

### Block 1 — Standup self-review (١٥ دقيقة)
- [ ] افتح `gtm_conversation_tracker.csv` — اقرأ آخر ٧ أيام
- [ ] افتح `evidence_events_tracker.csv` — اقرأ الـ events أمس
- [ ] افتح `soft_launch_meetings_tracker.yaml` — اقرأ commitments اليوم
- [ ] افتح Moyasar dashboard — تأكد لا فواتير عالقة

سؤال: "أمس وعدت أحد بـ X — هل أرسلته؟"

### Block 2 — Outreach block (٤٥ دقيقة)
**القاعدة:** founder-led فقط، لا أتمتة، 5 رسائل دافئة/يوم max.

- [ ] افتح warm list (LinkedIn/phone existing relationships)
- [ ] اختر 5 أشخاص (انظر `WARM_LIST_WORKFLOW.md`)
- [ ] اكتب رسالة 1-line (3 variants لكل، أرسل الأنسب يدوياً)
- [ ] سجّل في `gtm_conversation_tracker.csv` (status: contacted)

ممنوع: cold WhatsApp · LinkedIn auto · scraping · bulk emails.

### Block 3 — Content block (٢٠ دقيقة)
- [ ] اكتب LinkedIn post صغير (2-3 paragraphs) — موضوع اليوم من `AEO_CONTENT_CALENDAR_AR.md`
- [ ] أو حدّث AEO draft واحد في `docs/commercial/operations/aeo_drafts/`
- [ ] أو سجل صوت 5 دقائق Loom لـ AEO video

CTA الموحّد: free diagnostic، Calendly link.

### Block 4 — Demo prep (١٠ دقائق)
- [ ] لو في ديمو اليوم: راجع `MARKET_INTELLIGENCE_DEMO_SCRIPT_AR.md` + Truth Matrix
- [ ] افتح `no_overclaim.yaml` — تأكد كل feature ستعرضه = Production
- [ ] جهّز demo account (sample data، لا أرقام حقيقية)

## 6.2 الـ Evening Loop (٣٠ دقيقة، ٦:٠٠ – ٦:٣٠ م)

### Block 1 — Pipeline update (١٥ دقيقة)
- [ ] حدّث `gtm_conversation_tracker.csv` بكل محادثة اليوم
- [ ] حدّث `evidence_events_tracker.csv` بكل event (discovery_completed, demo_booked, proposal_sent, paid)
- [ ] سجّل أي objection جديد في `objection_engine_registry.yaml`
- [ ] حدّث HubSpot stage لكل deal لمست اليوم

### Block 2 — Friction log (١٠ دقائق)
في `docs/commercial/operations/friction_log.md` (أنشئ لو ما موجود):
- ما المعطّل أكثر شي اليوم؟
- ما الـ tooling اللي يحتاج إصلاح؟
- ما الـ message اللي ما اشتغل؟

### Block 3 — Tomorrow plan (٥ دقائق)
- [ ] أعلى 3 priorities بكره
- [ ] أي ديمو أو مكالمة محجوزة
- [ ] أي proposal لازم ينرسل خلال 24h

## 6.3 الـ Sunday Weekly Review (٩٠ دقيقة، ١٠:٠٠ – ١١:٣٠ ص)

### Block 1 — Scorecard (٣٠ دقيقة)
افتح `COMMERCIAL_WEEKLY_SCORECARD_AR.md` و املأ:

| Metric | Target W1 | Target W2 | Actual |
|--------|-----------|-----------|--------|
| Warm contacts sent | 25 | 25 | ? |
| Discovery calls completed | 5 | 8 | ? |
| Demos booked | 2 | 3 | ? |
| Proposals sent | 1 | 2 | ? |
| Closed paid (Rung 1+) | 0 | 1 | ? |
| AEO drafts published | 2 | 3 | ? |

### Block 2 — Decision Gates (٣٠ دقيقة)
- لو W1 Actual < ٧٠٪ Target → root cause في 3 أسطر
- لو objection معيّن تكرر ≥ 2 مرات → كتابة AEO هذا الأسبوع
- لو proposal لم يُرد عليه > ٧٢ ساعة → follow-up draft للموافقة

### Block 3 — Content planning (٢٠ دقيقة)
- اختر ٣ موضوعات للأسبوع الجاي من `AEO_CONTENT_CALENDAR_AR.md`
- جدول الـ post times (Sun/Tue/Thu 9am KSA)
- حدّد CTA لكل post

### Block 4 — Next week priorities (١٠ دقائق)
- أعلى 3 أهداف الأسبوع الجاي
- أي risk ظاهر؟ (مالي، تشغيلي، قانوني)

## 6.4 HubSpot Stages Mapping

| Stage | Definition | Exit criteria | Next action |
|-------|-----------|---------------|-------------|
| **New** | لمسة أولى (LinkedIn reply, form fill, intro email) | استجابة خلال 7 أيام | Discovery scheduled |
| **Contacted** | تواصل founder، لم يحجز Discovery بعد | استجابة خلال 14 يوم أو drop | Discovery call |
| **Qualified** | Discovery اكتمل، Score ≥ 60 | tier_A/B + الحاجة لديمو | Demo scheduled |
| **Demo** | Demo اكتمل، الـ champion إيجابي | Proposal مطلوب | Proposal draft 24h |
| **Proposal** | Proposal sent، صلاحية 14 يوم | توقيع أو رفض | Invoice أو reason logged |
| **Closed Won** | دفعة مقدمة وصلت Moyasar | Kickoff session مجدول | Sprint kickoff |
| **Closed Lost** | رفض صريح أو انتهاء صلاحية | السبب موثّق | Nurture or remove |
| **Nurture** | Tier C، لا الآن | استئناف اشتباك بعد 30/60/90 يوم | Monthly check-in |

**Move criteria:**
- New → Contacted: founder أرسل أول رسالة موثّقة
- Contacted → Qualified: Discovery كامل في `gtm_conversation_tracker.csv` بـ Score
- Qualified → Demo: demo on calendar + invite مرسل
- Demo → Proposal: proposal draft generated بـ `proposal_renderer.render_proposal()`
- Proposal → Closed Won: Moyasar payment_id موثّق + ZATCA invoice issued

**SLA per stage:**
- New → Contacted: ≤ ٢٤ ساعة
- Contacted → Qualified: ≤ ٧ أيام
- Qualified → Demo: ≤ ٧ أيام
- Demo → Proposal: ≤ ٢٤ ساعة
- Proposal → Closed Won/Lost: ≤ ١٤ يوم (proposal expiration)

## 6.5 الـ Pipeline Velocity Targets (Day 1-14)

```
Day 1-3:   25 warm contacts sent
Day 4-7:   5 Discovery calls done · 2 demos booked
Day 8-10:  3 demos done · 1 proposal sent
Day 11-13: 2 proposals sent · 1 in negotiation
Day 14:    1 closed paid (target)
```

**Leading indicators (لو تأخرت):**
- Day 3 لو < 15 warm contacts → outreach block ضعيف
- Day 7 لو < 3 Discovery → script يحتاج تعديل
- Day 10 لو 0 demos → الـ qualification متساهلة جداً
- Day 13 لو 0 proposals → demo ما يقفل

---

# Part 7 — Anti-Failure Patterns (DON'T LIST)
## أنماط الفشل — لا تفعل أبداً

كل بند هنا من تجارب فشل حقيقية في الـ founder-led sales. اقرأ كل يوم اثنين.

## DON'T 1 — لا تخصم قبل الاعتراض الصريح
**لماذا:** يبني توقع خصم في كل صفقة لاحقة. السعر = anchor.
**بدلاً:** الـ value reframe. "٤٩٩ = ٠.٣٪ من خسارتك" قبل أي خصم.
**استثناء:** خصم beta-customer مكتوب من اليوم الأول (١٠ عملاء أوائل، ١٥٪).

## DON'T 2 — لا تمدّد free trials
**لماذا:** "أسبوع آخر مجاناً" يخلق free-anchor دائم. يصعّب التحويل لـ paid.
**بدلاً:** Diagnostic مجاني بحدود واضحة (١٠ دقائق فقط، نتيجة واحدة). بعدها Sprint مدفوع.

## DON'T 3 — لا تبيع Rung 3+ قبل Rung 1 proof
**لماذا:** retainer بدون proof = churn في الشهر الثاني. الـ adoption ينهار.
**القاعدة:** اعرض Managed Ops فقط بعد:
- Sprint مكتمل
- Proof Pack مستلم
- `adoption_os.retainer_readiness.evaluate(...).eligible == True`

## DON'T 4 — لا تَعِد بـ features ليست في production
**القاعدة:** قبل أي عرض/ديمو، افتح `dealix/registers/no_overclaim.yaml`. لو الـ feature بحالة `Planned` أو `Pilot` فقط، **ممنوع ذكرها للعميل**.
**العبارة الآمنة:** "هذه في roadmap الـ Q3، لو احتجتها قبل ندخل في Rung 4 custom build."

## DON'T 5 — لا cold WhatsApp أبداً
**لماذا:** ينتهك non-negotiables الدالة + قانون مكافحة الـ spam السعودي + يحرق العلامة.
**بدلاً:** founder-led intro من علاقة موجودة فقط. لو ما في warm intro، الـ channel = LinkedIn DM أو AEO content أو event in-person.

## DON'T 6 — لا تَجمع contacts بـ scraping
**لماذا:** غير قانوني (PDPL) + يكسر non-negotiable.
**بدلاً:** opt-in lists فقط — landing page form، event signup، LinkedIn reply.

## DON'T 7 — لا تستخدم أرقام CRM وهمية في الديمو
**لماذا:** لو العميل اكتشف، الـ trust يموت. لو camera تلتقط real data، خرق PDPL.
**بدلاً:** demo account واحد بـ synthetic data معروف، نفس الـ data في كل ديمو.

## DON'T 8 — لا تَعِد بـ guaranteed revenue/leads/conversion
**القاعدة:** كل proposal يحمل bilingual disclaimer:
> "Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة"

## DON'T 9 — لا تذكر اسم عميل في public material بدون إذن مكتوب
**Founder approval إلزامي** لأي:
- Case study بـ اسم
- LinkedIn post يذكر logo
- Press release
- Investor deck slide

## DON'T 10 — لا توقّع شيء > 5K SAR بدون founder + legal review
**القاعدة:** Rung 4/5 = custom MSA = founder writes/approves فقط. لا standard template.

## DON'T 11 — لا تَعرض ٨ packages في proposal واحد
**القاعدة:** عرض واحد لكل محادثة. الـ tier محدد قبل الـ proposal من Discovery score.

## DON'T 12 — لا تَخفّض السعر للقاء deadline
**لماذا:** ينقل اللحظة من قيمة → ضغط زمني. الـ deal لا يصمد.
**بدلاً:** "العرض صالح ١٤ يوم. لو فات بدون قرار، نكتب proposal جديد بنفس السعر."

## DON'T 13 — لا تُرسل دون founder approval خارجياً
**القاعدة:** كل output من الـ agent = draft للمؤسس. الـ founder يرسل يدوياً.

## DON'T 14 — لا تُسجّل مكالمة بدون إذن صريح
**القاعدة:** اطلب إذن في الـ opening. سجّل النص فقط لو الإذن لفظي. لو طلب video recording، اكتب موافقة قبل البدء.

## DON'T 15 — لا تترك objection غير موثّق
**القاعدة:** كل اعتراض → سطر في `objection_engine_registry.yaml` خلال ٢٤ ساعة. لو تكرر ≥ ٢ → AEO draft.

---

# Part 8 — Founder-Only Decision Triggers
## قرارات تتطلب موافقة المؤسس فقط

الـ sub-agents (sales OS, proposal renderer, qualification) تعمل بـ autonomy محدودة. هذي القائمة = boundaries.

## 8.1 Hard Gates (لا يمر بدون موافقة Bassam)

| Trigger | لماذا | كيف يطلب |
|---------|-------|-----------|
| **Deal > 5,000 SAR** | Rung 3+ يحتاج SOW دقيق | Slack DM + proposal draft للمراجعة |
| **Custom scope deviation** | أي تعديل على standard templates | red flag في الـ proposal draft |
| **Customer name in public material** | trademark + PR risk | written approval via email |
| **Partner contract execution** | revenue share + IP terms | full draft + legal review |
| **Refund > 500 SAR** | financial impact + precedent | refund reason + bank ack |
| **Pricing exception > 15%** | beta discount cap | written justification |
| **Press release / media response** | brand consistency | full text + 24h review |
| **Investor / press contact** | narrative control | escalate immediately |
| **Regulator / government contact** | compliance + legal | escalate immediately |
| **Cease & desist / legal notice** | legal counsel needed | escalate within 1h |

## 8.2 Soft Gates (sub-agent acts، founder reviews in 24h)

| Trigger | sub-agent action | founder review |
|---------|------------------|----------------|
| **New Tier A1 lead** | draft Discovery invite | morning standup |
| **Demo booked** | draft pre-demo email | same day |
| **Proposal generated** | draft + queue for send | within 24h |
| **Objection logged** | add to registry + draft response | weekly review |
| **AEO content draft** | generate + queue for review | weekly content block |

## 8.3 Auto-allowed (لا تحتاج founder approval)

- transactional emails من whitelist (`auto_client_acquisition/email/transactional.py`)
- intake confirmation للـ leads
- internal scorecard updates
- `evidence_events_tracker.csv` appends
- `gtm_conversation_tracker.csv` updates
- internal Slack alerts للـ founder

## 8.4 Escalation path

```
sub-agent decision needed →
  check this list →
    if Hard Gate → block + draft escalation Slack →
    if Soft Gate → execute + queue founder review →
    if Auto-allowed → execute + log →

emergency (regulator, security, press, legal) →
  immediate Slack to bassam.m.assiri@gmail.com →
  WhatsApp ping →
  hold all related actions
```

## 8.5 Approval audit trail

كل founder approval (Hard أو Soft) يُسجّل في:
- `docs/commercial/operations/founder_weekly_decision_template.yaml`
- approval_id, date, decision, rationale, asset_ref

مراجعة أسبوعية: Sunday review block يقرأ آخر ٧ أيام approvals.

---

# Part 9 — Sector-Specific Discovery Probes
## أسئلة Discovery خاصة بالقطاع

عند تأكيد القطاع في Q5/Q9، انتقل لأحد المسارات التالية بدل الـ generic 7. الـ score يحسب من 12 نقطة لكل قطاع (مقابل 100 في `QUALIFICATION_SCORE.md`).

## 9.1 Agency probes (4 إضافية)

1. **عدد العملاء النشطين الآن؟** → < 5 = SMB، 5-20 = mid، 20+ = scale.
2. **متوسط mandate الشهري؟** → < 10K = خفيف، 10K-50K = متوسط، 50K+ = retainer ready.
3. **هل يطلب العملاء reports تفصيلية أم headlines فقط؟** → "تفصيلية" = Dealix يساعد، "headlines" = pain أقل.
4. **هل خسرتم عميل في آخر 3 شهور بسبب reporting/proof؟** → نعم = trigger قوي.

## 9.2 SaaS probes (4 إضافية)

1. **MRR الحالي؟** → < 50K = early، 50K-500K = growth، 500K+ = scale.
2. **CAC payback period؟** → > 18 شهر = pain، < 12 شهر = صحي.
3. **هل عندكم AE أم product-led فقط؟** → AE = Rung 3 fit، PLG-only = Rung 1/2 لقياس funnel.
4. **متى آخر churn analysis كامل؟** → "ما عملنا" = فرصة، "monthly" = متقدم.

## 9.3 Retail / E-commerce probes (4 إضافية)

1. **عدد الـ orders/شهر؟** → < 500 = SMB، 500-5K = mid، 5K+ = scale.
2. **AOV (متوسط قيمة الطلب)؟** → < 200 SAR = transactional، 200-2K = considered، 2K+ = high-touch.
3. **هل في فريق CX/customer service مستقل؟** → نعم = Dealix integrates، لا = خارج النطاق.
4. **نسبة الـ abandoned cart الآن؟** → > 70% = pain حاد، < 50% = صحي.

## 9.4 إضافة الـ probes لـ score الإجمالي

أي إجابة "ألم حاد" في الـ probes = +5 نقاط على `QUALIFICATION_SCORE.md`.
أي إجابة "متقدم/صحي" = +3 نقاط (الأقل ألماً، لكن adoption أسرع).

---

# Part 10 — Saudi Selling Etiquette
## آداب البيع السعودية

## 10.1 الـ Cultural rules

1. **الـ relationship يسبق الـ transaction** — أول 5-10 دقائق من أي مكالمة = شخصي (الأهل، السفر، المشاريع الجانبية). لا تقفز للـ pitch.
2. **اللقب يحترم** — أبو فلان / دكتور / مهندس / الأستاذ. لو شك، اسأل: "كيف تحب أناديك؟"
3. **الـ "إن شاء الله"** = "نشوف، مو الآن". ليست yes. ليست no. اطلب next action محدد.
4. **التأجيل ≠ رفض** — السوق يأخذ وقت. follow-up بأدب كل 7-10 أيام مقبول.
5. **الـ silence مهم** — لا تملأ كل لحظة صمت. الـ partner يفكر.

## 10.2 الـ Timing rules

| الوقت | الحالة |
|-------|--------|
| Sunday 9-11am | الأفضل للـ Discovery |
| Sunday-Tuesday 9am-2pm | الأفضل للـ Demo |
| Wednesday afternoon | غالباً مشغول (نهاية أسبوع عمل) |
| Thursday-Friday | تجنّب outreach (نهاية أسبوع KSA) |
| Ramadan | تخفيض 30%، nights better than days |
| Summer (Jun-Aug) | C-suite يسافر، follow-up أكثر من initial |
| Hajj/Eid | لا outreach اسبوع كامل قبل وبعد |

## 10.3 الـ Channel rules

| Channel | متى | متى لا |
|---------|-----|--------|
| LinkedIn DM | warm intro فقط، personalized | لا للـ bulk |
| WhatsApp | بعد إذن لفظي صريح في مكالمة | لا cold ever |
| Email | follow-up رسمي، proposals | لا spam |
| Phone call | بعد LinkedIn rapport | لا cold call أول مرة |
| In-person event | الأقوى، استثمر | يحتاج تخطيط |

## 10.4 Language tone

- **عربي** للـ 80% من الجمهور — حتى لو يجاوب إنجليزي، ابدأ عربي
- **الـ formal "أنتم"** في الكتابة، الـ informal "أنت" في المكالمة بعد الـ rapport
- **لا تستخدم slang** — يفقد المهنية
- **الـ emojis** في WhatsApp مقبول معتدل، في email ممنوع، في proposal ممنوع تماماً

---

# Part 11 — Operational Risk Register (First 14 Days)
## سجل المخاطر التشغيلية — أول 14 يوم

## 11.1 Risk matrix

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| R-01 | Moyasar في test mode عند إرسال invoice حقيقي | متوسط | عالي جداً | run `scripts/moyasar_live_cutover.py` قبل أول proposal، confirm via `/api/v1/founder/launch-status` |
| R-02 | Gmail OAuth غير مهيأ على Railway | متوسط | عالي | run `scripts/zatca_preflight.py`، fallback إلى founder personal email |
| R-03 | فقدان أول lead بسبب slow follow-up | عالي | عالي | SLA: contact ≤ 24h، evening loop checklist |
| R-04 | Demo يظهر feature في `Pilot` status | متوسط | عالي جداً | pre-demo checklist: open `no_overclaim.yaml` |
| R-05 | Cold WhatsApp accidentally sent | منخفض | حرج | non-negotiable في الـ code، manual review لكل بضاعة |
| R-06 | Proposal بدون disclaimer | متوسط | عالي | proposal_renderer enforces bilingual disclaimer |
| R-07 | عميل يطلب refund > 500 SAR | منخفض | متوسط | Hard Gate (Part 8) — founder only |
| R-08 | Pricing mismatch بين docs و YAML | عالي حالياً | متوسط | Appendix C — reconcile قبل proposal #1 |
| R-09 | Lead في Tier D يستهلك ساعات founder | عالي | متوسط | qualification rubric صارم، 15-min cap |
| R-10 | AEO content يخالف no_overclaim | متوسط | عالي | content_block: check register قبل publish |
| R-11 | Demo recording يخزّن PII عميل | منخفض | حرج (PDPL) | demo بـ synthetic data فقط، recording إذن مكتوب |
| R-12 | Proposal expires بدون follow-up | عالي | متوسط | day-12 reminder automated في founder calendar |

## 11.2 Weekly risk review (Sunday)

- [ ] أي risk تحقق هذا الأسبوع؟
- [ ] أي risk جديد ظهر؟
- [ ] mitigation أي risk فشل؟
- [ ] هل أي risk يحتاج تصعيد لـ legal/finance؟

---

# Part 12 — Communication Templates (Founder Drafts)
## نماذج التواصل — مسودات المؤسس

كل template هنا = draft للمؤسس، لا يُرسل تلقائياً. الـ founder ينسخ، يخصص، يرسل يدوياً.

## 12.1 Warm intro LinkedIn DM (3 variants)

**Variant A — Direct value**
> "أهلاً [الاسم]. شفت [post/announcement محدد]. عندي تشخيص مجاني (10 دقائق) يكشف كم lead بيضيع أسبوعياً من بطء الرد. لو في وقت 15 دقيقة هذا الأسبوع، Sunday 10am يمشي؟"

**Variant B — Mutual connection**
> "[الاسم]، [اسم مشترك] ذكرك في سياق [topic]. أبني Dealix — Revenue Ops طبقة فوق CRM للسوق السعودي. تشخيص مجاني لو تحب نشوف ناسب — 10 دقائق فقط."

**Variant C — Trigger-based**
> "[الاسم]، شفت [trigger: announcement, hiring, expansion]. الـ pattern اللي أشوفه: بعد X، الـ leads تزداد بسرعة أكبر من فريق المتابعة. تشخيص مجاني نشوف فيه إذا في فجوة. 10 دقائق هذا الأسبوع؟"

## 12.2 Discovery scheduling email

**Subject:** Discovery 15 دقيقة — Dealix Revenue Ops

> "أهلاً [الاسم]،
>
> شكراً للاهتمام. كما اتفقنا — Discovery قصير 15 دقيقة عشان نقيّم هل في fit.
>
> الجدول المقترح:
> - [Day] [Time] KSA
> - [Day] [Time] KSA
>
> Calendly: [link]
>
> أرسل لي confirmation أو slot بديل.
>
> Bassam Assiri
> Founder, Dealix
> bassam.m.assiri@gmail.com"

## 12.3 Pre-demo confirmation email

**Subject:** Demo Dealix غداً [date] — تحضير سريع

> "[الاسم]، تأكيد demo غداً [day] [time] KSA (مدة 30 دقيقة).
>
> قبل الديمو، لو تقدر تحضّر:
> 1. مثال على lead ضاع مؤخراً (بدون PII)
> 2. تقدير: كم lead/أسبوع، متوسط قيمة الـ deal
> 3. الـ stack الحالي (CRM، WhatsApp Business، إلخ)
>
> Meeting link: [Zoom/Meet]
>
> أراك غداً.
> Bassam"

## 12.4 Post-demo follow-up (within 24h)

**Subject:** ملخص demo + Proposal Dealix Mini Sprint

> "[الاسم]، شكراً للوقت اليوم.
>
> الملخص:
> - الـ pain: [اقتباس Q5]
> - التكلفة المقدرة: [Q6 رقم]/أسبوع
> - الـ next step المتفق عليه: Mini Sprint 499 SAR، 3 أيام
>
> العرض مرفق (PDF، صالح 14 يوم).
>
> الـ payment link لـ 250 SAR مقدم: [Moyasar URL]
>
> لو تحب نراجع العرض قبل التوقيع، 15 دقيقة [day] [time]؟
>
> Bassam"

## 12.5 Proposal expiry reminder (day 12)

**Subject:** عرض Dealix [REF] — يومين متبقية

> "[الاسم]، فقط تذكير ودي — العرض المرفق [REF] صالح حتى [date]. يومين متبقية.
>
> لو تحتاج وقت إضافي، نقدر نمدّد بنفس السعر — أرسل لي طلب تمديد رسمي.
>
> لو القرار صار 'لا'، أحترم رأيك — قل لي السبب لو ممكن (يساعدنا نحسن).
>
> Bassam"

## 12.6 Nurture sequence (Tier C, monthly)

**Month 1 (post-Discovery):**
> "[الاسم]، نشرنا تحليل [topic] هذا الأسبوع — قد يهمك: [link]. لا redirect، فقط مشاركة."

**Month 2:**
> "[الاسم]، شفت [industry event/news]. تذكرتك. لو تغيّرت الأولويات، أنا هنا."

**Month 3:**
> "[الاسم]، 90 يوم من آخر محادثة. تحب نعيد التشخيص المجاني؟ في features جديدة قد تناسب."

## 12.7 Polite decline (Tier D / disqualified)

> "[الاسم]، شكراً للمحادثة الصريحة. بناءً على ما شاركته، أعتقد إن Dealix مو الـ fit الصحيح حالياً — [reason محدد بأدب].
>
> توصية بديلة: [tool/approach مختلف]. لو وضعكم تغير، عندك رقمي.
>
> Bassam"

---

# Part 13 — Metrics & Definitions of Done
## المقاييس وتعريفات الإنجاز

## 13.1 الـ Core 8 metrics (تتبع يومي)

| Metric | Definition | Source | Target W1 | Target W2 |
|--------|------------|--------|-----------|-----------|
| warm_contacts_sent | unique people contacted via warm channel | `gtm_conversation_tracker.csv` | 25 | 25 |
| discovery_completed | 15-min call done + score in tracker | tracker | 5 | 8 |
| qualification_score_avg | mean Score across week | tracker | 60+ | 65+ |
| demos_booked | calendar invite + accepted | calendar | 2 | 3 |
| demos_completed | demo done + debrief filled | `founder_meeting_debrief_template.yaml` | 1 | 3 |
| proposals_sent | PDF sent + payment link generated | Moyasar + email | 1 | 2 |
| paid_revenue_sar | actual SAR received | Moyasar dashboard | 0 | 499+ |
| objections_logged | new objection ids added | `objection_engine_registry.yaml` | 5 | 8 |

## 13.2 Definitions of Done (per stage)

**Discovery DoD:**
- 10+ من 12 سؤال مجاب
- Score مسجّل (0-100)
- Tier محدد (A1/A2/B/C/D)
- Next action مع date
- entry في `gtm_conversation_tracker.csv`
- event `discovery_completed` في `evidence_events_tracker.csv`

**Demo DoD:**
- 30 دقيقة مكتملة بدون feature خارج Production
- recording مع إذن (نص فقط)
- `founder_meeting_debrief_template.yaml` ممتلئ
- next action صريح (proposal أو pause مع reason)
- event `demo_completed` مسجّل

**Proposal DoD:**
- PDF bilingual generated عبر `proposal_renderer`
- كل ادعاء = no_overclaim Production/Partial
- VAT 15% line منفصل
- Disclaimer موجود
- صلاحية 14 يوم محددة
- Reference number فريد
- Payment link Moyasar valid (لا sk_test_ في production)
- founder signature

**Closed Won DoD:**
- 50% مقدم في Moyasar (confirmed)
- ZATCA invoice issued (PDF + XML)
- Kickoff session مجدول خلال 7 أيام
- DPA موقّعة
- entry `closed_won` في tracker
- Slack/email confirmation للعميل

## 13.3 Quality gates (weekly)

- لو qualification_score_avg < 50 → الـ qualification متساهلة جداً
- لو demos_completed / demos_booked < 70% → الـ booking ضعيف
- لو proposals_sent / demos_completed < 50% → الـ demo لا يقفل
- لو objections_logged < 3 → الـ Discovery سطحي

---

# Appendix A — First 14 Days Action Plan

## Week 1 (May 24-30)

| Day | Date | Primary action | Secondary |
|-----|------|----------------|-----------|
| 1 | Sun May 24 | Launch playbook + warm list draft (25 names) | AEO post #1 |
| 2 | Mon May 25 | Outreach round 1 (10 contacts) | Discovery scheduled goal: 2 |
| 3 | Tue May 26 | Outreach round 2 (10 contacts) | Discovery #1 |
| 4 | Wed May 27 | Discovery #2 + demo prep | AEO post #2 |
| 5 | Thu May 28 | Demo #1 + outreach (5 contacts) | proposal draft |
| 6 | Fri May 29 | Friction log review + content | rest/personal |
| 7 | Sat May 30 | Weekly scorecard + plan W2 | AEO post #3 |

## Week 2 (May 31 - Jun 6)

| Day | Date | Primary action | Secondary |
|-----|------|----------------|-----------|
| 8 | Sun May 31 | Demo #2 + proposal sent | Discovery #3 |
| 9 | Mon Jun 1 | Outreach round 3 (10 contacts) | follow-up proposal #1 |
| 10 | Tue Jun 2 | Demo #3 + objection review | AEO post #4 |
| 11 | Wed Jun 3 | Proposal #2 sent | Discovery #4 |
| 12 | Thu Jun 4 | Negotiation calls + proposal #3 | AEO post #5 |
| 13 | Fri Jun 5 | Close push + invoice generation | refinements |
| 14 | Sat Jun 6 | **TARGET: 1 closed paid Rung 1** + weekly review | retro + W3 plan |

---

# Appendix B — Critical File References

| Need | File path |
|------|-----------|
| Pricing canonical | `/home/user/dealix/dealix/config/pricing.yaml` |
| No-overclaim register | `/home/user/dealix/dealix/registers/no_overclaim.yaml` |
| Qualification score | `/home/user/dealix/docs/sales/QUALIFICATION_SCORE.md` |
| Client selection | `/home/user/dealix/docs/sales/CLIENT_SELECTION_DECISION.md` |
| Existing playbook | `/home/user/dealix/docs/commercial/operations/FOUNDER_SALES_PLAYBOOK_AR.md` |
| Objection registry | `/home/user/dealix/docs/commercial/operations/objection_engine_registry.yaml` |
| Demo script (short) | `/home/user/dealix/docs/commercial/MARKET_INTELLIGENCE_DEMO_SCRIPT_AR.md` |
| Demo script (30 min) | `/home/user/dealix/docs/sales-kit/dealix_demo_script_30min.md` |
| Pilot agreement | `/home/user/dealix/docs/sales/PILOT_AGREEMENT_DRAFT.md` |
| Full pilot agreement | `/home/user/dealix/docs/sales-kit/dealix_pilot_agreement.md` |
| Battlecards v2 | `/home/user/dealix/docs/sales-kit/dealix_competitor_battlecards_v2.md` |
| Warm list workflow | `/home/user/dealix/docs/sales-kit/WARM_LIST_WORKFLOW.md` |
| Weekly scorecard | `/home/user/dealix/docs/commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md` |
| AEO content calendar | `/home/user/dealix/docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md` |
| Founder debrief | `/home/user/dealix/docs/commercial/operations/founder_meeting_debrief_template.yaml` |
| Founder weekly decision | `/home/user/dealix/docs/commercial/operations/founder_weekly_decision_template.yaml` |
| Evidence tracker | `/home/user/dealix/docs/commercial/operations/evidence_events_tracker.csv` |
| Conversation tracker | `/home/user/dealix/docs/commercial/operations/gtm_conversation_tracker.csv` |
| Soft launch tracker | `/home/user/dealix/docs/commercial/operations/soft_launch_meetings_tracker.yaml` |

---

# Appendix C — Pricing Reconciliation Note

**Discrepancy flagged:**

`dealix/config/pricing.yaml` (canonical YAML) lists:
- diagnostic: 4,999 / 9,999 / 15,000 / 25,000 SAR
- sprint: from 25,000 SAR
- retainer: 4,999 – 35,000 SAR/mo

The master plan brief (and this playbook) uses a different ladder:
- Rung 0: Free Diagnostic
- Rung 1: Mini Sprint 499 SAR
- Rung 2: Data Pack 1,500 SAR
- Rung 3: Managed Ops 2,999 / 4,999 / 7,999 SAR/mo
- Rung 4: Custom AI 5K-25K SAR
- Rung 5: Executive Command Center 12K-25K SAR/mo

**Action required from founder before sending any external proposal:**
1. Decide which ladder is the canonical one going forward.
2. Update `dealix/config/pricing.yaml` to match the chosen ladder (or update this playbook to match YAML).
3. Re-sync `TRUST_PACK_PROPOSAL_AR.md` and `FOUNDER_SALES_PLAYBOOK_AR.md` (currently reference ten_lead_audit at 499 and agency_proof_pack at 990, neither in YAML).
4. Add `pricing_5_rung_ladder` claim to `no_overclaim.yaml` once decided.

**Until reconciled:** all external pricing communications must be founder-approved manually. Do not let any automated proposal renderer ship with conflicting price anchors.

---

# Appendix D — Disclaimers (paste into every proposal)

**عربي:**
> "النتائج التقديرية ليست نتائج مضمونة. Dealix يقدّم تشخيص، توصيات، وتوثيق قرارات — لا يضمن أرقام إيرادات أو عملاء. كل ادعاء فني في هذا العرض موثّق في سجل الادعاءات الداخلي. PDPL: DPA موقّعة قبل أي معالجة بيانات. ZATCA: فواتير Phase 2 compliant. صلاحية العرض ١٤ يوم من تاريخ الإصدار."

**English:**
> "Estimated outcomes are not guaranteed outcomes. Dealix provides diagnosis, recommendations, and decision documentation — not revenue or customer-count guarantees. Every technical claim in this proposal is tracked in the internal no-overclaim register. PDPL: DPA signed before any data processing. ZATCA: Phase 2 compliant invoicing. Proposal valid for 14 days from issue date."

---

**End of playbook.**

**Review cadence:** Sunday weekly during Days 1-14. Major revision at Day 14 retro.
**Owner:** Bassam Assiri.
**Next review:** 2026-05-31 (end of W1).
