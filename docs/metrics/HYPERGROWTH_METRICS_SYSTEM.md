# Hypergrowth Metrics System

A three-tier tree. Tier-1 is the North Star. Tier-2 are the leading
indicators. Tier-3 are the operating counters.

## Tier 1 — North Star

See [`docs/strategy/NORTH_STAR_METRIC.md`](../strategy/NORTH_STAR_METRIC.md).

**Definition**: Qualified Saudi B2B revenue opportunities advanced to
cash, proof, or expansion in the trailing 30 days.

The North Star is updated daily by reading the existing evidence CSV at
[`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv).

## Tier 2 — Leading indicators (weekly)

| Metric | Source | Target | KPI dict |
|---|---|---|---|
| Qualified leads added | `docs/ops/pipeline_tracker.csv` | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Positive replies | `docs/commercial/operations/evidence_events_tracker.csv` | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Samples delivered | evidence tracker | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Proposals issued | evidence tracker | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Paid invoices | proof ledger | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Active retainers | renewal scheduler | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |
| Trust events approved | approval center | Per quarterly goal | [KPI_DEFINITION_DICTIONARY](../strategy/KPI_DEFINITION_DICTIONARY.md) |

## Tier 3 — Operating counters (daily)

Pulled from existing systems. The CEO does not look at these directly; they
roll up into Tier 2 in the weekly scorecard.

| Counter | Source |
|---|---|
| Approval queue length | `auto_client_acquisition.approval_center` |
| Friction events | `auto_client_acquisition.friction_log` |
| Eval pass rate | `dealix/execution_assurance/registry.yaml` red-team prompts run |
| Renewals due in next 7 days | `auto_client_acquisition.payment_ops.renewal_scheduler` |
| Bottleneck count | `scripts/dealix_bottleneck_radar.py` |

## How the tree rolls up

- Tier 3 counters feed into Tier 2 in the weekly scorecard
- Tier 2 trends feed into Tier 1 in the monthly review
- Tier 1 drives the quarterly capital allocation in [`docs/finance/CAPITAL_ALLOCATION_SYSTEM.md`](../finance/CAPITAL_ALLOCATION_SYSTEM.md)

## Cross-references

- [`docs/strategy/DEALIX_GOAL_TREE.md`](../strategy/DEALIX_GOAL_TREE.md) — goals ↔ metrics
- [`docs/strategy/KPI_DEFINITION_DICTIONARY.md`](../strategy/KPI_DEFINITION_DICTIONARY.md) — exact definitions
- [`docs/founder/CEO_WEEKLY_REVIEW.md`](../founder/CEO_WEEKLY_REVIEW.md) — weekly rollup ritual
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml) — live targets

## Non-negotiables

Every metric has a real source row. Estimates are flagged `is_estimate: true`
in the API surface. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
