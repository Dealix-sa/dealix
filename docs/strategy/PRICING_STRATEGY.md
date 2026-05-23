# Pricing Strategy

> What we charge, why, and when we change it.
> Tactical price changes go through Weekly CEO Review. Strategy edits this file.

## Pricing Principles

1. **Productize first, then price** — fixed scope before fixed price
2. **Anchor low, climb fast** — start at SAR 499 to remove friction, scale to retainer
3. **Cash before MRR** — every rung up to 1,500 SAR is one-time (fast cash)
4. **Retainer is the goal** — recurring is where leverage compounds
5. **Never discount the productized floor** — discounting signals "not productized"

## The Five-Rung Offer Ladder

| Rung | Offer | Price | Type | Time | Goal |
|---|---|---|---|---|---|
| 1 | Free Diagnostic | 0 SAR | one-time | 30 min call + 1 doc | Qualify + book Sprint |
| 2 | Revenue Sprint | 499 SAR | one-time | 7 days | First paid relationship + proof |
| 3 | Data Pack | 1,500 SAR | one-time | 5 days | Tangible artifact + upsell path |
| 4 | Managed Ops | 2,999 – 4,999 SAR / mo | retainer | monthly | Recurring revenue + retention |
| 5 | Custom AI | 5K – 25K SAR / mo | retainer + project | scoped | High-trust, high-LTV |

## Rung Logic

- **Free → 499** conversion target: ≥ 30%
- **499 → 1,500** conversion target: ≥ 40%
- **1,500 → 2,999 retainer** conversion target: ≥ 30%
- **2,999 → 4,999 expansion** target: ≥ 40% in month 3+

Track these in `docs/revenue/REVENUE_METRICS.md`.

## When To Raise A Price

Raise the price of a rung when:
- Conversion to next rung is > 50% (the rung is too cheap)
- Delivery time has dropped ≥ 30% from baseline (margin allows raise)
- You can show ≥ 3 evidence packs at that rung
- Demand exceeds delivery capacity for that rung

How much to raise: 20% increments. Test for one month. If conversion holds ≥ 80% of prior, lock the new price.

## When To Discount

**Default answer: don't.**

Allowed exceptions (must log in `pricing_experiments.md`):
- Founding 3 retainers at any rung — disclosed as founding-customer pricing, capped at 3
- Bundle discount when upselling — must net higher than single-rung price
- Annual prepay — max 15% discount, must collect cash up front

Forbidden:
- Discounting Free Diagnostic (it's already free)
- Discounting the 499 Sprint (kills the productized floor)
- Discounting Custom AI without founder + advisor approval

## Experiments

All pricing experiments go through:
1. Pre-write the hypothesis in `revenue/pricing_experiments.md` (private)
2. Run for ≥ 14 days or ≥ 10 buyer interactions, whichever first
3. Decide: lock new price, revert, or keep testing
4. Log decision in `DECISION_LOG.md`

## Saudi Market Notes

- Always price in SAR (never USD)
- Always show VAT separately (currently 15%)
- Always offer bank transfer + Stripe + Tabby; cash on request
- Always issue a tax invoice within 24 hours
- Always include Arabic invoice copy

## When Customers Push Back

Common objections + scripted responses live in `pipeline/objections.md` (private). Strategic stance:
- "Too expensive" → reframe to total cost of doing nothing (lost deals × deal size)
- "Why monthly" → explain compounding + monthly evidence reports
- "Can we pay quarterly?" → yes, prepay, 10% discount max
- "Can you do it for free first?" → no — Free Diagnostic exists for that reason

## Pricing Review Cadence

- Weekly: glance at conversion rates per rung
- Monthly: review pricing experiments log
- Quarterly: revisit this strategy doc; full repricing only if North Star metric is missing

## What This Strategy Refuses

- Tiered SaaS pricing (Bronze/Silver/Gold) — not our motion this quarter
- Usage-based pricing — not our motion this quarter
- Free trial of paid rungs — Free Diagnostic is the trial
- Annual contracts > 12 months — no
