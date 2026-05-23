# Founder Bottleneck System

## Purpose
Surface the tasks that only the founder is doing, decide which to keep, and move the rest off the founder.

## Log
`dealix-ops-private/founder/founder_bottleneck_log.csv` with columns:
`date, task, reason, delegation_target, status`.

## Daily capture
At end of day, the founder writes 1–3 rows about tasks that:
- Only the founder could do.
- Took longer than expected.
- Required context only the founder has.

## Weekly review
- Look at the last week's rows.
- For each, mark a delegation target:
  - **Templatize**: turn into a template anyone could follow.
  - **Automate**: file in `productization/automation_backlog.md`.
  - **Contractor**: assign to a contractor (with onboarding).
  - **Keep**: legitimately founder-only.
- At least one row per week must move from `Pending → In-progress`.

## Anti-patterns
- "I'll just do it because it's faster".
- Delegating without documentation.
- Treating the log as documentation theater.

## Outcome
Over time, founder hours move from execution to direction, decision, and design.
