# KPI Definition Dictionary

The exact, unambiguous definition of every KPI surfaced anywhere in the CEO
layer. If a KPI is named in a doc, a script, an API, or a dashboard, its
definition lives here.

The live targets (numeric thresholds) live in
[`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml)
under `kpis_targets`.

## KPI table

| KPI | Definition | Source-of-truth file | Updated |
|---|---|---|---|
| `qualified_leads_added_weekly` | Distinct `lead_identified` rows in week W | [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv) | Daily |
| `positive_replies_weekly` | Distinct `reply_received` rows in week W flagged positive | [`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv) | Daily |
| `samples_delivered_weekly` | Distinct `sample_delivered` rows in week W | evidence tracker | Daily |
| `proposals_issued_weekly` | Distinct `proposal_sent` rows in week W | evidence tracker | Daily |
| `paid_invoices_weekly` | Distinct `payment_received` rows in week W from proof ledger | proof ledger (`auto_client_acquisition.proof_ledger`) | Daily |
| `active_retainers` | Distinct active subscriptions in renewal scheduler | renewal scheduler | Daily |
| `approval_queue_latency_p50` | Median time between approval requested and approval decided | `auto_client_acquisition.approval_center` | Daily |
| `friction_events_weekly` | Friction log aggregate count in week W | `auto_client_acquisition.friction_log` | Daily |
| `eval_pass_rate` | Red-team prompts passing in latest eval run | `dealix/execution_assurance/registry.yaml` red-team output | Per release |
| `move_bucket_ratio` | `move_hours / total_hours` from time audit | PRIVATE_OPS `ceo/leverage_time_audit.csv` | Weekly |
| `bottleneck_count` | Open items in bottleneck radar | `scripts/dealix_bottleneck_radar.py` | Daily |
| `north_star_trailing_30d` | NSM as defined in [NORTH_STAR_METRIC](NORTH_STAR_METRIC.md) | NSM compute | Daily |

## Rules for adding a KPI

1. It must have a single source-of-truth file
2. Its definition must be one sentence
3. Its update cadence must be named
4. It must not duplicate an existing KPI under a different name
5. The change goes through [`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md) with `type: policy`

## Cross-references

- [DEALIX_GOAL_TREE](DEALIX_GOAL_TREE.md)
- [NORTH_STAR_METRIC](NORTH_STAR_METRIC.md)
- [`docs/metrics/HYPERGROWTH_METRICS_SYSTEM.md`](../metrics/HYPERGROWTH_METRICS_SYSTEM.md)
- [`docs/company/KPI_SYSTEM.md`](../company/KPI_SYSTEM.md) — historical definitions
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml)

## Non-negotiables

Definitions here are canonical. Mismatches with code or other docs are bugs.
See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
