# Experiment Backlog

Every proposed change to the system is logged as an experiment with a
falsifiable success criterion.

## 1. Backlog row

```
experiment_id,proposed_at,owner,layer (intelligence|distribution|
revenue|marketing|trust|brand),hypothesis,
success_criterion,counter_metric,duration_days,
status (proposed|approved|running|finished|abandoned),
result_summary
```

## 2. Discipline

- One **success criterion** + at least one **counter-metric**.
- A clear duration; no open-ended experiments.
- A re-measurement on fresh data before claiming a win.
- A "kill criteria" — when do we stop early?

## 3. Approvals

The founder approves every experiment before it runs. No experiment
changes external send behaviour without per-message approval still
in place.

## 4. Banned

- ❌ Experiments that disable trust gates.
- ❌ Experiments that A/B test customer-facing pricing.
- ❌ Open-ended "let's see what happens" runs.
