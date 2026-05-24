# Beachhead Sector Scorecard — Template

Fill one row per candidate sector. Score 0–5 per criterion. The row
score does **not** itself constitute a public claim; only when paired
with `source` + `is_estimate=false` evidence in the Proof Ledger may
it be cited externally.

## Worksheet

| Sector | Fit (0–5) | Buying urgency (0–5) | Decision-maker reachability (0–5) | Reference accounts available (0–5) | Active conversations | Paid pilots collected | Review date | Source |
|---|---|---|---|---|---|---|---|---|
| _example_ | _score_ | _score_ | _score_ | _score_ | _count_ | _count (zero until proof)_ | YYYY-MM-DD | api / fallback / manual |

## Decision rules

- A sector is a **beachhead candidate** only when total score ≥ 16/20
  AND ≥ 1 paid pilot has been collected.
- A beachhead is **scaled** only after 3 paid pilots in the same sector
  (per Article 13 Build Order).
- No claim about a sector may be published until the Proof Pack from
  the first pilot in that sector is approved (case_study_publish gate).
