# Monthly Strategy Update — التحديث الاستراتيجي الشهري

## Purpose
Monthly written update that reconciles the past month's learning with the current strategy, producing concrete next-month adjustments. The monthly strategy update is the artifact that prevents Dealix from drifting from its operating reality.

## Owner
Founder.

## Inputs
- Four weekly intelligence reviews from the month.
- Company memory entries from the month.
- Trust and AI command center summaries.
- Win-loss reviews.
- Sector performance scorecards.
- Pricing learning entries.
- Audit findings.

## Outputs
- Monthly strategy update file: `docs/learning/strategy/<YYYY>-M<MM>.md`.
- Next month's three to five priorities, owned and dated.
- Any policy, playbook, or template diffs queued for the month.

## Rules (numbered)
1. The update is written by the founder. Not delegated.
2. The update is at most 1,500 words.
3. The update references at least one entry from each input source.
4. Next-month priorities are specific, owned, and dated.
5. Strategy reversals (decisions undone since last month) are explicitly noted.
6. The update is closed in the first week of the month for the prior month.

## Metrics
- Updates completed per quarter (target 3 of 3).
- Priorities from prior month completed (target greater than or equal to 60 percent).
- Reversals per quarter (low is good; zero suggests over-confidence).

## Cadence
Monthly. First week of the month.

## Evidence (paths)
- `docs/learning/strategy/`

## Verifier
Founder.

## Runtime Command
`make learning.monthly.update MONTH=<YYYY-MM>` opens the file with prior month's inputs loaded.

## Template

```
# Strategy Update — Month YYYY-MM

## State of the business (250 words)
Sprints closed, sectors active, open incidents, AI posture, trust posture. Plain language. Numbers where evidenced.

## What worked this month (200 words)
Patterns from win-loss, sector scorecards, message performance. Reference the source paths.

## What did not work (200 words)
Defects, incidents, lost deals. Specific. No spin.

## What I learned (200 words)
The signal I could not have predicted at the start of the month. Often the most valuable section.

## Strategy adjustments (200 words)
What we are changing in scope, sectors, pricing, or operations. Reference the file paths being changed.

## Reversals (100 words, may be N/A)
Decisions from prior months that we are undoing. Why.

## Priorities for next month
1. <priority>, owner, due date.
2. <priority>, owner, due date.
3. <priority>, owner, due date.
4-5. <optional>

## Memory entries this month
- Cross-links to entries added to COMPANY_MEMORY.

## Open questions
- What I do not yet know that I want to understand by next month.
```

## How the monthly update sits in the system

The monthly update is the largest of the recurring learning artifacts. It absorbs four weekly reviews, dozens of memory entries, and the month's audit findings into one piece of writing the founder owns end-to-end.

It is the document that the founder hands to a co-founder or senior hire on day one. It is the document that an investor or partner can read to understand how Dealix actually operates, not how it markets itself.

Strategy reversals are uncomfortable to write and important to write. A decision made in March and reversed in May, with the reversal documented, builds trust in the process. A reversed decision that is silently forgotten erodes it.

## Operating substance
Most service businesses do not write monthly strategy updates because the strategy "has not changed". Dealix writes them because writing the update is what surfaces whether the strategy has actually held. Often, the act of writing reveals that the strategy drifted three weeks ago and no one noticed.

The 1,500-word cap matters. Long strategy updates become unread strategy updates. Short ones get read by the founder before the next month's first weekly review, and become the lens through which the month is observed.

Reading the four weekly reviews before writing is the discipline. Without that re-read, the monthly update becomes a fresh narrative disconnected from what actually happened. With the re-read, it is a synthesis.

The open questions section is the seed for the next month's experiments. A clearly stated open question often becomes an experiment hypothesis within two weeks.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
