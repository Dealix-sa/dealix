# Dealix Company OS Scorecard

> Single page that shows whether each of the 12 company systems is in PASS,
> READY INTERNAL, FIX, or BLOCKED. Computed by
> `scripts/verify_company_os.py` and reviewed weekly in
> `docs/founder/WEEKLY_CEO_REVIEW.md`.

## Scoring Rules

| Score | Status |
|---:|---|
| 90–100 | PASS |
| 75–89 | READY INTERNAL |
| 50–74 | FIX |
| 0–49 | BLOCKED |

## Systems

| System | Score | Status | Evidence | Verification |
|---|---:|---|---|---|
| Founder OS | 0 | BLOCKED | `docs/founder/` | `scripts/verify_company_os.py` |
| Strategy OS | 0 | BLOCKED | `docs/strategy/` | `scripts/verify_company_os.py` |
| Revenue OS | 0 | BLOCKED | `docs/revenue/` | `scripts/verify_company_os.py` |
| Acquisition OS | 0 | BLOCKED | `docs/acquisition/` or `docs/strategy/GTM_STRATEGY.md` | `scripts/verify_company_os.py` |
| Sales OS | 0 | BLOCKED | `docs/sales/` or `dealix/sales_os/` | `scripts/verify_company_os.py` |
| Delivery OS | 0 | BLOCKED | `docs/delivery/` or `dealix/workflows/` | `scripts/verify_company_os.py` |
| Trust OS | 0 | BLOCKED | `docs/trust/` | `scripts/verify_company_os.py` |
| Finance OS | 0 | BLOCKED | `docs/revenue/CASH_RULES.md` + `docs/finance/` (if present) | `scripts/verify_company_os.py` |
| Client Success OS | 0 | BLOCKED | `docs/client_success/` or `dealix/client_os/` | `scripts/verify_company_os.py` |
| Product OS | 0 | BLOCKED | `docs/product/` | `scripts/verify_company_os.py` |
| Content OS | 0 | BLOCKED | `docs/content/` | `scripts/verify_company_os.py` |
| Learning OS | 0 | BLOCKED | `docs/learning/` | `scripts/verify_company_os.py` |

## Health Score

`COMPANY_HEALTH = round(sum(system_scores) / 12)`

The rolling health score is recorded in
`docs/founder/COMPANY_HEALTH_SCORE.md`.

## How Scores Move

A system score is the percentage of required core files for that system
that exist and are non-empty. The verifier is the source of truth.

Add new required files by editing `SYSTEMS` in
`scripts/verify_company_os.py`.

## Cadence

- Run on every PR (CI workflow `dealix-company-os.yml`).
- Reviewed weekly in the CEO Review.
- Reviewed monthly with strategy decisions.
