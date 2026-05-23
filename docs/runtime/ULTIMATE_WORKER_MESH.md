# Ultimate Worker Mesh

The worker mesh is the deterministic backbone of Dealix. AI agents
*draft*; workers *execute*. The mesh is what the founder trusts.

## Contract

* Each worker is a Python script under `scripts/run_*_worker.py`.
* Each worker imports `api.internal.runtime_reader` to read state.
* Each worker writes to `runtime/worker_state.csv` exactly once per run.
* No worker performs external send. Workers that would otherwise need to
  send (e.g. outreach worker) append to `approvals/approval_queue.csv`
  instead.

## Observability

`/workers` in the Founder Console reads `worker_state.csv` and renders
last-run / status / failures-24h / next-run / notes. Anything missing
shows as "—".

## Add a worker

1. Create `scripts/run_<name>_worker.py`. Use one of the existing
   scripts as a template.
2. Make it idempotent. Re-running must produce the same artifact.
3. Add a row in `worker_state.csv` on every run.
4. Register the worker in `registries/agent_registry.yaml` if it
   wraps an agent.
5. Update this doc with the new row.
