# Ultimate Worker Mesh — شبكة العُمَّال الشاملة

Status: v1
Owner: Founder

## 1. Purpose — الغرض

The Worker Mesh is the network of workers that performs all internal batch and stream work for Dealix. The orchestrator schedules; the mesh executes.

شبكة العُمَّال هي الشبكة التي تنفذ كل العمل الدُّفعي والمتدفق داخل Dealix. المنسق يجدول، والشبكة تنفذ.

## 2. Mesh Domains — مجالات الشبكة

| Domain | Examples |
|---|---|
| Intelligence | ICP collectors, signal normalizers, dedupe |
| Outreach | Draft generators, language QC, queue compilers |
| Approvals | Queue maintenance, expiry, escalation |
| Trust | Guardian regression checks, quarantine reaper |
| Finance | Cost rollups, AI spend reconciliation |
| Runtime | Heartbeat reconciliation, freshness reporters |
| Data | CSV ingest, shadow refresh, promotion jobs |

## 3. Worker Identity — هوية العامل

- Each worker has a service identity.
- Workers cannot impersonate each other.
- Cross-domain calls go through declared interfaces, not direct DB access.

## 4. Communication — الاتصال

- Workers do not call each other directly.
- They communicate via:
  - File contracts under `/opt/dealix-ops-private/<domain>/`.
  - Postgres queues (in `staging` or `app` per case).
  - Internal API endpoints when a control action is needed.

## 5. Heartbeats and Freshness — النبض والحداثة

- Heartbeats every minute to the orchestrator.
- Freshness SLO per worker; breach opens a risk and marks `stale` on the Console.
- Founder can trip the worker kill switch from the Console.

## 6. Backpressure — ضغط الارتداد

- If Guardian queue depth exceeds threshold, upstream workers pause.
- If LLM cost cap reached, drafting workers pause.
- If Postgres saturation high, ingest workers slow.

## 7. Observability — الرصد

- Metrics: throughput, latency, error rate, freshness, cost.
- Logs: structured with `worker_id`, `run_id`, `trace_id`.
- Traces: end-to-end spans across workers when a single artifact flows through multiple domains.

## 8. Deployment — النشر

- Workers run as separate processes or containers under the same cluster identity boundary as APIs.
- Rolling deploys; one domain at a time.
- Health checks per worker; orchestrator refuses to schedule on unhealthy nodes.

## 9. Failure Domains — مناطق الفشل

| Domain failure | Effect |
|---|---|
| Intelligence | Stale signals; older drafts; flagged on Console |
| Outreach | Queue does not grow; founder sees empty queue with reason |
| Approvals | Decisions still possible; expiry/escalation paused |
| Trust | All dependent writes blocked (fail closed) |
| Finance | Cost rollups stale; analytics flagged stale |
| Runtime | Mesh self-reports `stale`; founder paged |
| Data | Ingest queues build up but nothing is lost |

## 10. Non-Negotiables — خطوط حمراء

- No worker has external send capability.
- No worker writes outside its declared outputs.
- No worker is exempt from heartbeats or freshness reporting.
- No worker scales beyond its declared resource quota.

## 11. References — مراجع

- `docs/runtime/WORKER_ORCHESTRATOR_V1.md`
- `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
- `docs/data/ULTIMATE_DATA_PLATFORM.md`
- `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`
