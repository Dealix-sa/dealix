# Worker Orchestrator v1

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Focused on Results.

The Worker Orchestrator is the component that owns scheduling, state
tracking, and kill-switch enforcement for every Dealix agent. It is
the only sanctioned scheduler. It writes to a single file:
`runtime/worker_state.csv` in the private ops runtime. The Founder
Console reads from that file via
`GET /api/v1/internal/workers/health`.

## Scope

The orchestrator owns:

| Concern                                  | Responsibility                                                          |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| Worker scheduling                        | Decide which workers run, when, and at what cadence.                    |
| Worker state                             | Track `status`, `last_run`, `failure_count`, `owner` per worker.        |
| Kill switch enforcement                  | Refuse to start a worker whose agent is disabled in the registry.       |
| Write-target enforcement                 | Refuse a worker write that escapes its `allowed_write_targets`.         |
| Retry policy                             | Re-run failed workers per policy; surface persistent failures.          |
| Eval gate dependency                     | Skip a worker that produces drafts if the eval gate is red.             |

The orchestrator does not:

- Send external messages.
- Touch Postgres business data directly.
- Approve or reject queued items.
- Edit any CSV other than `runtime/worker_state.csv`.

## State file schema

`runtime/worker_state.csv` has the columns from the bootstrap:

| Column           | Type     | Notes                                                                  |
| ---------------- | -------- | ---------------------------------------------------------------------- |
| `id`             | string   | Worker id, prefixed with the agent id (e.g., `distribution_operator_draft`). |
| `name`           | string   | Human-readable name.                                                    |
| `status`         | enum     | `idle`, `running`, `succeeded`, `failed`, `disabled`, `killed`.        |
| `last_run`       | ISO ts   | Most recent completion time.                                            |
| `failure_count`  | int      | Number of consecutive failures.                                         |
| `owner`          | string   | Accountable agent id from the registry.                                 |

The Founder Console maps the file to:

```
[
  {"id": "...", "name": "...", "status": "...", "last_run": "...", "failure_count": N},
  ...
]
```

## Worker statuses

| Status       | Transition rules                                                                     |
| ------------ | ------------------------------------------------------------------------------------ |
| `idle`       | Default. Waiting for the next scheduled trigger.                                      |
| `running`    | Worker is executing. Set on start.                                                    |
| `succeeded`  | Last run finished without raising. Sets `last_run`.                                  |
| `failed`     | Last run raised. Increments `failure_count`. Sets `last_run`.                        |
| `disabled`   | The agent's kill switch is flipped in the registry. Worker will not run.             |
| `killed`     | Operator-initiated stop. Worker will not run until re-enabled.                       |

State transitions are written by the orchestrator. Workers do not
edit their own row directly.

## Scheduling

Each worker has a declared cadence:

| Cadence            | Notes                                                            |
| ------------------ | ---------------------------------------------------------------- |
| `realtime`         | Triggered by an event (e.g., a new draft).                       |
| `every_N_minutes`  | Cron-style interval; N is a small integer.                       |
| `hourly`           | Every hour, on the hour.                                          |
| `daily`            | Once per day at a defined UTC time.                              |
| `weekly`           | Once per week.                                                    |
| `monthly`          | Once per month.                                                   |

Cadences are configured in a worker registry separate from the agent
registry. The agent registry says what an agent is allowed to do; the
worker registry says when it runs.

## Kill switch enforcement

Before starting a worker, the orchestrator:

1. Reads the agent entry from `registries/agent_registry.yaml`.
2. If `enabled: false`, marks the worker `disabled` and skips.
3. If the agent is enabled, checks for an open incident on the agent
   in `trust/incidents.csv`.
4. If an incident is open and `severity in [high, critical]`, the
   worker is skipped and a trust flag is raised.

The Founder Console can flip the kill switch via
`POST /control/agents/{id}/disable`. The change takes effect on the
orchestrator's next state read (typically within seconds).

## Write-target enforcement

Each worker declares a target directory. The orchestrator wraps the
worker's write API and rejects any write whose path does not begin
with one of the agent's `allowed_write_targets`. The rejection is
recorded in:

| File                            | Row written                                                |
| ------------------------------- | ---------------------------------------------------------- |
| `trust/trust_flags.csv`          | `severity: high`, `description: worker_write_out_of_scope` |
| `trust/approval_decisions.csv`   | `action: worker_write_rejected`, `risk: high`              |

The worker is marked `failed`. The agent's `failure_count` is
incremented. If the count exceeds a threshold, the orchestrator
flips the kill switch and notifies the founder.

## Retry policy

| Failure mode                              | Retry                                                              |
| ----------------------------------------- | ------------------------------------------------------------------ |
| Transient I/O                             | Exponential backoff, max 3 retries.                                |
| Schema drift on read                       | No retry. Worker fails and DQ system is notified.                  |
| Eval gate red                              | No retry until gate green.                                         |
| Policy denial                              | No retry. The denial is the expected outcome.                       |
| Worker timeout                             | One retry; then mark failed.                                        |

The Founder Console exposes `POST /workers/{id}/retry` for
operator-initiated retries. The retry records an audit row with
`action: worker_retry`, `risk: low`.

## Eval gate dependency

Workers that produce drafts (Distribution Operator, Content
Strategist, Offer Architect, etc.) check the latest row of
`evals/eval_status.csv` before starting. If any blocking suite has
`fail > 0`, the worker is skipped and the founder is notified via the
brief.

## Failure escalation

| Failure type                                       | Escalation                                                            |
| -------------------------------------------------- | --------------------------------------------------------------------- |
| Single failure                                     | Logged in `runtime/worker_state.csv`; no escalation.                  |
| Three consecutive failures on same worker          | Trust flag opened at `severity: medium`; founder brief mentions.      |
| Five consecutive failures                           | Trust flag at `high`; Incident Response Agent opens an incident.     |
| Write rejection                                    | Trust flag at `high` immediately; kill switch candidate.              |
| Concurrent writer detection                         | Trust flag at `critical`; orchestrator pauses both workers.          |

## Founder Console exposure

| Endpoint                            | Purpose                                  |
| ----------------------------------- | ---------------------------------------- |
| `GET /workers/health`               | List workers and their last state.       |
| `POST /workers/{id}/retry`          | Manual retry. Audit recorded.            |
| `POST /control/agents/{id}/disable` | Flip the kill switch.                    |
| `POST /control/agents/{id}/enable`  | Restore.                                 |

## Boot sequence

On orchestrator boot:

1. Load `registries/agent_registry.yaml`.
2. Load `runtime/worker_state.csv`. Recover statuses.
3. For each worker whose `status == running` at boot, mark `failed`
   (the previous instance crashed mid-run).
4. Read `policies/dealix_control_policy.yaml` so the policy adapter
   is warmed.
5. Begin the schedule loop.

## Shutdown sequence

1. Mark all `running` workers as `failed` if they cannot drain in the
   grace window.
2. Persist the final state file.
3. Exit.

## Discipline

1. The orchestrator is the only writer of `runtime/worker_state.csv`.
2. Workers do not bypass the orchestrator.
3. Kill switches are honored before scheduling, not after.
4. Eval gate red means drafts pause.
5. Every state transition is observable; every failure has an owner.

## Cross-references

- `ULTIMATE_WORKER_MESH.md` for the full mesh diagram.
- `PRIVATE_OPS_RUNTIME_CONTRACT.md` for write-target ownership.
- `EVAL_GATE_V1.md` for the eval gate dependency.
- `AUDIT_EVENT_MODEL.md` for the action vocabulary.
