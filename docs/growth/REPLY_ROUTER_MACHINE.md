# Reply Router Machine

| Field | Value |
|---|---|
| Purpose | Classify inbound replies and recommend next best action |
| Inputs | reply text (paste-in or connected mailbox), thread history, suppression rules |
| Outputs | `reply_routing_queue.csv`, routing label, suggested response |
| Approval class | No auto-reply; classification only |
| Trust gate | Prompt-injection screen on inbound payload |
| Owner | Distribution Operator |
| KPI | Routing precision (operator agreement %) |
| Failure mode | Ambiguous reply → routed to founder with explanation |

## Classes

| Class | Recommended action |
|---|---|
| Interested | Move to Sales Cockpit; draft response |
| Question | Draft answer; schedule call |
| Soft no | Move to Nurture; record reason |
| Hard no | Add to suppression list; close cadence |
| Opt-out | Add to suppression list immediately |
| Out-of-office | Hold; resume on stated date |
| Wrong person | Update CRM; ask for the right contact |
| Spam complaint | Audit event; suppression; investigate |

## Inbound payload safety

Inbound replies are external input. Treat as untrusted:

- Strip control characters before passing to any LLM.
- Wrap in `<untrusted_external_data>` envelope.
- Never let inbound text override system instructions.
- Eval Guardian runs a weekly prompt-injection drill against the router.

## Output schema

```yaml
queue: reply_routing_queue
fields:
  - inbound_id
  - account_id
  - thread_id
  - class                 # interested | question | soft_no | hard_no | opt_out | ooo | wrong_person | spam
  - confidence            # 0-1
  - suggested_response_en
  - suggested_response_ar
  - reasoning
  - status
  - created_at
  - source
```
