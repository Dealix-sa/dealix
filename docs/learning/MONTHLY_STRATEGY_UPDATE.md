# Monthly Strategy Update

> The end-of-month aggregation of all learnings.
> Inputs: every other file in `docs/learning/`.
> Output: a one-page strategic note + decisions for next month.

## Cadence

- Written on the last Sunday of each month
- During / after the Weekly CEO Review
- Saved as `weekly_reviews/monthly-YYYY-MM.md` (private)
- Public-safe excerpt may go to Board Memo (per `BOARD_MEMO_TEMPLATE.md`)

## Format

```markdown
# Monthly Strategy Update — YYYY-MM

## North-Star Status
- Cash collected: SAR ____ (vs target ____)
- MRR: SAR ____ (Δ ____)
- Trust incidents: ____ (target 0)
- 90-day milestone progress: ___ / ___ targets

## What We Learned This Month
1. {1-sentence learning from EXPERIMENT_LOG}
2. {1-sentence learning from WIN_LOSS_REVIEW}
3. {1-sentence learning from SECTOR_PERFORMANCE}
4. {1-sentence learning from MESSAGE_PERFORMANCE}
5. {1-sentence learning from PRICING_LEARNING}
6. {1-sentence learning from AGENT_EVALS}

## What's Working
- _____
- _____
- _____

## What's Not
- _____
- _____

## Decisions For Next Month
- BUILD: _____
- FIX: _____
- KILL: _____
- DEFER: _____
- ICP weight change: _____ (if any)
- Pricing change: _____ (if any)
- Sector add/remove: _____ (if any)
- Playbook update: _____ (if any)

## One Strategic Question To Answer Next Month
> _____

## Reading
- Anything external worth re-reading this month: links
```

## Discipline

- One page max
- Every section filled (never "n/a" two months in a row)
- Decisions section must have at least one KILL and one BUILD (proves we have direction)
- Strategic Question must be answerable through measurement

## Roll-Up Linkages

| Learning source | Surfaces in |
|---|---|
| Experiment results | Decision section |
| Win/loss patterns | ICP weight section |
| Sector performance | Sector add/remove section |
| Message performance | Playbook update section |
| Pricing learning | Pricing change section |
| Agent evals | Trust + product sections |

## Decision Implementation

Every decision in the Monthly Strategy Update:
- Gets a corresponding row in `DEALIX_EXECUTION_LEDGER.md`
- Gets an owner (founder until otherwise)
- Gets a deadline
- Gets a measurement at next month's update

## When To Pivot

If 3 consecutive Monthly Strategy Updates show no progress on the North-Star Status:
- Trigger a quarterly strategy reset
- Founder + advisor
- Re-read `NORTH_STAR.md` against current evidence
- Decide: persevere, pivot, kill an offer, or change ICP

This is the company's "are we on the right track" check. Don't skip it.

## What This Refuses

- Filler updates
- "Same as last month" (always something to say)
- Hiding negative numbers
- Inventing learnings to fill the section
- Punting decisions ("we'll decide next month") two months running
