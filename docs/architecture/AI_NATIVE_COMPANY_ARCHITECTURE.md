# AI-Native Company Architecture

> Define how AI supports Dealix without taking uncontrolled external
> action.

## Purpose

Make the architecture of AI inside Dealix unambiguous: where AI lives,
what data it sees, what tools it may invoke, what review it must pass,
and how its actions become real.

This is the single picture every new agent, every new tool, and every
new approval surface must fit into.

## High-Level Flow

```
User  /  Worker  /  Agent  Request
            │
            ▼
   ┌────────────────────┐
   │  Context Boundary  │   what data the AI may see
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │ Tool Permission    │   which tools the AI may use
   │ Check              │
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │     AI Agent       │   scoped, model-pinned, prompt-pinned
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │  Output Contract   │   JSON schema validated, fail-closed
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │  Trust Guardian    │   adversarial + content + claim review
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │  Policy Evaluator  │   deterministic YAML rules
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │  Approval Queue    │   founder decision (A2/A3)
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │     Audit Log      │   what was proposed, decided, executed
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │  Worker Execution  │   the only thing that touches the world
   └────────┬───────────┘
            ▼
   ┌────────────────────┐
   │   Observability    │   metrics, costs, eval health
   └────────────────────┘
```

## Context Boundary

The context boundary defines, for a given AI call:

- **What data is visible.** Redacted snapshots only. PII, secrets, and
  internal metrics are filtered out unless the agent declares a
  legitimate need *and* the data class is in its scope.
- **What tools are reachable.** Tools are configured per agent; the
  agent cannot discover or invoke a tool it was not granted.
- **What action class can be requested.** An A1-only agent cannot
  produce an A2 request, even if asked.
- **What outputs must be reviewed.** Every output goes through Trust
  Guardian unless explicitly classified read-only / internal.

## Tool Permission Levels

| Level | Capability | Examples | Default reviewer |
|-------|------------|----------|------------------|
| T0 | No tools | Pure text generation against frozen context | A1 internal |
| T1 | Read-only internal data | Read `lead_intelligence`, `worker_state` | A1 |
| T2 | Draft generation | Produce text/JSON to be reviewed | A1/A2 |
| T3 | Internal write to queues | Write to `outreach_queue`, `proposal_queue` | A2 (always) |
| T4 | External action request | Ask a worker to send / publish | A2 (always) + Trust Guardian + Policy |
| T5 | Never automatic | Contracts, refunds, public proof, pricing changes | A3 — founder click only |

Every agent declares its highest tool level in config. Attempts to
escalate at runtime are blocked and logged as a security event.

## Output Contracts

Every agent has a JSON schema for its output. We treat schema failures
as fatal: the output is discarded, an `agent.output_contract_violation`
audit event is written, and the agent is rate-limited until a human
reviews.

## Trust Plane Composition

Trust runs in two stages:

1. **Policy Evaluator** — deterministic, fast, YAML-driven. Catches
   suppression, A3 lockout, evidence requirements, pricing matrix
   limits.
2. **Trust Guardian** — model-based judgment. Catches injection,
   overclaim, unsupported claims, sensitive data leakage.

Stricter wins. If either says deny, the action is denied. If either
cannot run, the Trust Plane fails closed.

## Approval Queue

The Approval Queue is the **only** path from "agent wants to do X" to
"X happens". Founder approves explicitly, with the evidence and risk
classification visible. A2 actions require one click; A3 actions
require manual execution by the founder, never the worker.

## Audit Log

Append-only `audit_events` table. Every step above writes at least
one event. Audit IDs are stable and quoted in `/ceo`, `/approvals`,
`/trust`, and `/workers`.

## Worker Execution

Workers are the **only** components allowed to touch the world: send
email, post a message, capture a payment, publish a file. They drain
queues that have been approved upstream. They never originate an
action.

## Observability

Every layer emits structured events to the observability pipeline.
Metrics we track per layer:

- **Boundary:** rejections, escalations.
- **Tool Permission:** denied tool calls, level-up attempts.
- **Agent:** invocations, p95 latency, token cost, eval score.
- **Output Contract:** violations.
- **Trust Guardian:** allow / deny / escalate rates, top reason codes.
- **Policy:** rule fire counts.
- **Approval Queue:** queue depth, time-to-decision, override rate.
- **Worker:** runs, failures, retry counts.

## Rule

> AI can **propose** actions. Dealix decides through **policy, approval,
> and audit**.

There is no path from agent intent to customer impact that bypasses the
queue and the log.

## See Also

- [`DEALIX_OPERATING_LAYER_V1`](../ops/DEALIX_OPERATING_LAYER_V1.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
- [`TRUST_GUARDIAN_AGENT`](../ai/TRUST_GUARDIAN_AGENT.md)
- [`WORKER_ORCHESTRATOR_V1`](../runtime/WORKER_ORCHESTRATOR_V1.md)
- [`EVAL_RED_TEAM_SYSTEM`](../ai/EVAL_RED_TEAM_SYSTEM.md)
