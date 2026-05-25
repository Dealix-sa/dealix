# Dealix Financial Model v1

## Purpose
Track Dealix revenue, cash, runway, and offer economics.

## Owner
Sami / Finance owner.

## Review Cadence
Weekly.

## Revenue Lines

| Revenue Line   | Type           | Price Range            | Notes                          |
|----------------|----------------|------------------------|--------------------------------|
| Signal Sample  | one-time       | 0–199 SAR              | entry / qualification          |
| Revenue Sprint | one-time       | 2,500–7,500 SAR        | primary first offer            |
| Managed Pilot  | one-time/project | 9,500–25,000 SAR     | larger engagement              |
| Revenue Desk   | recurring      | 5,000–20,000 SAR/month | retainer                       |
| Dealix OS      | custom         | later                  | only after proof               |

## Core Metrics

### Cash
- cash_collected
- cash_expected
- overdue_cash

### Pipeline
- pipeline_value
- weighted_pipeline
- proposals_pending

### Recurring
- MRR
- active_retainers
- churn_risk

### Efficiency
- founder_hours_per_sprint
- delivery_hours_per_sprint
- gross_margin_estimate

### Survival
- monthly_expenses
- net_burn
- runway_months

## Simple Calculations

Runway:
```
cash_on_hand / monthly_net_burn
```

Gross Margin:
```
(revenue - direct_costs) / revenue
```

Weighted Pipeline:
```
sum(deal_value * probability_by_stage)
```

## Rules
- No full delivery without payment, PO, or written approval.
- Every proposal must have expected value and follow-up date.
- Any discount above 20% requires CEO approval.
- Refunds are A3 and never automatic.
- Finance review happens weekly.

## Evidence
- revenue/cash_collected.csv
- revenue/pipeline_value.csv
- revenue/mrr_tracker.csv
- finance/expenses.csv
- finance/runway_estimate.md

## Last Reviewed
YYYY-MM-DD
