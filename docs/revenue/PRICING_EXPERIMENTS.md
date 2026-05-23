# Pricing Experiments

Pricing is tested, not guessed.

## Cadence
- One pricing experiment per month, set in the Monthly Strategy Review.
- Runs for a defined number of proposals or weeks.
- Recorded in `dealix-ops-private/revenue/pricing_experiments.md`.

## Experiment template

```
## Experiment ID
DLX-PRX-0001

## Hypothesis
Raising the Revenue Sprint floor from 2,500 to 3,500 SAR will not reduce
close rate by more than 10%.

## Variant
Old: 2,500 SAR floor
New: 3,500 SAR floor

## Sample
Next 10 Sprint proposals.

## Success criterion
Close rate remains within 10% of baseline.

## Result
[Filled at end of experiment.]

## Decision
[Adopt / Revert / Adjust]
```

## Rule
A pricing change without an experiment is a guess. A guess is logged as a decision in `DECISION_LOG.md` with explicit acknowledgement that no experiment was run.
