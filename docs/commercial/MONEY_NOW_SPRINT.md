# Money Now Sprint

**Goal:** get Dealix to first real paid revenue safely and quickly.
**Mode:** draft-only, approval-first. Nothing is sent or charged automatically.

## Primary closeable offer
- **Revenue Proof Sprint — 499 SAR.** Low price, clear scope, manual delivery.
- We expect it to be the fastest path to a first `payment_received` event.

## What the engine generates each run
Run: `python scripts/commercial/run_money_now_sprint.py`

- Today's top closeable offer.
- Up to 10 target prospect slots (founder fills real warm-list names).
- A personalized draft message per prospect (AR).
- Manual payment / invoice checklist.
- Evidence-event checklist (see `PAYMENT_AND_CLOSE_PATH.md`).
- Proof-pack delivery checklist.
- Follow-up queue.

Outputs land in `reports/money_now/` (gitignored; founder reviews before sharing).

## Revenue recognition rule (non-negotiable)
Revenue is **only** recognized when a `payment_received` evidence event exists in
`data/money_now/evidence_events.json`. A drafted or manually-sent message never
counts as revenue.

## Safety
No auto-send. No live charge. No fake customers — prospect slots are empty labels
until the founder fills real names. Verify with
`python scripts/commercial/verify_money_now_sprint.py`.
