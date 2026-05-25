# Founder Machine Priority Map

## Purpose
The Dealix repo has 183 machines under `auto_client_acquisition/` plus
40+ API routers. This document is the **only ordered list of which machines
matter first**. Do not build P2 before P0 has movement.

## P0 — Must build / wire now
1. CEO Command Center (`apps/web/app/ceo`)
2. Sales Cockpit (`apps/web/app/sales-cockpit`)
3. Approval Center (`apps/web/app/approvals`)
4. Lead Intelligence Machine (`auto_client_acquisition/icp_scorer`, `lead_inbox`)
5. Outreach Draft Machine (`auto_client_acquisition/outreach_window`, `email/`)
6. Follow-Up Machine (`auto_client_acquisition/sales_os/follow_ups`)
7. Proposal + Payment Capture (`auto_client_acquisition/proof_engine`, `payment_ops`)

## P1 — Build after first active funnel
1. Sample Factory (`auto_client_acquisition/proof_to_market`)
2. Reply Router (`auto_client_acquisition/customer_inbox`)
3. Sector Scorecard (`auto_client_acquisition/scorecards`)
4. Proof-to-Demand (`auto_client_acquisition/proof_engine`)
5. Partner Referral Machine (`api/v1/referral-program`)

## P2 — Build after first paid sprint
1. Retention Machine (`auto_client_acquisition/customer_success`)
2. Customer Portal (already exists in `frontend/`)
3. Delivery QA Dashboard
4. Productization Dashboard
5. Cost Control Center

## Rule
- P0 must show movement (drafts queued, approvals flowing, at least one payment captured) before any P2 work begins.
- P1 unlocks only after P0 is producing daily output.
- Every machine that produces external action must be gated by Approval Center.
