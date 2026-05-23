# Ultimate Worker Mesh

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust · Focused on Results.

The worker mesh is the topology of all agents, workers, and queues
in Dealix. It is intentionally narrow: a small number of explicit
workers, each writing to a single directory, all under the orchestrator,
all coordinated through CSV queues. There is no event bus, no
side-channel, no shared mutable state outside the runtime tree.

## Mesh diagram

```
                            ┌─────────────────────────────┐
                            │     Founder Console          │
                            │  /api/v1/internal/*          │
                            │  (auth: x-dealix-internal-token) │
                            └──────────────┬──────────────┘
                                           │
                                           │ reads/writes
                                           ▼
            ┌────────────────────────── trust/approval_decisions.csv ──┐
            │                                                          │
            │   (append-only audit ledger; single canonical record)    │
            │                                                          │
            └────────────────▲──────────────────────────────────────┬──┘
                             │ audit emit                            │
                             │                                       │ scheduling
                ┌────────────┴─────────────┐    ┌───────────────────▼─────────────────┐
                │  Worker Orchestrator     │    │  runtime/worker_state.csv            │
                │  (state machine, kill    │◄───┤  (one writer: orchestrator)          │
                │   switches, retries)     │    └───────────────────▲─────────────────┘
                └──────┬───────────────────┘                        │
                       │ schedules                                  │ state reads
                       │                                            │
       ┌───────────────┴─────────────────────────────┐              │
       │                                             │              │
   ┌───▼────┐ ┌─────────┐ ┌────────┐ ┌─────────┐ ┌─▼────────┐ ┌───────────┐
   │ CEO    │ │ Brand   │ │ Growth │ │ Distrib │ │ Content  │ │ Offer     │
   │ Copilot│ │ Guardian│ │ Strat  │ │ Operator│ │ Strategy │ │ Architect │
   └───┬────┘ └───┬─────┘ └────┬───┘ └────┬────┘ └────┬─────┘ └────┬──────┘
       │           │           │          │            │            │
       │ founder/  │ brand/    │ growth/  │ outreach/  │ marketing/ │ product/
       ▼           ▼           ▼          ▼            ▼            ▼
   founder/   brand/        growth/    outreach/    marketing/  product/
   *.md       *.csv         *.csv      *.csv        *.csv       *.csv

   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
   │Perf      │ │ Trust    │ │ Eval     │ │ Finance  │ │ Delivery │ │ Security │
   │Analyst   │ │ Guardian │ │ Guardian │ │ Copilot  │ │ Copilot  │ │ Guardian │
   └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
        │             │            │             │            │            │
        │ distrib/    │ trust/     │ evals/      │ finance/   │ sales/     │ security/
        ▼             ▼            ▼             ▼            ▼            ▼
   distrib/      trust/        evals/        finance/      sales/       security/
   *.csv         *.csv          *.csv          *.csv         *.csv        *.csv

   ┌────────────────┐ ┌───────────────┐ ┌────────────────────────────┐
   │ Productization │ │ Partner Rev   │ │ Proof Safety / Incident Resp│
   │ Agent          │ │ Agent         │ │                            │
   └──────┬─────────┘ └──────┬────────┘ └──────────────┬─────────────┘
          │                  │                          │
          │ product/          │ customer_success/       │ proof/, trust/
          ▼                  ▼                          ▼
       product/         customer_success/          proof/, trust/
       *.csv            *.csv                       *.csv
```

The arrows are write paths. Read paths are unrestricted within the
runtime tree.

## Mesh principles

1. **Single writer per file.** Each CSV has exactly one sanctioned
   writer (an agent or the Founder Console router). This eliminates
   write conflicts at the file system level.
2. **CSV-mediated communication.** Workers do not call each other.
   They write to a queue file; another worker reads it.
3. **Audit is the spine.** Every state-changing operation produces a
   row in `trust/approval_decisions.csv`. The audit ledger is the
   only mandatory cross-cutting write.
4. **Orchestrator is the metronome.** The orchestrator schedules,
   tracks state, and enforces kill switches. No other component
   schedules.
5. **Founder Console is the only mutation surface.** Workers may
   write to their assigned directory, but state-changing operations
   that escalate or approve flow through the console.

## Failure isolation

| Failure                                           | Blast radius                                                                  |
| ------------------------------------------------- | ----------------------------------------------------------------------------- |
| One worker fails                                  | Only its assigned files are affected. Other workers continue.                  |
| Orchestrator crashes                              | Workers stop scheduling but in-flight runs finish; on restart, in-flight runs are marked `failed`. |
| Runtime directory unavailable                     | Workers cannot run; Founder Console reads return `data_source: "no-runtime"`. |
| Postgres outage                                   | Business endpoints fail; operating endpoints continue.                         |
| Eval gate red                                     | Drafts pause; non-draft workers continue.                                      |
| Agent disabled                                    | Only that agent's workers stop.                                                |
| Suppression list missing                          | Distribution Operator stops queueing (fail-closed).                            |
| Policy file missing                               | Policy evaluator denies all guarded actions by default.                        |

The mesh's small surface and explicit ownership make these failure
modes diagnosable in minutes, not hours.

## Retry policy

Detailed in `WORKER_ORCHESTRATOR_V1.md`. Summary:

- Transient I/O: exponential backoff, max 3 retries.
- Schema drift: no retry; DQ system notified.
- Eval gate red: skip until green.
- Policy denial: no retry.
- Worker timeout: one retry.

## Kill switches

Every agent in `registries/agent_registry.yaml` carries
`kill_switch: true`. Kill switches are:

1. **Per-agent.** Flipping a kill switch disables every worker the
   agent owns.
2. **Recorded.** The flip is audit-emitted with
   `action: agent_disable` or `agent_enable`.
3. **Reversible.** The founder can re-enable via the Founder Console.
4. **Honored on next schedule.** The orchestrator reads agent state
   before each worker dispatch.

The Founder Console endpoints:

- `POST /api/v1/internal/control/agents/{id}/disable`
- `POST /api/v1/internal/control/agents/{id}/enable`

## Eval gate as a global stop

If `evals/eval_status.csv` shows a blocking suite failure on its
most recent row, draft-producing workers pause until the next pass
is green. Non-draft workers (scorecard refresh, snapshot writers)
continue. The orchestrator surfaces this as a single state in the
founder brief.

## Trust flag as a soft brake

Trust flags are advisory. Workers continue to run, but the founder
brief surfaces flags at `severity >= medium`. A flag at `severity:
critical` is treated as an incident; the Incident Response Agent
opens a row in `trust/incidents.csv`, and the orchestrator considers
the incident when deciding whether to schedule.

## Capacity and concurrency

The mesh is intentionally low-concurrency:

| Worker class                  | Concurrency  |
| ----------------------------- | ------------ |
| Snapshot workers              | 1 per worker |
| Draft-producing workers       | 1 per worker |
| Audit-writing actions          | 1 globally   |
| Scorecard refresh              | 1 globally   |

This avoids the need for distributed locking on the CSV tier.

## Observability

| Surface                              | Purpose                                  |
| ------------------------------------ | ---------------------------------------- |
| `runtime/worker_state.csv`            | Per-worker state.                        |
| `trust/approval_decisions.csv`        | Audit of state changes.                  |
| `trust/trust_flags.csv`               | Active trust concerns.                   |
| `evals/eval_status.csv`               | Eval gate state.                         |
| `data/dq_score.csv`                   | Data quality posture.                    |
| Founder Console (`/workers/health`)    | Aggregated worker view.                  |

The four-pillar scorecard pulls from these sources and produces the
founder's daily view.

## Discipline

1. The mesh is small and explicit.
2. Workers do not call each other.
3. Audit is the spine.
4. The orchestrator is the metronome.
5. The Founder Console is the only mutation surface.
6. Failure isolation is a property of the topology, not a hope.
