# Dealix Operating Layer v1

> The layer that turns Dealix from a set of systems into a measurable,
> trust-gated, founder-controlled operating company.

## Purpose

Turn Dealix from a collection of dashboards, agents, and scripts into a
single coherent operating company:

- Every system has an owner.
- Every action has a trust class.
- Every worker has a health signal.
- Every decision is auditable.
- Every CEO move is visible as a *next best action*, not a click.

This layer sits **on top of Founder Console v5** and **under** every AI
agent, worker, and external action. Nothing should reach a customer
without passing through it.

## Core Rule

> No system is real until it has all eight of the following.

| # | Requirement | Question it answers |
|---|-------------|---------------------|
| 1 | Source of truth | Where does the data live? |
| 2 | Runtime owner | Who runs it? |
| 3 | Health check | How do I know it's alive? |
| 4 | Audit trail | What did it do, when, why? |
| 5 | Trust class | A1 / A2 / A3? |
| 6 | Failure mode | What does broken look like? |
| 7 | Recovery path | How do we get back? |
| 8 | CEO-visible status | Where does it show up in `/ceo`? |

If a system cannot answer all eight, it is **not in production** — it is
a prototype. Prototypes never touch customers.

## The Seven Operating Layers

### 1. Founder Control Layer

The surfaces the founder uses to run the company every day.

- `/ceo` — daily top action, funnel, cash, blockers.
- `/approvals` — A2/A3 queue, decisions, evidence.
- `/sales-cockpit` — bottleneck of the week.
- `/workers` — worker health, last run, failures.
- `/trust` — open trust flags, policy hits, suppressions.
- `/finance` — cash position, payment capture, retainer pipeline.

**Owner:** Founder.
**Rule:** Every other layer must feed at least one of these surfaces.

### 2. Revenue Runtime Layer

The path a unit of revenue actually walks through Dealix:

```
lead intelligence
  → outreach approval
  → sent / draft
  → reply
  → sample
  → proposal
  → payment capture
  → delivery
  → retention
  → proof
```

**Owner:** Sales OS + Approval Worker.
**Rule:** A lead cannot skip a stage. Every transition is audited.

### 3. Trust Layer

The plane that decides whether an action may proceed.

- Approval class (A1/A2/A3).
- Evidence requirement.
- Suppression check (PDPL + DNC + bounce + opt-out).
- No-overclaim scan (revenue guarantees, fabricated metrics, fake
  logos).
- Audit log emission.
- Never-auto-execute for A3.

**Owner:** Policy-as-Code + Trust Guardian Agent.
**Rule:** Trust Layer fails closed. If the evaluator cannot run, no
external action proceeds.

### 4. Worker Layer

The recurring jobs that move Dealix forward without manual prompts.

Required workers for v1:

- `lead_scoring_worker`
- `approval_queue_worker`
- `follow_up_queue_worker`
- `sales_cockpit_summary_worker`
- `finance_summary_worker`
- `trust_flag_worker`
- `worker_health_worker`
- `ceo_summary_worker`

**Owner:** Worker Orchestrator (see
[`WORKER_ORCHESTRATOR_V1`](../runtime/WORKER_ORCHESTRATOR_V1.md)).
**Rule:** A worker without a health check, retry policy, and disable
switch is not a worker — it is a script.

### 5. Data Layer

The single source of truth for runtime state.

- **v0 (now):** CSV bootstrap in `data/` (good enough to start).
- **v1 (next):** Postgres primary for the eight runtime tables that
  power founder surfaces.
- **v2 (later):** Event sourcing on top of Postgres for full replay.

See [`POSTGRES_PRIMARY_MODE`](../data/POSTGRES_PRIMARY_MODE.md).

**Rule:** CSV is for export. Postgres is for runtime. Never the other
way around.

### 6. AI Governance Layer

Every AI agent must declare and respect:

- **Scope:** what task and which data it touches.
- **Tools:** which permission level it may invoke (T0–T5).
- **Inputs:** what data class it may read.
- **Output contract:** structured, validatable, and reviewed.
- **Evals:** quality + safety + injection resistance.
- **Red team suite:** what it has been shown to refuse.
- **Kill switch:** how to disable it without redeploy.

See [`AI_NATIVE_COMPANY_ARCHITECTURE`](../architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md)
and [`EVAL_RED_TEAM_SYSTEM`](../ai/EVAL_RED_TEAM_SYSTEM.md).

### 7. Observability Layer

What we measure to know Dealix is healthy:

- **Business KPIs:** approved outreach/day, replies/day, samples/week,
  proposals/week, paid/month, cash, retainer count.
- **Worker health:** last run, failures in 24h, queue depth, p95
  runtime.
- **DORA-style delivery metrics:** change lead time, deployment
  frequency, change fail rate, time to restore.
- **AI quality:** eval pass rate, red-team pass rate, hallucination
  rate per agent.
- **Trust incidents:** suppression hits, overclaim blocks, prompt
  injection attempts.

**Rule:** A KPI without an owner and a target is decoration. Remove it.

## Cross-Layer Promotion Rule

> Autonomy increases only when **trust, audit, and recovery** are
> *stronger* than manual operation.

This is the only rule that gates moving an action from A3 → A2, or A2 →
A1. We do not promote because something "works". We promote because we
can prove it would fail safely.

## What v1 Locks In

By the time Operating Layer v1 is live:

- `/ceo` shows a real, computed top action.
- `/approvals` decisions flow through Policy-as-Code.
- `/workers` reflects real worker state, not mocked data.
- `/trust` flags are emitted by the Trust Guardian Agent.
- Every external-impact action passes a policy file, a Trust Guardian
  review, and an audit write.
- Postgres is the source of truth for the runtime tables.
- The next-stage verifier (`make next-stage`) is green in CI.

Anything beyond this (Eval/Red Team automation, AI Unit Economics
dashboards, Productization OS) is layered on top of this base — never
underneath it.

## See Also

- [`CEO_COPILOT_SYSTEM`](../ai/CEO_COPILOT_SYSTEM.md)
- [`TRUST_GUARDIAN_AGENT`](../ai/TRUST_GUARDIAN_AGENT.md)
- [`REVENUE_AGENT_SWARM`](../ai/REVENUE_AGENT_SWARM.md)
- [`EVAL_RED_TEAM_SYSTEM`](../ai/EVAL_RED_TEAM_SYSTEM.md)
- [`POLICY_AS_CODE_SYSTEM`](../trust/POLICY_AS_CODE_SYSTEM.md)
- [`WORKER_ORCHESTRATOR_V1`](../runtime/WORKER_ORCHESTRATOR_V1.md)
- [`AI_NATIVE_COMPANY_ARCHITECTURE`](../architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md)
- [`POSTGRES_PRIMARY_MODE`](../data/POSTGRES_PRIMARY_MODE.md)
- [`AI_UNIT_ECONOMICS_SYSTEM`](../finance/AI_UNIT_ECONOMICS_SYSTEM.md)
- `policies/founder_console_policy.yaml`
