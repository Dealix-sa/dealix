# Reply Router Machine

## purpose
Classify inbound replies and route them to the right next-action
queue with a suggested response — never auto-replying.

## inputs
- Founder-forwarded replies (email).
- Founder-logged LinkedIn replies.
- Founder-logged WhatsApp replies (if any).

## outputs
`distribution/reply_router.csv`:
```
reply_id,account_id,channel,sentiment,intent
  (interested|info_request|objection|meeting_request|
   not_now|opt_out|spam),
suggested_response,attached_proof_id,fallback_share,
created_at,status
```

## source
- Founder-provided inbound text.
- No mailbox scraping.

## approval_class
per-reply.

## trust_gate
The system suggests a response; the founder sends it. `opt_out`
replies are auto-marked PDPL opt-out and removed from all queues.

## owner
sales operator → founder.

## worker
`distribution_reply_router_worker`.

## KPI
- Replies classified per day.
- Time from reply to next action.
- Opt-out compliance rate (must be 100 %).

## failure_mode
- Sentiment misread.
- Intent mis-labelled.

## recovery_path
- Operator can re-classify; the router learns from the correction.

## kill_switch
`make growth-kill-reply-router`.

## audit
`audit/distribution_reply_router_runs.jsonl`.
