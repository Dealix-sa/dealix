# Revenue Metrics

> What we measure. What we report. What we ignore.
> Source of truth for the Daily Brief "Money" section.

## North-Star Metric

**Cash collected (SAR) per month** — the only metric that survives all other arguments.

## Reported Daily

| Metric | Source | Target (this quarter) |
|---|---|---|
| Cash collected today | `revenue/cash_collected.csv` | track only, no daily target |
| Cash collected MTD | computed | SAR 5K minimum, SAR 10K stretch |
| Proposals pending (count + SAR) | `pipeline/pipeline_tracker.csv` (stage=proposal_sent) | 3+ |
| Payments overdue (count + SAR + oldest days) | `revenue/invoices/` aging | 0 |
| MRR | `revenue/mrr_tracker.csv` | growing month-over-month |

## Reported Weekly

| Metric | Source | Target |
|---|---|---|
| Cash collected this week | computed | SAR 1.5K average |
| New customers | `pipeline/` (closed-won this week) | ≥ 1 |
| MRR delta | `mrr_tracker.csv` (week-over-week) | positive |
| Pipeline value (committed + probable) | computed | growing |
| Close rate (proposals → paid) | computed weekly rolling | ≥ 35% |
| Best channel / best sector / best message | `learning/` | reviewed in Weekly CEO Review |

## Reported Monthly

| Metric | Source | Target |
|---|---|---|
| Cash collected MTD final | computed | SAR 5K month 1 → SAR 25K by month 6 |
| MRR end-of-month | `mrr_tracker.csv` | growth ≥ 30% MoM until 25K MRR |
| Stream mix (Sprint / Pack / Managed / Custom) | computed | 25 / 10 / 60 / 5 by end of Q1 |
| Average deal size (closed-won) | computed | trending up |
| Time to first cash (lead → paid) | computed | < 21 days (Sprint) |
| LTV (Managed Ops cohort) | `mrr_tracker.csv` × retention | ≥ SAR 35K |
| Gross margin per rung | computed | per `REVENUE_MODEL.md` |

## What We Don't Report (intentionally)

- Daily MRR (too noisy)
- Vanity counts (pageviews, follower counts) unless tied to lead conversion
- Forecasts beyond Committed + Probable (Possible is for planning, not reporting)
- "Pipeline-weighted ARR" (uses fake-precision multipliers)
- Anyone else's metric we can't compute from our own data

## Definitions (locked)

- **Cash collected** = bank-confirmed receipt minus refunds in the period
- **MRR** = sum of active retainer monthly values, prorated for partial months
- **Pipeline value (committed)** = signed contracts not yet paid
- **Pipeline value (probable)** = stage ≥ proposal_sent × stage probability from `PIPELINE_STAGES.md`
- **Close rate (proposals → paid)** = paid within 60 days of proposal sent / total proposals sent in same period
- **LTV (Managed Ops)** = monthly value × average retention months (use 12 as default until cohort data exists)

## Reporting Hygiene

- Every metric source is one CSV (or one query)
- Every CSV has a header row and immutable schema
- No metric is hand-computed — if it isn't automated, it isn't reported
- A metric without a source → flagged in Daily Brief as `MISSING:`

## Anomaly Rules

- Cash drop > 30% week-over-week → investigate same day
- MRR drop (churn) → investigate immediately + log in `clients/`
- Close rate < 15% for 2 weeks → revisit proposal quality + qualification
- Pipeline value flat for 2 weeks → revisit outbound volume + ICP scoring

## Review Cadence

- Daily: 5 metrics in the Brief
- Weekly: full weekly metrics in the Review
- Monthly: full monthly metrics + cohort analysis in Board Memo

## What This Refuses

- Vanity dashboards
- Goodhart's Law victims (any metric the team starts gaming — kill it)
- Metrics not tied to a decision we'd actually make
- Charts without context (every chart in a memo gets a one-line takeaway)
