# Cash Discipline System

## Purpose
Keep cash visible and protected. No surprises at month-end.

## Daily
- Record any received payment the same day in `revenue/cash_collected.csv`.
- Record any spend the same day in `finance/expenses.csv`.

## Weekly
- Reconcile `cash_collected.csv` against the bank statement.
- Reconcile `expenses.csv` against the bank statement.
- Note discrepancies in `trust/approval_log.csv` with `type=reconciliation`.

## Monthly close
1. Lock the month in `expenses.csv` (no further edits without note).
2. Compute totals: revenue, direct cost, gross margin.
3. Produce a one-page summary in `business_audit/monthly_summary_<YYYY-MM>.md`.
4. Compare against last month and against year-to-date.

## Cash runway
- Track personal + business runway separately.
- Minimum 6 months of runway before any non-revenue-generating spend.

## Reserves
- Set aside 20% of every cash receipt into a separate account for tax + VAT obligations.
- Set aside another 10% as an emergency reserve.

## Forbidden patterns
- Treating verbal yes as cash.
- Spending against future revenue before it's collected.
- Mixing personal and business finances on the same account.

## Audit
- Monthly: founder self-audit.
- Annual: external accountant review.
