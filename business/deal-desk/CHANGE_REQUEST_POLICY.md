# Change Request Policy

## Definition
Any customer-initiated request that changes scope, timeline, or price after a SOW is signed.

## Process
1. Customer raises request in writing (email or `/client-portal/[id]`).
2. Founder estimates effort within 2 business days.
3. Founder issues a Change Order (CO) — a mini-quote attached to the original SOW.
4. Customer approves CO before work begins.
5. CO is logged in `business/_data/deals.ledger.json` with `parentDealId`.

## What counts as scope creep (and triggers a CO)
- New OS module requested.
- New integration outside the SOW.
- New geography / tenant.
- New deliverable requested in the weekly review without a CO.

## What does NOT trigger a CO
- Bug fixes within the agreed deliverable.
- Clarifications that don't change effort.
- Wording / styling tweaks.

## Pricing of change orders
- Use the published list price for in-catalog work.
- For ad-hoc work, charge at the customer's rate card or the founder's bench rate, whichever is higher.

## Anti-patterns
- "Just one more thing" without a CO. Always issue the CO; don't let scope drift.
- Verbal scope changes in calls. Always require email or portal confirmation.

## Founder discretion
For small, goodwill-driven scope additions under 1 hour of effort, founder may absorb without a CO once per quarter per customer.
