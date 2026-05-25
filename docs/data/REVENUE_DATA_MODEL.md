# Revenue Data Model
## Purpose
Define how Dealix tracks revenue from lead to retention.
## Entities
### Lead
A company or buyer candidate.
Fields:
- company
- sector
- contact
- stage
- priority
- next_action
- last_touch
- notes
### Revenue Action
A commercial action taken by Dealix.
Fields:
- date
- lead_or_client
- action
- type
- status
- next_action
- evidence
### Proposal
A formal offer.
Fields:
- client
- offer
- scope
- amount
- follow_up_date
- start_condition
- status
### Payment
A cash or approval event.
Fields:
- client
- offer
- amount_sar
- payment_method
- status
- notes
### Retainer
A recurring agreement.
Fields:
- client
- plan
- monthly_amount_sar
- status
- start_date
- next_renewal
## Flow
Lead → Revenue Action → Sample → Proposal → Payment/PO → Delivery → Feedback → Retainer
## Rules
- Every lead has next_action.
- Every proposal has follow-up date.
- Every payment event has evidence.
- Every retainer has renewal date.
