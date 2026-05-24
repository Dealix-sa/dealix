# Account Scoring Model

> Composite score per account. Decision support — never decision authority.

## 1. Inputs

| Component | Sub-signals |
|---|---|
| **Fit** | Sector match, size match, geo match, motion match |
| **Intent** | Trigger events, inbound history, response history |
| **Capacity** | Our delivery capacity, founder bandwidth |
| **Strategic** | Founder override, partner relationship |

## 2. Formula

```
score = 100 * (0.40 * fit
             + 0.35 * intent
             + 0.15 * capacity
             + 0.10 * strategic)
```

Each component normalised 0-1.

## 3. Output

`growth/account_scores.csv` columns:

```
account_id, name, sector_id, segment_id, fit, intent, capacity, strategic, score, recommendation, last_updated, source
```

`recommendation` values:

- `engage_now` — score ≥ 75 and capacity ≥ 0.5
- `engage_soon` — score 60-74
- `nurture` — score 40-59
- `hold` — score < 40 or capacity < 0.3

## 4. Cadence

- Daily refresh at 05:00 KSA.
- Founder override accepted and recorded in audit.

## 5. Trust posture

`engage_now` does **not** auto-send. It surfaces in the daily brief and Sales Cockpit; founder approves the action.

## 6. Verifier

`scripts/verify_growth_system.py` enforces:

- File present.
- All columns present.
- All scores in 0-100.
- All `source` values valid.
