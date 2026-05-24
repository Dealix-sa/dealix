# Founder Hour ROI

How to price a CEO hour so the ROI matrix has a real input on the Leverage
dimension.

## The base rate

`base_rate = annual_target_revenue / (move_hours_per_year * 2)`

Where `move_hours_per_year = move_hours_per_week * 48` (excluding holidays).

Example: target 1,200,000 SAR ARR, 12 Move hours/week, 48 weeks →
`base_rate = 1,200,000 / (576 * 2) ≈ 1,041 SAR/hour`.

The factor of 2 accounts for the fact that Move hours are the rare ones; an
hour of Move is roughly twice as valuable as a generic working hour because
it cannot be recovered later.

## Application

When evaluating a delegate / automate / hire decision:

1. Count the weekly hours the CEO currently spends on the task
2. Multiply by `base_rate` → annualized cost of NOT delegating
3. Compare against the cost of the alternative (contractor rate, tool cost, full-time hire)

If delegating saves more than `0.5 * base_rate_annualized` it should pass
the ROI matrix unless there is a trust or judgment block.

## Anti-patterns

- Using the base rate to bill customers (use [`docs/revenue/PRICING_AND_PACKAGING.md`](../revenue/PRICING_AND_PACKAGING.md) for that)
- Using it to justify hiring without an SOP — see [`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)
- Treating it as fixed — re-grade quarterly with revised target revenue

## Cross-references

- [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md)
- [HIRE_VS_AUTOMATE_VS_PARTNER](HIRE_VS_AUTOMATE_VS_PARTNER.md)
- [`docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`](../founder/FOUNDER_LEVERAGE_DASHBOARD.md)
- [`docs/founder/FOUNDER_TIME_AUDIT.md`](../founder/FOUNDER_TIME_AUDIT.md)

## Non-negotiables

The hour rate is an internal decision input, not a customer-facing price.
See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
