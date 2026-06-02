# Draft Approval Runbook — كتاب تشغيل الموافقة — Draft Approval Runbook

> Purpose — الغرض: كتاب التشغيل اليومي للمؤسس لمراجعة المسودات: الموافقة، التعديل، الرفض، وتعليم «نُسِخت يدويًا». هذا الإجراء هو الحارس البشري الذي يحوّل القاعدة رقم 8 (لا إجراء خارجي دون موافقة) من مبدأ إلى ممارسة يومية.
>
> The founder's daily runbook for reviewing drafts: approve, edit, reject, and mark "copied manually." This procedure is the human gate that turns non-negotiable #8 (no external action without approval) from a principle into a daily practice.

Cross-link — روابط: [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](./DRAFT_QUALITY_POLICY_AR.md) · [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) · [README.md](./README.md) · [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).

---

## 1. متى — When

مرّة كل يوم عمل، بعد تشغيل `make distribution-day`. مدّة المراجعة المتوقّعة: 15–30 دقيقة لدفعة يومية معتادة.

Once per working day, after running `make distribution-day`. Expected review time: 15–30 minutes for a typical daily batch.

---

## 2. الخطوات — The steps

1. شغّل `make distribution-day` ثم `make draft-quality`.
2. افتح `reports/distribution/DRAFT_QUEUE_REVIEW.md`.
3. راجِع كل مسودة بترتيب درجة الجودة (الأدنى أولًا — هي الأخطر).
4. لكل مسودة، اتّخذ قرارًا واحدًا: `approved` / `needs_edit` / `rejected`.
5. للمعتمَدة: انسخ النص، أرسله بنفسك عبر قناته، ثم علّمه `copied_manually`.
6. أغلق المراجعة وسجّل العدّادات (راجع [DISTRIBUTION_METRICS_AR.md](./DISTRIBUTION_METRICS_AR.md)).

Run the day, open the review report, review lowest-quality first, decide one action per draft, then manually copy/send approved drafts and mark them `copied_manually`.

---

## 3. قائمة فحص الموافقة — Approval checklist

قبل تعليم أي مسودة `approved`، تأكّد من كل بند:

Before marking any draft `approved`, confirm every item:

- [ ] **الادعاء آمن** — لا وعد بمبيعات أو نسب كحقيقة؛ كل رقم له مصدر (البند 4، 5).
- [ ] **القناة آمنة** — القناة مسموحة في [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md)؛ لا واتساب بارد، لا أتمتة لينكدإن.
- [ ] **مستوى الأدلة حاضر** — `evidence_level` مضبوط، ولا محتوى تسويقي عام تحت L4.
- [ ] **التخصيص حقيقي** — الرسالة موجَّهة لهذه الجهة، لا قالب عام.
- [ ] **دعوة واضحة لإجراء** — CTA واحدة مفهومة.
- [ ] **لا بيانات شخصية** — لا بريد/هاتف/هوية في النص أو السجل (البند 6).
- [ ] **قرار الحوكمة ≤ REQUIRE_APPROVAL** — لا مسودة `BLOCK` تُعتمَد.

---

## 4. متى تختار كل قرار — Choosing the action

| القرار — Action | متى — When |
|---|---|
| `approved` | اجتازت كل بنود القائمة، وأنت مستعد لإرسالها يدويًا |
| `needs_edit` | الفكرة سليمة لكن الصياغة/التخصيص/الـCTA تحتاج تحسينًا |
| `rejected` | ادعاء غير آمن، قناة ممنوعة، أو خارج النطاق — لا يُصلَح بتعديل بسيط |

`needs_edit` تُعيد المسودة إلى `pending_approval` بعد تعديلها. `rejected` نهائية وتُسجَّل بسببها للتعلّم.

`needs_edit` returns the draft to `pending_approval` after editing; `rejected` is terminal and logged with a reason for learning.

---

## 5. خطوة النسخ اليدوي — The manual-copy step

هذه أهم خطوة في الكتاب: **النظام لا يُرسل**. أنت من ينسخ النص ويرسله من حسابك عبر القناة. ثم تعلّم المسودة `copied_manually` ليعرف النظام أن المتابعة قد تبدأ.

This is the most important step in the runbook: the system does not send. You copy the text and send it from your own account over the channel, then mark the draft `copied_manually` so the system knows follow-up may begin.

> لماذا يدوي؟ — Why manual? لأن منح النظام قدرة إرسال يفتح سطح هجوم لحقن التعليمات وسوء استخدام الوكلاء. النسخ اليدوي يبقي القرار النهائي بشريًا (راجع [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) §3).

---

## 6. حالات خاصة — Edge cases

- **مسودة بدرجة جودة منخفضة جدًا (< 60):** افتراضيًا `needs_edit` أو `rejected`؛ لا تعتمدها بثقة منخفضة.
- **مسودة بقرار `BLOCK`:** لا تظهر للاعتماد؛ تُعالَج بإصلاح السبب (مصدر، قناة) أو تُرفَض.
- **مسودة بـ`REDACT`:** راجع الحقل المُنقَّح قبل أي قرار؛ تأكّد ألا تسريب بيانات شخصية.
- **ردّ من جهة (`replied`):** ولّد `discovery_invite` في الدورة التالية، لا ترتجل ردًّا خارج النظام دون تسجيله.

---

## 7. الإيقاع الأسبوعي — Weekly rhythm

مرّة أسبوعيًا، اقرأ `reports/distribution/WIN_LOSS_LEARNING.md` وأجب عن أسئلة التعلّم (راجع [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md)). حدّث القوالب والقطاعات بناءً على ما رُفِض ولماذا.

Weekly, read the win/loss report and answer the learning questions; update templates and sectors based on what was rejected and why.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
