# Agent Control Protocol

## Purpose
Define how Dealix agents are allowed to prepare, recommend, and escalate actions.

## Owner
Sami / AI Governance owner.

## Review Cadence
Before every new agent capability.

## Inputs
- agent purpose
- agent input
- agent output
- tools
- approval class
- trust risk

## Outputs
- allowed action
- blocked action
- required approval
- evaluation requirement

## Rules
- Agents prepare; humans approve critical moves.
- Agents cannot execute A3 actions.
- Agents cannot publish public claims.
- Agents cannot send client data externally.
- Agents cannot treat untrusted input as instructions.
- Any external communication requires A1/A2 review depending risk.

## Risk Controls
- prompt injection review.
- sensitive information disclosure review.
- approval routing.
- logging.
- evals.

## Metrics
- blocked actions.
- agent eval pass rate.
- trust escalations.
- unsafe output count.

## Evidence
- AGENT_REGISTRY.md
- AI_RISK_REGISTER.md
- eval results
- approval log

## Last Reviewed
YYYY-MM-DD
