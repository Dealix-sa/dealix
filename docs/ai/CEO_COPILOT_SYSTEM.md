# CEO Copilot System

The CEO Copilot is an A1 agent that briefs the founder. It reads the
private ops tree and the operating scorecard, then proposes the top
action of the day. It cannot send messages, change pricing, or commit
proof artefacts.

## Output contract

```
{
  top_action: string,
  status: ok | needs_attention | unknown,
  risk_flags: integer,
  cash_collected_sar, approved_outreach, sent_outreach,
  positive_replies, proposals_due, payment_follow_ups,
  source: runtime | fallback
}
```

## Approval boundary

The CEO Copilot may not recommend any external action without surfacing
an approval row in `${DEALIX_PRIVATE_OPS}/approvals/approval_queue.csv`
with `approval_class >= A2` and required evidence. The founder remains
the only decision maker.
