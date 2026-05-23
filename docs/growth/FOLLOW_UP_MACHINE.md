# Follow-Up Machine

## purpose
Generate next-best follow-up drafts on a cadence that respects the
buyer's last reply (or lack of reply).

## inputs
- Outbound history per account.
- Cadence templates approved by the founder.
- Reply state from the reply router.

## outputs
`distribution/follow_up_queue.csv`:
```
draft_id,account_id,parent_draft_id,step_index,
days_since_last_touch,subject,body,trigger_id,
fallback_share,created_at,status
```

## source
- Internal interaction history.
- Persona-allowed cadence templates.

## approval_class
per-cadence (template) + per-message (specific draft).

## trust_gate
- A cadence is approved as a template by the founder.
- Each specific draft is still approved individually.

## owner
distribution_operator → founder.

## worker
`distribution_follow_up_worker` (daily).

## KPI
- Follow-up density (target band).
- Reply lift between steps.
- Hard-stop trigger rate (founder hits stop).

## failure_mode
- Over-follow-up density.
- Following up after a "no thanks" reply.

## recovery_path
- Auto-throttle on density > threshold.
- Reply router marks `do_not_followup` on negative replies.

## kill_switch
`make growth-kill-follow-up`.

## audit
`audit/distribution_follow_up_runs.jsonl`.
