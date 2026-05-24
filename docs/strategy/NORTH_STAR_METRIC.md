# North Star Metric

A single number. If only one chart were on the wall, this one would be it.

## The metric

> **Qualified Saudi B2B revenue opportunities advanced to cash, proof, or
> expansion in the trailing 30 days.**

Computed from [`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv) +
[`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv).

## Why this one

- It includes cash (paid invoices)
- It includes proof (case studies, references — when approved through the
  proof system in [`docs/07_proof_os/`](../07_proof_os/))
- It includes expansion (existing customers buying again)
- It excludes vanity — pure leads, page views, follower counts

## Counter-metrics

A North Star without counter-metrics rewards gaming. Track these alongside:

| Counter | Why |
|---|---|
| Approval queue latency | If the NSM rises while latency rises, we are pushing past trust |
| Friction events / week | If the NSM rises while friction rises, we are burning future cash |
| Move-bucket ratio | If the NSM rises while CEO Move drops, we are unsustainable |

Both NSM and counters live in [HYPERGROWTH_METRICS_SYSTEM](../metrics/HYPERGROWTH_METRICS_SYSTEM.md).

## Cadence

- Daily: surfaced on the daily brief
- Weekly: charted in the weekly scorecard
- Monthly: trend reviewed in the monthly cadence ritual

## Cross-references

- [HYPERGROWTH_METRICS_SYSTEM](../metrics/HYPERGROWTH_METRICS_SYSTEM.md)
- [DEALIX_GOAL_TREE](DEALIX_GOAL_TREE.md)
- [KPI_DEFINITION_DICTIONARY](KPI_DEFINITION_DICTIONARY.md)
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml) `ceo_north_star_en` block

## Non-negotiables

The NSM is computed from real source rows; estimates are explicitly flagged.
See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
