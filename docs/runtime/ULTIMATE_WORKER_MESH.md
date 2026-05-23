# Ultimate Worker Mesh

> The set of background machines that actually run the company.
> Every worker is observable, retryable, and disableable — without a deploy.

---

## 1. Purpose

Run Dealix as a reliable set of **background machines** that prepare work, route decisions, execute approved actions, and surface failures to the founder fast.

The worker mesh is the **engine** of the Revenue Factory and the Delivery OS. The Founder Console is the **windshield**; the Trust Plane is the **brake**; the worker mesh is the **engine**.

---

## 2. Worker levels

Workers exist at four levels of autonomy. The level determines what the worker may do, how it is scheduled, and how it is gated.

### W1 — Cron Workers
- **What:** scheduled batch jobs.
- **Examples:** daily morning digest, CSV freshness check, daily revenue rollup, stale-worker alert.
- **Constraints:** read-only or internal-only writes; never produce A2/A3 actions on their own.
- **Schedule:** explicit cron (UTC).

### W2 — Queue Workers
- **What:** event-driven workers reading from a queue.
- **Examples:** lead enrichment, scoring, draft generation, reply classification, follow-up scheduling.
- **Constraints:** outputs may produce A1 records; A2 routing to approval is allowed; never send directly.
- **Backpressure:** the queue has a max depth; exceeding it pages the founder.

### W3 — Durable Workflows
- **What:** multi-step workflows that span hours/days with checkpoints and resumption.
- **Examples:** proposal → payment lifecycle, delivery lifecycle, retention lifecycle.
- **Constraints:** every state transition writes an event; failures resume from the last checkpoint, never from the start.
- **Engine:** RQ + a workflow table (Phase 1) → Temporal-style engine (Phase 2 trigger: workflow count > 10).

### W4 — Autonomous-but-Gated Agents
- **What:** agents that plan and prepare actions across multiple tools.
- **Examples:** sector intelligence agent, account research agent.
- **Constraints:** every tool call goes through `trust.allow_tool`; every external action goes through the approval queue. **No agent ever sends or commits without founder approval.**
- **Limit:** maximum runtime per agent invocation (default 5 minutes); maximum tool calls per invocation (default 20).

Promotion between levels follows the autonomy rule in the Operating OS: trust + audit + 14 days of evidence + rollback path + owner.

---

## 3. Required worker metadata

Every worker (W1–W4) registers the following metadata at startup. Workers without complete metadata are refused at registration time.

| Field            | Type      | Required | Notes                                            |
|------------------|-----------|----------|--------------------------------------------------|
| `worker_id`      | text      | yes      | Unique, kebab-case (`lead-discovery`).           |
| `owner`          | text      | yes      | Team or person accountable.                      |
| `schedule`       | text      | yes (W1) | Crontab in UTC, or `event:<queue_name>`.         |
| `input`          | json schema | yes    | Validated at start of every run.                 |
| `output`         | json schema | yes    | Validated at end of every run.                   |
| `last_run`       | timestamptz | -      | Updated by the runner.                           |
| `status`         | enum      | -        | `ok`, `failed`, `disabled`, `stale`.             |
| `failures_24h`   | int       | -        | Rolling count.                                   |
| `retry_policy`   | json      | yes      | `max_attempts`, `backoff_base_s`, `max_delay_s`. |
| `max_runtime_s`  | int       | yes      | Hard cap; runner kills the worker if exceeded.   |
| `audit_path`     | text      | yes      | The action verb(s) written to `audit_events`.    |
| `disable_switch` | boolean   | yes      | `true` ⇒ runner skips this worker.               |

Metadata lives in `dealix/runtime/workers/<worker_id>.yaml` (Phase 1) and the `worker_registry` table (Phase 2).

---

## 4. Worker contract

Every worker implements three callables:

```python
def setup(context: Context) -> None: ...
def run(context: Context, input: Input) -> Output: ...
def teardown(context: Context, status: Status) -> None: ...
```

- `setup` runs once per process.
- `run` runs once per invocation; must be idempotent (an `idempotency_key` is provided by the runner).
- `teardown` runs after every invocation (success or failure); responsible for cleaning resources.

Every `run` records `started_at`, `finished_at`, `status`, `error`, `retry_of` in `worker_runs`.

---

## 5. Retry & backoff

- Default retry policy: `max_attempts=3`, `backoff_base_s=30`, `max_delay_s=900`.
- Workers that touch external APIs use `retry_policy.respect_retry_after = true`.
- A worker that fails 3 consecutive runs is marked **degraded** and surfaces a `/workers` alert.
- A worker that fails 5 consecutive runs is **auto-disabled** and surfaces a top-action banner on `/ceo`.

---

## 6. Observability

Each worker run emits structured logs with:
- `worker_id`, `run_id`, `trace_id`, `started_at`, `finished_at`, `status`, `error`, `idempotency_key`.

Each worker exposes Prometheus-style counters:
- `worker_runs_total{worker_id, status}`
- `worker_run_duration_seconds_bucket{worker_id}`
- `worker_backlog{queue}`

These feed the Worker Health page (`/workers`) and the Observability layer.

---

## 7. Disable switch

- The disable switch is **always** on a record in the database — never a deploy flag.
- The founder may disable a worker from `/workers` with one click.
- The runner consults the switch **before every invocation**.
- Disabled workers are not retried automatically; they wait for the founder to re-enable.

A disable that requires a deploy is not a disable.

---

## 8. Worker catalogue (initial set)

These are the workers required to exit L5 (Revenue Factory). They are seeded by `dealix/runtime/seed_workers.py`.

| worker_id              | level | schedule          | purpose                                                        |
|------------------------|-------|-------------------|----------------------------------------------------------------|
| `lead-discovery`       | W1    | `0 5 * * *`       | Pull new accounts from sources, dedupe, write `accounts`.      |
| `lead-enrichment`      | W2    | `event:enrich`    | Add firmographics + signals to `lead_intelligence`.            |
| `lead-scoring`         | W2    | `event:score`     | Compute fit + intent; rank for outreach.                       |
| `outreach-draft`       | W2    | `event:draft`     | Generate outreach drafts; route to approval (A2).              |
| `suppression-check`    | W2    | `event:send`      | Last gate before send; consult suppression list.               |
| `outreach-send`        | W2    | `event:send`      | Send via integration; record in `conversation_log`.            |
| `reply-router`         | W2    | `event:reply`     | Classify replies; route to founder or to a follow-up worker.   |
| `followup-scheduler`   | W1    | `0 7 * * *`       | Compute next follow-up dates per `conversation_log`.           |
| `sample-factory`       | W3    | `event:sample`    | Generate sample assets; QA; route to approval (A2).            |
| `proposal-factory`     | W3    | `event:proposal`  | Render proposal from template; route to approval (A2).         |
| `payment-followup`     | W3    | `0 8 * * *`       | Walk `payment_capture_queue`; surface to founder.              |
| `delivery-intake`      | W3    | `event:intake`    | Create client workspace; seed intake doc.                      |
| `qa-runner`            | W2    | `event:qa`        | Run QA checklist; surface to founder for sign-off.             |
| `health-score`         | W1    | `0 9 * * MON`     | Compute weekly client health; route renewals to `/retention`.  |
| `proof-approval`       | W3    | `event:proof`     | Walk customer for proof approval; on receipt, publish (A3).    |
| `morning-digest`       | W1    | `0 4 * * *`       | Bilingual morning digest for the founder.                      |
| `evening-evidence`     | W1    | `0 16 * * *`      | Evidence rollup for the day; writes to `audit_events`.         |
| `dora-collector`       | W1    | `0 1 * * *`       | Compute DORA metrics for the prior 24h.                        |
| `eval-runner`          | W1    | `0 2 * * *`       | Run AI eval suites; write to `ai_eval_results`.                |
| `stale-worker-alert`   | W1    | `*/15 * * * *`    | Flag any worker that missed its schedule.                      |
| `backup-runner`        | W1    | `0 3 * * *`       | Daily backups + restore drill heartbeat.                       |

---

## 9. Worker → trust integration

Every worker that may produce an external action calls the trust plane **before** producing it:

```python
result = trust.evaluate(
    action="outreach_send",
    subject={"contact_id": contact_id},
    payload_digest=hash_payload(draft),
    actor=f"worker:{worker_id}",
    evidence={"draft_id": draft_id},
)

if result.decision == "DENIED":
    return skipped(reason=result.reason)
elif result.decision == "ALLOWED_WITH_APPROVAL":
    return route_to_approval(...)
elif result.decision == "ALLOWED":
    return send(...)
```

No worker reaches `integrations/` without going through this branch.

---

## 10. Rule

> **Every worker must be observable, retryable, and disableable.**

A worker that the founder cannot see, cannot retry, or cannot disable from `/workers` does not belong in the mesh.
