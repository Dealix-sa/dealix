# Worker Queue Architecture

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #4 (no production autonomy without rollback path).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Run Dealix factory workers reliably on the server. Define which workloads belong on a scheduled cron, which belong on an async queue, and which belong in a durable workflow engine.

## Current State (today)

- **ARQ + Redis** is operational: `core/queue/worker.py` configures 10 concurrent jobs, a 5-minute soft timeout, 3 retries, and 1-hour result retention.
- **Tasks**: `core/queue/tasks.py` defines `run_agent_job` and job status tracking.
- **Scheduled jobs**: `core/queue/weekly_self_improvement.py`.
- **CS handoff queue**: `core/queue/cs_handoff_task.py`.
- **Daily orchestration**: GitHub Actions (`daily-revenue-machine.yml`, `founder_commercial_daily.yml`, `daily_digest.yml`, `daily_snapshot.yml`, `founder_autonomous_ops_weekly.yml`, `founder_strongest_ops_daily.yml`).
- **Local snapshots**: `make v5-status`, `make v5-digest`, `make v5-snapshot`.

## Phased Architecture

### Phase 1 — Cron / GitHub Actions (today)

Best for:

- Scheduled reports and digests.
- Deterministic scoring runs.
- Daily snapshots.
- Internal aggregations with no external side effect.

Risk: a missed run is recoverable on the next tick.

### Phase 2 — ARQ on Redis (today, for elastic load)

Best for:

- Lead enrichment fan-out.
- Outreach draft generation.
- Reply classification batches.
- Sample generation jobs.
- Internal LLM calls with retries.

Risk: a job that produces an external side effect must still pass through the approval gate before the side effect happens; the queue does not approve.

### Phase 3 — Durable Workflows (future)

Best for:

- Proposal lifecycle (draft → approval → send → follow-up → close).
- Payment capture (proposal → invoice → reminder → cash → revenue event).
- Delivery lifecycle (start condition → milestones → QA → handover → feedback).
- Approval retries that must not lose state across redeploys.

Candidate engines: Temporal, LangGraph durable runs. This is a future RFC, not a current commitment.

## Queue Types (logical)

- `lead_discovery`
- `enrichment`
- `scoring`
- `outreach_draft`
- `approval_surfacing`
- `followup`
- `reply_route`
- `sample_factory`
- `proposal_factory`
- `payment_capture`
- `delivery`
- `retention`
- `content`
- `cs_handoff` (live)

Each logical queue maps to an ARQ task name or a scheduled Action. The mapping is documented in `core/queue/tasks.py`.

## Core Rules

- Every job is **idempotent** or **replay-safe**. Re-running on retry must not double-send or double-charge.
- External side effects (sending, billing, publishing) are **never** initiated by a queue worker alone; they require an approval record in `AuditLogRecord`.
- Failed jobs that touched external systems must produce an event in the revenue memory event store with a `causation_id`.
- Worker failures alert; backlog age above threshold alerts; missed daily Actions alert.
- A rollback path exists for every job that mutates a public-facing artifact (revert to prior version stored in event store).

## Runtime Wiring

- ARQ worker config: `core/queue/worker.py`.
- Task definitions: `core/queue/tasks.py`.
- Weekly self-improvement scheduler: `core/queue/weekly_self_improvement.py`.
- CS handoff: `core/queue/cs_handoff_task.py`.
- Event store (for causation IDs): `auto_client_acquisition/revenue_memory/event_store.py`.
- Audit trail: `db/models.py::AuditLogRecord`.
- Background job status: `db/models.py::BackgroundJobRecord`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Worker job success rate | ≥ 95% | `BackgroundJobRecord` |
| Job p95 latency | < 5 minutes (current soft timeout) | ARQ stats |
| Backlog age | < 1 hour for approval-bound queues | derived |
| Failed jobs touching external systems | 0 silent failures (must produce event) | event store |
| Missed scheduled Actions per week | 0 | GitHub Actions history |

## Cross-Links

- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/engineering/OBSERVABILITY_SLO_SYSTEM.md`
- `docs/data/GROWTH_DATABASE_MODEL.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/SLO.md`

## Open Items

- A formal idempotency-key registry (per logical queue) does not yet exist; today it is per-task discipline.
- Phase 3 (durable workflows) is not a current commitment; do not plan delivery against it.
- Backlog-age alerting is not yet wired; the SLO doc has the target but the alert plumbing is open.
