# Enterprise Proposal Flow

The path a proposal takes from "valid champion" to "signed". Every step has
a named output, an owner, and a date.

## The flow

```
1. Draft prepared           — owner: ceo / proposal operator
   Input: discovery notes, STAKEHOLDER_MAP, PROCUREMENT_READINESS check
   Output: docs/commercial/operations/proposals/<account>/draft.md

2. Internal review           — owner: ceo
   Walk: DEAL_DESK_SYSTEM checklist
   Output: approval / change request appended to docs/founder/DECISION_LOG_SYSTEM.md

3. Approval queued           — through auto_client_acquisition.approval_center
   Output: approval row, sent only after explicit approval

4. Sent to champion          — owner: ceo / proposal operator
   Output: timestamped event in proof ledger

5. Champion review           — buyer-side; track in close plan
   Output: revision requests

6. Final draft               — owner: ceo
   Output: signed-ready PDF + DOCX

7. Procurement / legal       — PROCUREMENT_READINESS gate
   Output: signed MSA, signed SOW

8. Signature                 — formal close
   Output: contract artefact, proof ledger event, capital ledger entry
```

## Inputs to a proposal draft

- [STAKEHOLDER_MAP](STAKEHOLDER_MAP.md) — to address by role
- [`docs/revenue/PRICING_AND_PACKAGING.md`](../revenue/PRICING_AND_PACKAGING.md) — pricing source
- [`docs/revenue/CLOSE_PLAN_TEMPLATE.md`](../revenue/CLOSE_PLAN_TEMPLATE.md) — mutual plan
- [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — what we will not commit to

## Cross-references

- [ENTERPRISE_SALES_MOTION](ENTERPRISE_SALES_MOTION.md)
- [DEAL_DESK_SYSTEM](../revenue/DEAL_DESK_SYSTEM.md)
- [CLOSE_PLAN_TEMPLATE](../revenue/CLOSE_PLAN_TEMPLATE.md)
- [PROCUREMENT_READINESS](PROCUREMENT_READINESS.md)
- [SECURITY_REVIEW_PACKET](SECURITY_REVIEW_PACKET.md)

## Non-negotiables

Proposals never include language outside the [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md)
list. Pricing only references the live PRICING_AND_PACKAGING. All sends
flow through the approval center.
