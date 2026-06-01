# Statement of Work Template — نموذج بيان نطاق العمل

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [NDA_TEMPLATE.md](NDA_TEMPLATE.md) | [DPA_TEMPLATE.md](DPA_TEMPLATE.md) | [../delivery/MVP_SCOPE_TEMPLATE.md](../delivery/MVP_SCOPE_TEMPLATE.md) | [../delivery/CHANGE_REQUEST_TEMPLATE.md](../delivery/CHANGE_REQUEST_TEMPLATE.md) | [../delivery/ACCEPTANCE_CRITERIA_TEMPLATE.md](../delivery/ACCEPTANCE_CRITERIA_TEMPLATE.md)

---

*Note: This is a template. All [PLACEHOLDER] fields must be completed before signature. SOW is a legally binding document — Founder reviews and signs each one.*

*ملاحظة: هذا نموذج. يجب ملء جميع حقول [المكان المحجوز] قبل التوقيع. بيان نطاق العمل وثيقة ملزمة قانوناً — يراجع المؤسس ويوقّع كل واحد منها.*

---

## STATEMENT OF WORK — بيان نطاق العمل

**SOW Reference:** [SOW-YYYY-NNN]
**Date:** [YYYY-MM-DD]

**Service Provider — مقدم الخدمة:**
[DEALIX_LEGAL_ENTITY_NAME] ("Dealix")
[DEALIX_ADDRESS]
[DEALIX_COMMERCIAL_REGISTRATION]

**Client — العميل:**
[CLIENT_COMPANY_NAME] ("Client")
[CLIENT_ADDRESS]
[CLIENT_COMMERCIAL_REGISTRATION]

This SOW is made pursuant to any master agreement between the parties, or if no master agreement exists, this SOW together with the NDA reference [NDA-REF] constitutes the full agreement for this project.

---

## 1. Project Overview and Objectives — نظرة عامة على المشروع وأهدافه

**1.1 Project Name:** [PROJECT_NAME]

**1.2 Objective:** [One paragraph describing what the project will achieve — specific, measurable, and limited to what is actually contracted. No aspirational language.]

**الهدف:** [فقرة واحدة تصف ما سيحققه المشروع — محدد وقابل للقياس ومقيَّد بما هو متعاقد عليه فعلاً. بدون لغة طموحية.]

**1.3 Background:** [Brief context — why is the client doing this project? What operational situation is it addressing?]

---

## 2. Scope of Work — نطاق العمل

### 2.1 In-Scope — ضمن النطاق

The following workflows and deliverables are included in this SOW:

- [Workflow / deliverable 1 — specific description]
- [Workflow / deliverable 2]
- [Workflow / deliverable 3]

### 2.2 Out of Scope — خارج النطاق

The following are explicitly excluded from this SOW. They may be addressed in a future engagement:

- [Excluded item 1]
- [Excluded item 2]
- [Excluded item 3]
- Any workflow or deliverable not listed in Section 2.1

**Note:** Any work outside Section 2.1 requires a signed Change Request per Section 8.

---

## 3. Deliverables — المخرجات

| # | Deliverable — المخرج | Format — الصيغة | Due Date — تاريخ الاستحقاق | Acceptance Criteria — معايير القبول |
|---|---|---|---|---|
| D1 | [Deliverable name] | [PDF / System / Report / Documentation] | [YYYY-MM-DD] | Per [ACCEPTANCE_CRITERIA_TEMPLATE.md] section D1 |
| D2 | [Deliverable name] | [Format] | [YYYY-MM-DD] | Per [ACCEPTANCE_CRITERIA_TEMPLATE.md] section D2 |
| D3 | [Deliverable name] | [Format] | [YYYY-MM-DD] | Per [ACCEPTANCE_CRITERIA_TEMPLATE.md] section D3 |
| D4 | Project documentation and handover | Markdown + supporting files | [YYYY-MM-DD] | Covers all items in handover checklist |

All acceptance criteria are defined in the Acceptance Criteria document, completed and countersigned before build begins.

---

## 4. Timeline and Milestones — الجدول الزمني والمعالم

| Milestone — المعلم | Description — الوصف | Date — التاريخ |
|---|---|---|
| M1 — SOW Signed | Project officially starts | [YYYY-MM-DD] |
| M2 — Data Access Confirmed | Client provides access per API/Data checklist | [YYYY-MM-DD] |
| M3 — Acceptance Criteria Signed | Both parties agree on D1-D4 criteria | [YYYY-MM-DD] |
| M4 — Build Complete (internal) | Dealix completes internal QA | [YYYY-MM-DD] |
| M5 — UAT Start | Client begins user acceptance testing | [YYYY-MM-DD] |
| M6 — UAT Sign-Off | Client signs [UAT_SIGNOFF_TEMPLATE.md] | [YYYY-MM-DD] |
| M7 — Handover Complete | Documentation and access transfer done | [YYYY-MM-DD] |

Timeline assumes client provides data access within [5] business days of SOW signature. Delays in data access extend the timeline by the same number of days.

---

## 5. Pricing and Payment Schedule — الأسعار وجدول السداد

**Total Project Value:** [SAR / USD] [AMOUNT] (excluding VAT)
**VAT (15% KSA):** [SAR] [VAT_AMOUNT]
**Total including VAT:** [SAR] [TOTAL_AMOUNT]

| Payment — الدفعة | Amount (excl. VAT) — المبلغ | Trigger — الموجِّب | Due Date — الاستحقاق |
|---|---|---|---|
| Installment 1 — 50% | [SAR] | SOW signature | Within [5] business days of signature |
| Installment 2 — 50% | [SAR] | UAT Sign-Off | Within [10] business days of UAT sign-off |

**Payment method:** Bank transfer to [DEALIX_BANK_DETAILS — to be provided on invoice].

**Late payment:** Work is paused if Installment 1 is not received within [10] business days of the trigger. Work continues only after payment confirmed received.

---

## 6. Client Responsibilities — مسؤوليات العميل

The project timeline and quality depend on the Client providing:

يعتمد جدول المشروع وجودته على قيام العميل بما يلي:

- [ ] Designated project contact (title/role) within [3] business days of SOW signature
- [ ] API/data access confirmed and tested within [5] business days of SOW signature
- [ ] Sample data (anonymized) provided within [5] business days
- [ ] Acceptance criteria review and sign-off within [3] business days of Dealix submitting draft
- [ ] UAT lead allocated with minimum [X] hours/week during UAT phase
- [ ] Timely feedback — Dealix will assume approval if no response received within [3] business days on review requests

---

## 7. Assumptions — الافتراضات

This SOW is based on the following assumptions. If any assumption proves incorrect, a Change Request may be required:

- Client's data is in the format described in the discovery call and meets the data quality floor documented in the MVP Scope Template
- Client's existing system supports the integration method agreed (API / export / other)
- No legal or regulatory restrictions prevent the data processing described in this SOW
- Client has authority to grant Dealix the data access required
- Project is conducted in [Arabic / English / bilingual] as agreed

---

## 8. Change Management — إدارة التغيير

Any change to scope, timeline, or price after this SOW is signed requires a written Change Request using the template at [../delivery/CHANGE_REQUEST_TEMPLATE.md](../delivery/CHANGE_REQUEST_TEMPLATE.md). Verbal agreements are not binding. Dealix will not commence work on any change until the Change Request is countersigned by both parties.

---

## 9. Acceptance Process — عملية القبول

Deliverables are accepted through the formal UAT process per [../delivery/UAT_SIGNOFF_TEMPLATE.md](../delivery/UAT_SIGNOFF_TEMPLATE.md). Acceptance is written. Verbal approval does not constitute acceptance. Final payment is released after written UAT sign-off.

---

## 10. Confidentiality and Data — السرية والبيانات

This SOW is subject to the NDA reference [NDA-REF]. Where personal data is processed, the DPA reference [DPA-REF] applies. Dealix's data handling obligations are set out in the Data Handling Policy, available on request.

---

## 11. Governing Law and Dispute Resolution — القانون والنزاعات

This SOW is governed by the laws of the Kingdom of Saudi Arabia. The parties shall first attempt to resolve any dispute through good-faith negotiation. If unresolved within [30] days, disputes shall be submitted to the courts of Riyadh.

---

## 12. Signature Block — توقيع الطرفين

**By signing below, both parties agree to the terms of this Statement of Work.**

**بالتوقيع أدناه، يوافق الطرفان على شروط بيان نطاق العمل هذا.**

| Dealix — ديليكس | Client — العميل |
|---|---|
| Name: [FOUNDER_NAME] | Name: [AUTHORIZED_SIGNATORY_NAME] |
| Title: Founder | Title: [TITLE] |
| Date: [YYYY-MM-DD] | Date: [YYYY-MM-DD] |
| Signature: ________________ | Signature: ________________ |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
