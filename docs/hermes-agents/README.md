# Hermes Agents Layer

## Purpose
Hermes Agents is the Dealix operating layer for founder support agents.

It defines agents for strategy, GTM, customer success, AI governance, security, reliability, finance, and board preparation.

## Current agents

| Agent | Mission | Owner | Risk |
|---|---|---|---|
| Founder Chief of Staff | Priorities, blockers, decisions, weekly outcomes | Founder | Medium |
| GTM Intelligence | ICP research, account context, proof gaps | GTM Lead | Medium |
| Customer Success | Health, onboarding, proof, risk | CS Lead | Medium |
| AI Governance | AI workflow review and evaluation checks | AI/Product Lead | High |
| Security and Reliability | Readiness, incidents, reliability risks | Engineering Lead | High |
| Finance and Board | Runway notes and executive memo drafts | Founder | Medium |

## CLI

List agents:

```bash
hermes-agents list-agents
```

List agents as JSON:

```bash
hermes-agents list-agents --json
```

Run governance check:

```bash
hermes-agents check
```

## Operating rules

- Every agent has an owner.
- Every agent has a mission.
- Every agent has allowed and blocked actions.
- High-risk agents require review.
- Every agent has an escalation path.
- Every agent has success metrics.

## Related files

- `hermes_agents/registry.py`
- `hermes_agents/policy.py`
- `hermes_agents/cli.py`
- `docs/hermes-agents/01-agent-charters.md`
- `docs/hermes-agents/02-governance-and-controls.md`
- `docs/hermes-agents/03-operations-cadence.md`
- `docs/hermes-agents/04-escalation-matrix.md`
