# Cold Email Draft Factory — مصنع مسودات البريد (250/يوم) — Cold Email Draft Factory

> الموضع في العمود الفقري: المكوّن السادس في طبقة *Market Production OS*.
> راجع [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) §0 (250 مسودة، صفر إرسال) و§4.

هذا المستند يحدّد **مصنع الإنتاج اليومي**: كيف تتحوّل prospects المؤهَّلة وإشاراتها إلى **250
مسودة جاهزة للمراجعة في اليوم**. القاعدة الحاسمة، وهي عقيدة المصنع كلها:

> **المصنع يُنتج مسودات فقط (`send_status = "draft"`). لا يُرسل أبدًا.**
> كل مسودة تُصفّ في بوابة الموافقة، ولا تتحوّل إلى إرسال إلا عبر المؤسس ضمن سقف يومي.
> `DAILY_DRAFT_TARGET = 250` · `MAX_AUTO_SENDS = 0`.

هذا ليس spam: الكثافة في **الإنتاج المحكوم**، لا في الإرسال. الإرسال مقيّد ببوابة بشرية وتدرّج.

---

## 1. كائن Draft — الحقول

المخطط المقروء آليًا: `schemas/outreach_draft.schema.json` (قيد البناء من المؤسس). المصنع
يُركّب `revenue_os/draft_pack` لإنتاج كل كائن:

```json
{
  "draft_id": "string",
  "prospect_id": "string",
  "company": "string",
  "sector": "string",
  "recipient_role": "string",
  "source": "founder_supplied|public_web_manual|inbound|referral|linkedin_company_search|partner_intro",
  "pain_hypothesis": "string",
  "personalization_note": "string",
  "offer": "0|1|2|3|4|enterprise",
  "subject": "string",
  "body": "string",
  "cta": "string",
  "language": "ar|en",
  "evidence_level": "L0|L1|L2|L3|L4|L5",
  "risk_level": "low|medium|high",
  "compliance_status": "pending|pass|fail",
  "approval_status": "pending|approved|rejected|rewrite",
  "send_status": "draft",
  "unsubscribe_included": true,
  "governance_decision": "string|null"
}
```

ملاحظات إلزامية على الحقول:

- `send_status` يبدأ **دائمًا** بقيمة `"draft"` ولا يغيّره المصنع. تغييره لاحقًا حصري لطبقة الإرسال.
- `unsubscribe_included` يجب أن يكون `true` قبل أي تمرير لبوابة الجودة.
- `recipient_role` **دور عام** (مثل «مدير المبيعات»)، لا اسم شخص ولا بريد ولا جوال — لا PII في المسودة.
- `compliance_status` و`approval_status` يبدآن `pending`؛ يحدّدهما المكوّنان 7 و8، لا المصنع.

---

## 2. قواعد التخصيص P0–P4

مستويات التخصيص نفسها في المرجع الرئيسي §4. القاعدة الحاكمة للمصنع:

> **لا تُنتَج مسودة أقل من P1 أبدًا.** أي مسودة بمستوى P0 تُرفض داخليًا قبل الصف.

| المستوى | الأساس | مثال على `personalization_note` |
|---|---|---|
| `P0` | قطاع فقط | (محظور كمخرج — لا يُصَفّ) |
| `P1` | شركة + قطاع | «[الشركة] في قطاع [X] — طبقة قرار للبيانات» |
| `P2` | ألم من موقع/وظيفة/محتوى | «لاحظت بحثكم عن [role]…» |
| `P3` | trigger حديث | «بعد إطلاق [خدمة] الشهر الماضي…» |
| `P4` | proof/offer مخصص | «نمط مشابه لـ [قطاع] — حالة آمنة مفترضة» |

- التخصيص يُبنى من حقول prospect + company/job signals (المكوّن 5)، لا من تخمين.
- كل مستوى أعلى من P1 يحتاج `evidence_ref` من طبقة الإشارات.
- اللغة (`language`) تُختار بحسب القطاع والجمهور: عربي افتراضيًا للقارئ السعودي، إنجليزي عند المناسبة.

---

## 3. مزيج الإنتاج اليومي (الهدف 250)

المصنع يوزّع الـ 250 على خمسة أنواع، لتوازن بين فتح علاقات جديدة ومتابعة القائم وإغلاق الحلقات:

| النوع | العدد اليومي | الوصف |
|---|---:|---|
| First-touch | 100 | أول تواصل مع prospect مؤهَّل جديد |
| Follow-up-1 | 75 | متابعة أولى لمن لم يردّ |
| Follow-up-2 | 50 | متابعة ثانية أخيرة قبل `nurture` |
| Proposal-intro | 15 | تمهيد لمقترح بعد اهتمام |
| Close-loop | 10 | إغلاق مهذّب لحلقة (إعادة جدولة/شكر/إحالة) |
| **المجموع** | **250** | |

- المتابعات (`follow-up`) لا تُرسَل آليًا — تُنتَج كمسودات وتنتظر الموافقة كأي مسودة.
- المتابعة الثانية الأخيرة تتضمّن مسارًا مهذّبًا للخروج (لا إلحاح، لا ضغط شراء).
- إذا لم تكفِ prospects المؤهَّلة لملء نوع ما، يُسجَّل العجز في تقرير اليوم ولا يُملأ بمسودات منخفضة الجودة.

---

## 4. تدفّق الإنتاج داخل المصنع

```txt
prospects (qualified/draft_ready)
  + job/company signals (P-level + message_angle)
→ draft_factory يختار العرض من السلّم الخماسي
→ يبني subject + body + CTA + personalization_note
→ يضبط send_status="draft" · unsubscribe_included=true
→ يضع compliance_status="pending" · approval_status="pending"
→ يربط governance_decision (لا مخرج بلا قرار حوكمة)
→ يُصَفّ في بوابة الجودة (المكوّن 7)
```

المصنع **لا يلمس** أي قناة إرسال، ولا يستدعي SMTP أو واجهة بريد. مخرجه كائنات بيانات فقط.

---

## 5. ما هو محظور في المصنع (Hard Rules)

- **لا إرسال** بأي شكل — المخرج مسودات بحالة `draft` حصرًا.
- لا مواضيع مضللة، ولا `Re:`/`Fwd:` زائفة، ولا انتحال علاقة سابقة غير موجودة.
- لا مسودة بلا `unsubscribe_included = true`.
- لا ادعاء نتيجة أو رقم مبيعات؛ الصياغة «فرص مُثبتة بأدلة»/«نمط حالة آمنة»، لا «نضمن مبيعات».
- لا PII في `recipient_role` أو `body` أو `subject`.
- لا مصدر من قائمة محظورة (scraping، أتمتة LinkedIn، قوائم مشتراة، واتساب بارد).
- لا مسودة من prospect بحالة `do_not_contact` أو في قائمة suppression.

> هذه القواعد يفرضها لاحقًا المكوّن 7 (بوابة الجودة والامتثال)، لكن المصنع يلتزم بها **استباقيًا**
> ليقلّل الرفض. (انظر [`07_COMPLIANCE_DELIVERABILITY_OS_AR.md`](07_COMPLIANCE_DELIVERABILITY_OS_AR.md).)

---

## 6. لماذا 250 مسودة وصفر إرسال؟

| المنطق | الأثر |
|---|---|
| الإنتاج رخيص، الإرسال مكلف السمعة | نولّد بسخاء ونرسل بحذر معتمد |
| المؤسس يرى أفضل 50 ويختار | جودة الإرسال ترتفع، والسمعة تُصان |
| كل مسودة قابلة للتدقيق قبل الإرسال | لا مفاجآت، لا خرق صامت |
| التعلّم من أنماط القبول/الرفض | المراجعة الأسبوعية تحسّن المصنع |

> الكثافة في الإنتاج المحكوم، لا في الإرسال. هذا هو الفارق بين Governed Market Production وspam.

---

## 7. الربط مع الطبقات الأخرى

- المدخل: [`04_PROSPECT_RESEARCH_OS_AR.md`](04_PROSPECT_RESEARCH_OS_AR.md) + [`05_SIGNAL_DETECTION_OS_AR.md`](05_SIGNAL_DETECTION_OS_AR.md).
- النواة المعاد استخدامها: `revenue_os/draft_pack` + `marketing_factory`.
- المخرج: بوابة الجودة [`07_COMPLIANCE_DELIVERABILITY_OS_AR.md`](07_COMPLIANCE_DELIVERABILITY_OS_AR.md) ثم بوابة الموافقة [`08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md`](08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md).
- العروض: السلّم الخماسي في المرجع الرئيسي §5.

---

## EN summary

The `Cold Email Draft Factory` is the sixth Market Production OS component and the daily
production core: it turns qualified prospects and their signals into **250 review-ready drafts per
day**. Its defining rule: the factory **produces drafts only** — every draft starts and stays at
`send_status = "draft"`, and the factory never touches a send channel or SMTP. Each draft carries
company, sector, recipient_role (generic role, no PII), source, pain_hypothesis,
personalization_note, offer, subject, body, CTA, language, evidence_level, risk_level,
compliance_status, approval_status, send_status (default `draft`), and unsubscribe_included
(must be `true`). Personalization never drops below P1, and any level above P1 requires a signal
evidence reference. The daily mix targets 100 first-touch, 75 follow-up-1, 50 follow-up-2, 15
proposal-intro, and 10 close-loop. Misleading subjects, fake Re:/Fwd:, missing unsubscribe, PII,
blocked sources, and any guaranteed-sales claim are forbidden — the factory enforces them
proactively before queuing to the quality gate. The factory composes `revenue_os/draft_pack`;
the schema is `schemas/outreach_draft.schema.json`. Density lives in governed production, never
in sending — that is the line between governed market production and spam.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
