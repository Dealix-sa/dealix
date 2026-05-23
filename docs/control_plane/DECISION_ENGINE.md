# Decision Engine

The Decision Engine classifies a candidate action into one of:

- `BUILD`
- `FIX`
- `KILL`
- `DEFER`
- `APPROVE`
- `REJECT`
- `ESCALATE`

## Scoring

Each candidate is scored on five 0–10 dimensions:

| Dimension | Meaning |
|---|---|
| `revenue_impact` | Direct or near-term effect on cash / MRR |
| `urgency` | How costly delay is |
| `risk_reduction` | How much it reduces revenue/trust/delivery risk |
| `founder_leverage` | How much it frees CEO time |
| `complexity` | Effort + coordination cost |

Aggregate score = `revenue_impact + urgency + risk_reduction + founder_leverage - complexity`.

## Rules (in order)

1. `trust_violation` → `REJECT` (overrides all).
2. `risk_reduction >= 8` → `FIX`.
3. `revenue_impact >= 8 AND urgency >= 7` → `BUILD`.
4. `founder_leverage >= 8 AND complexity <= 5` → `BUILD`.
5. `complexity >= 8 AND revenue_impact <= 5` → `DEFER`.
6. `revenue_impact <= 2 AND founder_leverage <= 2` → `KILL`.
7. Aggregate score `>= 18` → `APPROVE`.
8. Otherwise → `DEFER`.

## Why this engine exists

To prevent the failure mode: shipping interesting work that has no revenue,
delivery, trust, or founder-leverage justification. The engine forces the
question to be answered numerically before action.
