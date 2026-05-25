# Financial Dashboard

> The CEO finance view. Five panels. One screen.

## Panel 1 — Cash

- Cash on hand
- Cash collected (MTD, last 30 days)
- Cash expected (next 30 days)
- Bank reconciliation status (green / amber / red)

## Panel 2 — Burn & Runway

- Gross burn (last month)
- Net burn (last month)
- 3-month rolling net burn
- Runway (months) at current net burn

> Burn = the rate at which cash leaves the company.
> Runway = cash on hand / net burn.
> When net burn is negative (revenue > expenses), runway is effectively
> infinite under steady conditions; report as "profitable".

## Panel 3 — Revenue

- MRR (current)
- MRR (last month)
- Net new MRR (this month)
- Active retainers count
- Average deal size — Sprint
- Average deal size — Retainer (annualised when ≥ 6 months data)

## Panel 4 — Margin

- Gross margin estimate — Sprint
- Gross margin estimate — Retainer
- Direct cost per Sprint (tools + founder hours × shadow rate)
- Direct cost per Retainer (per month)

## Panel 5 — Operational Cash Health

- DSO (Days Sales Outstanding)
- Overdue invoices count and total
- Refund rate (this month)
- Refund rate (rolling 90 days)

## Update Cadence

- Daily: Panel 1
- Weekly: Panels 1, 3
- Monthly: All five panels + capital review

## Source

This dashboard renders from:

- `dealix-ops-private/revenue/cash_collected.csv`
- `dealix-ops-private/revenue/mrr_tracker.csv`
- `dealix-ops-private/finance/expenses.csv`
- `dealix-ops-private/finance/runway_estimate.md`

## Red Flags

| Flag | Threshold | Action |
|------|-----------|--------|
| Runway < 6 months | red | Capital allocation review |
| DSO > 21 days | amber | Tighten payment rules |
| Refund rate > 5% | red | Strategy review |
| Net new MRR negative 2 months in a row | red | Retention deep-dive |
| Gross margin < 50% (Sprint) | amber | Pricing experiment |
