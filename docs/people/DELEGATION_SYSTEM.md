# Delegation System

A delegation is a contract, not a hope. Every delegation has the same shape.

## The contract template

| Field | Notes |
|---|---|
| Mission | Why this exists, in one sentence |
| Inputs | What the operator receives (data, briefs, decisions) |
| Outputs | What the operator produces, in observable units |
| Weekly scorecard | 3–5 measurable rows that grade outputs |
| Handoff format | Where outputs land (file, ledger, system) |
| Quality bar | The minimum that counts as "done" |
| Cadence | Daily / weekly check-ins |
| Trial length | 30 days for first delegation; 14 days for follow-ups |
| Decision link | UUID of the [`DECISION_LOG_SYSTEM`](../founder/DECISION_LOG_SYSTEM.md) entry that authorized it |

## Roles to delegate first

Recommended order based on highest CEO-hour drain:

1. **Sales asset designer** — proposals, decks, samples (formatting & polish)
2. **Saudi B2B researcher** — strategic account list maintenance
3. **RevOps assistant** — pipeline tracker hygiene, follow-up queue
4. **Delivery coordinator** — handoff from sale to delivery, retainer rhythm
5. **Trust / QA reviewer** — approval queue triage, evidence completeness
6. **Frontend polish engineer** — non-differentiated UI work
7. **Data ops assistant** — CSV health, source freshness

Each role's full scorecard lives in `data/role_scorecards/<role>.md` (gitignored
template) — the slim version is in this directory.

## Anti-patterns

- Delegating a task with no SOP — write the SOP first, then delegate
- "Just do what I would do" — judgement-heavy work needs coaching, not delegation
- Weekly check-ins that are status updates, not scorecards — use the scorecard

## Cross-references

- [`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)
- [`docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`](../founder/FOUNDER_LEVERAGE_DASHBOARD.md)
- [FOUNDER_BOTTLENECK_REMOVAL](FOUNDER_BOTTLENECK_REMOVAL.md)
- [HIRING_TRIGGER_SYSTEM](HIRING_TRIGGER_SYSTEM.md)

## Non-negotiables

Delegations that touch customer-facing actions still require the existing
approval-center gates. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
