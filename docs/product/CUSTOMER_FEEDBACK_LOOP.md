# Customer Feedback Loop

> How customer feedback becomes product decisions (or doesn't).

## Capture Points

| Touchpoint | Capture mechanism | Storage |
|---|---|---|
| Discovery call | Founder notes | `sales/call_notes/{date}-{client}.md` (private) |
| Sprint handoff call | `CASE_STUDY_CAPTURE.md` | `clients/{client}/handoff-notes.md` |
| Managed Ops monthly call | Working session notes | `clients/{client}/monthly_summary-{month}.md` |
| Quarterly review (Revenue Desk) | Advisor + founder notes | `clients/{client}/quarterly-{Q}.md` |
| Inbound message / DM | Founder notes | `learning/inbound_feedback.md` |
| Lost-deal call (whenever possible) | `pipeline/win_loss_log.md` | private |

## Classification

Every captured feedback gets classified within 48 hours:

- **Affirmation** — confirms current direction (log + move on)
- **Frustration** — points to a real problem (intake row)
- **Feature request** — asks for something specific (intake row)
- **Pricing signal** — feels too expensive / too cheap (pricing_experiments)
- **Trust signal** — concerns about our model, claims, data (Trust review)
- **Out of scope** — not our problem; log for partner referral list

## From Feedback To Decision

```
Feedback → Classification → Intake row (if actionable) → Triage → Build / Defer / Kill
```

Threshold for action:
- **1 customer feedback** → log + watch
- **2 customers same theme** → intake row
- **3+ customers same theme** → escalate to Weekly CEO Review

## Feedback That Skips Aggregation

These need same-day response regardless of count:
- Trust concern (privacy, claim, data)
- Cancellation reason
- Negative public mention
- Refund request
- Incident report

## Feedback Anti-Patterns

- "Customer X wants this" → who, when, in what context? (require source)
- "Everyone is asking" → name 3 (require specifics)
- Founder gut-pattern recognition → log it as a hypothesis, validate with explicit asks
- Building on internal team intuition without external validation → log as `experiment`, not as `build`

## Closing The Loop

When we build something based on customer feedback:
1. Tell the customer when it ships
2. Ask: "Does this resolve what you raised?"
3. Capture the answer in `learning/`
4. If it didn't resolve: re-open the intake

When we **don't** build something:
1. Tell the customer the decision
2. Give the reasoning (Strategy Filter)
3. Offer alternative if there is one
4. If they're a fit, this often increases trust (we say no with clarity)

## Customer Advisory Patterns

For Managed Ops customers month 3+:
- Quarterly product session (30 min)
- Walk through what's coming, what we deferred, what we killed
- Capture which deferred items they'd vote up
- Use as input to product roadmap (with explicit attribution)

## Metrics

- Feedback captured this month: target ≥ 1 per active customer
- Feedback classified within 48 hr: target 100%
- Intake rows from feedback per month: track trend
- Build-from-feedback ratio: track (too high = we're a customer-driven order-taker; too low = we're not listening)

## Review Cadence

- Daily: any urgent (Trust / cancellation / refund)
- Weekly: classification of captured feedback
- Monthly: feedback themes → product roadmap input
- Quarterly: close-the-loop check with active customers

## What This Refuses

- Building everything customers ask
- Building nothing customers ask
- Letting feedback decay without classification
- Inventing customer wants
- Treating one customer's strong opinion as a quorum
