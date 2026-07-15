# Commercial Universe Wave B — Approval Queue Adapter

Wave A classifies tenant-scoped commercial accounts and produces an
approval envelope. Wave B connects that envelope to the existing canonical
Approval Command Center schema.

## Product value

Every department can work from the same commercial universe:

- sales and customer-success opportunities
- strategic, referral, channel, implementation, technology, and co-marketing partners
- service exchange and market-access relationships
- B2G-readiness and investor conversations

The adapter turns each internal opportunity into one reviewable card with
tenant scope, relationship, risk, proof target, and audit reference.

## Safety contract

This is an internal decision surface, not an outbound engine:

1. Research-only or unknown permission becomes a terminal blocked queue item.
2. Warm, inbound, referral, opted-in, or explicitly approved permission becomes
   pending with approval_required.
3. No sender, scheduler, CRM mutation, payment, scraping, or external API call
   is introduced.
4. The adapter reuses auto_client_acquisition.approval_center.schemas.ApprovalRequest;
   it does not create a second approval queue.
5. customer_id preserves tenant isolation and audit_ref links the item back to
   the source record.

## Integration contract

Call to_approval_request(account, envelope) after the pure Wave A classifier
has created an ApprovalEnvelope. The resulting request is compatible with the
existing Approval Command Center store and canonical action taxonomy.

The canonical action is preserved when already valid. Otherwise the adapter
maps partner relationships to partner_intro, LinkedIn channels to
draft_linkedin_manual, email channels to draft_email, and internal work to
follow_up_task.

## Next waves

- Wave C: persist the universe in the existing tenant-scoped database models.
- Wave D: build department workspaces and meeting-preparation views.
- Wave E: compose a daily command center from the canonical approval queue,
  proof ledger, and revenue spine.
- Wave F: allow only explicitly approved, auditable external execution paths.
