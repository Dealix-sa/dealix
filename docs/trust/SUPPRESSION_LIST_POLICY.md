# Suppression List Policy

The list of contacts and entities Dealix must not contact.

## What goes on the list
- Anyone who explicitly asks not to be contacted.
- Anyone the founder or an A2 reviewer adds for any business reason.
- Anyone covered by a client's exclusion list, while that client is active.
- Entities flagged by sanctions or regulatory screening.

## What does not go on the list
- A prospect who did not reply (use the nurture rules instead).
- A prospect who said "not now" without asking to stop contact.

## Storage
- `dealix-ops-private/trust/suppression_list.csv`.
- Append-only.
- Columns: entity_or_contact, reason, added_by, date_added.

## Enforcement
- Every outbound action checks the suppression list before send.
- A failed check is logged as an incident.
- Quarterly review for accuracy and to catch shadow entries.

## Rule
The suppression list overrides every other rule. If a contact is on the list, no message goes out, ever.
