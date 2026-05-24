# Founder Time Audit

A weekly logging rubric that produces the rows in PRIVATE_OPS
`ceo/leverage_time_audit.csv`. The audit is the input to
[FOUNDER_LEVERAGE_DASHBOARD](FOUNDER_LEVERAGE_DASHBOARD.md).

## How to capture

Two acceptable methods:

1. **Live tagging** — at the end of each work block, tag it Make / Manage / Move in a calendar event or notebook
2. **Friday recall** — block 15 minutes during [CEO_WEEKLY_REVIEW](CEO_WEEKLY_REVIEW.md) and reconstruct the week from the calendar

Either way, the output is one row per week with totals (not per-event).

## CSV schema

| Column | Type | Notes |
|---|---|---|
| `week_end` | ISO date (Friday) | Primary key |
| `make_hours` | int | Hours producing artefacts personally |
| `manage_hours` | int | Hours reviewing / approving / hiring / 1:1s |
| `move_hours` | int | Hours on strategy, learning, customers, decisions |
| `notes` | free text | What dominated this week |

## Decision rules

- A meeting where you're the producer (live demo / live drafting) → Make
- A review meeting (approving a draft) → Manage
- A customer discovery call → Move
- Hiring interview → Manage
- Writing a strategy doc (this kind of doc) → Move
- Writing production code → Make
- Architecting an OS (this kind of work) → Move
- "Quick check on the contractor's work" → Manage (and audit if it eats > 2 hours/week)

## Anti-pattern

If `make_hours > manage_hours + move_hours` for two consecutive weeks, the
verifier raises a `WARN` and the daily brief surfaces the top delegation
candidates. See [DELEGATION_DECISION_TREE](DELEGATION_DECISION_TREE.md).

## Cross-references

- [FOUNDER_LEVERAGE_DASHBOARD](FOUNDER_LEVERAGE_DASHBOARD.md) — the read view
- [CEO_ATTENTION_BUDGET](CEO_ATTENTION_BUDGET.md) — the budgeting rules
- [../people/DELEGATION_SYSTEM](../people/DELEGATION_SYSTEM.md) — the system to delegate Q4 items
- [`docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md`](../ops/FOUNDER_OPERATING_SYSTEM_AR.md) — the original AR rhythm doc

## Non-negotiables

This audit is for the CEO's own visibility. It is never shared externally
without explicit consent. See [DO_NOT_SAY](DO_NOT_SAY.md).
