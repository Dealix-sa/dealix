# Agent Handoffs

## Why Handoffs Matter

Most failures are not in the agent — they are in the seam between two
agents, or between an agent and a human. We define handoffs explicitly.

## Standard Handoff Shape

Every handoff has:
- A typed payload (input schema).
- A receiving party (next agent or named human).
- A handoff log entry with timestamp.
- A failure path (where the work goes if the receiver rejects it).

## Core Handoff Flows

### Sales Flow

```
Lead Finder ─► Scoring Agent ─► Message Agent ─► [A1/A2 human review] ─► Send
                                       │
                                       └─► Trust Guard (parallel)
```

### Proposal Flow

```
Founder call ─► Proposal Agent ─► [A2 founder approval] ─► Trust Guard ─► Send ─► Proof library
```

### Delivery Flow

```
Intake ─► Research ─► Score ─► Draft ─► Delivery QA Agent ─► [A1 founder QA] ─► Client
```

### Learning Flow

```
Logs ─► Learning Agent ─► Recommendation queue ─► [A1 founder review] ─► EXPERIMENT_LOG / DECISION_LOG
```

## Handoff Rules

1. No silent drops. If an agent cannot accept a payload, it returns a typed rejection.
2. No verbal handoffs. Every transition lives in a ledger.
3. Trust Guard runs on every external-bound artifact, in parallel where possible to keep latency low.
4. Human handoffs use the standard approval form in `docs/trust/HUMAN_APPROVAL_POLICY.md`.

## Failure Paths

| Failure | Action |
|---|---|
| Schema mismatch | Reject, log, alert system owner |
| Trust Guard flag | Block send, escalate to A2/A3 |
| Human approval timeout | Item stays in queue, no auto-send |
| Eval below floor | Demote agent, route to higher human level |
