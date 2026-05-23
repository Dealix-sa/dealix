# Proposal Follow-Up Rule

> Every proposal has a written follow-up date. No exceptions.

## Cadence

| Day | Action |
|-----|--------|
| 0 | Send proposal |
| +2 | Light note: "Any questions on the scope?" |
| +5 | Founder personal note: "What is the decision blocker?" |
| +7 | Decision request: yes / no / specific blocker |
| +14 | Proposal expires |

## When to stop

- Customer says no (clearly).
- Customer asks for a multi-week pause.
- Day +14 with no response.

## When to re-engage (after expiry)

Re-engagement is fresh discovery, not "bumping" the old proposal.

- New proposal requires a new discovery touch.
- A re-engagement message that says "checking in" is not allowed.

## Tracking

In `dealix-ops-private/sales/proposal_followups.csv`:

```
proposal_id, sent_date, day_2_done, day_5_done, day_7_done, outcome, outcome_date, loss_reason
```

## Anti-Patterns

- "Just bumping this to the top of your inbox."
- "Did you have a chance to look?"
- Daily follow-ups.
- Sending proposal #2 before #1 was decided.
- Letting a proposal go stale without an outcome.

## Operational

The CEO Command Center surfaces any proposal past its follow-up SLA.
The founder action is to **close it one way or the other**, not to
"keep it alive".
