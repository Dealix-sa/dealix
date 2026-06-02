# محرك المتابعة — Dealix Follow-up Engine

هذا الملف يحدّد **إيقاع المتابعة** (Day 0/2/4/7 وما بعد الرد/الاكتشاف/العرض/التسليم للدفع/الإعداد/الدليل) و**مجموعة الأسئلة اليومية**. الكيان `followup` يحمل الحقول حرفياً: `id`, `prospect_id`, `due_date`, `channel`, `message_ref`, `status`, `risk`.

This file defines the **follow-up cadence** (Day 0/2/4/7 plus post-reply/discovery/proposal/handoff/onboarding/proof) and the **daily question set**. The `followup` entity carries the fields above verbatim.

روابط / Related: [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) · [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) · [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md)

---

## الإيقاع الأساسي / The base cadence

| اليوم / Day | الغرض / Purpose | القناة المقترحة / Suggested channel |
|---|---|---|
| Day 0 | تواصل أول (مسودة معتمَدة). / First contact (approved draft). | `preferred_channel` |
| Day 2 | متابعة خفيفة تضيف قيمة. / Light, value-adding follow-up. | نفس القناة |
| Day 4 | متابعة بزاوية مختلفة. / Follow-up from a different angle. | نفس القناة |
| Day 7 | متابعة أخيرة قبل `nurture`. / Final follow-up before `nurture`. | نفس القناة |

> بعد Day 7 بلا رد، ينتقل العميل إلى `nurture` بإيقاع دوري خفيف، لا إلحاح. / After Day 7 with no reply, the prospect moves to `nurture` on a light periodic rhythm — no badgering.

## الإيقاعات المشروطة / Conditional cadences

| المحفّز / Trigger | المتابعة / Follow-up |
|---|---|
| post-reply (بعد الرد) | تأهيل الرد خلال يوم؛ اقتراح اكتشاف. / Qualify within a day; propose discovery. |
| post-discovery (بعد الاكتشاف) | ملخص + خطوة تالية خلال يوم عمل. / Summary + next step within one business day. |
| post-proposal (بعد العرض) | متابعة قرار بعد 2 و5 أيام. / Decision follow-up at day 2 and 5. |
| post-handoff (بعد التسليم للدفع) | تأكيد جاهزية الدفع والموافقات. / Confirm payment readiness and approvals. |
| post-onboarding (بعد الإعداد) | تأكيد الوصول والمخرج الأول. / Confirm access and the first deliverable. |
| post-proof (بعد الدليل) | عرض الترقية/التجديد المناسب. / Present the right upsell/renewal. |

> كل رسالة متابعة = مسودة بانتظار موافقة؛ `message_ref` يشير إلى مسودة معتمَدة. لا إرسال آلي. / Every follow-up is a draft pending approval; `message_ref` points to an approved draft. No auto-send.

---

## حالات المتابعة / Follow-up states (`status`)

| الحالة / State | المعنى / Meaning |
|---|---|
| `scheduled` | مجدولة على `due_date`. / Scheduled on the due date. |
| `drafted` | المسودة جاهزة بانتظار موافقة. / Draft ready, pending approval. |
| `sent` | أُرسِلت يدوياً بعد الموافقة. / Manually sent after approval. |
| `replied` | ردّ العميل. / Prospect replied. |
| `skipped` | تُخطِّيت (سبب موثَّق). / Skipped (documented reason). |
| `closed` | انتهى الإيقاع لهذا العميل. / Cadence closed for this prospect. |

`risk` يُسجَّل عند أي مؤشر إزعاج/امتثال يستدعي تخطّي المتابعة. / `risk` is logged when any annoyance/compliance signal warrants skipping.

---

## مجموعة الأسئلة اليومية / The daily question set

تُراجَع كل صباح عمل قبل أي متابعة:

Reviewed each business morning before any follow-up:

1. من ردّ أمس ويحتاج إجراءً اليوم؟ / Who replied yesterday and needs action today?
2. أي متابعة مستحقة اليوم (`due_date = today`)؟ / Which follow-ups are due today?
3. أي عميل تجاوز Day 7 بلا رد ويجب نقله إلى `nurture`؟ / Who passed Day 7 with no reply and should move to `nurture`?
4. أي مسودة بانتظار موافقة تؤخّر إيقاعاً؟ / Which pending-approval draft is delaying a cadence?
5. أي عرض مُرسَل ينتظر قرار متابعة (post-proposal)؟ / Which sent proposal awaits a decision follow-up?
6. أي عميل في `payment_handoff` ينتظر تأكيد موافقات؟ / Who in payment handoff awaits approval confirmation?
7. أي مخاطرة (`risk`) تستدعي إيقاف متابعة؟ / Which risk warrants pausing a follow-up?
8. أي فرصة ترقية/تجديد نضجت (post-proof)؟ / Which upsell/renewal matured?

---

## قواعد ملزمة / Binding rules

1. لا متابعة بلا مسودة معتمَدة. / No follow-up without an approved draft.
2. لا إلحاح ولا ضغط مزعج (راجع [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md)). / No badgering or annoying pressure.
3. لا قناة محظورة (واتساب بارد/أتمتة LinkedIn/اتصال آلي). / No forbidden channel.
4. لا PII في سجل المتابعة. / No PII in the follow-up record.
5. الإرسال يدوي بعد موافقة دائماً. / Sending is always manual after approval.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
