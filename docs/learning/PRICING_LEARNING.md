# Pricing Learning

> What we observe about price elasticity and willingness to pay.
> Drives next-quarter pricing decisions (per `PRICING_STRATEGY.md`).

## Sources

- Win/loss reasons citing price
- Negotiation patterns (counter-offers, requests for discount)
- Conversion rates per rung
- Upsell rate Sprint → next rung
- Renewal patterns at month 3 and month 12 for Managed Ops

## Monthly Capture

```markdown
# Pricing Learning — YYYY-MM

## Rung-Level Signals
| Rung | Sent | Closed | Win Rate | Avg Negotiation | Refunds |
|---|---|---|---|---|---|
| Free Diag | ___ | ___ → Sprint ___% | _ | n/a | n/a |
| Sprint 499 | ___ | ___ | ___% | ___ | ___ |
| Pack 1500 | ___ | ___ | ___% | ___ | ___ |
| Managed 2999 | ___ | ___ | ___% | ___ | ___ |
| Managed 4999 | ___ | ___ | ___% | ___ | ___ |
| Custom 5K-25K | ___ | ___ | ___% | ___ | ___ |

## Discount Requests
- Number of discount requests this month: ___
- Most common ask: _____
- Held the line: ___ %
- Approved exceptions (logged in pricing_experiments.md): ___

## Free Diagnostic → Sprint Conversion
- Diagnostics done: ___
- Sprints sold from diagnostics: ___
- Conversion rate: ___ %

## Sprint → Next Rung
- Sprint customers who upgraded within 30 days: ___ / ___
- Most common upgrade path: _____

## Managed Ops Renewal
- Month 3 renewal rate: ___ %
- Month 12 renewal rate: ___ %
- Most common churn reason at renewal: _____

## Signals This Month
- Anything pointing to "too cheap" (high win rate + low effort): _____
- Anything pointing to "too expensive" (high resistance, low close): _____
- Sector × price interactions: _____
```

## Decision Triggers

| Signal | Action |
|---|---|
| Rung win rate > 50% for 60 days | Consider raising 20% (test in next quarter) |
| Rung win rate < 15% for 60 days | Diagnose: pricing or fit? |
| Discount requests > 30% of proposals | Reframe value or move down a rung |
| Managed Ops month 12 renewal < 50% | Investigate value perception at month 6-12 |
| Sprint → next rung < 20% | Diagnose Sprint deliverable, not pricing |

## Per-Quarter Pricing Review

End of quarter, decide for each rung:
- Hold price
- Test +20%
- Test other framing (annual prepay, package change)
- Kill rung (if conversion + LTV don't justify)

Document in `revenue/pricing_experiments.md` (private).

## Forbidden

- Changing price mid-engagement
- Raising prices on existing retainer customers without 60-day notice
- Lowering prices to close (kills productized model)
- Stealth-discounting (every discount visible in invoice as line item)

## What This Refuses

- Pricing changes without data
- Big changes (> 30%) without staged testing
- Pricing optimization that ignores LTV
- Pricing optimization that ignores trust signal (cheap = "amateur" in some sectors)
