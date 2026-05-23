# Focus Policy

> What the founder is allowed to spend time on this quarter.
> If a request doesn't pass this policy, it's an automatic DEFER.

## Current Quarter Focus (until 2026-08-31)

**One thing:** Get to 3 paid sprints + 1 retainer + 1 public case study.

Everything else is in service of this.

## Allowed Time Allocation

| Activity | % of week | Hard cap |
|---|---|---|
| Sales (outreach, calls, proposals) | 35% | — |
| Delivery (active sprints, QA) | 35% | — |
| Trust + governance (approvals, claims, incidents) | 10% | — |
| Strategy + decisions (briefs, reviews, logs) | 10% | — |
| Content + authority (LinkedIn, case studies) | 5% | — |
| Product (only if it unblocks Sales or Delivery) | 5% | 8 hr/wk |

## Forbidden Time (this quarter)

- Net-new product features that don't unblock a paid sprint
- Hiring conversations beyond contractor scope
- Geo expansion outside Saudi
- Conference / event prep
- Paid acquisition setup
- Investor conversations beyond inbound
- Refactoring code that already works

If any of these consume > 2 hours in a week, log it in `RISK_REGISTER.md`.

## Decision Heuristic For New Requests

When something new lands (idea, ask, offer), apply this in order:

1. **Veto check** — does it violate any rule in `DEALIX_DECISION_RULES.md` Veto section? → REJECT
2. **Strategy Filter** — does it pass at least one of the 5 strategy tests? → If no, DEFER
3. **Time cap check** — does it fit in this quarter's allocation? → If no, DEFER
4. **Reversibility check** — is it cheap to undo? → If yes, BUILD small
5. **Otherwise** → ESCALATE to the next Weekly CEO Review

## What "Focus" Means When Things Go Well

When something works (a sector replies, a sprint closes, a message lands), the policy is:
- Double the volume of the working thing
- Pause two of the not-working things
- Update this file with the new % allocation

## What "Focus" Means When Things Go Wrong

When something breaks (incident, churn, missed delivery):
- Stop net-new starts for 48 hours
- Run a one-page post-mortem in `learning/`
- Append a rule to `DEALIX_DECISION_RULES.md` if the cause is systemic
- Resume only after the rule is in place

## Refresh Cadence

- Reviewed every Sunday in the Weekly CEO Review
- Rewritten every quarter (or when stage transitions)
- Locked otherwise — no mid-week edits without a logged decision
