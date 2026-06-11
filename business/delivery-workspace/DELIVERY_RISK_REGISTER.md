# Delivery Risk Register

Categories of risks and how to handle each.

## Access risk
Symptom: Customer hasn't granted access to the agreed system.
Action: Pause dependent deliverables. Escalate at week 2.

## Scope ambiguity
Symptom: Customer asks for things "while we're at it".
Action: Convert to a CO (`CHANGE_REQUEST_POLICY.md`).

## Capacity risk
Symptom: Multiple customers want the same slot.
Action: Stagger weekly reviews. Don't double-book Sundays.

## Reputation risk
Symptom: Customer wants to send a marginal-quality message under Dealix's gate.
Action: Refuse. Document why. Offer an alternative.

## Customer churn risk
Symptom: 2+ skipped weekly reviews, slow approvals.
Action: Trigger `generate_retention_risk_report.py`. Founder calls commercial owner.

## Process
1. Add risk via internal workspace JSON.
2. Severity: `low` / `med` / `high`.
3. Owner: Dealix or customer side.
4. Review weekly.
5. Close with note when resolved.
