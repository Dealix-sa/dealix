# Dealix 30-Day Execution Plan

> Mechanical, day-by-day plan. Every line item maps to a row that the
> private-ops audit (`audit_private_ops.py`) and the stage-gated roadmap can
> verify.

## Week 1 — Setup + Pipeline (Stages 0–1)

| Day | Action | Artefact |
|---|---|---|
| 1 | Run `make audit` and fix every failure | green audit |
| 1 | Add first 5 leads to `pipeline/pipeline_tracker.csv` | 5 rows |
| 2 | Add next 10 leads | 15 rows |
| 3 | Add final 10 leads | 25 rows |
| 3 | Run `make stage` — should now be on **Pipeline → Outreach** transition | `stage/current_stage.md` |
| 4 | Draft first 5 DMs and queue in `offers/revenue_sprint/founder_dm_pack.md` | 5 drafted |
| 5 | Send first 5 DMs and log in `revenue/revenue_action_log.csv` | 5 logged |
| 6 | Send 10 more DMs | 15 logged |
| 7 | Run `make weekly-close` and `make advance` | weekly review + stage bump |

## Week 2 — Outreach + Samples (Stages 2–3)

| Day | Action | Artefact |
|---|---|---|
| 8 | Finish remaining 10 DMs | 25 logged |
| 9 | Triage replies; pick top 3 for sample | reply notes |
| 10 | Build sample pack 1 from `sample_pack_template.md` | `sample_pack_1.md` |
| 11 | Build sample pack 2 | `sample_pack_2.md` |
| 12 | Build sample pack 3 | `sample_pack_3.md` |
| 13 | Send samples to the 3 prospects | 3 sample-send log rows |
| 14 | Weekly close + advance | weekly review |

## Week 3 — Proposal + Payment Attempt (Stages 4–5)

| Day | Action | Artefact |
|---|---|---|
| 15 | Convert strongest reply into a proposal via `proposal_fast_template.md` | `proposal_v1.md` |
| 16 | Send proposal; log + set `next_followup` | `action_type=proposal_sent` |
| 17 | Follow up on samples | log rows |
| 18 | If proposal accepted → send payment link / PO request | `payment_link_sent` |
| 19 | If not → revise, send to second prospect | new proposal |
| 20 | Capture written approval if verbal | `written_approval` |
| 21 | Weekly close + advance | weekly review |

## Week 4 — Delivery + Learning (Stages 6–7)

| Day | Action | Artefact |
|---|---|---|
| 22 | Run `client_intake.md` with paying client | intake doc |
| 23 | Begin delivery using `REVENUE_SPRINT_FACTORY.md` | delivery log |
| 24 | Mid-sprint QA via `qa_checklist.md` | QA row |
| 25 | Continue delivery | progress |
| 26 | Final QA + `delivery_report_template.md` | `delivery_report_*.md` |
| 27 | Handoff using `handoff_template.md` + `feedback_request.md` | feedback request sent |
| 28 | Retainer ask via `retainer_ask.md` | log row |
| 29 | Weekly close: write `weekly_intelligence_review.md`; commit one playbook update | weekly review + commit |
| 30 | Final audit: `make audit` should return PASS at every layer | green audit |

## Daily contract

Every working day:

```
make daily
```

This must:

1. Read private ops.
2. Print **Today's 3** from `founder/decision_queue.md`.
3. Print **Approvals waiting**.
4. Print yesterday's revenue actions.
5. Refresh the daily brief.

If `make daily` ever takes longer than 60 seconds, something is wrong —
investigate `dealix_cli/commands.py::daily`.

## Anti-scope rules

See `docs/product/NO_OVERBUILD_POLICY.md`. Short version:

- No new feature unless a paying customer is asking and paying.
- No new framework, language, or dependency without explicit approval.
- No automation that sends external messages without a human in the loop.
