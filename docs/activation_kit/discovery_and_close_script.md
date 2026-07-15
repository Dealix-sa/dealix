# Discovery & Close Script — سكربت الاكتشاف والإغلاق

> A 20-30 minute discovery call script plus objection handling. Run this on the free diagnostic call. Score the call afterward with [`qualification_scorecard.md`](qualification_scorecard.md).

---

## القسم العربي

### بنية المكالمة (20–30 دقيقة)

| المرحلة | الزمن | الهدف |
|---|---|---|
| الفتح | 2–3 دقائق | بناء سياق، توضيح أن هذه محادثة عمل لا عرض بيع |
| تشخيص الألم | 8–10 دقائق | فهم كيف يستقبلون العملاء المحتملين وأين تتسرّب الفرص |
| رصد إشارات BANT الثماني | ضمن التشخيص | استخراج الإشارات طبيعياً، لا استجواباً |
| الانتقال إلى التوصية | 4–5 دقائق | ربط ما سمعته بالخطوة المنطقية |
| الإغلاق | 3–5 دقائق | تثبيت الخطوة التالية أو إعادة التأطير |

### الفتح

> "شكراً على وقتك. هذه ليست مكالمة بيع — هي 20 دقيقة ننظر فيها معاً إلى كيف تستقبلون العملاء المحتملين وأين تضيع الفرص. في النهاية أعطيك رأياً صريحاً، حتى لو كان أن Dealix ليس الأنسب لكم الآن. هل يناسبك أن أبدأ ببعض الأسئلة؟"

### تشخيص الألم — أسئلة مفتوحة

- "صف لي رحلة العميل المحتمل عندكم من أول تواصل حتى أول اجتماع."
- "كم عميلاً محتملاً تستقبلون شهرياً تقريباً؟ وكم نسبة من تردّون عليه؟"
- "حين تصلكم قائمة حسابات، كيف تقررون من تتواصلون معه أولاً؟"
- "ما الذي حاولتم حلّه سابقاً ولم ينجح؟"

### رصد إشارات BANT الثماني طبيعياً

اربط كل إشارة بسؤال محادثة عادي — لا تذكر كلمة "تأهيل" أمام العميل:

| الإشارة | سؤال طبيعي |
|---|---|
| pain_clear (وضوح الألم) | "أين تشعر أن أكبر تسرّب يحدث؟" |
| owner_present (مالك حاضر) | "من سيكون مسؤولاً عن سير العمل هذا من جانبكم؟" |
| data_available (بيانات متاحة) | "هل لديكم قائمة حسابات أو تصدير CRM يمكن العمل عليه؟" |
| accepts_governance (قبول الحوكمة) | "نعمل بسجل تدقيق ومسودات تعتمدونها قبل أي إرسال — هل هذا يناسبكم؟" |
| has_budget (وجود ميزانية) | "خطوة أولى بسعر ثابت 499 ريال — هل هذا ضمن ما يمكنكم البدء به؟" |
| wants_safe_methods (طرق آمنة) | "نحن لا نعمل كشط بيانات ولا تواصل بارد بالجملة — هل هذا متوافق مع ما تبحثون عنه؟" |
| proof_path_visible (مسار إثبات واضح) | "إذا أعطيناكم 10 حسابات مرتّبة ومسودات، هل لديكم من يستخدمها فعلاً؟" |
| retainer_path_visible (مسار احتفاظ) | "إذا نجح هذا، هل تتصوّرون تكراره شهرياً؟" |

### الانتقال إلى التوصية

> "بناءً على ما سمعته، أرى أن [أعد صياغة الألم بكلماته]. الخطوة المنطقية هي [السبرنت / تشخيص أصغر / لا شيء الآن]. دعني أوضح ما يعنيه ذلك بالضبط."

- نتيجة ≥ 85 → اعرض **سبرنت ذكاء الإيرادات (499 ريال)**.
- نتيجة 70–84 → اعرض خطوة أصغر / أعد تأطير النطاق.
- نتيجة 45–69 → اكتفِ بتسليم التشخيص المجاني المكتوب.
- نتيجة < 45 → أحِل العميل بأدب لجهة أنسب.

### الإغلاق (للنتيجة ≥ 85)

> "اقتراحي: سبرنت ذكاء الإيرادات. 7 أيام، 499 ريال سعر ثابت. تستلمون 10 حسابات مرتّبة، مسودات ثنائية اللغة، وحزمة إثبات من 14 قسماً. الدفع 50% عند القبول و50% عند تسليم حزمة الإثبات عبر رابط ميسر، بفاتورة متوافقة مع ZATCA. أوضّح نقطة مهمة: **النتائج التقديرية ليست نتائج مضمونة** — نَعِد بالمنهجية ومقاييس سجل التدقيق، لا بصفقات مغلقة. هل نبدأ؟"

عند الموافقة: أرسل العرض الرسمي من `../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2` ورابط دفع ميسر، وحدّث `pipeline_tracker.csv`.

### معالجة الاعتراضات

| الاعتراض | الرد |
|---|---|
| "هل العربية طبيعية؟" | "كل مسودة عربية وإنجليزية، وتراجعونها وتعتمدونها قبل أي استخدام. لا شيء يخرج دون موافقتكم. في التشخيص أريكم مثالاً على بياناتكم." |
| "عندنا CRM بالفعل" | "ممتاز — السبرنت لا يستبدل CRM، بل يعمل على تصديره: يقيس جودة البيانات، يدمج المكرّرات، ويرتّب الحسابات. نُكمّل أداتكم لا ننافسها." |
| "الوقت مبكّر علينا" | "لذلك الخطوة الأولى تشخيص مجاني، والسبرنت سعر ثابت 499 ريال و7 أيام فقط — أصغر التزام ممكن لرؤية دليل حقيقي." |
| "أرسل لي معلومات" | "سأرسل صفحة واحدة، لكن الأنفع 15 دقيقة على بياناتكم تحديداً. هل الثلاثاء أو الأربعاء أنسب؟" |
| "السعر / مرتفع؟" | "499 ريال سعر ثابت لـ 7 أيام عمل بمخرجات محددة و14 قسم إثبات. لا رسوم خفية. والدفع نصفين يقلّل المخاطرة عليكم." |

---

## English Section

### Call structure (20-30 minutes)

| Stage | Time | Goal |
|---|---|---|
| Open | 2-3 min | Build context, frame it as a working conversation, not a pitch |
| Diagnose pain | 8-10 min | Understand how they receive leads and where opportunity leaks |
| Surface the 8 BANT signals | within diagnosis | Extract signals naturally, not as an interrogation |
| Transition to recommendation | 4-5 min | Connect what you heard to the logical step |
| Close | 3-5 min | Lock the next step or reframe |

### Open

> "Thank you for your time. This is not a sales call — it is 20 minutes where we look together at how you receive leads and where opportunity is lost. At the end I give you a frank opinion, even if that opinion is that Dealix is not the right fit for you right now. May I start with a few questions?"

### Diagnose pain — open questions

- "Walk me through your lead's journey, from first contact to first meeting."
- "Roughly how many leads do you receive per month, and what share do you reply to?"
- "When an account list lands, how do you decide who to contact first?"
- "What have you tried before that did not work?"

### Surface the 8 BANT signals naturally

Tie each signal to an ordinary conversation question — never say the word "qualify" to the customer:

| Signal | Natural question |
|---|---|
| pain_clear | "Where do you feel the biggest leak happens?" |
| owner_present | "Who would own this workflow on your side?" |
| data_available | "Do you have an account list or CRM export we could work from?" |
| accepts_governance | "We work with an audit trail and drafts you approve before any send — does that suit you?" |
| has_budget | "A fixed-price first step at 499 SAR — is that within what you can start with?" |
| wants_safe_methods | "We do not scrape data or do bulk cold outreach — is that aligned with what you want?" |
| proof_path_visible | "If we hand you 10 ranked accounts and drafts, do you have someone who will actually use them?" |
| retainer_path_visible | "If this works, can you picture repeating it monthly?" |

### Transition to recommendation

> "Based on what I heard, I see that [reframe the pain in their words]. The logical step is [the Sprint / a smaller diagnostic / nothing right now]. Let me explain exactly what that means."

- Score ≥ 85 → present the **Revenue Intelligence Sprint (499 SAR)**.
- Score 70-84 → propose a smaller step / reframe scope.
- Score 45-69 → deliver only the written free diagnostic.
- Score < 45 → refer the customer out politely.

### Close (for score ≥ 85)

> "My recommendation: the Revenue Intelligence Sprint. 7 days, 499 SAR fixed price. You receive 10 ranked accounts, a bilingual draft pack, and a 14-section Proof Pack. Payment is 50% on acceptance and 50% on Proof Pack delivery via a Moyasar link, with a ZATCA-compliant invoice. One important point: **estimated outcomes are not guaranteed outcomes** — we promise methodology and audit-trail metrics, not closed deals. Shall we begin?"

On agreement: send the formal proposal from `../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2` and a Moyasar payment link, and update `pipeline_tracker.csv`.

### Objection handling

| Objection | Response |
|---|---|
| "Is the Arabic natural?" | "Every draft is in Arabic and English, and you review and approve it before any use. Nothing goes out without your approval. In the diagnostic I will show you a sample on your data." |
| "We already have a CRM" | "Good — the Sprint does not replace a CRM, it works on its export: it scores data quality, merges duplicates, and ranks accounts. We complement your tool, we do not compete with it." |
| "It is too early for us" | "That is exactly why the first step is a free diagnostic, and the Sprint is a fixed 499 SAR over just 7 days — the smallest possible commitment to see real evidence." |
| "Send me info" | "I will send a one-pager, but the more useful path is 15 minutes on your specific data. Does Tuesday or Wednesday work better?" |
| "The price / is it high?" | "499 SAR is a fixed price for 7 working days with defined deliverables and a 14-section Proof Pack. No hidden fees. And paying in two halves lowers your risk." |

### Mandatory disclaimer for the close

State verbatim, in both languages, before taking payment:

> **النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.**

Dealix promises methodology and audit-trail metrics (DQ score, duplicates merged, unsafe drafts blocked, draft count, proof score, capital assets) — never closed deals, pipeline lift, or revenue.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
