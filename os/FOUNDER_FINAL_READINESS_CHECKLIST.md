# Dealix — Founder Final Readiness Checklist
# قائمة التحقق النهائية للمؤسس

**Date:** [Fill in before launch]
**Branch:** claude/dealix-company-os-operationalize-Jdi6K

This checklist must pass completely before Dealix is considered operationally ready.

---

## Section 1: Repository

- [ ] All OS files present: `os/` has 01-20 numbered files
- [ ] `os/config/` has all 12 config files (countries, sectors, channel-router, anti-ban-guardian, persuasion, scoring, offers, markets, buyer-personas, quotas, experiments, approval-gates)
- [ ] `os/schemas/` has all 10 schema files
- [ ] `os/examples/` has all 6 example files
- [ ] `os/growth/`, `os/sales/`, `os/delivery/`, `os/governance/`, `os/finance/`, `os/success/` all populated
- [ ] `dealix/os_runtime/` has all 12 Python modules
- [ ] `tests/os/` has 6 test files, all passing

---

## Section 2: OS Runtime

- [ ] `python scripts/validate_os_configs.py` exits 0 (all configs valid)
- [ ] `python scripts/validate_os_schemas.py` exits 0 (all schemas valid)
- [ ] `python -m dealix.os_runtime validate` exits 0
- [ ] `pytest tests/os -q` passes (0 failures)
- [ ] `python -m dealix.os_runtime score-company os/examples/company_fm_ksa.json` outputs Tier A
- [ ] `python -m dealix.os_runtime route-offer os/examples/company_legal_ksa.json` outputs legal_knowledge_document_os
- [ ] `python -m dealix.os_runtime approval-check cold_whatsapp` exits 2 (BLOCKED)
- [ ] `python -m dealix.os_runtime growth-dry-run --dry-run` exits 0

---

## Section 3: Doctrine Guards

- [ ] `cold_whatsapp` is blocked in approval_gate
- [ ] `linkedin_automation` is blocked in approval_gate
- [ ] `scraping` is blocked in approval_gate
- [ ] `use_client_data_for_training` is blocked in approval_gate
- [ ] `guaranteed_outcome_claim` is blocked in approval_gate
- [ ] `pii_in_logs` is blocked in approval_gate
- [ ] `send_first_email` requires approval in approval_gate
- [ ] `send_proposal` requires approval in approval_gate
- [ ] Persuasion min score is 82 in persuasion.yml
- [ ] All messages carry `governance_decision` field (verified in tests)

---

## Section 4: Growth Readiness

- [ ] Warm list prepared (data/warm_list.csv or equivalent)
- [ ] Email sender configured and domain warmed
- [ ] LinkedIn profile updated and founder is the only one who will send manually
- [ ] Daily brief script running (`scripts/os_daily_brief.py`)
- [ ] Channel quotas set in os/config/quotas.yml
- [ ] Anti-ban guardian limits configured in os/config/anti-ban-guardian.yml

---

## Section 5: Sales Readiness

- [ ] Sales pipeline defined (os/sales/SALES_PIPELINE.md)
- [ ] Objection library ready (os/sales/OBJECTION_LIBRARY.md)
- [ ] Pricing guardrails confirmed (os/sales/PRICING_GUARDRAILS.md)
- [ ] Discovery call template ready (os/14_DISCOVERY_CALL_TEMPLATE.md)
- [ ] Proposal template ready (os/15_PROPOSAL_TEMPLATE.md)
- [ ] Qualification scorecard ready (os/sales/DEAL_QUALIFICATION_SCORECARD.md)

---

## Section 6: Delivery Readiness

- [ ] Client onboarding process defined (os/delivery/CLIENT_ONBOARDING.md)
- [ ] QA checklist ready (os/delivery/QA_CHECKLIST.md)
- [ ] Handover template ready (os/delivery/HANDOVER_TEMPLATE.md)
- [ ] Delivery gates enforced in `dealix/os_runtime/delivery_gate.py`
- [ ] No build without scope document — confirmed in delivery_gate
- [ ] No production API without approval — confirmed in approval_gate

---

## Section 7: Governance Readiness

- [ ] Data handling policy defined (os/governance/DATA_HANDLING_POLICY.md)
- [ ] Human approval matrix defined (os/governance/HUMAN_APPROVAL_MATRIX.md)
- [ ] Audit log format defined (os/governance/AUDIT_LOG_FORMAT.md)
- [ ] All approvals routed through approval_gate.py (verified in tests)
- [ ] No secrets in repository (git-secrets or equivalent configured)

---

## Section 8: Finance Readiness

- [ ] Floor prices confirmed (os/sales/PRICING_GUARDRAILS.md)
- [ ] Margin guardrails confirmed (os/finance/MARGIN_GUARDRAILS.md)
- [ ] Retainer packages defined (os/finance/RETAINER_PACKAGES.md)
- [ ] Payment terms: 50% upfront, 50% on delivery
- [ ] Invoice process ready (Moyasar or equivalent)

---

## Sign-Off

Founder confirms all items above are checked:

Name: _______________________
Date: _______________________
Signature: _______________________

---

**Post-Readiness:** Proceed to first warm outreach batch when all checks pass.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
