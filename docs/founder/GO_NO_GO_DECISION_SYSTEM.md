# Go / No-Go Decision System

> The system that decides whether a major step happens.
> Anything that costs money, time > 1 week, or touches a customer.

## When to use

Trigger this system for:

- Hiring (even part-time)
- Spending > 2,000 SAR/month recurring
- Signing a contract > 5,000 SAR
- Launching a new offer rung
- Killing or pausing an existing rung
- Releasing a new AI agent capability to clients
- Public announcement (LinkedIn case study with named client)
- Geographic / vertical expansion

## The Five Gates

Each gate must be answered in writing, by the founder, before "Go".

### Gate 1 — Revenue Logic
- What revenue does this directly or indirectly produce within 90 days?
- Whose budget does it come from?
- If it produces no revenue in 90 days, why are we doing it now?

### Gate 2 — Delivery Logic
- Can we deliver this **today** at the quality our customers expect?
- If no, what is the gap, and how long to close it?

### Gate 3 — Trust Logic
- Does this require any new overclaim risk, agent autonomy, or
  data exposure?
- What is the rollback if trust breaks?

### Gate 4 — Learning Logic
- What will we learn from this that we cannot learn cheaper?
- What is the cheapest possible version of this experiment?

### Gate 5 — Capital Logic
- Cost in cash: _…_
- Cost in founder hours: _…_
- Opportunity cost (what we will *not* do because of this): _…_

## Decision Output

Write the decision in `dealix-ops-private/founder/decision_queue.md` with:

```
- id: yyyy-mm-dd-NN
  decision: ...
  outcome: GO / NO-GO / DEFER
  evidence:
    - ...
  cost_cash: ...
  cost_hours: ...
  opportunity_cost: ...
  reversal_trigger: ...
  review_date: ...
```

## Reversal Rules

- Every Go decision has a **reversal trigger** (a metric that, if hit,
  reverses the decision).
- Every No-Go decision has a **revisit trigger** (a metric that, if hit,
  reopens the decision).
- Defer decisions list the **evidence required** to convert to Go or No-Go.

## Anti-Patterns To Refuse

- "Let's just try it" without a reversal trigger.
- "We can always undo it" for irreversible actions (hires, public claims).
- "It's only a small amount" for recurring costs.
- "Strategic" used as a synonym for "I cannot justify revenue".
