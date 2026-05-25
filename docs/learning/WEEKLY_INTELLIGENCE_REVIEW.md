# Weekly Intelligence Review — المراجعة الأسبوعية للذكاء التشغيلي

## Purpose
The Sunday review template. The founder spends 60 minutes on Sunday consolidating the week's signals into one written reflection that feeds the next week's priorities.

## Owner
Founder.

## Inputs
- Trust Command Center daily snapshots.
- AI Command Center weekly summary.
- Closed sprint folders from the week.
- Open experiments and incidents.
- Learning Router pattern increments.

## Outputs
- Weekly review file: `docs/learning/reviews/<YYYY>-W<NN>.md`.
- Three queued items for next week (priority, owner, due date).

## Rules (numbered)
1. The review happens Sunday. Skipped weeks are explicitly logged.
2. The review is at most 800 words written by the founder.
3. The review references at least one decision, one update, one experiment from the Learning Command Center.
4. The review names three priorities for the coming week.
5. No marketing language. The review is operating notes.

## Metrics
- Reviews completed per quarter (target greater than or equal to 12).
- Priorities from the previous week's review completed (target greater than or equal to 70 percent).
- Length compliance (greater than 400 words, less than 800).

## Cadence
Weekly. Every Sunday.

## Evidence (paths)
- `docs/learning/reviews/`

## Verifier
Founder.

## Runtime Command
`make learning.weekly.review` opens a new review file with the week's data pre-loaded.

## Review template

```
# Week NN, YYYY — Intelligence Review

## What happened
- 100 words. Sprints, incidents, experiments, decisions.

## What I noticed
- 200 words. Patterns visible only this week or compounding from prior weeks. Reference Learning Router counts.

## What surprised me
- 100 words. The signal I did not expect. Often the most important section.

## What I'm changing
- 100 words. The one playbook, checklist, or policy diff this week. Reference the file path.

## What I'm running
- 100 words. The experiment or trial in motion. Reference the experiment ID.

## Three priorities for next week
1. <priority>, owner, due date.
2. <priority>, owner, due date.
3. <priority>, owner, due date.

## Memory entries
- Cross-links to entries added to COMPANY_MEMORY this week.
```

## Inputs to pull before writing

Before writing, the founder pulls:

- Trust Command Center current state (open incidents, A3 log, banned phrase scanner hits).
- AI Command Center current state (any pending promotions, any pause events).
- Closed sprints this week (count, on-time rate, defect rate).
- Open experiments and their progress.
- Learning Router pattern counts incremented this week.
- Any client communication received this week.

## Operating substance
The weekly review is the founder's compounding asset. One review is useful; 50 reviews in a year is a history. 200 reviews over four years is the institutional memory that no competitor can replicate.

The 800-word cap is deliberate. A short review is a focused review. The discipline is to leave out what is not load-bearing. If everything seems load-bearing, the founder rereads and cuts.

The three priorities are the most actionable output of the review. They are not all of next week's work; they are the three things that must happen regardless of what else comes up. The next week's review opens by checking which of the three actually happened.

Skipped weeks happen. When they do, the next-week's review acknowledges the skip and names the cause. We do not pretend skipped weeks did not exist; we name them so the pattern is visible.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
