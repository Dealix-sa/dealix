# Worker Orchestrator v1

> Run Dealix workers reliably with schedules, health, retries, and
> alerts.

## Purpose

Turn ad-hoc scripts into named, observable workers. Make `/workers`
show real state: who ran when, what failed, what is the queue depth,
who owns it, and how to disable it without a redeploy.

## Position in the Operating Layer

Worker Orchestrator is the Worker Layer of Operating Layer v1. Every
recurring or queue-draining job in Dealix runs through it.

## Worker Types

| Type | Trigger | Examples |
|------|---------|----------|
| Scheduled | Cron | `ceo_summary_worker` (daily), `finance_summary_worker` (hourly) |
| Queue-draining | Queue depth > 0 | `outreach_send_worker`, `payment_capture_worker` |
| Approval-triggered | Founder decision in `/approvals` | `outreach_dispatch_worker` |
| Event-triggered | New audit / webhook event | `reply_router_worker` |
| Durable workflow (later) | Multi-step state machines with checkpoints | `customer_onboarding_workflow` |

## Required Metadata (Per Worker)

Every worker registers itself with this metadata before it can run:

```yaml
worker_id: ceo_summary_worker
owner: founder
schedule: "0 6 * * *"              # cron, or null for queue/event
status: enabled                    # enabled | disabled | degraded
last_run:
  started_at: ISO-8601
  finished_at: ISO-8601
  result: success | failure
failures_24h: 0
queue_depth: 0
input_source: postgres:approval_queue
output_target: postgres:audit_events
retry_policy:
  max_attempts: 5
  backoff: exponential
  base_seconds: 30
  max_seconds: 1800
max_runtime_seconds: 600
disable_switch: configs/workers/ceo_summary_worker.enabled
health_check: GET /workers/health/ceo_summary_worker
```

These fields back the `worker_state` table and the `/workers` surface.

## First Workers (v1 set)

1. `ceo_summary_worker` — computes the daily top action for `/ceo`.
2. `sales_funnel_worker` — refreshes funnel + bottleneck for `/sales-cockpit`.
3. `approval_queue_worker` — refreshes counts + SLA for `/approvals`.
4. `worker_health_worker` — folds heartbeats into `worker_state`.
5. `trust_flag_worker` — folds Guardian + Policy outputs into open flags.
6. `finance_summary_worker` — refreshes cash, capture, retainer for `/finance`.
7. `follow_up_queue_worker` — schedules + drafts follow-ups (A2 review).
8. `payment_capture_worker` — drafts payment-capture follow-ups (A2 review).

None of these workers send external messages on their own. Workers that
*would* send external messages drain an **approved** queue produced by
the founder's decision in `/approvals`.

## Lifecycle

```
register → scheduled / enqueued → running → success / failure
                                       │
                                       └── retry per policy
                                       └── on terminal failure: alert + disable
```

Each transition writes a `worker.lifecycle` audit event with
`worker_id`, `run_id`, transition, and reason.

## Health Surface

`/workers` shows, per worker:

- `status` (enabled / disabled / degraded).
- `last_run` (when + result).
- `failures_24h` (count + last error fingerprint).
- `queue_depth` (for queue-draining workers).
- `p95_runtime` (last 24h).
- `disable_switch` (link + current value).
- `owner` (who to ping).

A worker missing a heartbeat for 2× its schedule moves to `degraded`
automatically, with an alert to its owner.

## Retry & Backoff

- Exponential backoff with jitter.
- Cap on `max_attempts`. After cap → `failed`, never silently retried.
- Idempotency keys required for any worker that produces external
  effects via queues.
- Poison-pill handling: messages that fail repeatedly are moved to a
  dead-letter table, never dropped silently.

## Disable Switch

Every worker has a file-based switch:

```
configs/workers/<worker_id>.enabled
```

- `true` (default) → worker runs on schedule / drains queue.
- `false` → worker no-ops, writes a `worker.disabled` audit event each
  scheduled tick.

The switch must take effect within one tick / one minute, whichever is
shorter. The founder can flip it from `/workers` without a redeploy.

## Rule

> No worker without **health, logs, and a failure mode**.

If a worker cannot meet all three, it is a one-shot script. One-shot
scripts live in `scripts/`, not in the orchestrator.

## Failure Modes

| Mode | Detection | Response |
|------|-----------|----------|
| Schedule miss | No heartbeat within 2× period | Mark `degraded`, alert owner |
| Repeated failure | `failures_24h` ≥ threshold | Auto-disable, alert founder |
| Stuck queue | Queue depth growing for N ticks | Alert owner, surface in `/ceo` blockers |
| Long-running run | `runtime > max_runtime_seconds` | Cancel run, mark failure, alert |
| Disable switch ignored | Audit shows run after disable | Open incident, never auto-recover |

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`POSTGRES_PRIMARY_MODE`](../data/POSTGRES_PRIMARY_MODE.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
- [`AI_UNIT_ECONOMICS_SYSTEM`](../finance/AI_UNIT_ECONOMICS_SYSTEM.md)
