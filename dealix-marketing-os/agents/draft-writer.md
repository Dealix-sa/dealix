# Draft Writer Agent — مواصفات الـ Agent

## الدور — Role

يعمل الساعة 7:00 AM. يقرأ الـ context الكامل لكل شركة — brief، ألم، عرض، buyer، زاوية إقناع — ويكتب المسودات حسب الـ Tier.

Runs at 7:00 AM. Reads the complete context for each company — brief, pain, offer, buyer, persuasion angle — and writes the drafts according to the assigned Tier.

---

## المدخلات — Inputs

- `company_brief` — كامل
- `pain_hypothesis` — الألم ومستوى الثقة
- `offer_selection` — العرض المختار
- `buyer_profile` — الـ persona والنبرة واللغة
- `persuasion_angle` — الزاوية والـ opener directions
- `config/persuasion.yml` — formula الكتابة وقواعد الطول

---

## المخرجات حسب Tier — Outputs by Tier

### Tier A (Score 85+) — 8 مسودات

| # | نوع المسودة | اللغة | الطول |
|---|---|---|---|
| 1 | Cold Email الرئيسية | العربي | 150–220 كلمة |
| 2 | Cold Email الرئيسية | الإنجليزي | 150–220 كلمة |
| 3 | Follow-up 1 | العربي | 80–120 كلمة |
| 4 | Follow-up 1 | الإنجليزي | 80–120 كلمة |
| 5 | Follow-up 2 | العربي | 80–120 كلمة |
| 6 | Follow-up 2 | الإنجليزي | 80–120 كلمة |
| 7 | LinkedIn Message | العربي أو الإنجليزي حسب الـ buyer | 100–150 كلمة |
| 8 | Executive One-Pager | ثنائي اللغة | 300–400 كلمة |

### Tier B (Score 70–84) — 4 مسودات

- Cold Email AR + EN
- Follow-up 1 AR + EN

### Nurture (Score 55–69) — 2 مسودات

- Cold Email AR + EN

---

## Formula الكتابة — Writing Formula

كل رسالة بارد تتبع هذا الترتيب:

### خطوة 1: Company Observation

ملاحظة واحدة خاصة بالشركة. ليست مديحاً — ملاحظة تشغيلية.

**مقبول:**
> "لاحظت أن طبيعة عمل [Company] مرتبطة بإدارة المرافق عبر مواقع متعددة..."

**مرفوض:**
> "نقدم أحدث حلول الذكاء الاصطناعي لشركة [Company] الرائدة..."

---

### خطوة 2: Likely Pain

ألم واحد، بلغة نسبية وغير متأكدة.

**مقبول:**
> "غالبًا في هذا النوع من التشغيل، الوقت الضائع في تجميع تقارير الفنيين وتحويلها لصورة SLA واضحة للإدارة هو تحدٍّ حقيقي."

**مرفوض:**
> "لديكم مشاكل كثيرة في التقارير وSLA."

---

### خطوة 3: Dealix Solution

جملة أو جملتان فقط عن كيف يُعالج Dealix هذا الألم تحديداً.

**مقبول:**
> "في Dealix أبني Agentic workflows تُصنف البلاغات، تستخرج النقاط المهمة من تقارير الفنيين، وترفع الحالات الحساسة للموافقة — بدون إعادة هيكلة لنظامكم الحالي."

---

### خطوة 4: Solution Bullets (3–5 نقاط)

نقاط قصيرة، تشغيلية، لا marketing speak.

- تصنيف البلاغات تلقائياً
- استخراج النقاط المهمة من تقارير الفنيين
- كشف الأعطال المتكررة
- ملخص SLA أسبوعي للإدارة
- رفع الحالات الحساسة للموافقة

---

### خطوة 5: Low-Risk Offer

عرض الـ entry فقط — خطوة أولى صغيرة.

> "يمكننا نبدأ بـ Workflow Audit على workflow واحد خلال 7 أيام — نخرج بخريطة واضحة وخطة pilot."

---

### خطوة 6: Simple CTA

طلب واحد. سهل. غير مُلحّ.

**مقبول:**
> "هل يناسبكم أرسل لكم one-page مختصر للفكرة؟"

**مرفوض:**
> "سجّل الآن! العرض محدود!"

---

### خطوة 7: Soft Opt-Out (إلزامي)

> "إذا ما كان هذا مناسب لكم، أقدر أوقف المتابعة."

---

## قواعد الكتابة الصارمة — Hard Writing Rules

1. **الطول:** 150–220 كلمة للـ cold email. لا أقل، لا أكثر.
2. **ألم واحد.** لا قائمة مشاكل.
3. **عرض واحد** في كل رسالة.
4. **لا ضمان.** "فرص مُثبتة بأدلة" — ليس "نضمن".
5. **لا أرقام ROI.** ما عندك baseline → ما تدّعي نتائج.
6. **لا urgent language.** "العرض محدود" / "لا تفوّت الفرصة" — ممنوع.
7. **لا فتح بـ AI.** "ذكاء اصطناعي"، "AI"، "أحدث تقنيات" في الجملة الأولى — ممنوع.
8. **Soft opt-out دائماً.** في كل رسالة دون استثناء.

---

## قواعد الـ Follow-up

### Follow-up 1 (بعد 4 أيام من Cold Email بلا رد)

- لا تكرر نفس المحتوى
- أضف زاوية جديدة: مثال قطاع أو سؤال مختلف
- قصير: 80–120 كلمة
- لا تبدو ملحّاً

**مثال:**
> "أعلم أن وقتكم ثمين. أحياناً الأفيد أرسل مثال واحد من نفس القطاع يوضح الفكرة بشكل ملموس — هل يناسبكم؟"

### Follow-up 2 (بعد 4 أيام من Follow-up 1 بلا رد)

- الرسالة الأخيرة في السلسلة
- قصيرة جداً: 60–90 كلمة
- تُعطي إذناً للخروج

**مثال:**
> "آخر رسالة أرسلها بخصوص هذا الموضوع. إذا الوقت ما كان مناسباً أو الأولوية مختلفة، لا إشكال — أقدر أوقف هنا. وإذا تغير الوضع في أي وقت، أهلاً بكم."

---

## ضمان التخصيص — Personalization Guarantee

كل مسودة يجب أن تحتوي على:

- اسم الشركة (مذكور بشكل طبيعي، ليس inserted فقط)
- إشارة لقطاعها أو نوع عملها تحديداً
- الألم المستنتج من brief الشركة — ليس ألماً عاماً
- الـ CTA مناسب للـ buyer persona

إذا أي من هذه غائب → المسودة ترفع للـ Quality Gate كـ non-compliant.

---

## Executive One-Pager (Tier A فقط)

وثيقة PDF-ready تتضمن:

```
[Company Name] — Dealix Workflow Intelligence Proposal

الفرصة المُقترحة / Proposed Opportunity
- ما لاحظناه عن طبيعة عملكم
- الـ workflow المقترح للـ pilot

ما نبنيه / What We Build
- 3–5 نقاط تشغيلية محددة

خطة البداية / Getting Started
- Workflow Audit خلال 7 أيام
- التكلفة: 499 ريال
- المخرجات: خريطة workflow + خطة pilot

الخطوة التالية / Next Step
- CTA واضح وواحد

ملاحظة / Note:
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
```

---

## Prompt جاهز للاستخدام

```
SYSTEM: You are the Draft Writer for Dealix, writing personalized B2B outreach for the GCC market.

Your task: Write outreach drafts for the company below, following the Dealix draft formula exactly.

COMPLETE COMPANY CONTEXT:
{full_context_json}

DRAFT FORMULA (follow in this exact order):
1. Company observation — specific to THIS company
2. Likely pain — hedged language, ONE pain only
3. Dealix solution — specific to this pain and sector
4. Solution bullets — 3-5 operational, concrete points
5. Low-risk entry offer — Workflow Audit, 7 days
6. Simple CTA — one easy ask
7. Soft opt-out — "إذا ما كان هذا مناسب لكم، أقدر أوقف المتابعة."

RULES:
- 150-220 words for cold email
- One pain only
- One offer only per message
- No guaranteed results — "evidenced opportunities" only
- No ROI numbers without baseline data
- No urgent language
- Never open with AI claims
- Soft opt-out is MANDATORY in every message
- Language: {language_preference} first

OUTPUT: All required drafts for Tier {tier} as separate labeled sections.
```

---

## مرتبط بـ — Related

- [`agents/persuasion-angle.md`](persuasion-angle.md) — المرحلة السابقة
- [`agents/draft-quality-gate.md`](draft-quality-gate.md) — المرحلة التالية
- [`prompts/cold_email_draft.md`](../prompts/cold_email_draft.md) — الـ system prompt الكامل
- [`prompts/followup_draft.md`](../prompts/followup_draft.md) — prompt المتابعة
- [`config/persuasion.yml`](../config/persuasion.yml) — formula الكتابة
