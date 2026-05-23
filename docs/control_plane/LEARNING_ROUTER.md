# Learning Router

The Learning Router converts weekly inputs into at least one learning
decision: `BUILD`, `FIX`, `KILL`, or `DEFER`.

## Inputs

- DMs sent
- Replies received
- Calls held
- Proposals sent
- Proposals won
- QA failures
- Trust escalations
- Product bugs opened
- Positive client feedback events

## Rules

| Signal | Decision | Area |
|---|---|---|
| `dms >= 25 AND replies <= 1` | FIX | messaging |
| `proposals_sent >= 2 AND proposals_won == 0` | FIX | pricing_or_scope |
| `calls >= 3 AND proposals_sent == 0` | FIX | proposal_cadence |
| `qa_failures >= 2` | FIX | delivery_quality |
| `trust_escalations >= 1` | FIX | trust_policy |
| `product_bugs >= 3` | FIX | product_quality |
| `feedback_positive >= 2` | BUILD | offer_expansion |
| no signal | DEFER | general |

## Cadence

The router runs weekly. Its output feeds:

- `docs/learning/MONTHLY_STRATEGY_UPDATE.md`
- `docs/learning/WIN_LOSS_REVIEW.md`
- `docs/learning/MESSAGE_PERFORMANCE.md`

## Rule

Every week must produce at least one learning outcome. If the router
returns only `DEFER`, the founder still records what data is missing.
