# Human Approval Matrix

> **Status:** Operating policy. Every external action requires a human approval.
> **Schema:** `schemas/launch/approval_item.schema.json` + `templates/launch/approval_queue.example.json`.

## The principle

> AI drafts and recommends. Humans approve. The human is the founder (or the founder's delegate).

## The 5 categories of action

### A. Read-only (no approval needed)

- Reading data from CRM, WhatsApp, email, files.
- Classifying content.
- Summarizing.
- Generating reports.
- Building drafts.

### B. Internal write (light approval)

- Updating a draft in the approval queue.
- Saving a note in the founder command room.
- Writing to internal logs.
- Generating a JSON for the founder's review.

These do not leave the system. They are visible only inside Dealix.

### C. External draft (medium approval)

- Drafting an email.
- Drafting a LinkedIn message.
- Drafting a WhatsApp message (after consent).
- Drafting a proposal.
- Drafting a case study.

These go into the approval queue. The founder reviews and approves. Then the founder (not Dealix) sends them.

### D. External action (high approval)

- Sending an email.
- Sending a LinkedIn message.
- Sending a WhatsApp message.
- Sharing a case study publicly.
- Publishing content (LinkedIn post, video, blog).

These require the founder's explicit approval. The trust preflight runs on every draft.

### E. Money action (highest approval)

- Setting a price in a proposal.
- Generating a payment handoff.
- Approving a discount.
- Closing a deal.
- Refunding (if applicable).

These require the founder's signature in the approval queue, with a `pricing_status` field, an `expiry`, and a `discount_pct` (if any).

## The 5 hard rules

1. **No category D action without a category C draft in the approval queue.** The draft must exist first.
2. **No category E action without the founder's signature in the queue.** Pricing is founder-only.
3. **No category C or D action with `evidence_level: L0` in client-facing copy.** L0 is internal only.
4. **No category D action without a `consent_record` for WhatsApp.** Consent is non-negotiable.
5. **No category A, B, C, D, E action that violates the trust preflight.** The preflight is the first gate.

## The approval queue item

```json
{
  "approval_id": "apr_001",
  "action_category": "D",
  "draft_id": "outreach_2024_agency_001",
  "channel": "email",
  "target_account_id": "agency_x_riyadh",
  "drafted_by": "founder",
  "drafted_at_iso": "2024-12-01T10:00:00Z",
  "preflight_status": "PASS",
  "founder_review_status": "pending",
  "evidence_level": "L2",
  "risk_level": "low",
  "approval_required": true,
  "approved_at_iso": null,
  "approved_by": null,
  "send_log": {
    "sent_at_iso": null,
    "channel_response": null
  }
}
```

## The lifecycle

```
drafted → preflight → queue → founder_review → approved → sent → logged
                ↓
              rejected → rewritten → drafted (loop)
```

## The escalation

- The founder can delegate category A, B, C to a delegate. Not D or E.
- The delegate's actions are still logged with the founder's name as the approver.
- Category E (money) is founder-only, no exceptions.

## The audit trail

The approval queue is append-only. To reverse an action, add a new row with `action: reversed`.

## The review cadence

- Daily at 9am: founder reviews the queue.
- Any item pending > 24h gets a reminder.
- Any item rejected 2+ times gets a rewrite assignment.
- Weekly review of the queue: which categories fired most? Which were rejected most?

## When to update

- When a new action category is added.
- When a new channel is added.
- When the founder delegates more (or less).
- When a violation occurs.
