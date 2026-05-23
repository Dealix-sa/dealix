# Experiment Backlog

The Experiment Backlog is the ranked queue of experiments Dealix is willing to run. Every experiment has a hypothesis, a metric, a sample size, and a stop rule before it starts.

**Source of truth:** `$PRIVATE_OPS/experiment_log.csv`
**Owner:** Marketing Lead + Founder
**Trust gate:** A1 for internal-only experiments; A2 for any experiment touching pricing, contract, or external send.

## Row schema

```
experiment_id, status, hypothesis_en, hypothesis_ar,
surface, primary_metric, secondary_metrics[],
sample_size_min, sample_size_max, stop_rule,
launched_at, concluded_at, outcome, learning_recorded
```

`status` moves through: `proposed` → `approved` → `running` → `concluded` → `learning_logged`.

## Approval gate

Every experiment is approved against four questions:

1. **Hypothesis.** What do we believe and why?
2. **Metric.** What single number will move if we're right?
3. **Sample size.** How much data do we need before we trust the result?
4. **Stop rule.** Under what condition do we stop the experiment early (positively or negatively)?

A proposal that cannot answer all four is not approved.

## Experiment types

| Type | Example | Approval class |
|------|---------|----------------|
| Copy experiment | Hero copy A vs B | A1 |
| CTA experiment | Single CTA vs dual CTA | A1 |
| Pricing experiment | Reference price vs custom variant | A2 |
| Channel experiment | Adding a new sector report distribution | A2 |
| Process experiment | Two-stage qualification vs one-stage | A1 |

## Run discipline

- Experiments do not overlap on the same surface unless designed as a factorial.
- The pre-registered primary metric is the only metric that decides the outcome.
- Secondary metrics are reported but do not override.
- Stop rules are honoured exactly.

## Outcome recording

| Outcome | Definition |
|---------|-----------|
| Supported | Primary metric moved in predicted direction, beyond noise threshold |
| Refuted | Primary metric moved in opposite direction or did not move |
| Inconclusive | Sample size not reached; result undetermined |
| Aborted | Stopped under a stop rule before conclusion |

Every outcome moves to the Learning Loop (`docs/performance/LEARNING_LOOP.md`).

## OWASP / NIST posture

Experiments that touch external surfaces are A2. The Trust Guardian (`docs/ai/TRUST_GUARDIAN_AGENT.md`) enforces this. No agent runs an experiment unsupervised.

## Failure modes

- **Pre-registration drift:** the primary metric is changed after data lands. Detection: experiment audit. Recovery: mark as inconclusive, do not credit.
- **Stop-rule bypass:** an experiment is continued past its stop rule because results were "almost" there. Detection: weekly review. Recovery: drop, re-design.
- **Backlog bloat:** more than 30 items in `proposed` for more than 60 days. Detection: monthly review. Recovery: prune ruthlessly.

## Recovery path

If the backlog becomes inconsistent (overlapping experiments, untraceable status), the founder freezes new experiments until reconciliation.

## Metrics

- Backlog size by status.
- Median time from `proposed` to `concluded`.
- Supported / refuted ratio.
- Learnings logged per quarter.

## Disclaimer

The backlog is intent. Outcomes are uncertain. Dealix does not guarantee experimental success. Estimated value is not Verified value.
