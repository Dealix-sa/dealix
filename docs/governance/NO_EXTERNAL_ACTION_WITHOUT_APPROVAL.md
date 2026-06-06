# No External Action Without Approval — بوابة الاعتماد قبل أي إجراء خارجي

> Non-negotiable #8. This is a hard gate, enforced in code by the `approval_center`
> and by the doctrine guard tests under `tests/`. No automation may bypass it.

## القاعدة (Arabic)

لا يُسمح لأي وكيل (agent) أو سكربت أو خدمة بإرسال أي شيء إلى طرف خارجي —
بريد، واتساب، لينكدإن، رسالة، فاتورة، أو أي محتوى — قبل اعتماد المؤسس الصريح.
كل مخرج خارجي يُجهّز كـ **مسودة** فقط، ويوضع في طابور الاعتماد.

## The Rule (English)

Every outward-facing action is **drafted, queued, and held** until the founder
explicitly approves it. Nothing ships to a third party automatically.

## What counts as an "external action"

| Action | Allowed without approval? |
|---|---|
| Drafting outreach text into the repo / queue | ✅ Yes (draft only) |
| Sending email / WhatsApp / LinkedIn message | ❌ No — approval required |
| Generating an invoice draft | ✅ Yes (draft only) |
| Charging a customer / issuing a live invoice | ❌ No — approval required |
| Writing a Proof Pack to the customer workspace | ✅ Yes (internal artifact) |
| Sharing a Proof Pack with the customer | ❌ No — approval required |
| Publishing anything publicly (site, social) | ❌ No — approval required |

## The approval contract

Each queued item carries a `governance_decision` field. Valid states:

- `queued_for_approval` — drafted, waiting for the founder.
- `approved` — founder approved; an authorized human may send.
- `rejected` — discarded with a reason.

A record with `status: pending_founder_approval` **must never** be auto-sent.

## How it shows up in the pipeline

See `data/revenue/pipeline.jsonl`: outreach events are written with
`status: pending_founder_approval` and `governance_decision: queued_for_approval`.
They only move to `approved` after an explicit founder decision recorded in the
Approval Register (`06_approval_register.md`) of each customer workspace.

## Refusals (tied to the 11 non-negotiables)

This gate exists alongside, and reinforces:

1. No scraping systems.
2. No cold WhatsApp automation.
3. No LinkedIn automation.
4. No fake / un-sourced claims.
8. **No external action without approval.** ← this document.

Any request to auto-send, bulk-send, or bypass the queue must be **refused**, with
a safe alternative offered (draft + queue for approval).

## Verification

`scripts/verify_dealix_launch_readiness.py` checks that this document exists and
that the pipeline seed contains no `auto_sent` external events.
