# تسليم التنفيذ — Dealix Delivery Handoff

هذا الملف يحدّد **حقول التسليم** والمشكلة التي يمنعها: «بعنا ثم صارت الفوضى في التسليم». الكيان `delivery_handoff` يحمل الحقول حرفياً: `id`, `customer_id`, `product_sold`, `scope`, `timeline`, `success_metric`, `first_workflow`, `required_access`, `owner`, `risks`, `next_meeting`.

This file defines the **handoff fields** and the problem it prevents: "we sold, then delivery became chaos." The `delivery_handoff` entity carries the fields above verbatim.

روابط / Related: [../distribution/PAYMENT_HANDOFF_AR.md](../distribution/PAYMENT_HANDOFF_AR.md) · [../distribution/PROPOSAL_FACTORY_AR.md](../distribution/PROPOSAL_FACTORY_AR.md) · [HANDOFF_PROCESS.md](HANDOFF_PROCESS.md) · [CLIENT_ONBOARDING.md](CLIENT_ONBOARDING.md) · [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md)

---

## المشكلة التي يمنعها / The problem it prevents

> **«بعنا، ثم صارت الفوضى في التسليم.»** بلا تسليم منظَّم: نطاق غير واضح، وصول ناقص، مالك غير محدَّد، توقعات غير متفق عليها، وتوسّع نطاق صامت. النتيجة عميل غير راضٍ ودليل ضعيف.
>
> **"We sold, then delivery became chaos."** Without a structured handoff: unclear scope, missing access, no named owner, misaligned expectations, and silent scope creep — yielding an unhappy customer and weak evidence.

هذا التسليم يربط ما بِيع (`product_sold` من العرض المعتمَد) بما سيُنفَّذ فعلاً، بحقول صريحة قبل أي عمل. / This handoff ties what was sold to what will actually be executed, with explicit fields before any work begins.

---

## حقول التسليم / Handoff fields

يُملأ عند انتقال العميل إلى `won` ودفع مؤكَّد (راجع [../distribution/PAYMENT_HANDOFF_AR.md](../distribution/PAYMENT_HANDOFF_AR.md)):

Filled when the customer reaches `won` with confirmed payment:

| الحقل / Field | الوصف / Description |
|---|---|
| `id` | معرّف التسليم. / Handoff id. |
| `customer_id` | العميل. / The customer. |
| `product_sold` | المنتج المباع من [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md). / The sold catalog product. |
| `scope` | النطاق المتفق عليه (مطابق للعرض المعتمَد). / Agreed scope (matching the approved proposal). |
| `timeline` | الجدول الزمني للتسليم. / Delivery timeline. |
| `success_metric` | مقياس النجاح المتفق عليه (قابل للقياس). / Agreed, measurable success metric. |
| `first_workflow` | أول مسار/مخرج يبدأ به التنفيذ. / The first workflow/deliverable to start. |
| `required_access` | الوصول والبيانات المطلوبة من العميل (ضمن DPA). / Required access and data (within the DPA). |
| `owner` | المالك المسؤول عن التسليم. / The accountable delivery owner. |
| `risks` | مخاطر التسليم المعروفة. / Known delivery risks. |
| `next_meeting` | موعد المراجعة التالي. / The next review meeting. |

> `scope` هنا يطابق `scope` و`out_of_scope` في العرض المعتمَد؛ أي تغيير يمر بمسار طلب التغيير، لا توسّعاً صامتاً. / Scope here mirrors the approved proposal's scope/out-of-scope; any change goes through the change-request process, not silent creep.

---

## التسلسل / Sequence

```text
payment_handoff (paid) → delivery_handoff filled → onboarding
→ first_workflow delivered → review (next_meeting) → proof pack
```

- يبدأ التسليم فقط بعد `paid` وتأكيد كل موافقات الدفع. / Delivery begins only after `paid` and all payment approvals.
- يربط `success_metric` بـ`measurement_method` في حزمة الدليل لاحقاً (راجع [../distribution/PROOF_PACK_FACTORY_AR.md](../distribution/PROOF_PACK_FACTORY_AR.md)). / Success metric links to the proof pack's measurement method.
- مواعيد ونطاق يتبعان [HANDOFF_PROCESS.md](HANDOFF_PROCESS.md) و[CLIENT_ONBOARDING.md](CLIENT_ONBOARDING.md). / Cadence and scope follow the existing handoff and onboarding docs.

---

## قواعد ملزمة / Binding rules

1. لا تسليم بلا `product_sold` و`scope` و`owner` و`success_metric`. / No handoff without product, scope, owner, and a success metric.
2. لا توسّع نطاق صامت؛ كل تغيير عبر طلب تغيير موثَّق. / No silent scope creep; every change via a documented change request.
3. لا PII في سجل التسليم؛ الوصول يُدار تحت DPA لا بنسخ بيانات في السجل. / No PII in the handoff record; access managed under the DPA.
4. `success_metric` مقياس واقعي لا وعد ولا ضمان. / Success metric is a realistic measure, not a promise or guarantee.
5. التسليم لا يبدأ قبل دفع مؤكَّد. / Delivery does not start before confirmed payment.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
