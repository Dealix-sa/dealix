# Delivery Control System

> Delivery turns sales into proof.

## Inputs

- Signed scope.
- Customer ICP definition.
- Customer signal preferences.
- Source data / lead universe access.

## Outputs

- Signed-off Proof Pack.
- Approved outreach pack.
- Customer feedback captured.
- Retainer ask logged.

## Rules

1. No delivery starts without payment / PO / signed scope.
2. Every A-priority lead has linked evidence.
3. No duplicate leads (dedupe stage runs before outreach pack).
4. No overclaim language in any customer-facing artifact.
5. Customer data is private and stays in customer-scoped workspace.
6. Scope is fixed at intake; mid-sprint scope changes require a written
   change order.

## Metrics

- Sprint cycle time (intake → handoff)
- QA fail rate (first pass / final pass)
- Founder edits per memo (lower = better)
- Customer feedback score
- Retainer conversion within 30 days of handoff
- Friction-log entries per Sprint

## Evidence

- `dealix-ops-private/delivery/sprint_register.csv`
- `dealix-ops-private/delivery/reports/<sprint_id>/`
- `dealix-ops-private/delivery/qa/<sprint_id>/`
- `dealix-ops-private/delivery/handoffs/<sprint_id>/`

## Verifier

- `make audit` runs the QA checklist against the most recent Sprint.
- Capital asset registry incremented at handoff signature.
- Retainer ask logged within 7 days of handoff.

## Review

- Weekly: open Sprint status.
- Monthly: cycle-time and QA-fail trend.
- Quarterly: stage-level overrun analysis.
