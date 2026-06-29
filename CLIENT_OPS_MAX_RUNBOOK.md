# Client Ops Max — Runbook

## Purpose

Client Ops Max runs the full client lifecycle from sale close through daily operations, weekly review, and renewal. It defines what Dealix prepares automatically and what requires the client or founder to approve.

## Lifecycle Stages

| Stage | What Happens |
|-------|-------------|
| sale_ready | Account scored, offer matched, proposal folder prepared |
| intake | Client provides channels, owners, sample data, approval rules |
| diagnosis | Workflow mapped, bottlenecks identified, owner map drafted |
| setup | Command queue built, workspace created, draft routes prepared |
| daily_ops | Daily queue reviewed, proof notes recorded, blocked items flagged |
| weekly_review | Proof report compiled, decisions recorded, next plan drafted |
| renewal | Renewal or expansion brief prepared, options presented to founder |

## Deliverables

1. client_intake_pack
2. workflow_diagnosis
3. owner_map
4. command_queue
5. draft_route_pack
6. daily_proof_note
7. weekly_proof_report
8. next_week_action_plan
9. renewal_or_expansion_brief

## Daily Delivery Checklist

- review_open_opportunities
- update_command_queue
- prepare_draft_routes
- record_proof_note
- log_owner_activity
- flag_blocked_items
- update_stage

## SLA Rules

- intake_completed_within_24h
- first_proof_note_by_day_2
- weekly_review_every_7_days
- approval_gates_never_auto_run

## Approval Gates (never auto-run)

- external_send
- final_price_commitment
- legal_terms_acceptance
- contract_signature
- guaranteed_revenue_claim

## Usage

```bash
python client_ops_max.py
```

Expected output:
```
CLIENT_OPS_MAX_READY=1
```

## Client Minimum Input

1. Approve sample data use
2. Confirm owners
3. Review proof
4. Approve external actions

## What Dealix Does Automatically

- Build workspace
- Map workflow
- Prepare command queue
- Prepare draft routes
- Record proof notes
- Prepare weekly review
- Prepare renewal brief
