# Offer Evolution System

> Offers evolve. Founders who do not evolve their offers stagnate.

## When an offer changes

An offer (a rung on `OFFER_LADDER.md`) changes when **at least two** of:

- It has not been sold in 90 days.
- It has lost > 50% of proposals on a price objection.
- It has produced > 1 D-tier outcome.
- Delivery time consistently exceeds the time budget by > 30%.
- A pricing experiment has produced > 30% improvement in conversion.

## How an offer changes

1. **Hypothesise.** Write the change as a one-line hypothesis with
   expected effect.
   _Example: "Reducing Sprint scope from 50 accounts to 30 will lift
   close rate from 40% to 60% without lowering price."_

2. **Pre-register the experiment.** Add to
   `dealix-ops-private/revenue/pricing_experiments.md` with:
   - hypothesis
   - sample size required (minimum 5 proposals)
   - decision rule
   - effective dates

3. **Run.** Apply the change to the next N qualified prospects.

4. **Decide.** After the sample is hit, decide one of:
   - **Adopt:** update `OFFER_LADDER.md`.
   - **Reject:** revert to baseline.
   - **Extend:** run another iteration with a refined hypothesis.

## Pricing Experiment Discipline

- We do **not** silently change prices for one customer.
- We do **not** run > 2 pricing experiments at the same time.
- Every experiment has a written decision rule **before** the data arrives.

## Offer Retirement

An offer is retired when:

- It has produced zero revenue for 6 months, and
- No graduation logic still requires it.

Retirement is documented in `KILL_LIST.md`.

## Offer Addition

A new offer (e.g. a new rung) requires a Go decision via
`GO_NO_GO_DECISION_SYSTEM.md`, with:

- A delivery template at least at "5 successes" maturity for the
  workflow it would productize.
- A price floor and ceiling.
- A named ICP segment that has pulled for it.
