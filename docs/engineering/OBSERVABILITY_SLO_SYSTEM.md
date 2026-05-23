# Observability & SLO System

## Doctrine Anchor
- Non-negotiables touched: #2 (no value claim without source evidence), #4 (no production autonomy without rollback path), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Ensure Dealix production workers, APIs, agents, queues, and scheduled Actions are reliable, observable, and held to explicit service-level objectives. The SLOs in this document supplement the API-level SLOs in `docs/SLO.md` with **operational SLOs** for the Revenue Factory.

## Existing Observability Surface

- Structured logs: structlog JSON, per `docs/OBSERVABILITY_ENV.md`.
- Request IDs propagated through middleware.
- Provider usage metrics (LLM, embedding, vector store).
- Optional tracing: Langfuse.
- AI-specific evals and observability: `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- 22-point production verifier: `make v5-verify`.
- Daily snapshot: `make v5-snapshot`, `.github/workflows/daily_snapshot.yml`.

## Operational SLOs (factory-level)

| Surface | SLO | Source |
|---------|-----|--------|
| Mission control / daily digest generation | 99% successful runs per quarter | `daily_digest.yml`, `daily_snapshot.yml` |
| Lead scoring job success | ≥ 95% | `BackgroundJobRecord` |
| Approval queue generation | daily, on every business day | `daily_digest.yml` |
| Proposal draft generation latency | within 24h of request | proposal worker |
| Payment follow-up queue | surfaced daily | revenue events |
| Worker job p95 latency | < 5 minutes (current soft timeout) | ARQ stats |
| Backlog age for approval-bound queues | < 1 hour | derived |
| Webhook handler success rate (Moyasar etc.) | ≥ 99.5% | webhook logs |
| Approval Center SLA breach rate | < 5% | `AuditLogRecord` |
| Cross-tenant access denials | 0 (any access attempt is a security event) | `AuditLogRecord` |

## Alerting Conditions

- A worker has failed three times consecutively on the same job.
- A queue's backlog has aged past its threshold.
- A scheduled daily Action did not produce its output.
- A worker attempted an external side effect without an approval record (this is a security incident, not a warning).
- AI provider error rate spikes above threshold over 15 minutes.
- Cost per outcome rises sharply without conversion improvement (see `docs/finance/AI_UNIT_ECONOMICS.md`).

## DORA-Aligned Engineering Metrics

Track engineering velocity and stability:

- **Deployment frequency** — how often we ship.
- **Change lead time** — commit to production.
- **Change failure rate** — fraction of deploys that caused incidents.
- **Mean time to recovery** — incident open to closed.

These are reviewed monthly; targets are calibrated against the team size.

## Core Rules

- Every SLO has a source-of-truth. A claim "we are at 99%" requires a query path to the underlying records.
- An SLO breach is logged and reviewed, not averaged away.
- A new external integration is not released until its observability and SLO are documented.
- Public claims about uptime, reliability, or automation savings are gated on measured numbers.

## Runtime Wiring

- API SLOs: `docs/SLO.md` (existing).
- Environment / observability config: `docs/OBSERVABILITY_ENV.md`.
- AI observability and evals: `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- 22-point production verifier: `make v5-verify`.
- Daily Actions: `.github/workflows/daily_digest.yml`, `daily_snapshot.yml`.
- ARQ worker stats: `core/queue/worker.py`.
- Audit log: `db/models.py::AuditLogRecord`.

## Cross-Links

- `docs/SLO.md`
- `docs/OBSERVABILITY_ENV.md`
- `docs/AI_OBSERVABILITY_AND_EVALS.md`
- `docs/runtime/WORKER_QUEUE_ARCHITECTURE.md`
- `docs/finance/AI_UNIT_ECONOMICS.md`
- `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`
- `docs/founder/BOARD_LEVEL_KPI_STACK.md`

## Open Items

- Alert routing is not yet centralized (which alerts go where, who is on call). A small RFC will define this.
- DORA metrics are not yet computed automatically; they will be derived from PR and deploy history.
- Backlog-age alerting needs a small library in `core/queue/`.
- A weekly operational SLO scorecard view in the cockpit is open.
