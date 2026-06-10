# Dealix CRM Pipeline Schema

## Stages

1. New
2. Research Complete
3. Fit Scored
4. Outreach Drafted
5. Contacted
6. Replied
7. Discovery Booked
8. Diagnostic Delivered
9. Proposal Sent
10. Won
11. Lost

## Lead fields

- id
- company
- sector
- pain
- source
- email
- phone
- score
- status
- next_action
- created_at

## Qualification rule

Qualified = score >= 60 AND contact exists AND pain is clear.
