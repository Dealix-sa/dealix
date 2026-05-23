# Feature Intake

> Every build idea has a written intake. No intake → no build.

## Intake Sources

- Founder personal idea
- Customer ask (one named customer)
- Repeated customer ask (≥ 3 customers)
- Friction Log pattern (≥ 3 occurrences in 30 days)
- Strategic decision

## Intake Template

```
- id: F-yyyy-mm-dd-NN
  title: "..."
  source: founder / customer / friction-log / strategy
  description: "..."
  who_asked: "..." (named individuals or customers)
  problem_statement: "what hurts today?"
  proposed_change: "what would change?"
  reach: how many customers benefit?
  impact_per_customer: low / med / high
  effort: hours estimate
  reversibility: reversible / one-way
  alternative_kept_open: "what we are not foreclosing"
  workflow_dependency: "level of the workflow this productizes" (0-4)
  decision: build / defer / kill
  decided_on: yyyy-mm-dd
  decided_by: Sami
  rationale: "..."
  reversal_trigger: "..."
```

## Triage Cadence

- Founder triages the intake queue weekly.
- Default decision: **defer** until the workflow it productizes is at
  Level 2 (templated).
- Build is the rarest outcome.

## Triage Rules

A feature is built when **all** are true:

1. The workflow it depends on is at Level 2 or higher.
2. Reach × impact > 1 (i.e. it benefits more than one customer
   meaningfully).
3. Effort is bounded; the build does not silently consume founder hours.
4. It has a clear reversal trigger.

A feature is killed when **any** is true:

- It depends on a workflow at Level 0.
- It is one customer's wish; no one else has asked.
- Effort estimate > 2 weeks of founder time, and the value is not
  named.
- It contradicts the autonomy or trust policy.

## Build Queue Discipline

- Maximum 2 active builds at a time.
- A new build cannot start until the current 2 close or one is killed.
- Each build has a written success metric and a kill-by-date.

## Anti-Patterns

- "Let me just hack something quickly" with no intake.
- A backlog of "ideas to maybe do" without dates.
- Closing an intake silently without a decision rationale.
