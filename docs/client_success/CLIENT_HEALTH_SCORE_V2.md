# Client Health Score V2

## Purpose
A 0–100 score per active client to predict churn and trigger interventions.

## Dimensions
| Dimension | Weight | Signal |
|---|---|---|
| Engagement | 25 | Replies within agreed cadence |
| Outcome confidence | 25 | Client cites the impact of recent delivery |
| Payment health | 20 | Invoices paid on time |
| Scope drift | 15 | Scope vs. proposal |
| Sentiment | 15 | Tone of recent messages |

## Score actions
- ≥ 80: green; pursue retainer expansion.
- 60–79: yellow; schedule a check-in to surface concerns.
- 40–59: orange; founder calls personally; offer to adjust scope.
- < 40: red; consider graceful wind-down; document in `pipeline/win_loss_log.md`.

## Where
Per-client `clients/<slug>/health_score.md`.

## Cadence
- Weekly while delivering.
- Monthly while on retainer.

## Recovery moves
- Red → schedule a 30-min review call within 48 hours.
- Orange → propose a written remediation plan with two concrete improvements.
- Yellow → next deliverable opens with the issue acknowledged.

## Anti-patterns
- Inflating sentiment scores to feel better.
- Treating health score as a vanity metric (it must drive action).
