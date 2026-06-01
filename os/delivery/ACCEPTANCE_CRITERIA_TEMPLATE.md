# Acceptance Criteria Template — قالب معايير القبول

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [UAT_SIGNOFF_TEMPLATE.md](UAT_SIGNOFF_TEMPLATE.md) | [CHANGE_REQUEST_TEMPLATE.md](CHANGE_REQUEST_TEMPLATE.md) | [../governance/SOW_TEMPLATE.md](../governance/SOW_TEMPLATE.md)

---

## Rule — القاعدة

**Acceptance criteria are defined BEFORE build starts. No criteria = no build.**

Undefined criteria create post-delivery disputes. If a client cannot articulate what "done" looks like before the build, that is a scoping problem — resolve it in [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) first.

**معايير القبول تُحدَّد قبل بدء البناء. بدون معايير = بدون بناء.**

المعايير غير المحددة تخلق نزاعات ما بعد التسليم. إذا لم يستطع العميل تحديد ما يعني "مكتمل" قبل البناء — هذه مشكلة في تحديد النطاق، تُحَل أولاً في قالب نطاق المنتج الأولي.

---

## Project Header — رأس المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Client label | [CLIENT_LABEL] |
| Acceptance criteria version | [1.0] |
| Defined by | [Dealix + Client — jointly] |
| Date defined | [YYYY-MM-DD] |
| Approved by (Dealix) | [Founder / Role] |
| Approved by (Client) | [Title / Role] |

---

## Acceptance Criteria Table — جدول معايير القبول

One row per deliverable. If a deliverable fails any Pass Criterion, it is not accepted — regardless of overall project progress.

صف واحد لكل مخرج. إذا فشل أي مخرج في معيار واحد — لا يُقبل، بغض النظر عن تقدم المشروع الإجمالي.

| # | Deliverable — المخرج | Definition of Done — تعريف الاكتمال | Verification Method — طريقة التحقق | Verified By — من يتحقق | Pass Criterion — معيار القبول | Status — الحالة |
|---|---|---|---|---|---|---|
| D1 | [e.g., Automated maintenance report] | System generates report from raw data with zero manual input | Run system end-to-end with live data; Dealix observes; client reviews output | Dealix + Client reviewer | Report matches manual benchmark ≥ 95% accuracy on 3 consecutive runs | [ ] Pass [ ] Fail |
| D2 | [e.g., Email delivery to stakeholders] | Report delivered to defined recipient list by scheduled time | Check delivery log; confirm receipt in recipient inbox | Client IT contact | 100% delivery success across 5 test cycles with no errors | [ ] Pass [ ] Fail |
| D3 | [e.g., Error handling] | System surfaces meaningful error message if source data is missing or malformed | Deliberately provide malformed input; observe system response | Dealix QA | Error message displayed; system does not crash; alert sent to admin within 2 minutes | [ ] Pass [ ] Fail |
| D4 | [e.g., Documentation] | Handover document covering system architecture, operating instructions, and maintenance guide delivered | Client receives document; reviews for completeness against checklist | Client + Dealix | All checklist sections present; client confirms readability | [ ] Pass [ ] Fail |
| D5 | [Add rows for each deliverable] | [Definition] | [Method] | [Who] | [Criterion] | [ ] Pass [ ] Fail |

---

## Non-Functional Criteria — المعايير غير الوظيفية

These apply to the system overall, not to individual deliverables.

هذه المعايير تنطبق على النظام بأكمله، وليس على مخرج بعينه.

| Category — الفئة | Criterion — المعيار | Target — الهدف | Verified By — من يتحقق |
|---|---|---|---|
| Performance | End-to-end processing time for standard input | < [X] minutes/seconds | Dealix timed test |
| Reliability | System uptime over 2-week test period | ≥ 99% | Monitoring log |
| Security | No client data written to logs or LLM prompts | Zero violations on audit | Dealix internal audit |
| Maintainability | System documented so a new Dealix team member can operate it without original builder | Documentation review by third party | Dealix |
| Compliance | PDPL-relevant personal data handled per DPA | Zero DPA violations | Dealix + Client legal |

---

## Conditional Acceptance — القبول المشروط

If a deliverable passes all criteria except one minor issue (does not block primary function), the client may issue Conditional Acceptance:

إذا اجتاز المخرج جميع المعايير ما عدا مشكلة ثانوية واحدة (لا تعيق الوظيفة الأساسية)، يمكن للعميل إصدار قبول مشروط:

- Issue is logged with a resolution deadline (max 7 business days)
- Conditional Acceptance does not release final payment — held until issue resolved
- If issue not resolved by deadline, Conditional converts to Fail

**Conditional Acceptance is not a precedent for accepting incomplete work.**

---

## Dispute Resolution — حل النزاعات

If Dealix and client disagree on whether a criterion is met:

1. Both parties document their assessment in writing.
2. Dealix proposes one specific additional test or evidence to resolve the disagreement.
3. Founder reviews and makes final call if unresolved after additional test.
4. If still unresolved — refer to SOW dispute resolution clause.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
