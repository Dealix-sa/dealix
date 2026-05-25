# Learning Loop

> Every week, Dealix learns one thing and writes it down. If nothing was
> learned, that is itself the lesson — the week was wasted.

## Weekly review template

Saved as `weekly_reviews/<ISO_week>.md` (e.g. `weekly_reviews/2026-W21.md`)
in the **private** ops repo, *not* this public repo.

```markdown
# Week <ISO_week> — <YYYY-MM-DD> to <YYYY-MM-DD>

## Stage

- Started week at: <stage>
- Ended week at: <stage>
- Advanced via `make advance`? <yes|no>

## Shipped (artefacts created or updated)

- <path/to/file>: <one-line what changed>

## Sold (revenue actions)

- DMs sent: <n>
- Replies: <n>
- Samples sent: <n>
- Proposals sent: <n>
- Payment attempts: <n>
- Cash collected (SAR): <amount>

## Learned (one playbook update)

- Playbook updated: <path>
- Reason: <one-line>
- Commit hash: <sha>

## Next week target

- Primary outcome: <named deliverable>
- Stage target: <stage>
- Specific number to hit: <metric>

## Open ambiguities

- [ ] <thing the founder is unsure about>
```

## How it is enforced

The verifier `scripts/verify_weekly_automation.py` checks (against the
private ops repo):

1. A file `weekly_reviews/<current_iso_week>.md` exists.
2. The file contains the section headers above.
3. At least one playbook update is recorded with a commit hash.
4. `metrics_history/weekly_metrics.csv` has a row for this week with non-zero
   values where rows exist (no row of zeroes).

`make weekly-close` is the *only* approved way to create the file — it
pre-fills sections from `revenue/revenue_action_log.csv` so the founder
cannot under-report by accident.

## Anti-patterns

- Writing the weekly review *without* a committed playbook update — that is
  reflection, not learning.
- Editing last week's review to make it look better — frozen after `make advance`.
- Skipping a week — leaves a gap the audit flags.
- Putting customer names in this public repo — names live in private ops only.

## Related

- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md` — the daily/weekly loops.
- `DEALIX_IMPLEMENTATION_AUDIT.md` — definition-of-done references this.
- `DEALIX_30_DAY_EXECUTION_PLAN.md` — what each week should produce.
