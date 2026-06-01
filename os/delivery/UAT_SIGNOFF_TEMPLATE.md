# UAT Sign-Off Template — قالب اعتماد قبول المستخدم

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [ACCEPTANCE_CRITERIA_TEMPLATE.md](ACCEPTANCE_CRITERIA_TEMPLATE.md) | [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [CHANGE_REQUEST_TEMPLATE.md](CHANGE_REQUEST_TEMPLATE.md) | [../18_HANDOVER_TEMPLATE.md](../18_HANDOVER_TEMPLATE.md)

---

## Rule — القاعدة

UAT is conducted by the client against the acceptance criteria defined before build. Dealix facilitates UAT but does not self-certify. No final payment is released until UAT sign-off is received. Any issue found during UAT is classified (Blocker / Major / Minor) before resolution is prioritized.

يُجري العميل اختبار قبول المستخدم مقابل معايير القبول المحددة قبل البناء. ديليكس تسهّل الاختبار ولا تصادق على نفسها. لا يُصرف الدفع النهائي حتى استلام توقيع اعتماد UAT. أي مشكلة تُكتشف أثناء UAT تُصنَّف (حاجب / رئيسي / ثانوي) قبل تحديد أولوية الحل.

---

## Project Header — رأس المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Client label | [CLIENT_LABEL] |
| UAT start date | [YYYY-MM-DD] |
| UAT end date | [YYYY-MM-DD] |
| UAT environment | [ ] Staging [ ] Production |
| Dealix UAT lead | [Role] |
| Client UAT lead | [Title / Role] |
| Acceptance criteria reference | [Link to ACCEPTANCE_CRITERIA_TEMPLATE.md — version] |

---

## Section 1 — Test Cases Executed | حالات الاختبار المنفَّذة

Reference the acceptance criteria table from [ACCEPTANCE_CRITERIA_TEMPLATE.md](ACCEPTANCE_CRITERIA_TEMPLATE.md). One row per test case.

| Test ID | Deliverable | Test Description | Steps | Expected Result | Actual Result | Status | Issue ID (if fail) |
|---|---|---|---|---|---|---|---|
| TC-001 | [D1 — Report generation] | Run system with standard input dataset | 1. Load approved dataset. 2. Trigger workflow. 3. Observe output | Report generated within [X] minutes, matching format spec | [Actual result] | [ ] Pass [ ] Fail | [ISS-001 or N/A] |
| TC-002 | [D1 — Accuracy] | Compare system output against manual benchmark | 1. Prepare manual report for same dataset. 2. Compare field-by-field | ≥ 95% accuracy across all data fields | [Actual result] | [ ] Pass [ ] Fail | |
| TC-003 | [D2 — Email delivery] | Confirm automated delivery to recipient list | 1. Trigger delivery. 2. Check inbox of each recipient within 10 min | All recipients receive report by scheduled time | [Actual result] | [ ] Pass [ ] Fail | |
| TC-004 | [D3 — Error handling] | Provide malformed input and observe behavior | 1. Submit dataset with known errors. 2. Observe system response | Error message displayed, admin alerted, no crash | [Actual result] | [ ] Pass [ ] Fail | |
| TC-005 | [D4 — Documentation] | Review handover document completeness | 1. Review against documentation checklist. 2. Confirm all sections present | All checklist items confirmed present and readable | [Actual result] | [ ] Pass [ ] Fail | |
| [Add rows] | | | | | | | |

**Test Summary:**

| Total test cases | Passed | Failed | Pass rate |
|---|---|---|---|
| [N] | [N] | [N] | [%] |

---

## Section 2 — Issues Found | المشكلات المكتشفة

For each failed test case, document the issue:

| Issue ID | Test Case | Description | Classification | Recommended Fix | Resolution Deadline | Status |
|---|---|---|---|---|---|---|
| ISS-001 | TC-[N] | [Clear description of what failed and what was observed] | [ ] Blocker [ ] Major [ ] Minor | [Proposed fix] | [YYYY-MM-DD] | [ ] Open [ ] Resolved |

**Issue Classification Definitions:**

| Classification — التصنيف | Definition — التعريف | Impact on Sign-Off |
|---|---|---|
| Blocker | System cannot perform its primary function. Core deliverable is non-functional. | UAT Fail — fix required before sign-off |
| Major | System works but a significant feature is incorrect or missing. Primary function is impaired. | Conditional sign-off — fix required within agreed deadline |
| Minor | Cosmetic or low-impact issue. Primary function is unaffected. | Sign-off can proceed — fix logged for next release |

---

## Section 3 — Overall Verdict | الحكم الإجمالي

| Verdict — الحكم | Condition — الشرط |
|---|---|
| [ ] **Pass** | All test cases passed. Zero Blockers. Zero Majors. |
| [ ] **Conditional Pass** | Zero Blockers. One or more Majors with agreed resolution deadline and holdback payment. |
| [ ] **Fail** | One or more Blockers remain open. UAT cannot sign off until Blockers are resolved and re-tested. |

**Verdict selected:** [ ] Pass [ ] Conditional Pass [ ] Fail

**If Conditional Pass — holdback terms:**
- Amount held back: [SAR] (portion of final payment)
- Release condition: All Major issues resolved and re-tested by [YYYY-MM-DD]
- If not resolved by deadline: Conditional converts to Fail → renegotiate timeline

---

## Section 4 — Retest Log (if applicable) | سجل إعادة الاختبار

| Date | Issue ID | Fix Applied | Retest Result | Retested By |
|---|---|---|---|---|
| [YYYY-MM-DD] | [ISS-NNN] | [Description of fix] | [ ] Pass [ ] Fail | [Client UAT lead role] |

---

## Section 5 — Signature Block — توقيع الطرفين

**By signing this document, both parties confirm: (1) UAT has been conducted against agreed acceptance criteria, (2) the verdict above reflects the genuine outcome of testing, (3) for Pass: final payment is released and handover process begins, (4) for Conditional Pass: final payment is partially released per holdback terms, (5) this document supersedes any verbal feedback or informal approval.**

**بالتوقيع على هذا المستند، يؤكد الطرفان: (1) أُجري UAT مقابل معايير القبول المتفق عليها، (2) الحكم أعلاه يعكس نتيجة الاختبار الحقيقية، (3) للقبول: يُصرف الدفع النهائي وتبدأ عملية الاستلام، (4) للقبول المشروط: يُصرف الدفع النهائي جزئياً وفق شروط الاحتجاز، (5) هذا المستند يحل محل أي تغذية راجعة شفهية أو موافقة غير رسمية.**

| Role — الدور | Name — الاسم | Date — التاريخ | Signature — التوقيع |
|---|---|---|---|
| Dealix Founder | [NAME] | [YYYY-MM-DD] | ________________ |
| Client UAT Lead | [TITLE] | [YYYY-MM-DD] | ________________ |
| Client Authorized Representative (if different) | [TITLE] | [YYYY-MM-DD] | ________________ |

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
