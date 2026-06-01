# MVP Scope Definition Template — قالب تحديد نطاق المنتج الأولي

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [ACCEPTANCE_CRITERIA_TEMPLATE.md](ACCEPTANCE_CRITERIA_TEMPLATE.md) | [CHANGE_REQUEST_TEMPLATE.md](CHANGE_REQUEST_TEMPLATE.md) | [RISK_REGISTER_TEMPLATE.md](RISK_REGISTER_TEMPLATE.md) | [../governance/SOW_TEMPLATE.md](../governance/SOW_TEMPLATE.md)

---

## Rule: Define Before Building — القاعدة: حدّد قبل أن تبني

This template must be completed and signed off by both Dealix and the client before any build work begins. Any scope defined after build starts is a change request. Undefined scope is not built.

يجب استكمال هذا القالب والموافقة عليه من ديليكس والعميل قبل بدء أي بناء. أي نطاق يُحدَّد بعد بدء البناء يُعامَل كطلب تغيير. النطاق غير المحدد لا يُبنى.

---

## Section 1 — Project Overview | نظرة عامة على المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| Client label | [CLIENT_LABEL — no PII] |
| Sector | [FM / Contracting / Industrial / Legal / Real Estate / B2B / International] |
| Project type | [Audit / Pilot / Full System / Retainer / Expansion Module] |
| SOW reference | [SOW-YYYY-NNN] |
| Dealix project lead | [Role] |
| Client project contact | [Title / Role] |
| Scope definition date | [YYYY-MM-DD] |
| Target delivery date | [YYYY-MM-DD] |

**One-sentence objective:**
[State what this MVP will achieve in one specific, measurable sentence. No adjectives. Example: "Automate the generation of weekly maintenance summary reports from raw work order data, reducing manual preparation time from 6 hours to under 1 hour."]

**الهدف في جملة واحدة:**
[حدد ما ستحققه هذه النسخة الأولى في جملة واحدة محددة وقابلة للقياس. بدون صفات مجردة.]

---

## Section 2 — In-Scope Workflows | العمليات ضمن النطاق

**Maximum 3 workflows for an MVP.** More than 3 workflows in an MVP is scope creep before build starts.

**الحد الأقصى 3 عمليات لأي منتج أولي.** أكثر من 3 عمليات في المنتج الأولي هو توسع في النطاق قبل البناء.

### Workflow 1 — [NAME]

- **Description:** [What this workflow does — input, process, output]
- **Current state:** [How it is done today — e.g., "Manual Excel consolidation from 5 team leads, emailed to manager every Sunday"]
- **Target state:** [What the system will do — e.g., "System pulls data from ERP export, generates formatted report, delivers to manager inbox by 07:00 Sunday"]
- **Data source:** [System name, format, access method]
- **Output format:** [PDF / Excel / Email / Dashboard / API response]

### Workflow 2 — [NAME]

- **Description:** [Description]
- **Current state:** [Current state]
- **Target state:** [Target state]
- **Data source:** [Source]
- **Output format:** [Format]

### Workflow 3 — [NAME] *(if applicable)*

- **Description:** [Description]
- **Current state:** [Current state]
- **Target state:** [Target state]
- **Data source:** [Source]
- **Output format:** [Format]

---

## Section 3 — Out of Scope | خارج النطاق

List explicitly what is NOT included in this MVP. Out-of-scope items are candidates for expansion modules.

اذكر صراحةً ما هو غير مشمول في هذه النسخة. العناصر خارج النطاق مرشحة لوحدات التوسع.

- [ ] [Item 1 — e.g., "Integration with client CRM system — future phase"]
- [ ] [Item 2 — e.g., "Arabic-language NLP processing — future phase"]
- [ ] [Item 3 — e.g., "Mobile app interface — out of scope entirely"]
- [ ] [Item 4 — e.g., "Historical data migration before 2022 — excluded"]
- [ ] [Item 5 — e.g., "Staff training program — separate engagement"]
- [ ] Any workflow not listed in Section 2 above

---

## Section 4 — Data Sources | مصادر البيانات

Complete [DATA_PROCESSING_CHECKLIST.md](DATA_PROCESSING_CHECKLIST.md) and [API_INTAKE_CHECKLIST.md](API_INTAKE_CHECKLIST.md) in parallel.

| Data Source | Format | Access Method | Owner | Classification | Confirmed |
|---|---|---|---|---|---|
| [System name] | [CSV / API / DB / Excel] | [Export / API / Direct DB read] | [Client IT / Dealix] | [Public / Internal / Confidential / Restricted] | [ ] |
| [System name] | [Format] | [Method] | [Owner] | [Class] | [ ] |

---

## Section 5 — Success Criteria | معايير النجاح

Each criterion must be measurable and verifiable. Defined here, formalized in [ACCEPTANCE_CRITERIA_TEMPLATE.md](ACCEPTANCE_CRITERIA_TEMPLATE.md).

كل معيار يجب أن يكون قابلاً للقياس والتحقق. يُحدَّد هنا، ويُرسمَّل في قالب معايير القبول.

| Criterion — المعيار | Measurement Method — طريقة القياس | Target — الهدف | Who Verifies — من يتحقق |
|---|---|---|---|
| [e.g., Report generation time] | [Timer from data pull to output delivery] | [< 5 minutes] | [Dealix + Client] |
| [e.g., Output accuracy] | [QA check against manually prepared report — 3 samples] | [≥ 95% accuracy] | [Client reviewer] |
| [e.g., System uptime] | [Monitoring log over 2-week test period] | [≥ 99%] | [Dealix] |

---

## Section 6 — Timeline Estimate | تقدير الجدول الزمني

| Phase — المرحلة | Duration — المدة | Start — البداية | End — النهاية |
|---|---|---|---|
| Data access and intake | [X] days | [Date] | [Date] |
| Build — Workflow 1 | [X] days | [Date] | [Date] |
| Build — Workflow 2 | [X] days | [Date] | [Date] |
| Internal QA | [X] days | [Date] | [Date] |
| UAT (client testing) | [X] days | [Date] | [Date] |
| Fix and finalize | [X] days | [Date] | [Date] |
| Handover | [X] days | [Date] | [Date] |
| **Total** | **[X] days** | [Date] | **[Date]** |

---

## Section 7 — Risks and Assumptions | المخاطر والافتراضات

Full risk detail in [RISK_REGISTER_TEMPLATE.md](RISK_REGISTER_TEMPLATE.md). List critical assumptions here.

| Assumption — الافتراض | Risk if Wrong — الخطر إن كان خاطئاً |
|---|---|
| [e.g., Client API access confirmed within 5 days of SOW signing] | [Project start delayed — may push delivery date] |
| [e.g., Data quality is as described in discovery — < 10% null fields] | [Additional data cleaning adds 5–10 days to build] |
| [e.g., Client UAT reviewer allocated 2 hours/week] | [UAT phase extended — delivery delayed] |

---

## Sign-Off — التوقيع

| Role — الدور | Name — الاسم | Date — التاريخ | Signature — التوقيع |
|---|---|---|---|
| Dealix Founder | [NAME] | [YYYY-MM-DD] | ________________ |
| Client Project Contact | [TITLE] | [YYYY-MM-DD] | ________________ |

**By signing, both parties confirm: (1) the scope defined above is agreed, (2) any additions require a signed Change Request, (3) build begins only after this document is countersigned.**

**بالتوقيع، يؤكد الطرفان: (1) الموافقة على النطاق المحدد أعلاه، (2) أي إضافات تستلزم طلب تغيير موقّعاً، (3) لا يبدأ البناء إلا بعد توقيع هذا المستند من الطرفين.**

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
