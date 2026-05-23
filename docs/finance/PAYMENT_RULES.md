# Payment Rules

The rules around accepting and acknowledging payments.

## Accepted methods
- Bank transfer (SAR).
- Local payment gateway (where applicable).
- Stripe for international clients (USD, by approval).

## Not accepted
- Personal channels for company invoices.
- Cash for amounts above the threshold set by Saudi regulation.
- Crypto.

## On receipt
- Reconcile against the matching invoice within 24 hours.
- Log in `cash_collected.csv`.
- Notify the client (acknowledgement, not pushy).
- Trigger the kickoff action for the engagement.

## On dispute
- Pause delivery only after written agreement with the client.
- Escalate to founder within 24 hours.
- Document the dispute in `dealix-ops-private/revenue/disputes.csv`.

## Rule
Cash discipline is operational discipline. A late reconciliation today becomes a missing number in next month's report.
