# Worker Orchestrator v1

The worker orchestrator is intentionally simple: cron-like jobs that
update CSVs under `${DEALIX_PRIVATE_OPS}` and write a row to
`runtime/worker_state.csv` after every run.

## Contract

Every worker must:

1. Read what it needs from the private ops tree (or built-in fallbacks).
2. Compute its report.
3. Append/update its rows.
4. Call `scripts/update_worker_state.py --worker <name> --status ok|failed`.
5. Never send anything externally.
6. Fail gracefully — a worker exception must update worker_state with
   `--status failed`, not crash the process loop.

## First workers

- `run_ceo_summary_worker.py` — composes the CEO summary report.
- `run_sales_funnel_worker.py` — refreshes the sales funnel report.
- `run_trust_flags_worker.py` — rolls up open trust flags.
- `run_finance_summary_worker.py` — composes the finance summary report.

## Scheduling

Use cron, systemd timers, or any external scheduler. The orchestrator
deliberately does not own scheduling — that would couple it to a server
runtime we have not committed to yet.
