# Ultimate Worker Mesh

The worker mesh is the set of background scripts that refresh the
Founder Console caches. Each worker is independent — no shared state
beyond the CSV runtime — and idempotent.

Current workers:

- `run_ceo_summary_worker.py`
- `run_sales_funnel_worker.py`
- `run_trust_flags_worker.py`
- `run_finance_summary_worker.py`

Add a new worker by:

1. Creating `scripts/run_<name>_worker.py` following the existing
   template.
2. Calling a `runtime_reader` helper for the read side.
3. Writing the cached JSON to `<private_ops>/founder/<name>.json`.
4. Updating `runtime/worker_state.csv`.
