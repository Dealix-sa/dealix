# Dealix Service Level Boundaries

This is what we commit to. Anything outside this list is a discussion, not a default.

## Response windows (business hours, Riyadh)

| Tier | First response | Resolution window |
| --- | --- | --- |
| P0 (production down) | 1 business hour | same business day |
| P1 (workflow blocked) | 2 business hours | next business day |
| P2 (cosmetic / non-blocking) | 1 business day | 5 business days |
| P3 (enhancement / feature request) | acknowledged in 2 business days | scheduled per roadmap |

Business hours: Sunday–Thursday, 09:00–18:00 KSA, excluding national holidays.

## Delivery rhythm

- Weekly proof report on Sunday morning.
- Monthly client review on the first Sunday of the month.
- Quarterly business review on customer cadence.

## What we do not commit to

- 24/7 on-call (available on retainer add-on).
- Sub-second response from third-party providers Dealix integrates with.
- Outcomes outside the scope of work — outcomes depend on customer execution.

## Change requests

- Logged in `business/_data/deals.ledger.json`.
- Reviewed in the weekly client review.
- Material changes require an addendum SOW.

## Escalation

- Founder is the single point of escalation. No customer ticket queue today.

## Measurement

- SLA compliance is logged monthly in `reports/operator/` and shared with the customer in the monthly review.
