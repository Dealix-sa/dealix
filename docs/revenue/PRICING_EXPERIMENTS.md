# Pricing Experiments

## Format

| ID | Hypothesis | Offer Affected | Sample | Success Metric | Rollback Condition | Status | Outcome |
|---|---|---|---:|---|---|---|---|

## Rules

1. One pricing experiment per offer at a time.
2. Minimum sample: 3 deals before declaring a result.
3. Pre-defined success metric — no moving the goalposts.
4. Pre-defined rollback condition — exit cleanly if the experiment hurts close rate.
5. Each experiment closes within 60 days. Inconclusive experiments are filed and reattempted later.

## Allowed Experiment Variables

- Headline price.
- Payment schedule (e.g., 50/50, 30/30/40).
- Bundle composition (e.g., Diagnostic + Sprint at a fixed price).
- Annual prepay incentive size.

## Disallowed Variables

- Different prices for the same offer to different prospects in the same week.
- Hidden discounts not documented in `PRICING_STRATEGY.md`.

## Learning Capture

Closed experiments are summarized in `docs/learning/PRICING_LEARNING.md`
with what we learned, decision, and next experiment to run.
