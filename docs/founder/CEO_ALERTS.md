# CEO Alerts

The control plane only interrupts the founder when an alert fires. Three
levels, each with a fixed trigger list.

## Red Alerts — immediate attention
- A3 action attempted.
- Public repo safety violation.
- Client delivery overdue.
- Payment failed for active client.
- CI broken on main.
- Data incident.
- Legal/compliance claim requested.

## Yellow Alerts — review today
- Proposal waiting approval.
- Follow-ups overdue.
- Client health below 60.
- Delivery QA pending.
- Pricing exception requested.

## Green Alerts — informational
- New lead batch ready.
- Weekly report generated.
- Content draft ready.

## Routing

| Level | Channel | Acknowledgement |
|---|---|---|
| Red | Daily brief top, separate notification | Same-day |
| Yellow | Daily brief Decisions section | Within 24h |
| Green | Daily brief body | None required |

## Rule

A Red alert that is not acknowledged within 24 hours is itself a Founder
Risk and is surfaced by the Risk Engine.
