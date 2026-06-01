# Change Request Template — قالب طلب التغيير

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [RISK_REGISTER_TEMPLATE.md](RISK_REGISTER_TEMPLATE.md) | [../governance/SOW_TEMPLATE.md](../governance/SOW_TEMPLATE.md) | [../finance/PRICING_GUARDRAILS.md](../sales/PRICING_GUARDRAILS.md)

---

## Rule — القاعدة

**Any change to scope, timeline, or price after SOW signature requires a signed Change Request. Verbal agreements do not count.**

In-scope additions, timeline extensions, and price adjustments are all change requests. "Small additions" are the most common margin killers. Log every request. Approve in writing. Build only after signature.

**أي تغيير في النطاق أو الجدول الزمني أو السعر بعد توقيع SOW يتطلب طلب تغيير موقّعاً. الاتفاقيات الشفهية لا تُعتمَد.**

الإضافات ضمن النطاق، وتمديد الجدول الزمني، وتعديلات الأسعار — كلها طلبات تغيير. "الإضافات الصغيرة" هي أكثر أسباب تآكل الهامش شيوعاً. سجّل كل طلب. اعتمد بالكتابة. ابنِ فقط بعد التوقيع.

---

## Change Request Header — رأس طلب التغيير

| Field — الحقل | Value — القيمة |
|---|---|
| CR Number | [CR-YYYY-NNN] |
| Date submitted | [YYYY-MM-DD] |
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Requestor | [Client Title/Role OR Dealix internal] |
| Request received via | [Email / Meeting / Call — no verbal-only] |
| Date of original SOW | [YYYY-MM-DD] |
| CR prepared by | [Dealix Founder / Role] |

---

## Section 1 — Description of Change | وصف التغيير

**What is being requested?** Be specific. Vague change requests are rejected.

**ما المطلوب تغييره؟** كن محدداً. طلبات التغيير الغامضة تُرفض.

[Describe the change in plain language. Include: what workflow/deliverable is affected, what the new requirement is, and why it was not included in the original SOW.]

**Arabic version / النسخة العربية:**
[وصف التغيير بالعربية إذا كان العميل يفضّل العربية]

---

## Section 2 — Reason for Change | سبب التغيير

Select the primary reason and add detail:

- [ ] Client requirements evolved after SOW signing
- [ ] New information discovered during build (data quality issue, system limitation)
- [ ] Regulatory or compliance requirement identified post-signing
- [ ] Dealix internal — improvement to original design
- [ ] Force majeure (external event outside either party's control)

**Detail:** [Explain why this change is needed now and was not identified at scoping]

---

## Section 3 — Impact Assessment | تقييم الأثر

### Scope Impact — أثر النطاق

| Impact — الأثر | Description — الوصف |
|---|---|
| Workflows added | [List new workflows added] |
| Workflows removed | [List workflows removed from original scope] |
| Deliverables modified | [List deliverables changed and how] |
| Out-of-scope items moved in | [List items from original out-of-scope now included] |

### Timeline Impact — أثر الجدول الزمني

| | Original — الأصلي | Revised — المعدَّل | Delta — الفرق |
|---|---|---|---|
| Delivery date | [YYYY-MM-DD] | [YYYY-MM-DD] | [+/- X days] |
| Phase affected | [Phase name] | [Revised phase] | [Description] |

### Price Impact — أثر السعر

| | SAR | Notes |
|---|---|---|
| Original contract value | [SAR] | Per SOW |
| Additional cost for this CR | [SAR] | Itemized below |
| **Revised total contract value** | **[SAR]** | If approved |

**Cost itemization:**

| Item — البند | Hours / Units | Rate | Total SAR |
|---|---|---|---|
| [e.g., Additional workflow build] | [X hours] | [SAR/hr] | [SAR] |
| [e.g., LLM API cost increase] | [X units] | [SAR/unit] | [SAR] |
| [e.g., Extended hosting] | [X months] | [SAR/mo] | [SAR] |
| **Total CR cost** | | | **[SAR]** |

---

## Section 4 — Estimated Risk if Change is Rejected | المخاطر المقدَّرة عند الرفض

[What happens to the project if this change request is not approved? Does the project continue as-is? Does it fail a deliverable? State clearly.]

---

## Section 5 — Approval Status | حالة الموافقة

| Decision — القرار | Date — التاريخ | Notes — ملاحظات |
|---|---|---|
| [ ] Pending | | |
| [ ] Approved | [YYYY-MM-DD] | |
| [ ] Approved with modifications | [YYYY-MM-DD] | [State modifications] |
| [ ] Rejected | [YYYY-MM-DD] | [State reason] |

---

## Section 6 — Signature Block — توقيع الطرفين

**By signing, both parties confirm: (1) this Change Request is agreed, (2) the revised scope, timeline, and price supersede the original SOW for the items listed above, (3) work on the change begins only after countersignature.**

**بالتوقيع، يؤكد الطرفان: (1) الموافقة على طلب التغيير هذا، (2) النطاق والجدول الزمني والسعر المعدَّلون يحلون محل SOW الأصلي للبنود المذكورة أعلاه، (3) لا يبدأ العمل على التغيير إلا بعد التوقيع من الطرفين.**

| Role — الدور | Name — الاسم | Date — التاريخ | Signature — التوقيع |
|---|---|---|---|
| Dealix Founder | [NAME] | [YYYY-MM-DD] | ________________ |
| Client Authorized Representative | [TITLE] | [YYYY-MM-DD] | ________________ |

---

## Change Request Log (per project) — سجل طلبات التغيير

Maintain a running log of all CRs for this project:

| CR Number | Date | Description | Approved | Cost (SAR) | Timeline Impact |
|---|---|---|---|---|---|
| CR-[YYYY]-001 | [Date] | [Brief] | [Y/N] | [SAR] | [+/- days] |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
