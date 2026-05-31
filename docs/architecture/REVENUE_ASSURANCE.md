# Revenue Assurance

Revenue marked "paid" without a verifying event triggers the
`revenue_paid_without_verification` critical alert.

## Verification policy

```json
{
  "policy_id": "revenue_verification_policy_v1",
  "verified_revenue_requires": [
    "payment_received",
    "signed_agreement",
    "retainer_activated",
    "partner_paid_customer"
  ],
  "excluded_from_verified_revenue": [
    "likes", "views", "meetings_booked",
    "verbal_interest", "unqualified_pipeline"
  ],
  "minimum_required": 1
}
```

## Revenue Quality

Per deal:

```
quality = margin + repeatability + retainer_potential + data_moat
        + partner_potential - delivery_burden - risk
```

| Verdict | Score | Action |
| --- | --- | --- |
| HIGH | ≥ 2.5 | Scale; productize; lock in retainer |
| MEDIUM | 1.0–2.49 | Optimize delivery; aim for retainer |
| LOW | 0–0.99 | Reprice, bundle, or pause |
| NEGATIVE | < 0 | Kill |
