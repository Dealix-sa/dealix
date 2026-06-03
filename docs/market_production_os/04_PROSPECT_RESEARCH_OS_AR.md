# Prospect Research OS — بحث العملاء المحتملين — Prospect Research OS

> الموضع في العمود الفقري: المكوّن الرابع في طبقة *Market Production OS*.
> راجع [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) §4 (مقياس Prospect) قبل أي توسيع هنا.

هذا المستند يحدّد **كيف يولَّد العميل المحتمل (prospect) بطريقة مشروعة فقط**، وكيف يُسجَّل،
ويُقيَّم، وينتقل بين حالاته حتى يصبح جاهزًا للمصنع. المبدأ الحاكم: **لا مُدخَل بلا مصدر معلن**،
ولا تقييم بلا أدلة. هذه الطبقة لا تكتب رسائل ولا ترسل — هي تجهّز المادة الخام للمصنع.

---

## 1. مصادر مسموحة فقط (Allowed Sources)

البحث هنا **يدوي أو مزوّد من المؤسس أو من الويب العام** — لا غير. كل prospect يحمل حقل
`source` يصف من أين جاء، ويُربط بـ `data_os.SourcePassport`: **لا يدخل أي سجل دون مصدر قانوني معلن.**

| المصدر | الوصف | الحالة |
|---|---|---:|
| `founder_supplied` | قائمة قدّمها المؤسس من شبكته/اجتماعاته | مسموح |
| `public_web_manual` | بحث ويب عام يدوي (موقع الشركة، صفحة «من نحن»، سجل تجاري عام) | مسموح |
| `inbound` | الشركة تواصلت أولًا (نموذج، رد، إحالة) | مسموح |
| `referral` | إحالة من عميل/شريك موثّق | مسموح |
| `linkedin_company_search` | بحث عام عن صفحة الشركة (manual, founder-approved per call) — توثيق يدوي فقط | مسموح بشرط |
| `partner_intro` | تعريف من شريك في `partnership_os` | مسموح |

### مصادر محظورة — تُرفض عند الإدخال (Blocked)

هذه ليست قدرات في Dealix؛ هي **سلوكيات ممنوعة** نمنعها عند البوابة:

- أي scraping آلي لمواقع أو دلائل أو شبكات.
- أتمتة LinkedIn أو سحب جهات الاتصال آليًا من أي شبكة مهنية.
- قوائم بريد مشتراة أو مُسرَّبة أو مستأجرة.
- أرقام واتساب مجمّعة للتواصل البارد.
- أي مصدر يخالف شروط الخدمة لمنصة المصدر.

> أي محاولة إدخال من مصدر محظور → يرفضها `revenue_os.anti_waste.validate_pipeline_step`
> برمز `blocked_source`، ولا يُنشأ السجل. (انظر [`07_COMPLIANCE_DELIVERABILITY_OS_AR.md`](07_COMPLIANCE_DELIVERABILITY_OS_AR.md).)

---

## 2. كائن Prospect — الحقول

المخطط المقروء آليًا (machine-readable) هو `schemas/prospect.schema.json` (قيد البناء من المؤسس).
الحقول الأساسية:

```json
{
  "prospect_id": "string",
  "company": "string",
  "sector": "string",
  "website": "string|null",
  "size_band": "micro|small|mid|large|null",
  "decision_maker_role": "string|null",
  "source": "founder_supplied|public_web_manual|inbound|referral|linkedin_company_search|partner_intro",
  "source_passport_id": "string",
  "lawful_basis": "legitimate_interest|consent|contract",
  "pain_hypothesis": "string",
  "evidence_refs": ["string"],
  "prospect_score": 0,
  "score_breakdown": { "sector_fit": 0, "likely_lead_flow": 0, "decision_maker_clarity": 0, "pain_signal": 0, "payment_ability": 0, "personalization_signal": 0, "risk_low": 0 },
  "personalization_level": "P0|P1|P2|P3|P4",
  "risk_level": "low|medium|high",
  "state": "researched",
  "suppression_checked": false,
  "governance_decision": "string|null"
}
```

> لا PII خام في السجل: لا بريد، ولا جوال، ولا هوية وطنية. التواصل الفعلي يُدار في طبقة الإرسال
> بعد الموافقة، لا في سجل البحث.

---

## 3. مقياس Prospect (مجموع = 100)

نفس المقياس في المرجع الرئيسي — **لا تغيّر الأوزان.** التقييم يدوي/مدعوم بأدلة، وكل عامل يحتاج `evidence_ref`:

| العامل | الوزن | ما يقيسه |
|---|---:|---|
| `sector_fit` | 20 | مطابقة القطاع لملف `revenue_os/saudi_targeting_profile` |
| `likely_lead_flow` | 20 | احتمال وجود تدفّق عملاء يستفيد من Dealix |
| `decision_maker_clarity` | 15 | وضوح صاحب القرار ودوره |
| `pain_signal` | 15 | قوة دليل الألم (إشارة موثّقة لا تخمين) |
| `payment_ability` | 15 | القدرة على الدفع ضمن السلّم الخماسي |
| `personalization_signal` | 10 | توفّر مادة تخصيص حقيقية (≥ P1) |
| `risk_low` | 5 | انخفاض المخاطر (قطاع غير شديد التنظيم، مصدر نظيف) |

**حدّ التأهيل: 60/100.** أقل من 60 → `nurture` أو `do_not_contact`، ولا يدخل المصنع.

مستويات التخصيص: `P0` قطاع فقط · `P1` شركة+قطاع · `P2` ألم من موقع/وظيفة/محتوى ·
`P3` trigger حديث · `P4` proof/offer مخصص. **لا يُمرَّر أي prospect للمصنع بأقل من P1.**

---

## 4. حالات Prospect (State Machine)

كل سجل يمرّ بحالات معرّفة. الانتقال يحتاج شرطًا، ولا قفز للأمام دون استيفائه:

| الحالة | المعنى | شرط الانتقال التالي |
|---|---|---|
| `researched` | جُمع وسُجّل بمصدر معلن | تقييم بالمقياس |
| `qualified` | score ≥ 60 + P1 على الأقل | يدخل المصنع |
| `draft_ready` | جاهز للمصنع (قطاع/عرض/ألم محدد) | توليد مسودة |
| `drafted` | أُنتجت مسودة (`send_status=draft`) | يدخل بوابة الجودة |
| `approved` | اعتمد المؤسس المسودة | ضمن سقف الإرسال اليومي |
| `sent` | أُرسلت دفعة معتمدة | انتظار رد |
| `replied` | وصل رد | تصنيف الرد |
| `meeting_booked` | حُجز اجتماع | تحضير مقترح |
| `proposal_needed` | يحتاج مقترحًا | إنتاج المقترح |
| `proposal_sent` | أُرسل المقترح | متابعة |
| `won` | تحوّل عميل | إغلاق إيجابي |
| `lost` | لم يتحوّل | أرشفة + تعلّم |
| `nurture` | غير جاهز الآن، يُعاد لاحقًا | إعادة تقييم دورية |
| `do_not_contact` | محظور التواصل نهائيًا | لا إجراء — إقفال |

> الحالات `approved`, `sent`, `replied` يملكها فعليًا `approval_center` وطبقة الإرسال
> (انظر [`08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md`](08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md)).
> هذا المستند يهتم أساسًا بـ `researched → qualified → draft_ready`.

---

## 5. معالجة Suppression وdo_not_contact

قبل أي ترقية إلى `draft_ready`، **يجب** ضبط `suppression_checked = true`:

- إذا كان النطاق/الشركة في قائمة `schemas/suppression.schema.json` → الحالة فورًا `do_not_contact`.
- أي طلب opt-out سابق أو شكوى → `do_not_contact` دائم، ولا يُعاد فتحه آليًا.
- قطاع شديد التنظيم بلا أساس قانوني واضح → `nurture` حتى يكتمل الأساس.

> فحص suppression هنا **استباقي** (قبل المسودة)؛ والفحص النهائي يتكرر عند الإرسال
> كشرط من شروط بوابة الإرسال الستة. الفحص مرتين تصميم مقصود لا تكرار زائد.

---

## 6. الربط مع الطبقات الأخرى

- المصدر القانوني: `data_os.SourcePassport` — كل prospect = passport واحد على الأقل.
- التقييم القطاعي: `revenue_os/saudi_targeting_profile` + `revenue_os/account_scoring`.
- المخرج التالي: [`05_SIGNAL_DETECTION_OS_AR.md`](05_SIGNAL_DETECTION_OS_AR.md) يضيف الإشارات ويرفع `pain_signal`.
- الاستهلاك: [`06_COLD_EMAIL_DRAFT_FACTORY_AR.md`](06_COLD_EMAIL_DRAFT_FACTORY_AR.md) يقرأ فقط prospects بحالة `qualified`/`draft_ready`.
- العقيدة: المرجع الرئيسي §1 (اللاءات الإحدى عشرة).

---

## EN summary

`Prospect Research OS` is the fourth component of the Market Production OS. It ingests prospects
**only** from lawful sources — founder-supplied lists, manual public-web research, inbound,
referrals, partner intros, and `linkedin_company_search` (manual, founder-approved per call).
Scraping, LinkedIn automation, purchased lists, and bulk cold-WhatsApp contact lists are
**blocked behaviors**, rejected at ingestion via `revenue_os.anti_waste` with `blocked_source`.
Every prospect carries a declared `source` tied to `data_os.SourcePassport`; no record exists
without a lawful basis, and no raw PII is stored. Each prospect is scored on the 7-factor model
(sum = 100, qualify threshold = 60) and assigned a personalization level (P0–P4); nothing below
P1 is passed to the factory. The state machine runs `researched → qualified → draft_ready →
drafted → approved → sent → replied → meeting_booked → proposal_needed → proposal_sent → won /
lost`, with `nurture` and `do_not_contact` as terminal/holding states. Suppression is checked
before draft-readiness and again at send time. The machine-readable contract is
`schemas/prospect.schema.json`.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
