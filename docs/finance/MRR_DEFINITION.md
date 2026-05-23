# MRR — Definition

> Locked. Changes require Weekly CEO Review approval.

## Definition

**MRR (Monthly Recurring Revenue)** = sum of active retainer monthly values at the end of the reporting period.

```
MRR = Σ (active_retainer_monthly_value × in_period_fraction)
```

## Includes

- Managed Ops monthly fees (committed + paying)
- Custom AI monthly fees (committed + paying, excluding setup fees)
- Any monthly recurring annex / addendum to existing retainers

## Excludes

- One-time fees: Sprint (SAR 499), Data Pack (SAR 1,500)
- Setup fees on Custom AI
- Late fees, refunds, credits (tracked separately in `cash_collected.csv`)
- Pending / probable contracts (not yet paying)
- Pilot months billed but not yet recognized

## Recognition Timing

A retainer counts toward MRR the month the first invoice is **paid** (not signed).

## Pro-Ration

Mid-month start:
- MRR for first month = (days_active / days_in_month) × full_monthly_value
- For headline MRR figure, end-of-month: pro-rated as above
- For trend graphs: use the day-30 full value

## Churn

- Customer cancels → MRR decreases by their monthly value starting the next billing cycle
- Mid-cycle cancellation refund (if any) tracked in `revenue/refunds.csv` separately from MRR
- Churn rate = MRR lost in period / starting MRR of period

## Expansion

- Tier change (2,999 → 4,999) → MRR increases by delta on first paid month at new tier
- Scope add (annex) → MRR increases by annex monthly value
- Expansion rate = expansion MRR / starting MRR of period

## Quick Ratio

```
Quick Ratio = (new MRR + expansion MRR) / (churned MRR + contraction MRR)
```

Target: > 4 (healthy growth)

## Reporting

- Daily Brief: current MRR (single number)
- Weekly Review: MRR delta vs last week, with breakdown (new / expansion / churn / contraction)
- Monthly Board Memo: full MRR walk + quick ratio + cohort retention

## Storage

- `revenue/mrr_tracker.csv` (private repo)
- Schema: date, customer, monthly_value, status (new/active/expansion/contraction/churn), notes

## What This Definition Refuses

- Counting one-time fees as MRR
- Counting probable / committed contracts before they pay
- "Annualized" headline numbers that conflate MRR and ARR misleadingly
- Excluding refunds from the cash narrative (always show both)
- Changing the definition mid-period (annual review only)
