# Data Processing Checklist — قائمة معالجة البيانات

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [CLIENT_ACCESS_MATRIX.md](CLIENT_ACCESS_MATRIX.md) | [../governance/DATA_HANDLING_POLICY.md](../governance/DATA_HANDLING_POLICY.md) | [../governance/CLIENT_DATA_CLASSIFICATION.md](../governance/CLIENT_DATA_CLASSIFICATION.md) | [../governance/DPA_TEMPLATE.md](../governance/DPA_TEMPLATE.md)

---

## Rule — القاعدة

This checklist is completed at project intake — before any client data is accessed, processed, or stored. Items marked STOP must be resolved before proceeding. A partially completed checklist is treated as "not complete."

تُكمَل هذه القائمة عند استقبال المشروع — قبل الوصول إلى أي بيانات للعميل أو معالجتها أو تخزينها. البنود المميزة بـ STOP يجب حلها قبل المتابعة. القائمة غير المكتملة جزئياً تُعامَل كـ "غير مكتملة".

---

## Project Header — رأس المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Client label | [CLIENT_LABEL] |
| Data review date | [YYYY-MM-DD] |
| Reviewed by | [Dealix Founder / Role] |

---

## Section 1 — Data Classification | تصنيف البيانات

Reference [../governance/CLIENT_DATA_CLASSIFICATION.md](../governance/CLIENT_DATA_CLASSIFICATION.md) for classification definitions.

| Data Source — مصدر البيانات | Classification — التصنيف | Notes — ملاحظات | Confirmed |
|---|---|---|---|
| [Data source 1] | [ ] Public [ ] Internal [ ] Confidential [ ] Restricted | | [ ] |
| [Data source 2] | [ ] Public [ ] Internal [ ] Confidential [ ] Restricted | | [ ] |
| [Data source 3] | [ ] Public [ ] Internal [ ] Confidential [ ] Restricted | | [ ] |

- [ ] All data sources classified and documented above.

---

## Section 2 — Personal Data (PII) Identification | تحديد البيانات الشخصية

**(STOP if any item below is checked "YES" and DPA is not yet signed.)**

| Check — الفحص | Yes / No | If Yes — Action Required |
|---|---|---|
| Data contains names of individuals | [ ] Yes [ ] No | Anonymize before processing OR obtain DPA + PDPL compliance confirmation |
| Data contains national ID numbers | [ ] Yes [ ] No | STOP — Restricted. DPA + explicit PDPL consent required before any processing |
| Data contains phone numbers or personal emails | [ ] Yes [ ] No | DPA required. Anonymize in all logs and exports |
| Data contains health or biometric data | [ ] Yes [ ] No | STOP — Restricted. Legal review required before proceeding |
| Data contains financial account details | [ ] Yes [ ] No | STOP — Restricted. Founder approval + DPA required |
| Data contains employee performance or HR data | [ ] Yes [ ] No | Confidential. DPA required. No export without client explicit approval |

- [ ] PII assessment complete. All identified PII items actioned above.

---

## Section 3 — Sample Data Received and Tested | استلام البيانات النموذجية وإختبارها

| Step — الخطوة | Status — الحالة |
|---|---|
| [ ] Anonymized sample data received from client | [ ] Complete — date: [YYYY-MM-DD] |
| [ ] Sample data format matches project requirements | [ ] Confirmed / [ ] Issues found: [describe] |
| [ ] Sample data loaded and processed in test environment (no production) | [ ] Complete |
| [ ] Data quality assessed — null rate, format consistency, completeness | [ ] Complete — null rate: [%], issues: [describe] |
| [ ] Data quality acceptable for building OR additional cleaning required | [ ] Acceptable / [ ] Cleaning required — add to timeline |

---

## Section 4 — Production Data Access Method | طريقة الوصول لبيانات الإنتاج

| Step — الخطوة | Detail — التفصيل | Confirmed |
|---|---|---|
| [ ] Data access method defined | [ ] API [ ] Scheduled export [ ] Direct DB read [ ] Manual upload | [ ] |
| [ ] Access credentials management agreed | Credentials shared how: [method — NOT via email plaintext] | [ ] |
| [ ] Access limited to required data only (least privilege) | Scope of access: [describe] | [ ] |
| [ ] No permanent standing access — access removed at project close | Removal date: [YYYY-MM-DD or "on handover"] | [ ] |

---

## Section 5 — Legal Agreements | الاتفاقيات القانونية

**(STOP if DPA is required but not signed.)**

| Agreement — الاتفاقية | Required? | Status | Date Signed |
|---|---|---|---|
| NDA (Non-Disclosure Agreement) | Always | [ ] Signed [ ] Pending | [YYYY-MM-DD] |
| DPA (Data Processing Agreement) | Required if personal data processed | [ ] Signed [ ] Pending [ ] Not required | [YYYY-MM-DD] |
| Data Classification Schedule (attached to DPA) | If DPA required | [ ] Attached [ ] Pending | [YYYY-MM-DD] |

---

## Section 6 — Data Retention and Deletion | الاحتفاظ بالبيانات وحذفها

| Item — البند | Agreed Value — القيمة المتفق عليها | Confirmed |
|---|---|---|
| Data retention period post-project | Max 90 days after handover (per Data Handling Policy) | [ ] Agreed with client |
| Data return or deletion method at end of retention period | [ ] Return to client [ ] Secure deletion | [ ] Documented in DPA |
| Client notified of deletion date | Notification date: [YYYY-MM-DD] | [ ] |

---

## Section 7 — Storage and Security | التخزين والأمان

| Control — الضابط | Status — الحالة |
|---|---|
| [ ] Client data stored in approved location only | Location: [cloud provider, region, bucket/container name] |
| [ ] Client data NOT stored in LLM prompt history, logs, or training data | Confirmed by: [Dealix Founder] |
| [ ] Client data NOT stored in shared or personal accounts | Confirmed by: [Dealix Founder] |
| [ ] Encryption in transit confirmed (TLS 1.2+) | Confirmed: [ ] Yes |
| [ ] Encryption at rest confirmed | Confirmed: [ ] Yes |
| [ ] Access controls documented — who can access, from where, and for how long | See: [CLIENT_ACCESS_MATRIX.md] |
| [ ] No client credentials stored in code repositories or plaintext files | Confirmed: [ ] Yes |

---

## Sign-Off — التوقيع

| Role — الدور | Name — الاسم | Date — التاريخ |
|---|---|---|
| Dealix Founder | [NAME] | [YYYY-MM-DD] |

**All STOP items must be resolved before this sign-off. Any STOP item unresolved = checklist incomplete = no data access.**

**جميع بنود STOP يجب حلها قبل هذا التوقيع. أي بند STOP غير محلول = القائمة غير مكتملة = لا وصول للبيانات.**

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
