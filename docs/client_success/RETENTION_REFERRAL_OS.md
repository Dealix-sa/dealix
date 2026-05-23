# Retention & Referral OS

> The system that keeps customers and asks — only at the right moment — for referrals.

## 1. Health model

Per-customer health combines:

- Outcome attribution (was the promised outcome delivered?)
- Usage (is the customer engaging with the operating cadence?)
- Operator NPS (every 60 days)
- Open issues (and time-to-resolution)

Health bands: **green**, **amber**, **red**.

## 2. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Per-customer health refresh |
| Bi-weekly | Operating review with customer |
| Monthly | Outcome review with founder counterpart |
| Quarterly | Business review + roadmap |

## 3. Expansion

Expansion is triggered when:

- Customer is **green** for ≥ 60 days.
- A new outcome opportunity appears in the operating review.
- Pricing guardrails support the upgrade.

Expansion drafts go through `/approvals`.

## 4. Referral asks

Referral asks only after a delivered outcome and the customer is **green**. See `PARTNER_REFERRAL_MACHINE.md` for the queue contract.

## 5. Saves

When a customer becomes **amber** or **red**:

- Trigger a save play (named, time-boxed, owner identified).
- Founder is informed in the daily brief.
- Save plays are recorded in audit.

## 6. KPI

| KPI | Target |
|---|---|
| Net Revenue Retention (NRR) | tracked monthly |
| Logo retention | tracked quarterly |
| Referrals per healthy customer per year | tracked |

## 7. Trust

Customers in **red** do not receive marketing nurture. Their channel is operator-led only.
