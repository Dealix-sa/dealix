# Risk Register Template — سجل المخاطر

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [MVP_SCOPE_TEMPLATE.md](MVP_SCOPE_TEMPLATE.md) | [CHANGE_REQUEST_TEMPLATE.md](CHANGE_REQUEST_TEMPLATE.md) | [DATA_PROCESSING_CHECKLIST.md](DATA_PROCESSING_CHECKLIST.md) | [../governance/INCIDENT_RESPONSE.md](../governance/INCIDENT_RESPONSE.md)

---

## Rule — القاعدة

The risk register is populated at project start and reviewed at every project status call. Any risk that materializes becomes either a change request or an incident. Risks do not disappear — they are managed, mitigated, or escalated.

يُعبَأ سجل المخاطر عند بدء المشروع ويُراجع في كل اجتماع حالة. أي خطر يتحقق يصبح إما طلب تغيير أو حادثة. المخاطر لا تختفي — تُدار أو تُخفَّف أو تُصعَّد.

---

## Project Header — رأس المشروع

| Field — الحقل | Value — القيمة |
|---|---|
| Project name | [PROJECT_NAME] |
| SOW reference | [SOW-YYYY-NNN] |
| Client label | [CLIENT_LABEL] |
| Risk register version | [1.0] |
| Owner | [Dealix Founder] |
| Last reviewed | [YYYY-MM-DD] |

---

## Risk Matrix — مصفوفة المخاطر

**Impact scale:** High = project failure or significant rework / Medium = delay or cost increase / Low = minor inconvenience
**Probability scale:** High = likely if no action taken / Medium = possible / Low = unlikely but worth monitoring

| Risk ID | Risk Description | Impact | Probability | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-001 | Client API access delayed | High | Medium | Confirm API access timeline in SOW. Escalate at 5 days past agreed date. | Client IT + Dealix | Open |
| R-002 | Data quality worse than expected at intake | High | Medium | Review sample data before build starts. Define acceptable data quality threshold in MVP Scope. Add data cleaning buffer to timeline. | Dealix | Open |
| R-003 | Scope creep — "small addition" requests | High | High | All additions require signed CR. No verbal agreements. Weekly scope check against original SOW. | Founder | Open |
| R-004 | Key client contact leaves during project | Medium | Low | Identify backup contact at project start. Document all decisions in writing so knowledge is not person-dependent. | Client | Open |
| R-005 | Integration with legacy system blocked | High | Medium | Validate integration approach in API Intake Checklist before build starts. Define fallback approach (file export) if API unavailable. | Dealix + Client IT | Open |
| R-006 | AI output quality below acceptance criteria | High | Low | Define acceptance criteria before build. Run QA testing on 3+ sample batches before UAT. Identify error patterns early. | Dealix QA | Open |
| R-007 | Legal or compliance block on data usage | High | Low | DPA signed before data access. Classify all data before processing. PDPL review for personal data. | Founder + Client legal | Open |
| R-008 | Payment delayed past milestone date | Medium | Medium | SOW includes payment terms and work-pause clause at 21 days overdue. Invoice sent on milestone completion date. Track in invoice tracker. | Founder | Open |

---

## Project-Specific Risks — مخاطر خاصة بالمشروع

Add rows for risks specific to this engagement:

| Risk ID | Risk Description | Impact | Probability | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-009 | [Project-specific risk] | [H/M/L] | [H/M/L] | [Mitigation] | [Owner] | Open |
| R-010 | [Project-specific risk] | [H/M/L] | [H/M/L] | [Mitigation] | [Owner] | Open |

---

## Risk Status Definitions — تعريفات حالة المخاطر

| Status — الحالة | Meaning — المعنى |
|---|---|
| Open | Risk is active and mitigation is in place |
| Materialized | Risk has occurred — now a change request or incident |
| Closed | Risk no longer applies (build phase passed, issue resolved) |
| Watch | Low probability but monitoring required |

---

## Risk Review Cadence — دورية مراجعة المخاطر

| Frequency — التكرار | Action — الإجراء |
|---|---|
| Weekly (every status call) | Review all Open risks. Update status. Escalate any that have materialized. |
| At build milestone | Full risk register review before moving to next phase. |
| At UAT start | Confirm all High-probability risks have been mitigated before client testing begins. |
| At project close | Archive risk register. Document which risks materialized and what the actual impact was (for future project estimation). |

---

## Escalation Path — مسار التصعيد

If a risk materializes:

1. **Identify:** Risk owner identifies materialization. Document with date, description, and current project impact.
2. **Classify:** Is this a Change Request (scope/cost/time impact) or an Incident (data breach, system failure, compliance issue)?
3. **Change Request path:** Open [CHANGE_REQUEST_TEMPLATE.md](CHANGE_REQUEST_TEMPLATE.md) within 24 hours.
4. **Incident path:** Follow [../governance/INCIDENT_RESPONSE.md](../governance/INCIDENT_RESPONSE.md) playbook.
5. **Notify Founder:** All materialized High or Medium risks — notify founder within 4 hours.
6. **Notify Client:** If client is impacted — notify within 24 hours. Do not delay client notification to resolve the issue first.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
