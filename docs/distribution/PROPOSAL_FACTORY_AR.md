# مصنع العروض — Dealix Proposal Factory

هذا الملف يحدّد **أقسام العرض المطلوبة** وقواعده. الكيان `proposal` يحمل الحقول حرفياً: `id`, `prospect_id`, `product_id`, `sector`, `problem`, `proposed_solution`, `scope`, `out_of_scope`, `timeline`, `price_min_sar`, `price_max_sar`, `assumptions`, `evidence_level`, `risks`, `payment_terms`, `next_step`, `approval_status`.

This file defines the **required proposal sections** and rules. The `proposal` entity carries the fields above verbatim.

روابط / Related: [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) · [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md) · [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md) · [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md) · [../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)

---

## الأقسام المطلوبة / Required sections

كل عرض يجب أن يحتوي **كل** الأقسام التالية، كلٌ مربوط بحقل على الكيان:

Every proposal must contain **all** of the following, each mapped to a field:

| القسم / Section | الحقل / Field | ملاحظة / Note |
|---|---|---|
| العميل والقطاع / Customer & sector | `sector`, `prospect_id` | مربوط بعميل مؤهَّل. / Linked to a qualified prospect. |
| المنتج / Product | `product_id` | من [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md). |
| المشكلة / Problem | `problem` | بصياغة العميل، لا مبالغة. / In the customer's words, no exaggeration. |
| الحل المقترح / Proposed solution | `proposed_solution` | مخرجات ملموسة. / Concrete deliverables. |
| النطاق / Scope | `scope` | محدَّد ومغلق. / Defined and closed. |
| خارج النطاق / Out of scope | `out_of_scope` | صريح لمنع التوسّع. / Explicit to prevent creep. |
| المدة / Timeline | `timeline` | مطابقة لمدة المنتج. / Matches the product's delivery days. |
| السعر / Price | `price_min_sar`, `price_max_sar` | داخل حدود [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md). |
| الافتراضات / Assumptions | `assumptions` | ما يعتمد عليه التنفيذ. / What execution depends on. |
| مستوى الدليل / Evidence level | `evidence_level` | L0–L5؛ يحكم الادعاءات. / Governs claims. |
| المخاطر / Risks | `risks` | تشغيلية وامتثالية. / Operational and compliance. |
| شروط الدفع / Payment terms | `payment_terms` | بلا تحصيل آلي. / No auto-charge. |
| الخطوة التالية / Next step | `next_step` | إجراء واحد واضح. / One clear action. |
| حالة الموافقة / Approval status | `approval_status` | لا إرسال قبل `approved`. / No send before approved. |

> تذييل إلزامي في كل عرض يُرسَل للعميل: «القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value». / Mandatory footer on every customer-facing proposal.

---

## القواعد / The rules

1. **لا عرض بلا عميل مؤهَّل.** يجب أن تكون حالة العميل `proposal_needed` (أو ما بعدها) في [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md). / No proposal without a qualified prospect.
2. **لا سعر نهائي بلا موافقة.** `approval_status` يبقى غير معتمَد حتى موافقة المؤسس على السعر؛ السعر داخل النطاق المعتمد فقط. / No final price without approval; price within the approved band only.
3. **لا نطاق مفتوح.** كل عرض يحدّد `scope` و`out_of_scope` صراحةً. / No open scope; both fields explicit.
4. **لا ضمانات.** لا أرقام مبيعات/تحويل/ROI كوعد؛ القيمة «فرص مُثبتة بأدلة» وفق `evidence_level`. / No guarantees; value framed as evidence-backed opportunities.

---

## حالات الموافقة / Approval states (`approval_status`)

| الحالة / State | المعنى / Meaning |
|---|---|
| `draft` | مُصاغ، السعر ضمن النطاق، بانتظار مراجعة. / Drafted, price in band, awaiting review. |
| `pending_approval` | في طابور موافقة المؤسس. / In the founder approval queue. |
| `changes_requested` | يحتاج تعديل. / Needs edits. |
| `approved` | معتمَد؛ مسموح بالإرسال اليدوي. / Approved; manual send allowed. |
| `sent` | أُرسِل بعد الاعتماد. / Sent after approval. |
| `rejected` | مرفوض؛ لا يُرسَل. / Rejected; not sent. |

> بعد `approved` وإرسال العرض، ينتقل العميل إلى `proposal_sent`، ثم — عند توفر شروط الدفع — إلى `payment_handoff` (راجع [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md)). / After approval and sending, the prospect moves to `proposal_sent`, then to `payment_handoff` once payment preconditions are met.

---

## قواعد ملزمة / Binding rules

1. كل عرض مربوط بمنتج (`product_id`) وسعر داخل الحدود. / Every proposal links to a product with a price within bands.
2. لا PII زائدة في نص العرض. / No excess PII in the proposal text.
3. لا إرسال بلا `approved`، ولا تحصيل آلي. / No send without approval; no auto-charge.
4. كل ادعاء قيمة مربوط بـ`evidence_level` كافٍ. / Every value claim ties to a sufficient evidence level.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
