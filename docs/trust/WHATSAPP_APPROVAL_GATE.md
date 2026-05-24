# WhatsApp Approval Gate

WhatsApp sends are class **A2**. They cannot leave the server unless:

1. The agent / human caller routes through
   `api.internal.integration_gate.request_external_send(...)`.
2. The `integration_id` is `whatsapp_greenapi`.
3. The recipient handle is NOT in
   `private_ops/outreach/suppression_list.csv`.
4. The content does NOT contain a guarantee phrase (policy rule
   `no_guaranteed_revenue_claims`).
5. A row exists in `private_ops/approvals/approval_queue.csv` with
   `status=approved` and the founder's decision id.
6. Environment is configured for live send AND the daily limit has
   not been exhausted.

## Approval flow

```
agent → draft  →  private_ops/outreach/outreach_queue.csv (status=queued)
                  ↓
                  private_ops/approvals/approval_queue.csv (status=pending)
                  ↓
                  founder decides → approval_decisions.csv (decision=approved)
                  ↓
                  integration_gate.request_external_send → audit_log.jsonl
                  ↓
                  GreenAPI send → outreach_queue.csv (status=sent)
                  ↓
                  followup_queue.csv (next_action, due)
```

## Daily-limit behaviour

`WHATSAPP_DAILY_LIMIT` must be set in production. The caller is
responsible for maintaining the day's counter (suggested:
`private_ops/runtime/whatsapp_daily.csv`). The gate refuses any call
when the counter ≥ limit.

## Failure modes (and what they mean)

| Symptom | Meaning | Fix |
|---|---|---|
| Gate returns `DENY` with `live_send_disabled` | `WHATSAPP_ALLOW_LIVE_SEND` is false | flip after safety gate passes |
| Gate returns `DENY` with `founder_approval_required` | no approved row in queue | route through approval flow |
| Gate returns `DENY` with policy `DENY` | content matched a forbidden phrase or the recipient is suppressed | rewrite or remove from list |
| Gate returns `ALLOW_MOCK` | mock mode is on | expected in CI / dev |

## Audit

Every gate decision writes one JSON line to
`$DEALIX_PRIVATE_OPS/trust/audit_log.jsonl`. The recipient handle is
hashed; the policy decision, integration id, action, and mock/live
flags are recorded verbatim.
