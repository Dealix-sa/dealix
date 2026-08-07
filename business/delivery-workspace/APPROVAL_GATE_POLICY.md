# Approval Gate Policy

Customer-facing items requiring written approval before going live.

| Item | Approver | Tool |
| --- | --- | --- |
| Persuasion angle batch | Commercial owner | `request_client_approval.py` |
| WhatsApp draft batch | Commercial owner | `approve_outreach_draft.py` |
| Workflow change in production | Operator + Commercial owner | `request_client_approval.py` |
| First proof report | Commercial owner | `record_client_approval.py` |
| Public case study draft | Commercial owner + Marketing | manual + signed PDF |

## SLA
- Approval requested → response within 2 business days. After 5 business days of silence the SOW pauses.

## Storage
Approvals are written to `client_workspaces.json` with reviewer + decidedAt. Audit log captures the change.
