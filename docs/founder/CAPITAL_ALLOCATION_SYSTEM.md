# Capital Allocation System

How runway, hiring, and discretionary spend get prioritized — and what
must be true before a new line item is funded.

## Purpose

Make capital decisions the same way every time so the company doesn't
drift into "we have cash, let's hire."

## Owner

Founder. Reviewed monthly.

## Cadence

- Monthly capital review on the 1st (rolled into the next CEO weekly).
- Re-priced whenever a milestone shifts ±2 weeks.

## Source of Truth

- Burn: monthly bank statement export → `data/finance/burn_<month>.csv`
- Runway: derived (cash on hand ÷ trailing 90-day burn)
- Open commitments: `docs/finance/COMMITMENT_REGISTER.md`

## Inputs

- Cash on hand
- Trailing burn
- Committed but unpaid (vendor invoices outstanding)
- Forecast revenue (only contracted, never pipeline)

## Outputs

- Updated runway figure
- A green / yellow / red signal at /ops/founder
- A list of "fundable now" vs "deferred" items

## KPI

- Runway updated monthly (12/12)
- 0 unbudgeted commitments > 5,000 SAR in the last 90 days
- Burn forecast accuracy ±10% over rolling 90 days

## Trust Boundary

Internal only. Capital numbers are never published externally without
explicit founder approval and a banned-claim scan.

## Failure Mode

- Runway not updated for > 35 days → CEO weekly review surfaces the gap.
- Unbudgeted commitment slips in → counted as a process failure, not a
  personal one. Fix the process.

## Recovery Path

1. Pull bank statement.
2. Re-compute trailing burn.
3. Update this doc and `data/finance/burn_<month>.csv`.
4. Re-rank fundable items.

## Verification

```bash
make business-os
```

## Next Action

If today is the 1st, run the monthly review. If today is not the 1st,
nothing required — but check the green/yellow/red signal at /ops/founder.
