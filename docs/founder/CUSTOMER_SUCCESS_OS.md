# Customer Success OS

What happens after the signature. The system that converts paid
customers into renewals, references, and case studies.

## Purpose

Stop the gap between "signed contract" and "first measurable value" from
being where customers churn.

## Owner

Founder today. Hand-off candidate after the third paying customer.

## Cadence

- Day 0: onboarding kickoff within 24h of contract signature.
- Day 7: first value milestone check.
- Day 30: first business review.
- Day 60: renewal early-warning signal.
- Day 90: case-study eligibility decision.

## Source of Truth

- Per-customer state: `data/customers/<handle>/state.yaml`
- Onboarding script: `scripts/dealix_customer_onboarding_wizard.py`
- Delivery template: `docs/ops/FIRST_CUSTOMER_DELIVERY_TEMPLATE.md`

## Inputs

- Signed contract + scope
- Customer-side admin contact
- Source data access confirmed
- Approved kickoff agenda

## Outputs

- Value milestones logged
- Renewal early-warning score
- Case-study consent + drafts (never published before approval)

## Stages

| Stage | Window | Exit Criteria |
| --- | --- | --- |
| Onboarding | Day 0–7 | First value milestone delivered |
| Activation | Day 7–30 | Three measurable wins logged |
| Business review | Day 30 | Customer agrees to next 60 days |
| Renewal prep | Day 60–90 | Renewal scope drafted |
| Renewal | Day 90+ | Renewal signed OR documented churn reason |

## KPI

- Day-7 milestone hit on ≥ 80% of customers
- Renewal rate ≥ 80% (after first 5 paying customers)
- Mean time-to-first-value < 7 days

## Trust Boundary

External communications with the customer (emails, WhatsApp) are A3
under `policies/dealix_control_policy.yaml` — gated by approval + audit.

## Failure Mode

- Day-7 milestone missed → fires an early-warning entry.
- Customer goes quiet for > 14 days → flagged in war-room.
- Case study drafted but not approved → cannot be published.

## Recovery Path

1. Run the early-warning script for that customer.
2. Reach out via approved channel.
3. Log the recovery as a decision in the decision log.

## Verification

```bash
make business-os
python scripts/verify_everything.py --layer customer_success_os
```

## Next Action

Open `data/customers/`. For every active customer, confirm the next
milestone date is set and the owner is named.
