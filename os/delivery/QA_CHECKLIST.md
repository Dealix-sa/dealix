# Dealix — QA Checklist
# قائمة مراجعة الجودة

**Version:** 1.0 | Gate: QA must pass before delivery to client.

---

## Pre-QA Gate

Before running QA, confirm:
- [ ] Scope document signed
- [ ] Acceptance criteria documented and agreed
- [ ] Sample data available (no production data required yet)
- [ ] Demo path works end-to-end in sandbox

---

## Functional QA Checklist

### Agent / Workflow Behavior
- [ ] Primary workflow runs without errors on sample data
- [ ] Edge cases handled (empty inputs, malformed data, missing fields)
- [ ] Error messages are meaningful (not stack traces to user)
- [ ] Timeout behavior defined and tested
- [ ] Retry logic confirmed where applicable

### Human Approval Points
- [ ] All human approval gates are active and cannot be bypassed
- [ ] Approval notifications working
- [ ] Approval override by founder tested
- [ ] Blocked actions actually block (cold_whatsapp, linkedin_automation, etc.)

### Data Handling
- [ ] No PII in logs
- [ ] Sample data only — no production data used in build phase
- [ ] Data stays in client environment (if data sovereignty required)
- [ ] No data sent to external models without documented approval

### Governance Decision Field
- [ ] Every output object carries governance_decision field
- [ ] governance_decision includes module, version, and key decision
- [ ] Audit log entries written for all significant actions

### Performance
- [ ] Key workflows complete within acceptable time (document target)
- [ ] No memory leaks in long-running agents
- [ ] Load tested to expected volume

---

## Demo Path Checklist

Before presenting to client:
- [ ] Demo runs on clean data (not prod)
- [ ] Happy path works flawlessly
- [ ] 2 edge cases demonstrated and handled gracefully
- [ ] Dashboard / output format reviewed with client preview
- [ ] No hardcoded test data in demo path

---

## QA Sign-Off

QA completed by: [name]
Date: [date]
Acceptance criteria met: [yes / no — details]
Issues found: [list or "none"]
Gate passed: [yes / no]
Next step: UAT with client

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
