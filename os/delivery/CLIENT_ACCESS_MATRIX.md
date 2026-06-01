# Client Access Matrix — مصفوفة وصول العميل

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [DATA_PROCESSING_CHECKLIST.md](DATA_PROCESSING_CHECKLIST.md) | [API_INTAKE_CHECKLIST.md](API_INTAKE_CHECKLIST.md) | [../governance/DATA_HANDLING_POLICY.md](../governance/DATA_HANDLING_POLICY.md) | [../governance/HUMAN_APPROVAL_MATRIX.md](../governance/HUMAN_APPROVAL_MATRIX.md)

---

## Rule — القاعدة

**No access to any client system, data, or resource is assumed. Every access must be explicitly requested, approved in writing, and documented here. Principle of least privilege applies: minimum access needed to complete the defined task, for the minimum time required.**

**لا يُفترض الوصول إلى أي نظام أو بيانات أو مورد للعميل. كل وصول يجب طلبه صراحةً، والموافقة عليه كتابةً، وتوثيقه هنا. مبدأ الحد الأدنى من الصلاحيات: أدنى وصول مطلوب لإتمام المهمة المحددة، في أقل وقت مطلوب.**

---

## Project Header — رأس المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Client label | [CLIENT_LABEL] |
| Matrix version | [1.0] |
| Last updated | [YYYY-MM-DD] |
| Approved by (Dealix) | [Founder] |
| Approved by (Client) | [Client IT Lead — Role] |

---

## Access Matrix Table — جدول مصفوفة الوصول

**Access levels:** Read = can view / Write = can modify / Admin = can configure / None = no access

| System / Resource | Classification | Dealix Read | Dealix Write | Dealix Admin | Client Access | Access Method | Approved By | Expiry / Review |
|---|---|---|---|---|---|---|---|---|
| [e.g., ERP export endpoint] | Internal | Yes | No | No | Full | API key (sandbox) | Client IT + Founder | [Project end date] |
| [e.g., Production ERP] | Confidential | Yes (read-only) | No | No | Full | API key (prod, read-only) | Client IT + Founder | [Date — or on handover] |
| [e.g., Dealix staging environment] | Internal | Full | Full | Full | None | Internal only | Dealix | Ongoing |
| [e.g., Dealix production deployment] | Internal | Full | Full | Full | None (logs viewable on request) | Internal only | Dealix | Ongoing |
| [e.g., Client email distribution list] | Internal | No | No | No | Full (client adds recipients) | Client-managed | Client | N/A |
| [e.g., Shared project folder] | Internal | Yes | Yes | No | Full | Cloud storage link (expiring) | Founder | [YYYY-MM-DD] |
| [Add rows for each system] | | | | | | | | |

---

## Access Request Log — سجل طلبات الوصول

All access requests and approvals logged chronologically:

| Date | System | Access Type Requested | Requested By | Approved By | Approval Date | Notes |
|---|---|---|---|---|---|---|
| [YYYY-MM-DD] | [System] | [Read / Write / Admin] | [Dealix role] | [Client role + Founder] | [YYYY-MM-DD] | |

---

## Access Restrictions — قيود الوصول

The following access types are explicitly blocked for all Dealix team members unless founder provides written exception:

| Blocked Access Type — نوع الوصول المحظور | Reason — السبب |
|---|---|
| Production database write access | Risk of data corruption. Read-only access only. |
| Client HR or personnel systems | PII — restricted. No access without explicit legal review. |
| Client financial systems (ERP payment modules) | Restricted. No access without explicit DPA and founder approval. |
| Client email accounts or inboxes | Privacy. Dealix does not access personal or corporate email accounts. |
| Client social media accounts | Not in service scope. |
| Any system not listed in this matrix | Default = no access until added and approved. |

---

## Access Removal Protocol — بروتوكول إزالة الوصول

Access is revoked at the earlier of:
1. Project handover date (as defined in SOW)
2. 90 days after final delivery
3. Client or Dealix requests early removal
4. Breach or security incident

**Removal process:**
- [ ] Dealix notifies client IT of impending removal date 7 days before
- [ ] API keys and credentials revoked by client IT
- [ ] Dealix confirms keys no longer functional (test call returns 401)
- [ ] Access log updated with removal date
- [ ] Founder signs off on access removal completion

---

## Shared Credentials Policy — سياسة بيانات الاعتماد المشتركة

| Rule — القاعدة |
|---|
| No client credentials stored in code repositories (GitHub, GitLab) — use secrets manager |
| No client credentials in plaintext files, email threads, or chat messages |
| No client credentials stored in LLM prompts or conversation history |
| If credentials are rotated — old keys must be confirmed revoked before new keys are shared |
| Individual team member access — not shared accounts — wherever the system allows |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
