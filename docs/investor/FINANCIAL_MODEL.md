# Financial Model

The model that ties revenue, cost, and growth assumptions to a single rolling forecast.

## Inputs
- Cash collected (history) — `dealix-ops-private/revenue/cash_collected.csv`.
- MRR trajectory — `dealix-ops-private/revenue/mrr_tracker.csv`.
- Per-engagement cost — engineering, delivery, sales.
- Overhead — tools, infrastructure, professional services.
- Hiring plan — keyed off `HIRING_TRIGGERS.md`.

## Outputs
- Rolling 12-month revenue forecast (base, conservative, stretch).
- Rolling 12-month cost forecast.
- Cash position by month.
- Runway under each scenario.
- Sensitivity table on the two or three biggest assumptions.

## Storage
- Model lives in `dealix-ops-private/investor/financial_model.xlsx`.
- A redacted summary may be shared in the data room.

## Cadence
- Refreshed monthly.
- Reviewed in the Monthly Strategy Review.

## Rule
The model is a planning tool, not a sales tool. Conservative case drives decisions; stretch case drives ambition.
