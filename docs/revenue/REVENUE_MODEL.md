# Revenue Model

> How money actually flows into Dealix.
> Pairs with `OFFER_LADDER.md` and `PRICING_STRATEGY.md`.

## Revenue Streams (this quarter)

| Stream | Type | Trigger | Cash timing |
|---|---|---|---|
| Free Diagnostic | none (lead gen) | Booked call | n/a |
| Revenue Sprint (499 SAR) | one-time | Signed scope | On signature, before delivery |
| Data Pack (1,500 SAR) | one-time | Sprint complete + upsell | Before delivery |
| Managed Ops (2,999 – 4,999 SAR/mo) | recurring | Contract signed | Monthly, in advance |
| Custom AI (5K – 25K SAR/mo) | recurring + setup | SOW signed | 50% setup up front, monthly thereafter |

## Cash-Collection Rules

1. **No work begins before payment received** (Sprint and Data Pack)
2. **No retainer month begins without that month's invoice paid** (Managed Ops, Custom AI)
3. **Refund policy:** see `docs/finance/BILLING_POLICY.md` — pro-rated refund only for Managed Ops first month if cancelled within 7 days
4. **No barter, no equity-for-services, no "pay us later"**

## Revenue Recognition

- **Sprint / Data Pack** — recognized on delivery handoff
- **Managed Ops / Custom AI** — recognized monthly as service delivered
- Track in `revenue/cash_collected.csv` (private repo) and `dealix/payments/` (if integrated)

## Unit Economics (target, end of Q1)

| Metric | Target |
|---|---|
| Sprint gross margin | ≥ 70% (founder time only) |
| Managed Ops gross margin | ≥ 60% (founder + AI; contractor counted at full burdened cost) |
| LTV (Managed Ops) | ≥ SAR 35,000 (12-month retention assumption × 2,999) |
| CAC (this quarter, founder-led) | < SAR 500 / paid customer (founder time costed) |
| LTV / CAC | > 70 (founder-led phase only) |
| Time to first cash from lead | < 21 days for Sprint |

When LTV/CAC drops below 5 in a paid-acquisition phase (future), pause the channel.

## Revenue Mix Targets (end of Q1)

- 60% from Managed Ops (recurring)
- 25% from Sprints (one-time)
- 10% from Data Packs (one-time)
- 5% from Custom AI (project + retainer)

If one-time exceeds 60% beyond month 6, we're not converting fast enough → revisit upsell flow.

## Forecasting

Maintained in `revenue/mrr_tracker.csv` (private). Forecast columns:
- Committed (signed contracts only)
- Probable (≥ 80% close probability, dated)
- Possible (50–80% close probability, dated)
- Pipeline (< 50%, undated)

Founder uses **Committed + Probable** for cash planning. Never spend against "Possible".

## What This Model Refuses

- Equity deals
- Trade arrangements
- Annual contracts > 12 months
- Revenue share with the client's outcomes (compliance + governance complexity)
- Anonymous or untracked payments
- Cash payments without a logged tax invoice

## Stream Kill Criteria

A stream gets killed if:
- < 2 customers in 90 days (Sprint excepted in month 1)
- Margin drops below 40% sustained
- It pulls > 30% of founder time without generating > 30% of revenue
- A trust risk emerges that can't be mitigated

When killed, archive its docs under `docs/_archive/` and log in execution ledger.

## Stream Add Criteria

A new stream gets added only if:
- It serves Tier 1 ICP
- It can be productized within 7 days
- It doesn't require automating an L4 (prohibited) action
- It has a defined exit / handoff
- It passes Strategy Filter

## Review Cadence

- Weekly: cash collected, MRR delta, overdue payments
- Monthly: unit economics, stream mix, forecast vs actual
- Quarterly: stream kill / add review
