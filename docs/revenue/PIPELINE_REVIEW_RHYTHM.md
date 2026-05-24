# Pipeline Review Rhythm

A weekly 30-minute review the CEO runs in front of the pipeline tracker.
The point is not to look at all deals — it is to make sure the few that
matter are moving.

## The four questions

1. **Which deals have a date?** — qualified, scheduled next-step, named decision-maker
2. **Which deals have no next step?** — every deal must have an owner + a next step or it gets cut
3. **Which deals are stuck > 14 days?** — kick or kill
4. **Which deals need a [CLOSE_PLAN_TEMPLATE](CLOSE_PLAN_TEMPLATE.md)?** — anything over the deal-desk threshold

## Inputs

- [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv)
- [`docs/commercial/operations/evidence_events_tracker.csv`](../commercial/operations/evidence_events_tracker.csv)
- [`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv) — top strategic accounts

## Outputs

- List of next-step nudges (queued for the operator)
- Cuts (deals removed from pipeline) — appended to [`docs/founder/DECISION_LOG_SYSTEM.md`](../founder/DECISION_LOG_SYSTEM.md) with `type: cut`
- Close plans triggered ([CLOSE_PLAN_TEMPLATE](CLOSE_PLAN_TEMPLATE.md))

## Anti-patterns

- Cluttering the tracker with "interesting" leads — they need a next step or they go
- Reviewing every deal — review the top 20 + everything > 14 days stale
- "Let me follow up one more time" — fourth follow-up without a step-change means kill

## Cross-references

- [REVENUE_LEADERSHIP_SYSTEM](REVENUE_LEADERSHIP_SYSTEM.md)
- [DEAL_DESK_SYSTEM](DEAL_DESK_SYSTEM.md)
- [`docs/ops/DAILY_OPERATING_LOOP.md`](../ops/DAILY_OPERATING_LOOP.md)

## Non-negotiables

Nudges queue as drafts in the approval center; nothing is sent without human
approval. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
