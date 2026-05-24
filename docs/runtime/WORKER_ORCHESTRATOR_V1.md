# Worker Orchestrator v1 — مُنسِّق العُمَّال

Status: v1
Owner: Founder

## 1. Purpose — الغرض

The orchestrator schedules and supervises every worker that produces or transforms internal artifacts. It guarantees freshness, ordering, and audit.

المُنسِّق يجدول ويشرف على كل عامل ينتج أو يحول الملفات الداخلية. يضمن الحداثة والترتيب والتدقيق.

## 2. Worker Definition — تعريف العامل

A worker is a registered job with:
- `id`
- `purpose`
- `schedule` (cron or interval)
- `inputs` (paths or queries)
- `outputs` (paths)
- `freshness_sla_minutes`
- `kill_switch`
- `owner`
- `audit_required: true`

Workers are declared in `registries/workers.yaml` (analogous to the agent registry; same fail-closed loader contract).

## 3. Scheduling — الجدولة

- Cron-style triggers for periodic jobs.
- Interval triggers for fast loops (e.g., heartbeat reconciliation).
- Event triggers for queue arrivals (e.g., new CSV in inbox).
- Jitter applied to avoid thundering herds.

## 4. Heartbeats and Freshness — النبض والحداثة

- Every worker emits a heartbeat on start, periodic during long runs, and on completion.
- The orchestrator computes freshness % per worker over the rolling window.
- A worker that misses its SLA is marked `stale`; the Founder Console reflects this; a risk is opened automatically.

## 5. Retries and Backoff — إعادة المحاولة

- Default: exponential backoff with jitter, capped at 5 attempts.
- Idempotency is required: a worker that runs the same input twice must produce the same output.
- After max attempts, the run is failed; an alert is emitted; no silent skip.

## 6. Concurrency and Ordering — التزامن والترتيب

- Per-worker concurrency limit declared in the registry.
- Per-stream ordering preserved (e.g., CSV ingest by filename timestamp).
- Cross-worker dependencies declared explicitly; the orchestrator topologically sorts them.

## 7. Resource Quotas — حصص الموارد

- CPU/memory per worker capped.
- LLM cost cap per worker per day (where workers call LLM Gateway).
- Storage quotas under `/opt/dealix-ops-private/<domain>/`.

## 8. Failure Modes — أنماط الفشل

- Worker crash -> auto-restart with backoff; after threshold, kill switch flipped and founder paged.
- Input missing -> run skipped with reason; audit entry; never silent.
- Output rejected by Guardian -> run failed; quarantine populated.
- Orchestrator down -> all workers stop on next heartbeat; nothing runs unsupervised.

## 9. Audit — التدقيق

Every run emits:
- `worker_id`, `run_id`, `started_at`, `ended_at`, `inputs_hash`, `outputs_hash`, `outcome`, `cost`, `retries`.

## 10. Non-Negotiables — خطوط حمراء

- No worker runs without registry registration.
- No worker writes outside its declared outputs.
- No worker bypasses the Guardian for any output destined for external surfaces.
- No worker without a kill switch.

## 11. References — مراجع

- `docs/runtime/ULTIMATE_WORKER_MESH.md`
- `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
- `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
