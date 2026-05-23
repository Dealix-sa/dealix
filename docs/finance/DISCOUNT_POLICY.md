# Discount Policy

## Purpose
Govern when, how much, and how to record discounts.

## Defaults
- Standard discount: none.
- Multi-month commitment: up to 10% on rung 4 retainers if 6+ months prepaid.
- First-paying customer offer: up to 30% on a single engagement, founder approval required.
- Anti-ICP discount: forbidden.

## Approval matrix
| Discount % | Approval required |
|---|---|
| 0–10% | Founder sign-off in `finance/discount_log.csv` |
| 11–20% | Founder approval + a written reason citing strategic value |
| 21–30% | Founder approval + Trust workflow approval |
| > 30% | Forbidden without explicit reason and Trust + finance review |

## Logging
For every discount applied:
- `finance/discount_log.csv`: `date, client, offer, list_price_sar, discounted_price_sar, reason, approved_by`
- Note in the proposal that price reflects an approved discount.

## Anti-patterns
- Discounting to "get the deal closed this week".
- Discounting because the buyer is a friend.
- Discounting without a written reason.

## Counter to "we have a budget of X"
- Offer to scope down to fit the budget, not to discount.
- Or move the buyer to a lower rung of the ladder.

## Review cadence
- Monthly: review the discount log for patterns. > 3 discounted deals in a month is a pricing signal, not a one-off.
