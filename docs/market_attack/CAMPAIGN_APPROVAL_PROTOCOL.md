# Campaign Approval Protocol

> The exact gates a campaign passes through before any external
> sending. Doctrine: **no external send without an approval row**.

## Approval classes

| Class                  | Required approvers                | Use case                                |
| ---------------------- | --------------------------------- | --------------------------------------- |
| founder_only           | Founder                           | Warm intros, single-recipient messages  |
| founder_review         | Founder                           | Authority posts, sector content         |
| governance             | Founder + Governance owner        | Anything with sensitive claims          |
| partner_and_founder    | Founder + Partner counter-sig     | Partner co-branded campaigns            |

## Stages

1. **Draft** — `campaign_registry.status=draft`. No queue rows allowed.
2. **Assets ready** — every asset in `campaign_assets.csv` for this
   campaign must be `approval_status=approved` and have a
   `proof_status` other than `evidence_required`.
3. **Queue staged** — queue rows in `campaign_queue.csv` with
   `send_status=queued`. The system will not move anything past
   `queued` without an explicit approval row.
4. **Approval row** — a separate file
   `<PRIVATE_OPS>/campaigns/approval_log.csv` records:
   `approval_id,campaign_id,queue_ids,approver,approved_at,scope,notes`.
5. **Live** — `campaign_registry.status=live`. Sending allowed via
   the documented manual channel only.
6. **Postmortem** — see `CAMPAIGN_POSTMORTEM_SYSTEM.md`.

## Hard refusals

- Cold WhatsApp blasts.
- LinkedIn automation (connect + follow-up sequences via 3rd party
  tools without human approval per send).
- Scraping personal email addresses for outreach.
- Any "AI agent" that sends external messages without an approval row.

These are refused even if the user requests them — they violate
PDPL and the proof-safe doctrine.
