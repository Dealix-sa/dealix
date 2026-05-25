# MRR Definition

> "MRR" is a precise term. Use it precisely.

## What counts as MRR

A retainer (rung 3, Revenue Desk) contributes to MRR only if:

1. A signed agreement exists with a monthly fee.
2. The first month is **paid**.
3. The contract is currently active (not paused, not on notice).

The MRR contribution = the monthly fee, in SAR.

## What does **not** count as MRR

- One-off Sprints, even if recurring across months.
- Pilots, even if multi-month.
- Trial retainers (free or discounted first month) — counted in
  "trial MRR", reported separately.
- Verbal commitments without a signed agreement.
- Invoiced retainers not yet paid.
- Retainers on notice in their notice period (counted in MRR until
  the notice period ends, then dropped).

## How we report MRR

- **Active MRR:** sum of currently active retainer monthly fees.
- **Net new MRR:** new retainers - lost retainers - expansions - contractions.
- **Trial MRR:** trial / discounted retainers (separate line item).

We do **not** annualise MRR (ARR) until we have ≥ 6 months of MRR history.

## Churn Definitions

- **Logo churn:** number of retainers lost / number active at period start.
- **Revenue churn:** SAR lost / total MRR at period start.

We do **not** report churn until we have ≥ 3 retainers with ≥ 3 months
of history.

## Expansion / Contraction

- Expansion: retainer renews at higher monthly fee. Logged as expansion MRR.
- Contraction: retainer renews at lower monthly fee. Logged as contraction MRR.

## Anti-Patterns

- Including unpaid retainers in MRR.
- Including Sprints (one-off) in MRR.
- Reporting "ARR" by multiplying current MRR × 12 before the retainer
  base is stable.
- Reporting an MRR delta that bundles trial and paid retainers.

## Source of Truth

`dealix-ops-private/revenue/mrr_tracker.csv` with columns:

```
month, customer_id, retainer_status, monthly_fee, contract_start, contract_end, paid, notes
```

The MRR Command Center reads this file each morning.
