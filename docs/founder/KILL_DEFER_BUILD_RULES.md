# Kill / Defer / Build Rules

> The operating filter for any new work proposal.
> Read `DEALIX_DECISION_RULES.md` first — this file is the day-to-day cheat sheet.

## Quick Test (60 seconds)

Ask in order:

1. **Does this serve cash collected in the next 60 days?**
   - Yes → continue to question 2
   - No → DEFER

2. **Does this fit the Focus Policy time allocation?**
   - Yes → continue to question 3
   - No → DEFER

3. **Is it cheap to undo (≤ 1 day rollback)?**
   - Yes → BUILD small, measure
   - No → continue to question 4

4. **Is the success metric defined and measurable?**
   - Yes → BUILD with the metric as the kill switch
   - No → DEFER until the metric is defined

5. **If similar work already exists, can we kill that first?**
   - Yes → KILL the old, then BUILD the new
   - No → BUILD as addition (and log why duplication is acceptable)

## Kill Triggers

Kill on sight if any of these are true:
- The workstream has not produced a logged customer interaction in 30 days
- The workstream has consumed > 8 founder hours without a logged outcome
- The workstream conflicts with current quarter Focus
- The success metric was never defined and still isn't
- Two systems are doing the same thing (kill the weaker)

## Defer Triggers

Defer (don't kill) if any of these are true:
- The idea is sound but the timing is wrong (e.g. wait for first paid sprint)
- The idea needs evidence from another experiment first
- The idea is interesting but doesn't pass the Strategy Filter today
- The cost is high and reversibility is low — needs more data

Every DEFER includes a **revisit date**. No date = implicit KILL.

## Build Triggers

Build if all of these are true:
- Passes Strategy Filter (≥ 1 of 5 tests)
- Fits Focus Policy time allocation
- Has a defined success metric
- Has a defined kill switch (when to stop)
- Has an owner (always the founder until a hire fills the role)
- Has been written into a one-pager (no Slack-only proposals)

## Build Sizes

- **XS** — ≤ 2 hours. Just do it, log in execution ledger.
- **S** — ≤ 1 day. Open a PR, link to Strategy Filter test passed.
- **M** — ≤ 3 days. One-pager required, weekly review checkpoint.
- **L** — > 3 days. Requires explicit Weekly CEO Review approval, must include kill switch and 14-day review.
- **XL** — > 2 weeks. Not allowed this quarter. Period.

## What This Filter Refuses

- "Just one more feature" — no
- "It's almost done, let's finish it" — no, sunk cost is not a build reason
- "It will be useful eventually" — that's the DEFER bucket
- "It will look bad to kill this publicly" — kill privately, learn loudly

## How To Disagree With This Filter

If you (the founder) want to override the filter, you must:
1. Log the override in `DECISION_LOG.md` as an `ESCALATE` row
2. Write one paragraph in `founder/decision_log.md` (private) explaining why
3. Set a 14-day review date — if the override isn't paying off by then, kill it
