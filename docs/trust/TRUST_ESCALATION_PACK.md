# Trust Escalation Pack

## Purpose
Handle risky claims, data exposure, unsafe automation, and external commitments.

## Trigger
Use when:
- a claim may be unsupported
- client data may be exposed
- proposal has unusual terms
- agent output is risky
- A2/A3 action appears

## Actions
1. Classify action A0/A1/A2/A3.
2. If A3, block.
3. If A2, require explicit approval.
4. Rewrite risky language.
5. Log decision.
6. Add checklist or policy update if repeated.

## Metrics
- blocked A3 actions
- approvals pending
- incidents
- risky claims rewritten

## Evidence
- approval_log.csv
- incident log
- updated policy
