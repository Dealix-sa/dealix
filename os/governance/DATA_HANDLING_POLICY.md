# Data Handling Policy — سياسة التعامل مع البيانات

**Version:** 1.0 | **Owner:** Founder | **Effective Date:** 2026-06-01 | **Review:** Annually

Cross-links: [CLIENT_DATA_CLASSIFICATION.md](CLIENT_DATA_CLASSIFICATION.md) | [DPA_TEMPLATE.md](DPA_TEMPLATE.md) | [HUMAN_APPROVAL_MATRIX.md](HUMAN_APPROVAL_MATRIX.md) | [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) | [../delivery/DATA_PROCESSING_CHECKLIST.md](../delivery/DATA_PROCESSING_CHECKLIST.md)

---

## 1. Scope — النطاق

This policy covers all client data processed by Dealix or its agents — including data received, stored, analyzed, transformed, or transmitted as part of any project, audit, pilot, retainer, or pre-sales engagement.

تغطي هذه السياسة جميع بيانات العملاء التي تعالجها ديليكس أو وكلاؤها — بما يشمل البيانات المُستقبَلة والمخزَّنة والمحلَّلة والمحوَّلة أو المنقولة في إطار أي مشروع أو تدقيق أو تجريب أو استيعاب أو تواصل قبل البيع.

**In scope:**
- Client operational data (records, reports, workflow outputs)
- Personal data of client employees or customers included in datasets
- Credentials or API keys shared by the client with Dealix
- Sample and test data received before SOW is signed

**Out of scope:**
- Publicly available company information used in research (covered by [../01_CLAUDE.md](../01_CLAUDE.md))
- Dealix's own internal operational data

---

## 2. Classification — التصنيف

Four-tier classification. Full definitions and examples in [CLIENT_DATA_CLASSIFICATION.md](CLIENT_DATA_CLASSIFICATION.md).

| Tier — المستوى | Description — الوصف | Examples — الأمثلة |
|---|---|---|
| **Public** | Freely available, no harm if shared | Company name, public website, job titles |
| **Internal** | Business-sensitive but not individually identifiable | Workflow docs, KPIs, process maps, internal reports |
| **Confidential** | High sensitivity — limited distribution | Contracts, financials, pricing, customer lists, personnel data |
| **Restricted** | Highest sensitivity — strict access control | Credentials, API keys, national IDs, legal matters, health data |

Every dataset received from a client is classified before processing. Unclassified data is treated as Restricted until assessed.

---

## 3. Storage Rules — قواعد التخزين

| Rule — القاعدة |
|---|
| Client data is stored ONLY in approved, named storage locations per project (documented in CLIENT_ACCESS_MATRIX.md) |
| Client data is NEVER written to LLM prompt history, conversation logs, or any AI model training pipeline |
| Client data is NEVER stored in personal cloud accounts (Google Drive personal, personal Dropbox, etc.) |
| Client data is NEVER stored in code repositories (GitHub, GitLab) — use secrets managers for credentials |
| Confidential and Restricted data is encrypted at rest (AES-256 or equivalent) and in transit (TLS 1.2+) |
| Access to stored client data requires individual (not shared) credentials and is logged |

---

## 4. Access Control — ضبط الوصول

| Principle — المبدأ | Application — التطبيق |
|---|---|
| Need-to-know | Access granted only to team members whose role requires it for the specific task |
| Least privilege | Read access by default. Write access only when the task requires it. Admin access never assumed. |
| No shared credentials | Each team member has individual access. No shared passwords or API keys. |
| Time-limited access | Access expires at project handover or 90 days post-delivery, whichever is earlier |
| Documented | All access documented in CLIENT_ACCESS_MATRIX.md before it is granted |
| Founder approval | Access to Restricted data requires explicit founder approval before granting |

---

## 5. Retention — الاحتفاظ بالبيانات

| Category — الفئة | Retention Period — فترة الاحتفاظ | Action at End of Period |
|---|---|---|
| Project data (all tiers) | Max 90 days after handover sign-off | Securely deleted OR returned to client — per DPA |
| Sample data (pre-SOW) | Max 30 days after decision to proceed or not | Securely deleted |
| Credentials (API keys, passwords) | Duration of active project only | Revoked and confirmed deleted immediately at project close |
| Legal documents (signed SOW, NDA, DPA) | 7 years — legal requirement | Retained in secure document management, not in project data folders |

**Retention does not mean permission to process.** Retained data may only be accessed for audit or dispute resolution purposes, not re-processed for new purposes.

---

## 6. Breach Response — الاستجابة للاختراق

A data breach includes: unauthorized access, accidental disclosure, loss of a device containing client data, or any situation where client data may have been exposed to an unauthorized party.

| Step — الخطوة | Action — الإجراء | Timing — التوقيت |
|---|---|---|
| 1 | Team member who detects potential breach stops accessing data and notifies Founder immediately | Immediately |
| 2 | Founder assesses whether a breach has occurred and its scope | Within 1 hour |
| 3 | Founder notifies affected client | Within 24 hours of confirmed breach |
| 4 | Incident documented in incident register — reference [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) | Within 24 hours |
| 5 | Root cause identified and remediation implemented | Within 72 hours |
| 6 | Regulatory notification (PDPL authority) if personal data is involved | Per PDPL requirements |

**No breach is managed silently.** Clients are notified within 24 hours regardless of assessed impact. This is non-negotiable.

---

## 7. PDPL Compliance — الامتثال لنظام PDPL

Saudi Arabia's Personal Data Protection Law (PDPL) applies to all personal data of Saudi residents processed by Dealix.

| PDPL Principle — مبدأ PDPL | Dealix Implementation |
|---|---|
| **Consent** | Personal data is not processed without the data subject's consent (obtained by the client as data controller) or a valid legal basis documented in the DPA |
| **Purpose limitation** | Data is processed only for the purpose stated in the DPA. No secondary processing without a new legal basis. |
| **Data minimization** | Only data strictly necessary for the defined workflow is accessed. No bulk data pulls when subset suffices. |
| **Accuracy** | Dealix does not modify source personal data. If inaccuracies are found, the client is notified. |
| **Storage limitation** | Retention periods per Section 5 above. No data held beyond the agreed period. |
| **Security** | Technical and organizational measures per Sections 3 and 4 above. |
| **Accountability** | Founder is the designated data protection responsible party. DPA signed for all personal data processing. |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
