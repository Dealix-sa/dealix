# تجارب التسعير — Pricing Experiments

> Sample size. Duration. Kill rule. No hunches.

## Purpose
Test pricing changes deliberately, not by feel. Avoid one anecdote becoming permanent policy.

## Owner
Founder/CEO.

## Inputs
- Current pricing in `OFFER_LADDER.md`.
- Win-rate and margin trend from `REVENUE_METRICS.md`.
- Capacity (proposals per month).

## Outputs
- Active experiments list in this file.
- Per-experiment result file in `dealix-ops-private/experiments/YYYY-MM-DD_<slug>.md`.
- Pricing change decision in Monthly Strategy Review when an experiment passes.

## Rules
1. An experiment changes exactly one variable at a time (price, payment terms, or bundle).
2. Minimum sample size: 6 qualified proposals (3 in each arm if A/B).
3. Minimum duration: 30 days.
4. Kill rule must be defined before launch. Common kills: win-rate drop > 30%, margin drop > 20%, time-to-close increase > 50%.
5. Experiments do not run during the last 14 days of a quarter (revenue-close period).
6. Pricing changes from an experiment become policy only after a Monthly Strategy Review decision.

## Metrics
- Experiments run per quarter: target 1–2.
- Experiments completing (vs aborted): track.
- Time to result: median ≤ 45 days.

## Cadence
Per experiment. Reviewed in Monthly Strategy Review.

## Evidence
`dealix-ops-private/experiments/`.

## Verifier
`make pricing-experiments-verify` — confirms each active experiment has kill rule, sample size, deadline.

## Runtime Command
`make experiment-start slug=<slug>`

---

## Experiment design template

```
# Pricing Experiment — <slug>
Started: YYYY-MM-DD
Deadline: YYYY-MM-DD (30 days minimum)
Owner: Founder/CEO

## Hypothesis
"If we change <variable> from <current> to <new>, then <outcome> will move by <amount> within <time>, because <reason>."

## Variable changed
<one variable only>

## Arms
- Control: current pricing
- Variant: new pricing

## Assignment rule
<how proposals are assigned to control or variant>

## Sample size
Total: ≥ 6 qualified proposals (3 per arm if A/B).
Counting only proposals to ICP-fit ≥ 6 prospects.

## Success criteria
1.
2.

## Kill criteria
1. Win-rate drop > 30% in variant: stop.
2. Margin drop > 20% in variant: stop.
3. Time-to-close increase > 50% in variant: stop.
4. Single customer complaint about pricing fairness: stop and review.

## Tracking
| Proposal id | Arm | Sent | Outcome | SAR | Days to outcome |
|---|---|---|---|---|---|

## Result (filled at deadline)
- Variant win-rate vs control: NN% vs NN%
- Variant margin vs control: NN% vs NN%
- Time-to-close variant vs control: D vs D
- Statistical comfort: subjective on small samples; note residual uncertainty.

## Decision
[ ] Adopt variant — change pricing in OFFER_LADDER.md
[ ] Keep control — pricing unchanged
[ ] Re-run with adjustment — describe
[ ] Inconclusive — defer

## Learning
<one sentence>
```

## What experiments are NOT for
- Justifying a price the founder already wants.
- Testing irreversible bundle changes (those go through A2 Go/No-Go gate).
- Discounting individual deals (that's negotiation, not experiment).

## Statistical humility
- Small samples are normal here. Treat results as directional, not significant.
- Triangulate with margin and customer feedback, not just win-rate.
- Trust the kill rule even if "we're close to significance."

## Coordination with other systems
- Pricing experiments do not run in parallel with offer evolution graduation (`OFFER_EVOLUTION_SYSTEM.md`).
- Pricing experiments do not interact with Refund Policy (`docs/finance/REFUND_POLICY.md`).

## Examples of acceptable experiments
- Raise Signal Sample from SAR 18,000 to SAR 22,000.
- Move Revenue Sprint payment from 50/50 to 60/40.
- Bundle Sprint + Desk at a 10% combined discount.

## Examples of unacceptable experiments
- Offering a free pilot to a "logo".
- Adding a "guaranteed ROI" tier.
- Changing currency to USD without legal review.

## القواعد العربية
1. تجربة واحدة تغير متغيرًا واحدًا.
2. حجم العينة لا يقل عن 6 عروض مؤهلة، مدة 30 يومًا على الأقل.
3. قاعدة الإيقاف محددة قبل البدء.

## Cross-links
- `OFFER_LADDER.md`
- `REVENUE_MODEL.md`
- `REVENUE_METRICS.md`
- `docs/founder/MONTHLY_STRATEGY_REVIEW.md`
- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md`
