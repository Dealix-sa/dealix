# Agents

## Purpose
Define the AI agents Dealix operates, what each one is allowed to do, and how its work is verified.

## Owner
Sami / Trust + Product owners.

## Review Cadence
Monthly, plus after any incident or capability change.

## Inputs
- Agent specifications (model, scope, tools, data access).
- Trust OS Approval Matrix and Autonomy Policy.
- Logs of agent actions.
- Incident reports.
- Customer-facing outputs produced with agent assistance.

## Outputs
- Agent inventory (purpose, owner, autonomy level, allowed tools).
- Per-agent guardrails and approval class.
- Test and evaluation results.
- Risks logged and resolved.

## Rules
- Every agent maps to an autonomy level (L0-L3); no agent runs at L4-prohibited actions.
- Every external commitment produced by an agent requires A1+ human review before send.
- A3 actions can never be executed by an agent.
- Agent inventory, prompts, and tool access are versioned in the repo; secrets live in the secret store, not in prompts.

## Metrics
- Number of agents in production.
- Agent-driven actions per week, by autonomy level.
- Incidents per agent per quarter.
- Human override rate per agent.

## Evidence
- agent inventory file(s) in this folder.
- trust/approval_log.csv entries tied to agent actions.
- evaluation suites and test results.
- incident response logs.

## Last Reviewed
YYYY-MM-DD
