# Client Service Autopilot — Runbook

## Purpose

Combines RCMax, Auto14, Client Ops Max, Deal Conversation Intelligence, and Deal Strategy Brain into a single client service pack. Given an account, sector, and client message, it prepares everything needed to serve the client — while keeping all sensitive actions behind approval gates.

## What It Auto-Prepares

1. client_workspace
2. intake_pack
3. workflow_diagnosis
4. owner_map
5. command_queue
6. draft_route_pack
7. conversation_readout
8. deal_strategy
9. proposal_folder
10. daily_delivery_plan
11. weekly_review_pack
12. proof_report_template
13. renewal_plan

## Approval Queue (never auto-run)

- external_email_send
- whatsapp_send
- calendar_invite_send
- final_price_commitment
- legal_terms_acceptance
- contract_signature
- guaranteed_revenue_claim
- public_claim_without_review

## Usage

```bash
python client_service_autopilot.py
```

```python
import client_service_autopilot as csa

payload = csa.build_payload(
    account='Alpha Trading',
    sector='Retail',
    message='ارسل العرض',
)
print(payload['deal_strategy']['next_best_action'])
print(payload['approval_queue'])
```

## Safety Guarantees

- `live_sends == 0` always
- `final_commitments == 0` always
- All approval_queue items have `auto_run == False`
- Proposal folder is always `draft_only`
- Renewal brief always requires `approval_required == True`

## How to Use with a Real Client Tomorrow

1. Run: `python client_service_autopilot.py`
2. Share the `client_workspace` with the client
3. Send the `intake_pack` questions (founder reviews first)
4. Review `conversation_readout` to understand the client's stage
5. Review `deal_strategy` for the recommended next action
6. Check `approval_queue` and approve only what is ready
7. Review `proof_report_template` after Day 2
8. Use `weekly_review_pack` for the Day 7 review call
