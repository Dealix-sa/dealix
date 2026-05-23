# Client Health Score v2

## Purpose
Evaluate whether a client is ready for retention, proof, expansion, or closure.

## Score
| Signal | Points |
|---|---:|
| Client used report | 20 |
| Positive feedback | 20 |
| Asked for more opportunities | 20 |
| Wants follow-up support | 15 |
| Clear next opportunity | 15 |
| Approved proof or testimonial | 10 |

## Meaning
- 90–100 = retainer ready.
- 70–89 = strong nurture.
- 50–69 = needs more value.
- below 50 = close or learn.

## Rules
- Retainer ask only if value is visible.
- Case study only with approval.
- Low health score requires win/loss review.

## Inputs
Each signal is scored from the evidence file for the client:
- feedback.md
- delivery_report.md
- handoff.md
- proof_approval.md

## Output
- clients/<client_name_private>/health_score.md
- summary row in client_success/retention_tracker.csv
- top-of-funnel risks bubbled up to
  client_success/client_success_dashboard.md
