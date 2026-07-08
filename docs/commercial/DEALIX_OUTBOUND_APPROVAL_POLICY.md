# Dealix Outbound Approval Policy

The Launch Conversation & Negotiation Engine is **draft-only** and
**approval-first**. This policy defines what the engine may do automatically and
what always requires explicit founder approval.

## Always allowed (automatic, internal)

- Read the repo and data files.
- Score targets and match offers.
- Generate email / WhatsApp / LinkedIn / call **drafts**.
- Build objection responses, negotiation plans, and proof packs.
- Write reports and CSVs to `reports/dealix_conversation_negotiation/`.
- Build the approval queue and follow-up queue as **pending** items.

## Never without explicit founder approval

- Sending any email, WhatsApp, LinkedIn message, or SMS.
- Placing a call or booking a meeting.
- Issuing a proposal, invoice, or capturing payment.
- Merging a PR, changing production, or rotating secrets.
- Enabling any live outbound channel.
- Claiming unproven results or inventing clients / revenue.
- Cold WhatsApp, mass blast, LinkedIn scraping/automation.
- Any government-access claim.

## Approval queue item

Every external action becomes an item in `approval_queue.csv` / `latest.json`:

```json
{
  "id": "APP-0001",
  "target_company": "…",
  "contact_name": "…",
  "channel": "email | whatsapp | linkedin | call",
  "draft": "…",
  "reason": "…",
  "risk": "low | medium | high | blocked",
  "proof_attached": "proof_pack",
  "decision_options": ["approve", "revise", "reject", "hold"],
  "approval_required": true,
  "status": "pending_founder_approval"
}
```

The founder chooses **approve / revise / reject / hold** and only then sends the
approved draft manually.

## Safety guard

If any of these environment flags are truthy, the engine halts with
`BLOCKED_BY_SAFETY_GUARD` and produces no drafts:

```
EXTERNAL_SEND_ENABLED, EMAIL_SEND_ENABLED, WHATSAPP_SEND_ENABLED,
WHATSAPP_ALLOW_LIVE_SEND, SMS_SEND_ENABLED, AUTO_WHATSAPP_ENABLED,
AUTO_EMAIL_ENABLED, AUTO_LINKEDIN_ENABLED, AUTO_PAYMENT_CAPTURE_ENABLED,
AUTO_MERGE_ENABLED, PRODUCTION_MUTATION_ENABLED
```

`OUTBOUND_MODE` must remain `draft_only`.

## Canonical founder identity

- Founder: **Sami Assiri**
- Only approved email: **sami.assiri11@gmail.com** (enforced in code)

No other email address is used in any draft, regardless of what appears in
contacts, history, or data files.
