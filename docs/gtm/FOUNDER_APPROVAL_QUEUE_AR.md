# Founder Approval Queue — طابور موافقة المؤسس — How approval-ready drafts reach the founder

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تصف كيف تنتقل المسودات «الجاهزة للموافقة» من بوابة الجودة إلى قرار المؤسس، وتربط مركز الموافقة وبوابات الموافقة الصلبة دون تكرارها. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة.

---

## 1) المبدأ الحاكم — لا إرسال بلا قرار بشري (AR)

كل مسودة في هذه الطبقة تولد بـ `governance_decision = "approval_required"`. اجتياز بوابة الجودة لا يعني الإرسال — يعني فقط أن المسودة **جاهزة لإنسان**. القرار النهائي (إرسال، تسعير، التزام، تسليم دفع) **للمؤسس وحده**، اتساقًا مع المبدأ في [`os/06_APPROVAL_GATES.yml`](../../os/06_APPROVAL_GATES.yml): أي إجراء يؤثر على الخارج أو على بيانات حقيقية أو على التزامات تجارية يتوقف تلقائيًا حتى موافقة صريحة.

## 1) Governing Principle — No Send Without a Human Decision (EN)

Every draft in this layer is born `governance_decision = "approval_required"`. Passing the quality gate is not a send — it only means the draft is **ready for a human**. The final decision (send, pricing, commitment, payment handoff) belongs to the **founder alone**, consistent with [`os/06_APPROVAL_GATES.yml`](../../os/06_APPROVAL_GATES.yml): any action that affects the outside world, real data, or commercial commitments halts automatically until explicit approval.

---

## 2) من بوابة الجودة إلى الطابور — From the quality gate to the queue (AR)

المسودة تصبح مؤهَّلة للطابور فقط حين تجتاز **كل** سطر في [`auto_client_acquisition/gtm_os/draft_quality_gate.py`](../../auto_client_acquisition/gtm_os/draft_quality_gate.py) عبر `validate_outreach_draft()`. الناجحة تُرجِع `verdict = "pass"` و`governance_decision = "approval_required"`؛ الفاشلة تُرجِع `"BLOCK"` (أعد الصياغة قبل إعادة الإدراج). التفاصيل الكاملة لأكواد الحجب في [`outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) — لا نكرّرها هنا.

تجميع الدفعة اليومية يتم عبر `summarize_gate_results()`، الذي يُنتج `approval_ready_ids` و`blocked_ids` و`top_failure_reasons`. هذه المخرجات تُغذّي الأمر اليومي في [`scripts/gtm_daily_command.py`](../../scripts/gtm_daily_command.py) → القسم «أعلى قائمة الموافقة» (حتى 50 مسودة).

## 2) From the Quality Gate to the Queue (EN)

A draft becomes queue-eligible only when it passes **every** line of [`gtm_os/draft_quality_gate.py`](../../auto_client_acquisition/gtm_os/draft_quality_gate.py) via `validate_outreach_draft()`. A pass returns `verdict = "pass"` and `governance_decision = "approval_required"`; a fail returns `"BLOCK"` (rewrite before re-queue). The full block-code list lives in [`outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) — not duplicated here.

The daily batch is aggregated by `summarize_gate_results()`, which yields `approval_ready_ids`, `blocked_ids`, and `top_failure_reasons`. These feed the daily command in [`scripts/gtm_daily_command.py`](../../scripts/gtm_daily_command.py) → the "Top approval queue" section (up to 50 drafts).

```json
{
  "draft_id": "opaque-id",
  "verdict": "pass",
  "governance_decision": "approval_required",
  "sector": "agency",
  "offer": "revenue_proof_sprint_499",
  "recipient_role": "Marketing Director",
  "personalization_tier": "P2",
  "evidence_level": "L2"
}
```

---

## 3) قرارات المؤسس — The founder decisions (AR/EN)

لكل عنصر في الطابور، يختار المؤسس قرارًا واحدًا. لا قرار تلقائي. تُمرَّر القرارات عبر مركز الموافقة (`approval_policy`, `founder_rules`, `approval_store`) في [`auto_client_acquisition/approval_center/`](../../auto_client_acquisition/approval_center/).

| القرار — Decision | الأثر — Effect | الحالة بعده — Status after |
|---|---|---|
| **اعتماد — Approve** | يصبح مؤهَّلًا لخطة الإرسال الآمن (لا إرسال فوري) | `queued` → جدولة الدفعة |
| **رفض — Reject** | لا يُرسَل؛ يبقى محجوبًا | يبقى `drafted` (محجوب) |
| **إعادة صياغة — Rewrite** | يعاد إلى المصنع لإعادة كتابة كاملة | `drafted` (إعادة بوابة) |
| **اختصار — Shorten** | تقصير النص مع الإبقاء على الزاوية | `drafted` (إعادة بوابة) |
| **اجعله رسميًا — Make formal** | رفع النبرة إلى رسمية تنفيذية | `drafted` (إعادة بوابة) |
| **غيّر العرض — Change offer** | استبدال العرض بآخر من الكتالوج المعتمد | `drafted` (إعادة مطابقة عرض) |
| **انقله للتنشئة — Move to nurture** | تأجيل؛ متابعة لاحقة | `nurture` |
| **لا تتواصل — Do not contact** | نهائي؛ يُكافئ قائمة الكبح | `do_not_contact` |

كل قرار يُسجَّل في `approval_store` مع طابع زمني ومرجع، ليبقى أثر تدقيق كامل. القرارات التي تعيد المسودة للمصنع (Rewrite / Shorten / Make formal / Change offer) تُعيد تشغيل بوابة الجودة قبل العودة للطابور. `Do not contact` نهائي ولا رجعة عنه.

For each queue item the founder picks one decision; nothing is auto-decided. Decisions flow through the approval center (`approval_policy`, `founder_rules`, `approval_store`) in [`approval_center/`](../../auto_client_acquisition/approval_center/). Each is logged with a timestamp and reference for a full audit trail. Decisions that return a draft to the factory (Rewrite / Shorten / Make formal / Change offer) re-run the quality gate before re-queueing. `Do not contact` is terminal.

---

## 4) العلاقة بالبوابات الصلبة — Relation to the hard gates (AR)

طابور هذه الطبقة لا يستبدل بوابات الموافقة المؤسسية؛ يجلس فوقها. سجل البوابات في [`os/06_APPROVAL_GATES.yml`](../../os/06_APPROVAL_GATES.yml) يفرض موافقة بشرية على القرارات عالية المخاطر — منها أول بريد لشركة (`G01`)، المتابعة (`G02`)، مشاركة سعر (`G03`)، إرسال عرض (`G04`)، وتشغيل أي أتمتة تؤثر على الخارج (`G09`). اعتماد مسودة هنا = استيفاء البوابة المناسبة، لا تجاوزها. سلطة التجاوز للمؤسس فقط.

## 4) Relation to the Hard Gates (EN)

This layer's queue does not replace the institutional approval gates; it sits on top of them. The gate registry in [`os/06_APPROVAL_GATES.yml`](../../os/06_APPROVAL_GATES.yml) forces human approval on high-risk decisions — including the first email to a company (`G01`), follow-ups (`G02`), sharing a price (`G03`), sending a proposal (`G04`), and running any externally-facing automation (`G09`). Approving a draft here means satisfying the relevant gate, never bypassing it. Override authority is founder-only.

---

## 5) ما بعد الاعتماد — After approval (AR)

المسودات المعتمَدة لا تُرسَل تلقائيًا. تدخل **خطة الإرسال الآمن** عبر `plan_sending_batches()` في [`auto_client_acquisition/gtm_os/sending_ramp.py`](../../auto_client_acquisition/gtm_os/sending_ramp.py)، التي تحترم منحنى التدرّج وصحة الدومين وقائمة الكبح وحد التكرار. الردود الإيجابية تُوجَّه إلى [`whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md`](whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md) — بموافقة فقط.

## 5) After Approval (EN)

Approved drafts are not sent automatically. They enter the **safe sending plan** via `plan_sending_batches()` in [`gtm_os/sending_ramp.py`](../../auto_client_acquisition/gtm_os/sending_ramp.py), which honors the ramp curve, domain health, suppression list, and frequency cap. Positive replies route to [`whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md`](whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md) — consent-only.

---

## 6) إعادة الاستخدام — لا تكرار — Reuse, not duplication

- **مركز الموافقة:** [`auto_client_acquisition/approval_center/`](../../auto_client_acquisition/approval_center/) — `approval_policy`, `founder_rules`, `approval_store`, `approval_renderer`.
- **البوابات الصلبة:** [`os/06_APPROVAL_GATES.yml`](../../os/06_APPROVAL_GATES.yml).
- **بوابة الجودة:** [`auto_client_acquisition/gtm_os/draft_quality_gate.py`](../../auto_client_acquisition/gtm_os/draft_quality_gate.py).
- **الأمر اليومي:** [`scripts/gtm_daily_command.py`](../../scripts/gtm_daily_command.py).
- **سجل العميل المحتمل ودورة الحالة:** [`prospects/PROSPECT_OS_AR.md`](prospects/PROSPECT_OS_AR.md).

This layer links the approval center; it does not duplicate its rules.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة. لا إرسال ولا تسعير ولا التزام بلا موافقة المؤسس.
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
