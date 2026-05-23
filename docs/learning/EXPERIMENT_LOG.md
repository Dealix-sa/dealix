# Experiment Log

> Every formal experiment Dealix runs. One row per experiment.
> An idea without a row in this log isn't an experiment — it's a vibe.

## Schema

```
exp_id | started_at | hypothesis | success_metric | duration | budget_cap | status | result | learning
```

- **status**: `running` · `succeeded` · `failed` · `inconclusive` · `aborted`
- **result**: 1-line summary of measured outcome
- **learning**: 1-line takeaway

## Active + Recent Log

```
EXP-001 | 2026-05-23 | Logistics-sector LinkedIn DM (sector-trigger framing) lifts reply rate vs generic | reply rate ≥ 15% | 30 days | 4 founder hr | running   | -                     | -
EXP-002 | 2026-05-23 | Free Diagnostic CTA in LinkedIn post drives ≥ 1 inbound per post | 1+ inbound/post | 6 weeks | 4 founder hr | running   | -                     | -
EXP-003 | 2026-05-23 | Bilingual handoff doc (AR + EN side-by-side) raises client feedback score | ≥ 0.5 pt lift | 5 sprints | 2 hr/sprint | running   | -                     | -
```

## Experiment Template

```yaml
exp_id: EXP-NNN
started_at: YYYY-MM-DD
sponsor: founder
hypothesis: |
  We believe that {change} will produce {measurable outcome}
  in {audience/context} within {time window}.
why_now: |
  What data or observation prompted this experiment.
success_metric: |
  Specific number + measurement method
duration: 30 days | 6 weeks | etc
budget_cap:
  founder_hours: X
  cash: SAR Y
  risk_level: low | medium | high
risk_mitigation: |
  What we'll do if it goes wrong (kill switch criteria, rollback)
trust_check: |
  How this experiment stays within approval matrix
status: running
result: ""
learning: ""
decision: ""  # adopt | iterate | kill
```

## Discipline

- No experiment without a row
- No row without success metric defined upfront
- No experiment runs past duration without an explicit extension decision
- Result + learning + decision filled within 7 days of end

## Experiment Categories

- **Messaging** — message framings, channels, formats
- **Pricing** — rung pricing tests (also logged in `pricing_experiments.md`)
- **Delivery** — playbook variations
- **Trust** — new policies, gate strictness
- **Content** — format / channel / topic
- **Product** — feature usage / adoption tests

## Forbidden Experiments

- Experiments that bypass trust gates
- Experiments on suppression-list contacts
- Experiments that risk client data
- Experiments without a kill switch
- Experiments that can't be measured
- Experiments that compete with focused execution this quarter (one experiment per category at a time)

## Weekly Experiment Review

In Weekly CEO Review:
- How many experiments running?
- Any to extend / kill / wrap up?
- Any results to act on (adopt / iterate / kill)?

## Monthly Experiment Audit

- Total experiments started vs completed
- % succeeded / failed / inconclusive / aborted
- Patterns: which categories produce most adopted changes?
- Patterns: which experiments tend to never finish?

## What This Log Refuses

- Running experiments to look busy
- Running experiments without budget caps
- Quiet abandonment (always log status `aborted` with reason)
- Treating an opinion as a proven result
- Skipping the learning capture
