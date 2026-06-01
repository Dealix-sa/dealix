# Client Data Classification Guide — دليل تصنيف بيانات العميل

**Version:** 1.0 | **Owner:** Founder | **Effective Date:** 2026-06-01 | **Review:** Annually

Cross-links: [DATA_HANDLING_POLICY.md](DATA_HANDLING_POLICY.md) | [DPA_TEMPLATE.md](DPA_TEMPLATE.md) | [../delivery/DATA_PROCESSING_CHECKLIST.md](../delivery/DATA_PROCESSING_CHECKLIST.md) | [../delivery/CLIENT_ACCESS_MATRIX.md](../delivery/CLIENT_ACCESS_MATRIX.md)

---

## How to Use This Guide — كيفية الاستخدام

At project intake, classify every dataset and data source received from the client using the four-tier system below. Classification drives storage, access control, and handling rules. When in doubt, classify upward (assign the higher tier).

عند استقبال المشروع، صنّف كل مجموعة بيانات ومصدر بيانات تستقبله من العميل باستخدام النظام الرباعي أدناه. التصنيف يحدد التخزين وضبط الوصول وقواعد المعالجة. في حالة الشك — صنّف للمستوى الأعلى.

---

## Tier 1 — Public | عام

**Definition:** Information that is already publicly available or poses no risk if disclosed.

**التعريف:** معلومات متاحة للعموم أصلاً أو لا تشكّل خطراً عند الإفصاح عنها.

**Examples — أمثلة:**
- Company name, registered address, commercial registration number
- Job titles and organizational structure as shown on the company website
- Public-facing product or service descriptions
- Industry classification (e.g., "FM company operating in Saudi Arabia")
- Public procurement announcements and RFP responses already released

**Handling rules:**
- Can be stored in general project documentation without encryption
- Can be included in research and briefing documents
- Can be referenced in proposals (with attribution where appropriate)
- No special access controls required

---

## Tier 2 — Internal | داخلي

**Definition:** Information used internally by the client that is not public but not individually sensitive. Business-sensitive. Moderate impact if disclosed.

**التعريف:** معلومات تستخدمها الشركة داخلياً، غير متاحة للعموم، لكنها ليست حساسة على مستوى الأفراد. حساسية تجارية. أثر متوسط عند الإفصاح.

**Examples — أمثلة:**
- Workflow documentation and standard operating procedures (SOPs)
- Process maps and operational flowcharts
- Internal KPIs and performance dashboards (non-financial)
- Meeting notes and project reports
- Non-financial operational data (work orders, maintenance logs, production volumes)
- Anonymized aggregate statistics

**Handling rules:**
- Store in project-designated folders with access limited to Dealix team members working on this project
- Encryption in transit required (TLS)
- Encryption at rest recommended but not mandatory for lowest-sensitivity Internal data
- Not to be shared with any third party without client consent
- Deleted or returned within 90 days of project close

---

## Tier 3 — Confidential | سري

**Definition:** High-sensitivity information. Restricted distribution within the client organization. Significant impact if disclosed to unauthorized parties.

**التعريف:** معلومات عالية الحساسية. توزيع مقيَّد داخل المؤسسة. أثر جوهري عند الإفصاح لجهات غير مخوَّلة.

**Examples — أمثلة:**
- Contracts, agreements, and legal documents
- Financial statements, budgets, and pricing data
- Customer and vendor lists with contact details
- Personnel data — names, salaries, performance reviews
- Proprietary formulas, technical specifications, or trade secrets
- Strategic plans, M&A discussions, or board-level decisions
- Client's own client data (second-level confidentiality)

**Handling rules:**
- Store in encrypted, access-controlled storage only
- Encryption at rest (AES-256 or equivalent) required
- Access strictly limited to named individuals with documented business need
- DPA must be in place before any Confidential data is processed
- Never included in LLM prompts or AI conversation history
- Transmission only via encrypted channel (not plain email)
- Deleted or returned within 90 days — with written confirmation of deletion

---

## Tier 4 — Restricted | مقيَّد

**Definition:** Highest sensitivity. Access to even one unauthorized person constitutes a breach. Legal consequences likely if disclosed. Requires immediate founder sign-off before any access.

**التعريف:** أعلى درجات الحساسية. وصول شخص واحد غير مخوَّل يُعدّ اختراقاً. عواقب قانونية محتملة عند الإفصاح. يتطلب موافقة المؤسس الفورية قبل أي وصول.

**Examples — أمثلة:**
- API keys, system passwords, authentication credentials
- National ID numbers (Saudi Iqama / ID), passport numbers
- Financial account details — IBAN, account numbers, card numbers
- Health or medical data (sensitive personal data under PDPL)
- Biometric data
- Legal case files, litigation materials, privileged communications
- Government security classifications

**Handling rules:**
- Founder approval required before access is granted
- Stored ONLY in a dedicated secrets manager or hardware-secured vault — never in files, email, or code
- Zero copies made beyond what is operationally necessary
- Never transmitted via email — use encrypted, expiring link or secure transfer tool
- Never included in any AI prompt, log, or system context
- Access logged individually with timestamp — every access event recorded
- Immediate secure deletion when purpose is complete — not held until 90-day window
- Breach of Restricted data triggers immediate incident response per [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

---

## Classification Decision Tree — شجرة قرار التصنيف

```
Is this data publicly available?
│
├─ YES → Tier 1 (Public)
│
└─ NO → Does it contain individual personal identifiers (names, IDs, biometrics, health)?
         │
         ├─ YES and it is credentials/legal/financial accounts → Tier 4 (Restricted)
         ├─ YES and it is personnel/customer data → Tier 3 (Confidential)
         │
         └─ NO → Does it contain contracts, financials, or strategic plans?
                  │
                  ├─ YES → Tier 3 (Confidential)
                  │
                  └─ NO → Tier 2 (Internal)
```

---

## Data Handling Summary Table — جدول ملخص قواعد المعالجة

| Rule | Tier 1 Public | Tier 2 Internal | Tier 3 Confidential | Tier 4 Restricted |
|---|---|---|---|---|
| Encryption in transit | Not required | Required | Required | Required |
| Encryption at rest | Not required | Recommended | Required | Required + vault |
| Access control | Open to project team | Project team only | Named individuals only | Founder approval + named only |
| LLM prompt allowed | Yes | No (unless anonymized) | No | No |
| DPA required | No | No | Yes | Yes + legal review |
| Retention | Per project | 90 days post-close | 90 days post-close | Delete when task complete |
| Breach protocol | Log | Notify founder | Notify founder + client | Immediate incident response |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
