# Founder Bottleneck Removal

The CEO is allowed to be the bottleneck for at most **three** things at a
time. Every Friday, the bottleneck radar emits the top items where the CEO
is on the critical path; for each one, the weekly review picks an action.

## Inputs

- `scripts/dealix_bottleneck_radar.py` output → `docs/metrics/bottlenecks_recent.csv` (already in repo)
- PRIVATE_OPS `ceo/decisions.jsonl` filtered to `owner == "ceo"` and `status in (pending, executing)`

## Weekly loop

1. List the bottlenecks where CEO is owner (top 5)
2. For each: apply [`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)
3. Three allowed to remain on CEO; the rest get delegated, automated, or killed
4. Decisions logged in [`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md)

## Cross-references

- [DELEGATION_SYSTEM](DELEGATION_SYSTEM.md)
- [`docs/founder/CEO_WEEKLY_REVIEW.md`](../founder/CEO_WEEKLY_REVIEW.md)
- [`docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`](../founder/FOUNDER_LEVERAGE_DASHBOARD.md)

## Non-negotiables

Bottleneck removal does not skip approval gates. If a bottleneck is itself
an approval gate, the answer is more reviewers, not removal. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
