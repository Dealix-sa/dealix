# Worker Orchestrator v1

We run six "safe" workers in this pass:

| Worker | Script | Output |
|---|---|---|
| ceo_summary | `scripts/run_ceo_summary_worker.py` | `founder/ceo_summary.json` |
| sales_funnel | `scripts/run_sales_funnel_worker.py` | `founder/sales_funnel.json` |
| trust_flags | `scripts/run_trust_flags_worker.py` | `founder/trust_flags.json` |
| finance_summary | `scripts/run_finance_summary_worker.py` | `founder/finance_summary.json` |
| operating_scorecard | `scripts/run_operating_scorecard_worker.py` | `founder/operating_scorecard.md` |
| sovereign_readiness | `scripts/run_sovereign_readiness_worker.py` | `founder/sovereign_readiness.md` |

Every worker:

1. Reads only from private-ops paths.
2. Writes into the founder/ subtree.
3. Updates `runtime/worker_state.csv` via `scripts/update_worker_state.py`.
4. **Never sends externally.**

## Scheduling

For now, schedule them via existing GitHub workflows (e.g.
`daily_snapshot.yml`) or cron on the deploy box. A dedicated cron file
is out of scope for this commit — the worker scripts are
schedule-tool-agnostic.

## Failure mode

If a worker crashes, its row in `worker_state.csv` flips to `failed`
with the exception string in `notes`. The Founder Console renders this
red in `/workers`. A founder click in `/workers` → "Retry" calls
`POST /workers/{id}/retry` which adds an audit-log entry; the next
scheduler tick re-runs the worker.
