# CEO Control Tower

The single screen the founder opens every day before anything else.

## Purpose
Give the founder a one-page view of the company state, the decisions that need attention, and the single next move that creates the most leverage.

## What it surfaces
- Is the company earning?
- Is the sales motion moving?
- Is delivery on time?
- Is there a risk on the board?
- What decision is waiting for the founder?
- What is the best opportunity today?
- What should be killed today?

## Inputs
- `docs/founder/COMPANY_HEALTH_SCORE.md`
- `docs/founder/DAILY_COMMAND_BRIEF.md`
- `docs/founder/DECISION_LOG.md`
- `docs/founder/RISK_REGISTER.md`
- `dealix-ops-private/revenue/cash_collected.csv`
- `docs/learning/EXPERIMENT_LOG.md`
- Pipeline + delivery state from operational systems

## Outputs
- One decision per area (Revenue / Sales / Delivery / Product / Trust / Founder)
- One "stop today" item
- One "double down today" item

## Cadence
- Open every morning before GitHub.
- Update at end of day with one line per area.
- Used as the starting point for the weekly CEO review.

## Rule
If the founder opens GitHub before this file, the founder is operating as a developer.
If the founder opens this file first, the founder is operating as a CEO.
