# Revenue Factory — Live Data

The map of which CSV feeds which dashboard, panel, or scorecard. This file
exists so that adding a new dashboard never requires guessing where data
lives.

## Source rows in the repo

| Source file | What it feeds |
|---|---|
| [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv) | Pipeline panel, sector scorecard, daily brief Q6 |
| [`docs/ops/pipeline_tracker_enriched.csv`](../ops/pipeline_tracker_enriched.csv) | Extended pipeline analytics |
| [`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv) | Strategic Account List, daily brief CEO accounts |
| [`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv) | NSM, weekly scorecard, sector scorecard, enterprise motion health |
| [`docs/commercial/operations/gtm_conversation_tracker.csv`](../commercial/operations/gtm_conversation_tracker.csv) | Conversation history, win/loss aggregates |

## Module sources

| Module | What it provides |
|---|---|
| [`auto_client_acquisition.approval_center`](../../auto_client_acquisition/approval_center/) | Pending approvals + queue latency |
| [`auto_client_acquisition.proof_ledger`](../../auto_client_acquisition/proof_ledger/) | Payment events, proof events |
| [`auto_client_acquisition.friction_log`](../../auto_client_acquisition/friction_log/) | Friction events aggregate |
| [`auto_client_acquisition.payment_ops.renewal_scheduler`](../../auto_client_acquisition/payment_ops/renewal_scheduler.py) | Renewals due |
| [`auto_client_acquisition.capital_os.capital_ledger`](../../auto_client_acquisition/capital_os/capital_ledger.py) | Capital assets registered |

## PRIVATE_OPS sources (sensitive)

| PRIVATE_OPS file | What it feeds |
|---|---|
| `ceo/decisions.jsonl` | Decision log surfaces in daily brief Q1/Q4/Q5 |
| `ceo/strategic_assumptions.csv` | Assumptions check, daily brief stale-bet flags |
| `ceo/capital_allocations.csv` | Capital allocation panel |
| `ceo/leverage_time_audit.csv` | Founder leverage dashboard |

See [`dealix/private_ops.py`](../../dealix/private_ops.py) for the resolution helper.

## Freshness SLA

| Source | Max staleness |
|---|---|
| pipeline_tracker.csv | 1 day |
| CEO_TOP50_TRACKER.csv | 7 days |
| evidence_events_tracker.csv | 1 day |
| Approval center, proof ledger | Real-time |
| PRIVATE_OPS CSVs | Per ritual cadence (daily / weekly / monthly) |

A breach for two consecutive checks raises a `WARN` in `make hyper-verify`.

## Cross-references

- [PAYMENT_CAPTURE_OS](PAYMENT_CAPTURE_OS.md)
- [`docs/metrics/HYPERGROWTH_METRICS_SYSTEM.md`](../metrics/HYPERGROWTH_METRICS_SYSTEM.md)
- [`docs/strategy/KPI_DEFINITION_DICTIONARY.md`](../strategy/KPI_DEFINITION_DICTIONARY.md)

## Non-negotiables

Every dashboard maps to a real source row. No invented counters. See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
