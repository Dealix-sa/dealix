# Client Feedback Loop

> How we capture and act on what clients tell us.
> Pairs with `docs/product/CUSTOMER_FEEDBACK_LOOP.md` (which covers all customer feedback including non-active).

## Capture Points (active clients)

- Day-7 handoff call (Sprint)
- Weekly report reply (Managed Ops)
- Monthly working session (Managed Ops)
- Quarterly review (Revenue Desk)
- Cancellation conversation (any)

## Capture Tool

For each captured feedback:
```yaml
captured_at: YYYY-MM-DD
client: {client_name}
context: handoff | weekly_reply | monthly_session | quarterly_review | cancellation
verbatim: |
  "..."
themes:
  - product
  - delivery
  - pricing
  - trust
  - other
classification: affirmation | frustration | feature_request | pricing_signal | trust_signal | out_of_scope
action_required: yes | no
action_taken: |
  ...
follow_up_due: YYYY-MM-DD
```

Stored in `clients/{client}/feedback.md` (private).

## Action Within 48 Hours

For every "action_required: yes":
- Founder responds to client acknowledging the input
- If feature request → opens intake row (per `FEATURE_INTAKE.md`)
- If pricing signal → logs in `pricing_experiments.md`
- If trust signal → logs in `trust/data_incidents.md` if severe
- If out of scope → notes for partner referral list

## Aggregation

- Monthly: pattern review across all clients
- Quarterly: themes feed Product Roadmap

## Closing The Loop

When we act on feedback:
- Tell the client: "We made the change you suggested; here's what it looks like"
- Ask: "Does this resolve it?"
- Capture answer

When we don't act:
- Tell the client why (Strategy Filter)
- Offer alternative if any
- Reaffirm the relationship

## Patterns That Trigger Escalation

- 2+ clients raise same frustration → intake row + Weekly Review
- 1 client raises trust concern → same-day founder review
- 1 cancellation → root cause + learning entry
- 1 unsolicited testimonial → case study capture + content opportunity

## What This Refuses

- "Survey fatigue" mass forms (we listen, we don't poll)
- Treating one client's preference as the company direction
- Quiet abandonment of received feedback
- Defending against feedback instead of using it
