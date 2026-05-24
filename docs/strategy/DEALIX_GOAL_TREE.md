# Dealix Goal Tree

OKR → KPI → metric → daily action. The tree is small on purpose: the more
nodes, the less attention each one gets.

## The tree

```
North Star: Qualified Saudi B2B revenue opportunities advanced to cash, proof, or expansion (trailing 30d)
│
├── Strategic Goal 1: Beachhead sector locked
│   ├── KPI: ≥ 3 paid customers in same sector in 90d
│   ├── Source: docs/ops/pipeline_tracker.csv + docs/commercial/operations/evidence_events_tracker.csv
│   └── Owner: ceo
│
├── Strategic Goal 2: Revenue Factory loops complete
│   ├── KPI: Every positive reply has a sample/proposal path within 72h
│   ├── Source: docs/commercial/operations/evidence_events_tracker.csv
│   └── Owner: ceo (until delegated per docs/people/HIRING_TRIGGER_SYSTEM.md)
│
├── Strategic Goal 3: Trust posture is enterprise-ready
│   ├── KPI: 100% of customer-facing actions through approval-center gates
│   ├── Source: auto_client_acquisition.approval_center
│   └── Owner: ceo
│
└── Strategic Goal 4: Founder leverage trending up
    ├── KPI: Move-bucket ratio ≥ 0.40 by week 12
    ├── Source: PRIVATE_OPS ceo/leverage_time_audit.csv
    └── Owner: ceo
```

## How the tree is used

- Quarterly: re-set goals during the quarterly review (see [`docs/founder/CEO_OPERATING_SYSTEM.md`](../founder/CEO_OPERATING_SYSTEM.md))
- Weekly: each goal grade rolls up from [HYPERGROWTH_METRICS_SYSTEM](../metrics/HYPERGROWTH_METRICS_SYSTEM.md)
- Daily: the brief surfaces any goal whose KPI is off track

## Cross-references

- [NORTH_STAR_METRIC](NORTH_STAR_METRIC.md)
- [KPI_DEFINITION_DICTIONARY](KPI_DEFINITION_DICTIONARY.md)
- [`docs/metrics/HYPERGROWTH_METRICS_SYSTEM.md`](../metrics/HYPERGROWTH_METRICS_SYSTEM.md)
- [`docs/strategy/CEO_STRATEGY.md`](CEO_STRATEGY.md)
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml)

## Non-negotiables

Goals are tracked against real sources. No invented progress. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
