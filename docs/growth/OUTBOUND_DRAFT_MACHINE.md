# Outbound Draft Machine

## purpose
Turn scored accounts + active triggers into personalised outbound
**drafts** that the founder can approve in one row.

## inputs
- `growth/account_scores.csv` (tier A/B only by default)
- `intelligence/trigger_events.csv` (status=queued, freshness ≤ decay)
- `growth/personas.csv`
- `data/private_ops_seed/growth/copy_blocks.csv` (approved openers + closers)

## outputs
`distribution/outbound_queue.csv` rows:
```
draft_id,account_id,persona_id,channel_hint,subject,body,
trigger_id,evidence_url,confidence,fallback_share,
created_at,status (queued/approved/sent/dismissed)
```

## source
- Primary: customer-provided ICP + signals.
- Enrichment: approved providers only.
- Fallback: marked `source=fallback` in every field that uses it.

## approval_class
per-message — every draft is approved one row at a time.

## trust_gate
The draft never leaves the queue without:
- founder approval recorded in `governance/approvals.csv`,
- brand_guardian voice pass,
- trust_guardian provenance pass.

## owner
distribution_operator (AI agent) → founder (human approver).

## worker
`distribution_outbound_draft_worker` (runs nightly + on trigger).

## KPI
- Drafts queued per day (target band).
- Approval rate ≥ 70 % (signal of voice + targeting fit).
- Reply rate post-send (lagging).
- Voice-violation rate < 2 %.

## failure_mode
- Persona / segment mismatch → off-tone drafts.
- Trigger expired by the time the draft is approved.
- Personalisation token missing → generic-looking draft.

## recovery_path
- Brand guardian rejects → regenerate with a stricter prompt.
- Stale trigger → expire row, mark `dismissed:stale`.
- Missing token → block from queue; raise gap to intelligence layer.

## kill_switch
`make growth-kill-outbound` or set
`DEALIX_DISTRIBUTION_OUTBOUND_ENABLED=0`.

## audit
Each run writes to `audit/distribution_outbound_runs.jsonl`.
