# Client Health Score

Each active client carries a health score, updated weekly.

| Signal | Score |
|---|---:|
| Used the delivered report or pack | 20 |
| Replied positively to the last update | 20 |
| Asked for more leads or scope | 20 |
| Booked meetings or closed deals from Dealix work | 20 |
| Expressed interest in monthly support | 20 |

## Banding
- **90–100** — Retainer ready. Move to upsell.
- **60–89** — Healthy nurture. Maintain cadence and add value.
- **0–59** — At risk. Investigate, escalate to founder, decide whether to recover or sunset.

## Updates
- Updated in the Weekly CEO Review.
- Stored in `dealix-ops-private/client_success/health_scores.csv`.

## Rule
A client at risk for two consecutive weeks is a founder priority that week.
