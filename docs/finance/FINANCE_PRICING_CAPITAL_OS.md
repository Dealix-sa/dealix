# Finance, Pricing, Capital OS

## Purpose
Govern money: how Dealix prices, collects cash, tracks unit economics, and protects margin.

## Sub-systems
- Pricing — `docs/finance/PRICING_ARCHITECTURE.md`
- Discounts — `docs/finance/DISCOUNT_POLICY.md`
- Bad revenue filter — `docs/revenue/BAD_REVENUE_FILTER_V2.md`
- Unit economics — `docs/finance/UNIT_ECONOMICS_SYSTEM.md`
- Cash discipline — `docs/finance/CASH_DISCIPLINE_SYSTEM.md`
- Payment path — `docs/finance/PAYMENT_PATH_SYSTEM.md`

## Operating model
- Dealix is bootstrapped. No external capital until product-market fit is proven across at least 3 paying customers.
- Founder draws minimum salary; profits reinvested in tooling and contractors only.
- All categories of spend are tracked in `finance/expenses.csv`.

## Pricing principles
1. Price by outcome, not effort.
2. Pre-publish a list price for every productized rung.
3. Custom builds require a written scope and price; no T&M without approval.
4. Discounts are exceptional, logged, and bounded.

## Unit economics targets
- Gross margin per engagement ≥ 70% for productized rungs.
- Custom build margin ≥ 50%.
- CAC must be < 20% of first-engagement revenue.
- LTV / CAC ≥ 4 within 6 months of first paying customer cohort.

## Cash discipline
- Daily: record any payment received the same day.
- Weekly: reconcile `cash_collected.csv` with bank statement.
- Monthly: close the books; produce a one-page finance summary.

## Trust integration
- Any deal above 25,000 SAR requires Trust workflow approval.
- Any refund or write-off > 1,000 SAR requires founder approval in `trust/approval_log.csv`.

## Verifier
`python scripts/verify_finance_pricing_os.py`
