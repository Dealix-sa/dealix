# Pricing Architecture

## Purpose
Define the list price and economics for every product rung.

## The 5-rung ladder
| Rung | Offer | List price | Notes |
|---|---|---|---|
| 1 | Free Diagnostic | 0 SAR | < 30 min; produces a one-page snapshot |
| 2 | Revenue Intelligence Sprint | 499 SAR | 7-day sprint; one outcome |
| 3 | Sector Data Pack | 1,500 SAR | Curated lead table + insight brief |
| 4 | Managed Ops Retainer | 2,999–4,999 SAR/mo | Monthly cadence; minimum 3 months |
| 5 | Custom AI Build | 5K–25K SAR | Fixed scope, fixed price |

## Pricing rules
- Always quote the list price first.
- Negotiate scope, not price, when challenged.
- All custom builds are fixed-fee with a written scope; no T&M without explicit founder approval.

## Margin guardrails
- Rung 2: target gross margin 80% (founder time accounted at 200 SAR/hr internal cost).
- Rung 3: target gross margin 75%.
- Rung 4: target gross margin 70%.
- Rung 5: target gross margin 50%.

## Annual review
- Re-evaluate list prices every 12 months or after 25 paying customers, whichever comes first.

## Forbidden patterns
- "Beta pricing" that lingers forever.
- Per-seat pricing before SaaS gate.
- Region-based pricing that disadvantages KSA buyers.

## Where to track
- Active retainers in `revenue/mrr_tracker.csv`.
- Unit economics in `finance/unit_economics.csv`.
- Discounts in `finance/discount_log.csv`.
