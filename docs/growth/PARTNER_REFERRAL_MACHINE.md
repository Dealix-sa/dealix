# Partner / Referral Machine

| Field | Value |
|---|---|
| Purpose | Drive co-sell, partner referrals, and customer referrals |
| Inputs | partner registry, customer health, NPS, delivered outcomes |
| Outputs | `partner_referral_queue.csv` |
| Approval class | Founder approves every ask |
| Trust gate | Customer health ≥ healthy; outcome delivered |
| Owner | Distribution Operator + Retention Copilot |
| KPI | Referral count, partner-sourced cash |
| Failure mode | Ask refused → wait 90 days; do not re-ask within window |

## Rules

- Ask for a referral only after a delivered outcome.
- Frame the ask around helping the referred party, not us.
- Provide a one-paragraph customer-friendly description and a relevant proof link.
- Never bulk-ask. One ask, one partner, one moment.

## Queue schema

```yaml
queue: partner_referral_queue
fields:
  - ask_id
  - source             # partner | customer
  - source_id
  - target_account_or_partner
  - outcome_evidence   # link to delivered outcome
  - draft_en
  - draft_ar
  - status
  - created_at
```
