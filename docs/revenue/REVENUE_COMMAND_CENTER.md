# Revenue Command Center

Single source of truth for **how money moves into Dealix**.

This is a *public* doc — operating data (lead names, contact info, revenue
amounts) live in the **private** ops repo and are referenced here by path only.

## Inputs

| Input | Public path (template) | Private path (live data) |
|---|---|---|
| Pipeline | this doc + `docs/ops/lead_machine/` | `pipeline/pipeline_tracker.csv` |
| Revenue actions | this doc | `revenue/revenue_action_log.csv` |
| Approvals queue | this doc | `founder/approvals_waiting.md` |
| Decisions queue | this doc | `founder/decision_queue.md` |

## Required columns — `pipeline/pipeline_tracker.csv`

```
id, lead_name, company, role, segment, linkedin_url, email, phone,
channel, message_version, sent_at, reply_status, next_followup,
demo_booked_at, plan, payment_status, revenue_sar, notes, stage, next_action
```

`stage` ∈ {`new`, `researched`, `contacted`, `replied`, `sampled`,
`proposed`, `payment_attempted`, `paid`, `delivered`, `won_retainer`, `lost`}.

`next_action` is non-empty for every row with `stage != lost`. The verifier
`scripts/verify_tier1_revenue.py` enforces this rule.

## Required columns — `revenue/revenue_action_log.csv`

```
date, action_type, lead_id, channel, summary, amount_sar, next_followup, link
```

`action_type` ∈ {`dm_sent`, `email_sent`, `call_made`, `meeting_held`,
`sample_sent`, `proposal_sent`, `payment_link_sent`, `po_received`,
`written_approval`, `paid`, `refund`}.

## Operating rules

1. **Every action goes in the log on the same day.** No batching at week-end.
2. **No external send is automated.** The CLI prepares the draft; the founder presses send.
3. **No deal is "in pipeline" without a `next_action` and a date.**
4. **Stages only advance via `make advance`**, which runs the stage gate verifier.

## Daily cadence

```
make daily            # see today's 3, approvals, yesterday's actions
make stage            # show current stage, exit criteria, gap list
```

## Weekly cadence

```
make weekly-close     # writes weekly_reviews/<ISO_week>.md
make advance          # bumps stage if exit criteria are met
```

## Failure modes (do not paper over)

| Symptom | Probable cause | First check |
|---|---|---|
| `make daily` shows no leads | pipeline tracker empty or path wrong | `wc -l $(PRIVATE_OPS)/pipeline/pipeline_tracker.csv` |
| `make stage` says "no current stage" | private ops not initialized | `python -m dealix_cli init --private-ops <path>` |
| Audit fails on revenue actions | log missing or row count < 1 | `cat $(PRIVATE_OPS)/revenue/revenue_action_log.csv` |
| Audit fails with "next_action empty" | row added without a follow-up | open tracker, add next_action |

## Related

- `docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md` — what the customer receives once they pay.
- `docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md` — public-facing offer description.
- `DEALIX_STAGE_GATED_ROADMAP.md` — stages and their machine-checkable exit criteria.
