# Email Draft Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/OUTBOUND_DRAFT_MACHINE.md`

## Purpose

The Email Draft Machine produces warm email drafts for personas where email is the appropriate channel (typically referrals, post-meeting follow-ups, partner introductions, and contact-form inbound responses). It queues drafts for Founder approval and respects deliverability and PDPL norms.

It is NOT a cold email blaster. It does not send unsolicited bulk email.

## Inputs

- **Approved offer-channel pairing** for email (per `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`).
- **Warm context** for each recipient — referral, prior touch, event meeting, or inbound submission.
- **Account scoring state** — Tier A only for outbound; Tier A or B for response.
- **Email account roster** — which Dealix mailbox is sending.

## Outputs

A queued email draft per (account, persona, occasion), formatted with:

```
to: <persona email — sanctioned source only>
from: <dealix mailbox>
subject: <short, specific>
body: <plain text by default; HTML only for branded broadcasts>
language: ar | en | bilingual (parallel)
attachment: <Proof Pack reference if relevant — never raw>
approval_class: A2
```

Drafts also include:

- A one-line warm context citation (e.g., "Met at <Event> 2026-04-12").
- An explicit opt-out line for any broadcast.

## Source of truth

This doc + the email approval queue.

## Approval class

**A2** — Founder + Operator per send. Broadcasts (>= 5 recipients) require A2 per batch and an additional channel-health check.

## Trust gate

- No unsolicited cold email outside an explicit campaign approved by Founder.
- All emails to KSA recipients follow PDPL norms; no use of email addresses from scraped sources.
- Unsubscribe / opt-out mechanism required on any broadcast.
- Email account warming required for new mailboxes before any volume.
- No image-only emails. Plain text default.
- No tracking pixels in initial-touch emails. Tracking pixels permitted only in opted-in nurture broadcasts.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder (per send / per batch).

## Worker script (placeholder)

`workers/email_draft_worker.py` (planned). Pulls approved offer-channel pairings, drafts, queues, enforces volume caps.

## KPI

| Metric | Target |
|---|---|
| Draft latency | <= 24 hours from trigger |
| Approval rate (no revision) | >= 70 percent |
| Deliverability (per Dealix mailbox) | >= 95 percent |
| Spam-flag rate | 0 (any flag triggers immediate pause) |
| Reply rate | observed; published in distribution review |

## Failure mode

- A draft is sent to a scraped address.
- Deliverability collapses (mailbox blocklisted).
- Unsubscribe link missing on a broadcast.
- Two emails to the same persona in the same week from two operators.

## Recovery path

1. Pause the affected mailbox.
2. Audit the recipient list provenance.
3. Investigate deliverability and warm the mailbox if needed.
4. Re-enforce per-persona touch cap.

## What this machine does NOT do

- It does not send cold bulk email.
- It does not buy email lists.
- It does not scrape emails from public sources.
- It does not bypass PDPL or recipient-region anti-spam rules.

## Cross-links

- Outbound Draft Machine: `docs/growth/OUTBOUND_DRAFT_MACHINE.md`
- Channel Portfolio: `docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`
- PDPL language: `docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`

## Disclaimer

Dealix does not guarantee replies, opens, or meetings from email dispatch. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
