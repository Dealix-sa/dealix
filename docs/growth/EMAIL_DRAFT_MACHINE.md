# Email Draft Machine

## purpose
Draft outbound emails to scored accounts. The Dealix system never
sends; the founder (or a verified delegate using their own SMTP)
sends.

## inputs
- `growth/account_scores.csv` (tier A/B).
- `growth/personas.csv`.
- Account-provided contact emails with `consent_status` = "permitted".

## outputs
`distribution/email_queue.csv`:
```
draft_id,account_id,persona_id,to_email,subject,body,
attachments[],trigger_id,evidence_url,fallback_share,
created_at,status
```

## source
- Customer CRMs (with consent).
- Public domain emails (only when `consent_status` = "permitted").
- Approved enrichment providers.

## approval_class
per-message.

## trust_gate
- Dealix produces an `.eml` draft or queue row.
- Sending is delegated to the founder via:
  - the founder console with a deliberate "send" action, or
  - an export the founder takes to their own mailbox.
- No SMTP credentials are stored long-term inside the Dealix runtime.

## owner
distribution_operator (drafter) → founder (sender).

## worker
`distribution_email_draft_worker`.

## KPI
- Drafts per day.
- Approval rate.
- Per-domain deliverability (when send is delegated and reported back).

## failure_mode
- Off-voice draft.
- Inactive recipient.
- Compliance violation (PDPL opt-out missed).

## recovery_path
- Voice / compliance rejection → block from queue.
- Hard bounce → mark `dismissed:hard_bounce`.

## kill_switch
`make growth-kill-email` or
`DEALIX_DISTRIBUTION_EMAIL_ENABLED=0`.

## audit
`audit/distribution_email_runs.jsonl`.

## hard refusals
- ❌ No mass-blasting from the Dealix runtime.
- ❌ No spoofed senders.
- ❌ No purchased lists.
- ❌ No sending into accounts marked PDPL opt-out.
