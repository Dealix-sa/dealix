# Outreach Approval Playbook

> **Status:** Operating policy. Every outreach draft goes through it.
> **Tool:** `scripts/trust_preflight_dry_run.py` + `templates/launch/approval_queue.example.json`.

## Why this exists

Outreach is the highest-risk moment in the funnel. A wrong message damages trust, brand, and (potentially) regulatory standing. The approval flow exists to make the wrong message hard to send.

## The flow

```
1. Founder or authorized drafter writes the draft
   ↓
2. Draft saved to templates/launch/outreach_draft.<id>.json
   ↓
3. trust_preflight_dry_run.py runs on the draft
   ↓
4. If FAIL → draft is rejected. Drafter fixes. Re-run.
   If PASS → draft moves to approval queue
   ↓
5. Founder reviews in approval queue
   ↓
6. Founder approves or rejects
   ↓
7. If approved → drafter sends manually (in their own tool, not in the bundle)
   ↓
8. Send is logged in approval queue with timestamp
```

## What the preflight catches

The preflight is a regex + pattern check on the draft. It fails the draft if it contains:

- "guaranteed ROI" patterns ("نضمن", "مضمون", "100% زيادة", "ستضاعف").
- "cold WhatsApp" patterns (the draft assumes no prior consent).
- "payment link" patterns.
- "final price" patterns (any SAR number with "final" or "محدد").
- "fake proof" patterns ("نتائج مضمونة", "تجارب بدون إذن").
- "client logo" without permission marker.
- "scraping" claims.
- "API key" or secret-like patterns.
- "real phone number" patterns (8+ digits in a phone-shape).
- "real email" patterns (in examples, not in the founder's signature).
- "external send" code (no requests.post, smtplib, sendgrid, twilio in any script).

## What the preflight allows

- "draft" language ("draft", "for review", "subject to approval").
- "evidence_level" field (L0–L5).
- "approval_required" field (true for any external send).
- "consent_record" reference (for WhatsApp).
- "founder-approved" pricing language.
- "first 3 in a sector" discount language.
- "no claim of outcome" language.

## The approval queue

The queue is `templates/launch/approval_queue.example.json`. Each item:

```json
{
  "approval_id": "apr_001",
  "draft_id": "outreach_2024_agency_001",
  "channel": "email",
  "target_account_id": "agency_x_riyadh",
  "drafted_by": "founder",
  "drafted_at_iso": "2024-12-01T10:00:00Z",
  "preflight_status": "PASS",
  "preflight_run_at_iso": "2024-12-01T10:05:00Z",
  "founder_review_status": "pending",
  "evidence_level": "L2",
  "risk_level": "low",
  "approval_required": true,
  "approved_at_iso": null,
  "approved_by": null,
  "rejection_reason": null,
  "send_log": {
    "sent_at_iso": null,
    "channel_response": null
  }
}
```

## The review cadence

- Daily at 9am: founder reviews the queue.
- Any draft pending > 24 hours gets a reminder.
- Any draft rejected 2+ times gets a rewrite assignment.

## The audit trail

The approval queue is **append-only in spirit**. Do not delete rows. To reverse a decision, add a new row with `action: reversed`.

## The hard rules

1. **No draft is sent without `preflight_status: PASS`.** The script must run.
2. **No draft is sent without `founder_review_status: approved`.** The founder must approve.
3. **No draft is sent without `evidence_level`.** L0 (no evidence) is allowed but flagged.
4. **No draft is sent without `risk_level`.** `low`, `medium`, `high`. The founder decides.
5. **No draft is sent without `approval_required: true`** for any external channel.
6. **No send is logged without `sent_at_iso` and `channel_response`.**

## The exceptions

There are no exceptions. The only way to skip the preflight is to not send. If you don't trust the draft enough to run it through preflight, you don't trust it enough to send.

## The reporting

Every Friday, the founder reviews the approval queue:

- How many drafts were rejected by the preflight?
- How many were rejected by the founder?
- What patterns emerged?
- Are there rewrites needed in the email/LinkedIn/call libraries?

The weekly review is logged in `reports/launch/WEEKLY_GTM_BOARD_REVIEW_TEMPLATE.md`.

## When to update the playbook

- When the preflight catches a pattern that is not in the regex list.
- When the founder starts approving drafts the preflight would reject (means: founder needs to add a regex).
- When the queue grows > 20 items pending (means: preflight is too strict, or drafter is too slow).
