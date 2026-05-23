# Learning Loop

How insight from an experiment becomes a permanent system change.

## 1. Steps

1. Experiment finishes with a recorded result.
2. The performance_analyst proposes a system change (template, weight,
   threshold, copy block).
3. The founder reviews the change in the approval queue.
4. The change is committed to the repo via a normal PR. Every change
   has an "experiment_id" reference in the commit message.
5. The next week's KPI snapshot validates the change persisted.

## 2. Ledger

`performance/learning_loop.csv`:
```
change_id,experiment_id,layer,what_changed,
applied_at,validated_at,reverted_at,note
```

## 3. Banned

- ❌ Changing weights or thresholds without a recorded experiment.
- ❌ Reverting silently — every revert is also a row.
- ❌ Claiming a learning without a re-measurement.
