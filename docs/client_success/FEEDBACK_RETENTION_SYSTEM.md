# Feedback & Retention System

## Purpose
Ask for feedback systematically, retain customers who got value, and learn from those who didn't.

## Feedback request (Day 7)
A short message that asks:
1. What worked?
2. What didn't?
3. Would you recommend us? (1–10)
4. What would make this worth a retainer?

## Retainer ask (Day 30)
A separate message that:
- References the original outcome.
- Proposes a continuation at rung 4 of the ladder.
- Includes a specific monthly cadence.

## Tracking
`dealix-ops-private/client_success/retention_tracker.csv`:
- `client, start_date, status, renewals, churn_reason, notes`.

## Status values
- `Engaged` — actively delivering.
- `Renewed` — moved to a retainer.
- `Closed-won-once` — single engagement, no retainer.
- `Churned` — ended despite a retainer.
- `Cooling` — declined retainer but open to next project.

## Anti-patterns
- Asking for testimonials before delivering value.
- Pushing a retainer when the deliverable scored < 75.
- Using vague follow-ups ("just checking in") instead of a specific ask.

## Capital asset
- Positive feedback → `content/proof_library.md` (with `proof_approval.md`).
- Negative feedback → `pipeline/win_loss_log.md` and an action item in `productization/automation_backlog.md` (if systemic).
