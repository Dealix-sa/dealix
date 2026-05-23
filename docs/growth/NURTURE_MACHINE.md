# Nurture Machine

## purpose
Long-cycle nurturing for accounts that are real fits but not ready
to buy. Surfaces relevant content to scored accounts in a respectful
cadence — without sending anything externally on its own.

## inputs
- `growth/account_scores.csv` (tier B / C).
- `marketing/content_calendar.csv`.
- Account's last engagement timestamp.

## outputs
`distribution/nurture_queue.csv`:
```
draft_id,account_id,content_id,step_index,channel_hint,
body,share_link,founder_note,fallback_share,created_at,status
```

## source
- Internal content + founder-approved curation.

## approval_class
per-sequence.

## trust_gate
Sequences are approved as templates. Each share is still queued for
founder approval — no auto-publishing on the account's behalf.

## owner
content_strategist → founder.

## worker
`distribution_nurture_worker` (weekly).

## KPI
- Nurture coverage (% of B-tier accounts touched per quarter).
- Tier movement: B → A conversion rate.
- Unsubscribe / "not interested" rate (must stay low).

## failure_mode
- Over-cadence.
- Stale content surfaced.

## recovery_path
- Auto-throttle on density.
- Calendar refresh.

## kill_switch
`make growth-kill-nurture`.

## audit
`audit/distribution_nurture_runs.jsonl`.
