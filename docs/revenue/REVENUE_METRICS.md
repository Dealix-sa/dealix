# Revenue Metrics

> The numbers the company is allowed to optimise.

## Tier 0 — Truth metrics (the only ones we report externally)

- **Cash collected.** Money in the bank account this period.
- **Active retainers.** Number of monthly retainers paid this month.
- **MRR.** Sum of retainer monthly contracts active right now.

Everything else is internal management metric.

## Tier 1 — Pipeline metrics

- Pipeline value (weighted by stage probability)
- Pipeline value (unweighted)
- Days in stage (per deal)
- Stage conversion rates (the GROWTH_MODEL.md table)
- Proposal-to-payment conversion rate
- Average deal size — Sprint
- Average deal size — Retainer (annualised)
- Average sales cycle — Sprint (days from Contacted → Paid)
- Average sales cycle — Retainer (days from Sprint Delivered → Retainer signed)

## Tier 2 — Revenue quality metrics

- Revenue Quality Tier mix (A / B / C / D %)
- % of revenue from retainers vs sprints
- % of revenue from primary ICP segment
- % of revenue retained quarter-over-quarter

## Tier 3 — Cash health

- Cash collected (by week, month)
- Cash expected (next 30, 60, 90 days)
- DSO (Days Sales Outstanding) — when invoiced
- Overdue invoice count and total
- Refund count and total

## SaaS metrics (deferred)

We do **not** report SaaS-style metrics (CAC, LTV, churn cohorts,
payback period) until **after** we have ≥ 5 retainers and ≥ 6 months
of retainer history. Reporting these earlier produces false precision.

When we begin reporting them, the definitions live in
`docs/finance/MRR_DEFINITION.md` and extensions thereof.

## Anti-Patterns

- Reporting Tier 1 or 2 metrics externally as if they were Tier 0.
- Reporting pipeline value as "revenue" (it is not).
- Reporting MRR with unpaid retainers included.
- Reporting "annualised" anything based on < 3 months of data.

## Verifier

`make weekly-close`:
- Reconciles cash_collected.csv to invoice + receipt files.
- Reconciles MRR tracker to active retainer contracts.
- Flags any external metric reported in the last week that has no
  matching ledger entry.
