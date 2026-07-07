# Human Approval & Outbound Policy — Saudi Opportunity Command Room

This policy is binding for the `dealix/opportunity_graph` layer and the
`/api/v1/opportunity-command` API. It aligns with `CLAUDE.md`, the Dealix safety
rules, and `docs/V14_FOUNDER_DAILY_OPS.md`.

## What the AI may do (always allowed)

- Search, classify, score, and segment companies.
- Suggest next actions and priorities.
- Draft outreach messages, follow-ups, and phone-call scripts.
- Summarize signals and build daily reports and weekly proof packs.
- Maintain the append-only approval/decision audit log.

## What requires explicit human approval (never automatic)

- Sending **any** external message (WhatsApp, email, LinkedIn, SMS, phone).
- Approving a target for outreach.
- Marking a draft as sent (a human must have sent it, and be named).
- Issuing any proposal, invoice, or contract.
- Enabling any live outbound channel.

## Hard prohibitions

- **No automated live sending.** There is no auto-send code path in this layer.
- **No cold WhatsApp blasts.**
- **No LinkedIn automation.**
- **No scraping** that violates platform terms or privacy expectations.
- **No purchased/unconsented lists** used as if consented.
- **No guaranteed-revenue or fabricated claims.** Use hypothesis language
  ("we expect" / "نتوقع", "the goal is" / "الهدف هو", "we will measure" /
  "سنقيس"). Never "guaranteed" / "مضمون".
- **No sensitive-data misuse** (patient records, minors, etc.).

## Approval state machine

```
draft created ──▶ pending
pending ──approve──▶ approved ──(human sends manually)──▶ mark_sent recorded
pending ──reject───▶ rejected
pending ──revise───▶ revise (edit, then re-queue)
```

Guard rails enforced in code (`dealix/opportunity_graph/pipeline.py`):

- `decide_draft` requires a named human `actor`.
- `mark_sent` refuses unless the draft is `approved` **and** a `human_sender`
  is provided — and it only records the send, it performs none.
- Every decision is written to `data/opportunity_graph/approvals.json`.

## Environment posture (must stay this way)

```
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Manual send only until an explicit, separately-approved controlled-live rollout
PR is merged. This document does not authorize that rollout.
