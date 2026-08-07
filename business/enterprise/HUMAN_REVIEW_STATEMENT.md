# Dealix Human Review Statement

Every outbound action involving the customer's brand, prospects, or money requires explicit human approval before it leaves the workspace.

## Approval matrix

| Action | Reviewer | Tool |
| --- | --- | --- |
| Outreach draft → outbound | Founder | `scripts/approve_outreach_draft.py` |
| Outreach draft → rejected | Founder | `scripts/reject_outreach_draft.py` |
| Quote → sent to customer | Founder + customer's commercial owner | `scripts/approve_quote.py` |
| Deal → won | Founder | `scripts/mark_deal_won.py` |
| Deliverable → handed off | Customer | `scripts/record_client_approval.py` |
| Invoice stub → invoice | Customer Finance + Founder | `scripts/generate_invoice_stub.py` (stub only; never sent automatically) |
| Public launch announcement | Founder + customer (if joint) | `scripts/generate_public_launch_pack.py` |

## Why human review

- Reputation: one bad message destroys months of trust. Worth a 30-second human gate.
- Doctrine: enforced by `tests/test_no_auto_send.py`.
- Customer expectation: enterprise buyers expect a human owns the relationship.

## Limits of automation

- AI can prepare the message. Human approves the meaning.
- Automation can score leads. Human decides priority.
- Automation can route data. Human owns the customer relationship.
