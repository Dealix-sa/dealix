# Financial Dashboard

> One screen the founder should be able to read in 60 seconds.

## Layout

```
┌─────────────────────────────────────────────────────────┐
│  CASH                                                    │
│  - Bank balance:       SAR _____                         │
│  - Cash collected MTD: SAR _____                         │
│  - Cash collected YTD: SAR _____                         │
│  - Runway:             _____ months                      │
│                                                          │
│  MRR                                                     │
│  - Current MRR:        SAR _____                         │
│  - MRR Δ (week):       +/-_____                          │
│  - MRR Δ (month):      +/-_____                          │
│  - Quick ratio:        _____ (target >4)                 │
│                                                          │
│  PIPELINE (committed + probable)                         │
│  - Committed:          SAR _____                         │
│  - Probable:           SAR _____                         │
│  - Close rate (30d):   _____%                            │
│                                                          │
│  OBLIGATIONS                                             │
│  - Overdue receivables: SAR _____ (oldest _____ days)    │
│  - Upcoming payables:   SAR _____ (next 30 days)         │
│                                                          │
│  UNIT ECONOMICS (rolling 90d)                            │
│  - Avg deal size:       SAR _____                        │
│  - LTV (Managed Ops):   SAR _____                        │
│  - CAC:                 SAR _____                        │
│  - LTV/CAC:             _____                            │
└─────────────────────────────────────────────────────────┘
```

## Source Files

- Bank balance: manually updated daily, from bank
- Cash collected: `revenue/cash_collected.csv` (private)
- MRR: `revenue/mrr_tracker.csv` (private)
- Pipeline: `pipeline/pipeline_tracker.csv` (private)
- Obligations: `revenue/invoices.csv` (private) + `revenue/payables.csv` (planned)

## Generation

- Manual (this quarter)
- Future: `scripts/generate_financial_dashboard.py` builds from CSVs
- Appears in Daily Brief Money section
- Full dashboard in Weekly CEO Review

## Decision Triggers

| Trigger | Action |
|---|---|
| Bank balance < 2× monthly burn | Lean mode: pause net-new build, focus on collection |
| Runway < 60 days | Emergency: founder + advisor session, defer all non-revenue work |
| MRR drops 2 weeks in a row | Investigate churn; adjust delivery or pricing |
| Overdue receivables > 10% of MRR | Halt new work to that client until resolved |
| LTV/CAC drops below 5 in paid phase | Pause paid acquisition |
| Close rate < 15% for 2 weeks | Revisit proposal quality + qualification |

## Anti-Patterns

- "Vanity metrics" (pageviews, follower counts, etc.) — not on this dashboard
- "Forecasted next quarter" headline — only committed + probable shown
- Combining business and personal finances on same dashboard — never

## Discipline

- Read daily (60 seconds)
- Update weekly (full data refresh)
- Re-design quarterly (does it still drive decisions?)
