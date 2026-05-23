# Operating Scorecard v1

Generator: `scripts/generate_operating_scorecard.py`.
Output: `${DEALIX_PRIVATE_OPS}/founder/operating_scorecard.md`.
Endpoint: `GET /api/v1/internal/control/scorecard`.

## Scores (0-100)

- **Revenue Score** — function of cash collected and positive replies.
- **Trust Score** — penalised by open trust flags and A3 attempts.
- **Runtime Score** — penalised by worker failures.
- **Founder Leverage Score** — rewards founder time saved (approved
  outreach, positive replies).
- **Productization Score** — rewards repeatable patterns landing in the
  productization candidates list.

## Bottleneck heuristic

1. Pending approvals > 5 → `founder_review_backlog`.
2. Sent > 0 and positive replies == 0 → `messaging_or_targeting`.
3. Payment capture queue not empty → `payment_capture`.
4. Otherwise → `no_data`.

## How to run

```
make operating-scorecard PRIVATE_OPS=/opt/dealix-ops-private
```
