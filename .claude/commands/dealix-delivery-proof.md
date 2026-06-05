---
description: Run or scaffold a paid Command Sprint delivery and assemble its Proof Pack
---

# /dealix-delivery-proof

Drive the delivery + proof layer (PR 6 scope).

## Source of truth
- "Delivery Map" in the blueprint and the `customers/_template/` factory.

## Non-negotiables enforced here
- No project without a Proof Pack.
- No project without a Capital Asset entry.
- No external send without human approval.
- Every artifact records: source, analysis, assumption, confidence, recommendation,
  approval_required, next_action, owner, due_date.

## When invoked
1. If scaffolding: create/extend `customers/_template/` (00_intake → 11_upsell_recommendation).
2. If delivering a real customer: copy the template to `customers/<slug>/`, never invent customer data,
   and walk the day-by-day delivery with approval checkpoints.
3. End by assembling `10_proof_pack.md` and flagging the upsell path.
