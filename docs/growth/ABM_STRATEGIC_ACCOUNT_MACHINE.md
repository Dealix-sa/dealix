# ABM Strategic Account Machine

## purpose
Run a per-account playbook for the top 20-50 strategic accounts —
multi-stakeholder, multi-channel, time-bound, founder-driven.

## inputs
- Tier-A accounts from `growth/account_scores.csv`.
- Strategic accounts named by the founder (override list).
- Trigger events for those accounts.
- Personas in those accounts (multiple per account).

## outputs
`distribution/abm_playbooks.csv`:
```
account_id,playbook_id,stakeholders[],planned_steps[],
current_step,next_action,evidence_pack_id,
fallback_share,created_at,status
```

## source
- Public registries + customer-shared signals.
- Founder-curated stakeholder list.

## approval_class
per-account.

## trust_gate
- The account playbook is approved as a unit (not as individual sends).
- Each external action inside the playbook is still drafted and
  queued — no broad approval to "send everything".

## owner
growth_strategist → founder.

## worker
`distribution_abm_worker` (weekly cadence + on trigger).

## KPI
- Meetings booked per strategic account per quarter.
- Stakeholder coverage (% of named buyers reached).
- Time from playbook open → first meeting.

## failure_mode
- Stakeholder churn (named buyer leaves the account).
- Misaligned message across stakeholders.

## recovery_path
- Refresh stakeholder list.
- Brand guardian audits cross-stakeholder voice consistency.

## kill_switch
`make growth-kill-abm`.

## audit
`audit/distribution_abm_runs.jsonl`.
