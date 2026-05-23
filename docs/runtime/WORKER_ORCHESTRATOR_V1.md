# Worker Orchestrator v1

Workers are plain Python scripts under `scripts/run_*_worker.py`. They:

- Read `$DEALIX_PRIVATE_OPS/...csv`.
- Use `api.internal.runtime_reader` helpers.
- Write a cached JSON snapshot to `<private_ops>/founder/...json`.
- Append a row to `runtime/worker_state.csv` with status and notes.

Each worker fails gracefully — it never raises out of the script and
never sends externally. A worker that cannot read its inputs records
`status=error` and continues.

Scheduled triggering is intentionally left to the host (cron, Railway
cron, systemd timers). The repo only ships the scripts.
