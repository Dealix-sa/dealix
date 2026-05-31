# Hermes Governance and Controls

## Purpose
Keep Hermes agents useful, accountable, and safe.

## Control principles

- Agents assist owners; owners remain accountable.
- High-risk work requires review.
- Every output needs a source or context trail.
- Every agent has allowed and blocked actions.
- Every agent has an escalation path.
- Every incident creates a follow-up record.

## Control matrix

| Control | Required for | Owner |
|---|---|---|
| Agent registry | All agents | Founder/Ops |
| Human review | Medium and high-risk outputs | Workstream owner |
| Evaluation | AI workflow outputs | AI/Product |
| Incident record | Security, reliability, customer, or AI incidents | Ops/Security |
| Decision record | Strategic or irreversible choices | Founder |
| Source trail | Research, claims, proof, and summaries | Agent owner |
| Access review | Tools and integrations | Engineering/Security |

## Risk levels

| Level | Meaning | Review |
|---|---|---|
| Low | Internal summary, low impact | Owner review |
| Medium | Business workflow or customer context | Workstream owner review |
| High | Security, AI governance, finance, or customer trust | Founder plus owner review |
| Critical | Material customer, legal, security, or production impact | Formal review before use |

## Required logs

Each agent run should record:

- Agent ID
- Owner
- Timestamp
- Inputs used
- Output created
- Review status
- Escalation needed
- Follow-up issue if needed

## Blocked patterns

Agents should not:

- Override owner decisions.
- Create unsupported public claims.
- Treat uncertain data as fact.
- Use sensitive data without documented purpose.
- Make high-risk recommendations without review.

## Monthly governance review

- Active agents
- Agents without owners
- High-risk outputs
- Incidents and follow-ups
- Tool usage and cost
- Prompt or workflow drift
- Retired agents
