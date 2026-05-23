# Dealix Stage-Gated Roadmap

> The single roadmap for Dealix. Stages advance **only** when the exit checklist
> in `execution_engine/stage_checklist_updater.py` is fully green and verified
> by `scripts/verify_stage_gated_roadmap.py`.
>
> Editing this file by hand is fine. Changing stage status is not — that is
> derived from `stage/current_stage.md` in the private ops repo and from the
> `make advance` command.

## Stages

| # | Stage | Goal | Exit criteria (machine-checked) | Owner |
|---|---|---|---|---|
| 0 | **Setup** | Repo + CLI + audit infrastructure exist | `python scripts/audit_dealix_implementation.py` exits 0 | Founder |
| 1 | **Pipeline** | 25 named leads loaded with stage + next_action | `pipeline/pipeline_tracker.csv` has ≥ 25 rows; every row has `next_action` non-empty | Founder |
| 2 | **Outreach** | 25 DMs sent and logged | `revenue/revenue_action_log.csv` has ≥ 25 rows where `action_type=dm_sent` | Founder |
| 3 | **Samples** | 3 sample packs prepared and stored | `offers/revenue_sprint/` contains ≥ 3 `sample_pack_*` files | Founder |
| 4 | **Proposal** | 1 proposal sent with follow-up date | `revenue/revenue_action_log.csv` has ≥ 1 `action_type=proposal_sent` and a non-empty `next_followup` | Founder |
| 5 | **Payment Attempt** | Payment / PO / written approval in flight | `revenue/revenue_action_log.csv` has ≥ 1 `action_type` in {`payment_link_sent`, `po_received`, `written_approval`} | Founder |
| 6 | **Delivery** | First sprint delivered + QA passed | `delivery/delivery_report_*.md` exists and `qa_checklist.md` is fully checked | Founder |
| 7 | **Learning** | Weekly review + 1 playbook update | `weekly_reviews/<ISO_week>.md` exists; commit log shows ≥ 1 playbook edit in last 7d | Founder |

## Gate enforcement

A stage cannot be marked complete unless **all** of the following are true:

1. `python scripts/verify_stage_gated_roadmap.py` exits 0.
2. `python scripts/verify_stage_evidence_automation.py` exits 0.
3. `stage/stage_exit_checklist.csv` (private) has every row for the stage with `status=done`.
4. `stage/evidence_report.md` (private) lists the artefacts proving exit.

When all four pass, run `python -m dealix_cli advance --private-ops ../dealix-ops-private`
to advance to the next stage.

## What this roadmap is NOT

- Not a sprint plan — see `DEALIX_30_DAY_EXECUTION_PLAN.md`.
- Not a product roadmap — see `docs/product/NO_OVERBUILD_POLICY.md` for the rule
  about adding scope (don't, unless paid).
- Not a vision document — vision lives in `README.md`.
