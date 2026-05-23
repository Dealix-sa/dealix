# Company Health Score

> Single number the CEO uses to know whether the company is operating well
> this week. Computed from the 12 system scores in
> `DEALIX_COMPANY_OS_SCORECARD.md`.

## Computation

```
health = round( sum(system_scores) / 12 )
```

Each system is scored 0–100 by its verification script.

## Bands

| Health | Status | What the CEO Does |
|---|---|---|
| 90–100 | PASS | Operate at normal cadence. Look for compounding bets. |
| 75–89 | READY INTERNAL | Run as a private beta. Do not make public claims. |
| 50–74 | FIX | Stop new work in failing systems. Drive scores up. |
| 0–49 | BLOCKED | Founder-level intervention required. Pause growth spend. |

## Current Score

To be updated by `scripts/verify_company_os.py` and the weekly review.

| Date | Health | Status | Notes |
|---|---:|---|---|

## Sub-scores

The detail lives in `DEALIX_COMPANY_OS_SCORECARD.md`. This file holds the
rolling top-line number so the CEO can read it in 10 seconds.
