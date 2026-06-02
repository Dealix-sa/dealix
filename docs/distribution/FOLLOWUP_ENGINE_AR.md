# Follow-up Engine — محرّك المتابعة — Follow-up Engine

> Purpose — الغرض: يشرح هذا المستند إيقاع المتابعة وأنه **يولّد قائمة مسودات للموافقة فقط**، ولا يرسل شيئًا تلقائيًا. كل متابعة مسودة `pending_approval` يقرّها المؤسس ثم ينسخها يدويًا.
>
> This document explains the follow-up cadence and that it **only generates a queue of drafts for approval**; it sends nothing automatically. Every follow-up is a `pending_approval` draft the founder approves, then copies manually.

Cross-link — روابط: [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) · [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md) · [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md).

---

## 1. القاعدة الحاكمة — The governing rule

المحرّك **يولّد** متابعات، ولا **يرسلها**. كل دورة يومية (`make distribution-day`) يحسب أي جهات تستحق متابعة اليوم، ويولّد لها مسودات `pending_approval`، ويعرضها في `reports/distribution/FOLLOWUP_QUEUE.md`. القرار النهائي بشري.

The engine **generates** follow-ups; it does not **send** them. Each daily run computes which prospects are due, generates `pending_approval` drafts, and lists them in `reports/distribution/FOLLOWUP_QUEUE.md`. The final decision is human.

المتابعات تُخزَّن في `data/revenue_execution/followups.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_FOLLOWUPS_PATH`).

---

## 2. إيقاع التواصل الأول — First-outreach cadence

| اليوم — Day | النوع — Type | الوصف — Description |
|---|---|---|
| Day 0 | `outreach_first` | تواصل أول |
| Day 2 | `outreach_followup_1` | متابعة أولى |
| Day 4 | `outreach_followup_2` | متابعة ثانية |
| Day 7 | `breakup` | رسالة إنهاء مهذّبة |

العدّ يبدأ من تاريخ `copied_manually` للتواصل الأول، لا من تاريخ التوليد — لأن النظام لا يعرف أن الرسالة أُرسِلت إلا حين يعلّمها المؤسس يدويًا.

The clock starts from the `copied_manually` date of the first outreach, not the generation date, because the system only knows a message was sent when the founder marks it manually.

---

## 3. مسارات ما بعد الحدث — Post-event cadences

| المُحفِّز — Trigger | المتابعة المُولَّدة — Generated follow-up | التوقيت — Timing |
|---|---|---|
| ردّ من الجهة — Reply received | `discovery_invite` | الدورة التالية |
| إرسال عرض — Proposal sent | `proposal` follow-up | بعد 48 ساعة |
| تسليم دفع — Payment handoff | `payment_followup` | بعد 24 ساعة |
| تهيئة — Onboarding done | تقرير قيمة أسبوعي — weekly value report | أسبوعيًا |
| يوم 21–30 — Day 21–30 | `renewal_upsell` | مرّة في النافذة |

كل بند أعلاه يُولَّد كمسودة `pending_approval`؛ لا شيء يُرسَل تلقائيًا. Every row above is generated as a `pending_approval` draft; nothing is sent automatically.

---

## 4. لماذا لا إرسال تلقائي — Why no auto-send

- **البند 8** — لا إجراء خارجي دون موافقة.
- **البند 2، 3** — منع أي أتمتة إرسال (واتساب بارد، لينكدإن).
- **أمان الوكلاء** — متابعة تلقائية تعني أن خطأ في التوقيت أو المحتوى يتضاعف بلا رقيب؛ التوليد-للموافقة يبقي كل إرسال تحت عين بشرية.

No auto-send because of non-negotiables #8, #2, #3, and agent safety: automatic follow-up would multiply timing/content errors unsupervised; generate-for-approval keeps every send under a human eye.

---

## 5. التوقّف عن المتابعة — Stopping follow-ups

تتوقّف سلسلة التواصل الأول في أي من الحالات:

The first-outreach sequence stops on any of:

- وصول ردّ (`replied`) → التحوّل إلى `discovery_invite`.
- طلب الجهة التوقّف → تُؤرشَف فورًا (`archived`) وتُحترَم الرغبة.
- بلوغ `breakup` (اليوم 7) دون ردّ → تُؤرشَف.

احترام طلب التوقّف غير قابل للتفاوض؛ لا «متابعة أخيرة» بعد طلب صريح بالتوقّف. Honoring a stop request is non-negotiable; there is no "one last follow-up" after an explicit stop.

---

## 6. لقطة من قائمة المتابعة — Follow-up queue snapshot

`reports/distribution/FOLLOWUP_QUEUE.md` يعرض لكل بند: معرّف الجهة (بلا بيانات شخصية)، نوع المتابعة، اليوم المستحَق، القناة، قرار الحوكمة، ومستوى الأدلة. المؤسس يقرأها ضمن حلقته اليومية (راجع [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md)).

The queue shows per item: prospect id (no PII), follow-up type, due day, channel, governance decision, and evidence level. The founder reads it within the daily loop.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
