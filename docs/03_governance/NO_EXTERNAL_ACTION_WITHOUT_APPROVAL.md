# No External Action Without Approval — لا إجراء خارجي بدون موافقة

> Doctrine — العقيدة: nothing leaves Dealix toward a third party — no message, email, WhatsApp, call script that we send, or any external-facing action — without explicit founder approval. Everything is produced as a draft and queued. The default state of every outbound artifact is `draft_only`.
>
> هذه الوثيقة هي بوابة الموافقة في ديالكس. لا تُرسَل أي رسالة أو بريد أو واتساب أو أي إجراء يواجه طرفًا خارجيًا دون موافقة صريحة من المؤسس. كل ناتج يُنشأ كمسودة ويُوضع في طابور المراجعة. الحالة الافتراضية لكل ناتج خارجي هي «مسودة فقط».

Cross-link: [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md), [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), [PROOF_TO_UPSELL_PLAYBOOK.md](../04_delivery/PROOF_TO_UPSELL_PLAYBOOK.md), [FIRST_OUTREACH_PACK.md](../../sales/FIRST_OUTREACH_PACK.md).

---

## Scope — النطاق

This doctrine governs every Dealix workflow, sprint, retainer, and tool that can produce an artifact intended for a person or organization outside Dealix. It applies to founder-operated work and to any automated module that drafts outbound content.

تحكم هذه العقيدة كل تدفق عمل وسبرنت واحتفاظ وأداة قد تُنتج ناتجًا موجَّهًا لشخص أو جهة خارج ديالكس. تنطبق على العمل الذي يديره المؤسس وعلى أي وحدة آلية تُنشئ محتوى صادرًا.

---

## What counts as an "external action" — ما الذي يُعَدُّ «إجراءً خارجيًا»

- Sending any message: WhatsApp, SMS, email, in-app message, or a call we place.
- Posting publicly on behalf of a customer or of Dealix referencing a customer.
- Sharing any file, dataset, or report that leaves the Dealix or customer workspace.
- Submitting a form, booking, or request to a third-party platform on a customer's behalf.
- Exposing any PII to a party that did not already hold it.

ما يُعَدُّ إجراءً خارجيًا: إرسال أي رسالة (واتساب، رسالة نصية، بريد، رسالة داخل التطبيق، أو مكالمة نُجريها)؛ النشر العلني نيابةً عن عميل أو عن ديالكس بذكر عميل؛ مشاركة أي ملف أو بيانات أو تقرير يغادر مساحة العمل؛ تقديم نموذج أو حجز أو طلب لمنصة طرف ثالث نيابةً عن العميل؛ كشف أي بيانات شخصية لطرف لم يكن يملكها.

What does NOT count: internal drafting, internal scoring, internal ledger writes, and producing a draft that stays in the queue.

ما لا يُعَدُّ إجراءً خارجيًا: الصياغة الداخلية، التقييم الداخلي، الكتابة في السجلات الداخلية، وإنتاج مسودة تبقى في الطابور.

---

## The flow — التدفق: draft → review → approve → send

1. **Draft** — a module or the founder produces the artifact with status `draft_only`. It carries the workflow ID, the intended recipient label, and the governance decisions attached to it.
2. **Review** — the founder reads the draft in full, including every BLOCK and REDACT decision. Bilingual artifacts are reviewed in both languages.
3. **Approve** — the founder records an explicit approval in the approval register. Approval is per artifact, per recipient, per send. There is no blanket approval.
4. **Send** — only after a logged approval, the send is executed (manually by the founder, or by the customer with the customer's own credentials). Dealix does not send on a customer's behalf without that customer's explicit, logged authorization.

التدفق: مسودة ← مراجعة ← موافقة ← إرسال. تُنشأ المسودة بحالة «مسودة فقط»؛ يقرؤها المؤسس كاملةً بلغتيها؛ يُسجِّل موافقة صريحة لكل ناتج ولكل مستلِم ولكل إرسالة دون موافقة شاملة؛ ثم يُنفَّذ الإرسال يدويًا فقط بعد موافقة مُسجَّلة.

---

## The approval register — سجل الموافقات

Every approval is recorded as an immutable entry. The register is the audit trail customers buy alongside the deliverable.

- `artifact_id` — the draft being approved.
- `recipient_label` — anonymized recipient reference (never raw PII in the register summary).
- `decision` — `approved`, `approved_with_edits`, `rejected`, `deferred`.
- `approver` — the founder identity.
- `timestamp` — when the decision was made.
- `governance_decisions` — the decision types resolved before approval.

كل موافقة تُسجَّل كقيد غير قابل للتعديل. سجل الموافقات هو أثر التدقيق الذي يشتريه العميل مع الناتج. يحتوي القيد على: معرّف الناتج، وصف المستلِم (دون بيانات شخصية خام في الملخص)، القرار (موافَق / موافَق مع تعديلات / مرفوض / مؤجَّل)، هوية المُوافِق، الطابع الزمني، وقرارات الحوكمة المحلولة.

---

## Forbidden auto-actions — الإجراءات الآلية المحظورة

These are refused outright. They are not configurable, not negotiable, and not unlocked by any tier:

- Cold WhatsApp outreach to non-permissioned contacts, or any WhatsApp automation that bypasses approval.
- LinkedIn automation: auto-connect, auto-message, or scraped-list messaging.
- Scraping or harvesting contacts from any source; Dealix only works from customer-owned, passported data.
- Bulk outreach to lists the customer cannot show permission for.
- Any "guaranteed return", "guaranteed sales", or fixed-ROI claim. Replace with evidenced opportunities / فرص مُثبتة بأدلة.
- Sending on a customer's behalf without explicit, logged customer authorization.

الإجراءات الآلية المحظورة (مرفوضة قطعًا وغير قابلة للتفعيل في أي باقة): التواصل البارد عبر واتساب أو أي أتمتة تتجاوز الموافقة؛ أتمتة لينكدإن (اتصال أو رسائل آلية أو مراسلة قوائم مسحوبة)؛ سحب أو حصاد جهات الاتصال من أي مصدر؛ التواصل بالجملة مع قوائم لا يستطيع العميل إثبات إذنها؛ أي ادعاء بعائد مضمون أو مبيعات مضمونة؛ الإرسال نيابةً عن العميل دون إذن صريح ومُسجَّل.

---

## Cross-references — مراجع متقاطعة

- Governance approval policy: [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).
- Non-negotiables: [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).
- Warm-list first outreach (draft discipline): [FIRST_OUTREACH_PACK.md](../../sales/FIRST_OUTREACH_PACK.md).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
