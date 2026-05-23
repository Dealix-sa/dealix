# Operating Loops

The five loops that, together, are Dealix Company OS. Everything else is a system supporting one of these five loops.

## Purpose
Lock the company on a small, ordered set of loops so the founder, the AI, and every operating document share the same skeleton. If a loop is missing, the company is incomplete. If a loop is broken, the company is failing — not slowly, but specifically.

## Owner
Sami (Founder).

## Review Cadence
Weekly, during the Weekly CEO Review.

## Inputs
- The Doctrine (`DEALIX_OPERATING_DOCTRINE.md`).
- The Scorecard (`DEALIX_COMPANY_OS_SCORECARD.md`).
- The Daily Command Brief (`docs/founder/DAILY_COMMAND_BRIEF.md`).
- The Weekly Intelligence Review (`docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`).
- Private ops data (pipeline, cash, approvals, friction).

## Outputs
- The five loops described below, each with owner, cadence, and artifact.
- A weekly loop-completion report (5/5 expected).
- A friction list when a loop fails to complete on cadence.

## Rules
- Every loop produces a written artifact every cycle.
- A missed loop is the highest-priority bottleneck for the next week.
- The five loops are non-overlapping: an action belongs to exactly one loop.
- The CEO Loop is the integrating loop — it reads from the other four and writes the company's posture for the next week.

## Metrics
- Loop completion rate (target: 5/5 every week).
- Days late on each loop.
- Artifact quality per loop (passes the document standard).

## Evidence
- Weekly artifacts in the docs and private ops.
- Loop-completion report at the bottom of each Weekly CEO Review.
- Friction log entries for loops missed.

## The Five Loops

### Revenue Loop
- **What it does:** Source leads, run outreach, qualify, propose, close, retain.
- **Cadence:** Daily.
- **Artifact:** Pipeline tracker delta + daily DM/proposal counts.
- **Owner:** Founder + AI sales agent.

### Delivery Loop
- **What it does:** Intake → Sample → Sprint → Proof Pack → Handover → Retainer eligibility.
- **Cadence:** Per engagement; reviewed weekly.
- **Artifact:** Proof Pack per Sprint, Capital Asset registered.
- **Owner:** Founder + AI delivery agent.

### Trust Loop
- **What it does:** Classify, approve, log, audit every outward action.
- **Cadence:** Per action; reviewed weekly.
- **Artifact:** Approval log + blocked-action log + suppression list.
- **Owner:** Founder + AI trust agent.

### Learning Loop
- **What it does:** Convert weekly operating data into doctrine and decisions.
- **Cadence:** Weekly.
- **Artifact:** Weekly Intelligence Review + doctrine updates.
- **Owner:** Founder + AI learning agent.

### CEO Loop
- **What it does:** Read the four operating loops, write the daily brief, run the weekly CEO Review, set the next week's posture.
- **Cadence:** Daily brief + Weekly Review.
- **Artifact:** Daily Command Brief + Weekly CEO Review.
- **Owner:** Founder only.

## Loop Dependencies

```
Revenue Loop ──┐
Delivery Loop ─┼─→  CEO Loop ──→  Doctrine updates ──→  All loops
Trust Loop ────┤
Learning Loop ─┘
```

The CEO Loop integrates. The Learning Loop converts. The other three execute.

## Last Reviewed
2026-05-23
