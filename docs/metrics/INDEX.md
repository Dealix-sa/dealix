# Metrics Hub — INDEX

The single place that names every metric the CEO looks at and ties each to a
North Star and to a real source-of-truth file. This hub does not invent new
counters; it indexes existing ones.

## Read in this order

1. [HYPERGROWTH_METRICS_SYSTEM](HYPERGROWTH_METRICS_SYSTEM.md) — the three-tier metric tree
2. [`docs/strategy/NORTH_STAR_METRIC.md`](../strategy/NORTH_STAR_METRIC.md) — the single most important metric
3. [`docs/strategy/KPI_DEFINITION_DICTIONARY.md`](../strategy/KPI_DEFINITION_DICTIONARY.md) — exact definitions per KPI
4. [`docs/strategy/DEALIX_GOAL_TREE.md`](../strategy/DEALIX_GOAL_TREE.md) — how metrics roll up to goals

## Cross-references

- [`docs/company/KPI_SYSTEM.md`](../company/KPI_SYSTEM.md) — historical KPI definitions
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml) — `kpis_targets` block is the live target source
- [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv) — pipeline counter source
- [`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv) — funnel event source

## Non-negotiables

Every metric in this hub must have a real source. No invented counters, no
hand-waved estimates without an `is_estimate: true` flag. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
