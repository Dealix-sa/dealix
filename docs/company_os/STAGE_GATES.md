---
title: Stage Gates
owner: Founder
status: active
cadence: review-monthly
last_review: 2026-05-23
---

# Stage Gates

The Dealix Company OS proceeds in stages. Each stage has an entry artefact and an exit artefact. No stage starts without the prior stage's exit artefact in place.

## Map

| Stage | Entry artefact | Exit artefact |
|---|---|---|
| 0 — Trust | docs/trust/APPROVAL_MATRIX.md | docs/trust/TRUST_COMMAND_CENTER.md |
| 1 — Revenue | docs/revenue/OFFER_LADDER.md | docs/revenue/REVENUE_COMMAND_CENTER.md |
| 2 — Offers | docs/offers/revenue_sprint/SCOPE.md | docs/offers/revenue_sprint/README.md |
| 3 — Delivery | docs/delivery/revenue_sprint/QA_CHECKLIST.md | docs/delivery/revenue_sprint/README.md |
| 4 — Learning | docs/learning/LEARNING_ROUTER.md | docs/learning/LEARNING_COMMAND_CENTER.md |
| 5 — Dashboard | docs/dashboard/CEO_DASHBOARD_DATA_MODEL.md | docs/dashboard/CEO_DASHBOARD_V2.md |
| 6 — AI Mgmt | docs/ai_management/AGENT_REGISTRY.md | docs/ai_management/AI_COMMAND_CENTER.md |
| 7 — Agents | docs/agents/AGENT_CONTROL_PROTOCOL.md | docs/agents/README.md |
| 8 — Product | docs/product/PRODUCTIZATION_MAP.md | docs/product/PRODUCTIZATION_COMMAND_CENTER.md |
| 9 — Finance | docs/finance/CASH_CONTROL.md | docs/finance/FINANCE_COMMAND_CENTER.md |
| 10 — Client Success | docs/client_success/ONBOARDING.md | docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md |
| 11 — Content | docs/content/LINKEDIN_CADENCE_PLAN.md | docs/content/LINKEDIN_CADENCE_PLAN.md |
| 12 — Partners | docs/partners/PARTNER_PROGRAM.md | docs/partners/PARTNER_PROGRAM.md |
| 13 — People | docs/people/HIRING_FRAME.md | docs/people/README.md |
| 14 — Company OS | docs/company_os/README.md | docs/company_os/README.md |
| 15 — Verify | scripts/verify_full_ops.py | scripts/verify_full_spectrum_os.py |

## Gate rule

A stage may not be referenced as a dependency until its exit artefact exists on disk. The verify script `scripts/verify_stage_gated_roadmap.py` checks this.

## Owner

Founder.
