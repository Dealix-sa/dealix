# MRR Definition

A single canonical definition so the number is comparable across months.

## In MRR
- Signed retainer contracts with a fixed monthly amount and active billing this month.
- Recognised once the first invoice is paid.

## Not in MRR
- Sprints, pilots, or any one-time engagement.
- Verbal commitments without a signed contract.
- Pending payments older than 30 days (move to AR, not MRR).
- Discounts that expire in fewer than 90 days (use the post-discount steady-state amount).

## Net New MRR
- New MRR added this month.
- Minus churned MRR (contracts ended).
- Minus contraction (downgraded contracts).
- Plus expansion (upgrades within an existing contract).

## Reporting
- Updated weekly in `dealix-ops-private/revenue/mrr_tracker.csv`.
- Summary in the Weekly CEO Review.
- Trend in the Monthly Strategy Review.

## Rule
There is one MRR number. If anyone reports a different one, this file wins.
