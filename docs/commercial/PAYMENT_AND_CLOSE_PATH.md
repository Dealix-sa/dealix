# Payment & Close Path (manual, evidence-based)

The close path is a chain of **evidence events**. Each event is recorded only when
it really happens. Revenue is recognized only at `payment_received`.

## Evidence chain
1. `lead_identified`
2. `message_drafted`
3. `human_approved`
4. `message_sent_manually`
5. `call_booked`
6. `invoice_sent`
7. `payment_received`  ← revenue recognized here, and only here
8. `work_delivered`
9. `proof_pack_delivered`
10. `follow_up_scheduled`

## Manual payment SOP
- Confirm scope in writing (draft).
- Prepare a manual invoice draft — do **not** auto-issue.
- Share manual payment details only after founder approval.
- Record `payment_received` once the payment is actually confirmed.
- **No live charge is enabled.** All payment steps are manual.

## Evidence file
`data/money_now/evidence_events.json` — schema
`dealix.money_now.evidence_events.v1`. Seeded empty; the founder appends real
events. Never fabricate events.
