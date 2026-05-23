# Performance Improvement OS

> The loop that makes Dealix get smarter every week. Three modes: Diagnose, Decide, Do.

## 1. Inputs

- Audit log
- KPI tree
- Win / loss records
- Eval scorecard
- DORA engineering metrics
- Customer NPS

## 2. Weekly cadence

| Day | Activity |
|---|---|
| Sunday | KPI snapshot + diagnostic |
| Monday | Hypothesis backlog refresh |
| Wednesday | Mid-week pulse |
| Friday | Learning loop — what did we ship and learn |

## 3. Diagnose

Performance Analyst surfaces:

- Top three winning patterns.
- Top three losing patterns.
- Bottlenecks blocking cash.
- Two-week negative trends.

## 4. Decide

Founder picks ≤ 3 experiments for the next week. Each has:

- Hypothesis
- Metric
- Duration
- Owner
- Stop condition

## 5. Do

Experiments run; learnings recorded; library updated.

## 6. Outputs

- `performance/experiment_backlog.csv`
- `performance/win_loss.csv`
- `performance/objection_library.csv`
- `performance/message_performance.csv`
- `performance/sector_performance.csv`

## 7. Cross-link to DORA

We track engineering DORA metrics (deployment frequency, lead time for changes, change-fail rate, time-to-restore) alongside revenue metrics, so that engineering speed never decouples from business outcomes.

## 8. Trust

No experiment is run without an approval record. No live customer is a guinea pig without consent.
