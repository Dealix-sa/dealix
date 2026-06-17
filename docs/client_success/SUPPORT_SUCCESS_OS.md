# Support & Success OS

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Support clients after delivery and protect retention. Customer support is not a cost center here — it is the source of retention data, feedback, retainer asks, and proof candidates.

## Queues

| Queue | Source | SLA |
|-------|--------|-----|
| Onboarding questions | New active client | Same business day |
| Delivery issues | Active engagement | 24 hours |
| Revision requests | Within scope | 48 hours |
| Out-of-scope requests | New scope candidate | 48 hours; quote within 3 business days |
| Feedback | Post-delivery | Recorded same week |
| Retainer asks | Strong feedback + scope clarity | Founder schedules within 1 week |
| Renewal risk | Health-score drop | Same-day review by founder |
| Refund inquiries | Any source | Founder reviews same day |

## Health Score Inputs (for renewal risk)

- Recency of last positive interaction
- Open delivery issues count
- Open revision requests count
- Time since last feedback
- Time since last retainer or expansion conversation
- Any complaint or escalation flag

A health-score drop is a signal, not a verdict. The renewal-risk review investigates the why before any action.

## Core Rules

- Every active client has a named relationship owner.
- Every client interaction is logged with timestamp and outcome.
- Customer support never makes pricing, scope, or contractual commitments without the founder.
- Customer support produces retention data — feedback, sentiment, and renewal signals — that flows back into the war room and the lifecycle OS.
- Public mention of a client (in proof or content) always requires written client approval recorded as a source-evidence link.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Daily | Open issues triaged; SLA breaches escalated |
| Weekly | Health-score review per active client |
| Monthly | Retention scorecard: churn risk, expansion candidates, proof candidates |

## Runtime Wiring

- Delivery docs (existing cross-link): `docs/delivery/DELIVERY_LIFECYCLE.md`.
- Lifecycle stages 8–13: `docs/client_success/CUSTOMER_LIFECYCLE_OS.md`.
- CS handoff queue: `core/queue/cs_handoff_task.py`.
- Audit log: `db/models.py::AuditLogRecord`.
- Revenue events (for retainer / expansion outcomes): `auto_client_acquisition/revenue_memory/event_store.py`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Issues responded within SLA | ≥ 95% | timestamps |
| Average resolution time | tracked, trending down | timestamps |
| Health-score drops resolved within 1 week | ≥ 80% | health-score deltas |
| Retainer conversion from strong feedback | tracked | revenue events |
| Proof candidates produced per quarter from delivered clients | tracked | proof worker |

## Cross-Links

- `docs/client_success/CUSTOMER_LIFECYCLE_OS.md`
- `docs/delivery/DELIVERY_LIFECYCLE.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`

## Open Items

- A first-class "support ticket" object does not yet exist in the database; today, support interactions are recorded across notes and the CS handoff queue.
- The health-score formula is conceptual; the numeric weights have not been calibrated against actual churn data because the dataset is still small.
- Renewal-risk alerting depends on the health score being computed; that pipeline is not yet wired.
- A retention scorecard view in the cockpit is open.
