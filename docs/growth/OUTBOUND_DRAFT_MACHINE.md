# Outbound Draft Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

The Outbound Draft Machine produces persona-specific, channel-specific outbound drafts for every qualified, triggered, ICP-fit account that the Account Scoring Model surfaces. It is the writing layer that sits between the intelligence layer and the channel-specific queue machines.

It does NOT send. It drafts and queues for approval.

## Inputs

- **Qualified accounts** from `docs/intelligence/ACCOUNT_SCORING_MODEL.md` (Tier A only).
- **Qualified triggers** from `docs/intelligence/TRIGGER_EVENT_SYSTEM.md`.
- **Active persona spec** from `docs/intelligence/BUYER_PERSONA_SYSTEM.md`.
- **Active offer-channel matrix** from `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`.

## Outputs

A draft record per qualified (account, persona, channel) triple, formatted as:

```json
{
  "draft_id": "DRAFT-YYYY-NNNN",
  "account_id": "ACME-001",
  "persona_role": "head_of_sales",
  "channel": "linkedin_dm_warm",
  "trigger_ref": "TRIG-2026-0421-HoS-Hire",
  "offer": "Trigger Activation Sprint",
  "draft_body": "...",
  "language": "ar|en|bilingual",
  "approval_class": "A2",
  "created_at": "YYYY-MM-DDTHH:MM:SS+03:00"
}
```

The draft body must follow the channel-specific format defined in the relevant queue machine doc.

## Source of truth

The Outbound Draft Machine reads from the Intelligence layer and writes to the channel-specific queue machines:

- `docs/growth/LINKEDIN_QUEUE_MACHINE.md`
- `docs/growth/EMAIL_DRAFT_MACHINE.md`
- `docs/growth/CONTACT_FORM_QUEUE_MACHINE.md`

Draft logs persist in the approval ledger under `docs/06_llm_gateway/AI_RUN_LEDGER.md` conventions.

## Approval class

**A2** — Founder + Operator. Every draft requires explicit approval before it leaves the queue.

## Trust gate

- The machine cannot write a draft for an account not in Tier A.
- The machine cannot write a draft for an off-matrix offer-channel pair without explicit operator override + Founder approval (A2 for the override too).
- The machine cannot include a guarantee phrase. The draft body is run through the voice checklist before queueing.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder (gate).

## Worker script (placeholder)

`workers/outbound_draft_worker.py` (planned). Triggered hourly via the operating scheduler. Reads from the account scoring snapshot, writes to the relevant queue machine.

## KPI

| Metric | Target |
|---|---|
| Draft latency (trigger to draft) | <= 24 hours |
| Approval rate (operator approves draft without revision) | >= 70 percent |
| Reply rate per approved draft | observed; published in Sprint Outcome Reports |
| Voice-checklist pass rate (first try) | >= 95 percent |

KPIs are reported in the weekly distribution review.

## Failure mode

- Draft includes a banned phrase (e.g., "AI-powered").
- Draft is written for a persona the account no longer has (Head of Sales changed roles).
- Draft references a stale trigger.
- Draft volume exceeds Founder approval throughput; backlog grows.

## Recovery path

1. Re-run the voice checklist on the queue.
2. Re-verify persona currency before drafting.
3. Decay stale triggers (>90 days) before drafting.
4. Slow draft generation to match approval throughput.

## What this machine does NOT do

- It does not send.
- It does not scrape.
- It does not bypass approval.
- It does not draft to out-of-ICP accounts.
- It does not draft in a language the persona does not read.

## Cross-links

- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`
- Brand voice (banned phrases): `docs/brand/DEALIX_BRAND_VOICE.md`

## Disclaimer

Dealix does not guarantee replies, meetings, or revenue from approved outbound drafts. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
