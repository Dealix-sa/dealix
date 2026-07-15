# AI Command Center

## Purpose
Govern Dealix AI agents, prompts, risks, outputs, and human oversight.

## Owner
Sami / AI Governance owner.

## Review Cadence
Weekly for active agents, monthly for inventory.

## Inputs
- agent outputs
- prompts
- eval results
- trust flags
- approval logs
- incidents

## Outputs
- agent approval level
- risk rating
- eval requirement
- blocked action
- prompt update
- safer output

## Rules
- Agents prepare; humans approve critical moves.
- No agent can execute A3.
- External commitments require approval.
- Prompt injection risk must be considered when agents read untrusted input.
- Sensitive information must not be exposed in public outputs.

## Metrics
- agent eval pass rate
- trust flags
- hallucination incidents
- blocked actions
- prompt updates

## Evidence
- AI system inventory
- AI risk register
- eval results
- approval logs
- incident reports

## Last Reviewed
2026-05-23
