# Proposal Conversion System

## Purpose
Turn engaged prospects into proposals, and proposals into cash.

## Proposal anatomy
1. **Outcome** — one sentence on what will be true after the engagement.
2. **Scope** — what is in and what is out.
3. **Deliverables** — concrete artifacts the client will receive.
4. **Price** — fixed price referencing the product ladder.
5. **Timeline** — start date, milestones, end date.
6. **Terms** — payment terms, IP, confidentiality.

## Templates
Per-offer templates live in `dealix-ops-private/sales/proposal_notes/`.

## Pricing
- Defaults from `docs/finance/PRICING_ARCHITECTURE.md`.
- Discounts only per `docs/finance/DISCOUNT_POLICY.md`.

## Approvals
- Any custom build proposal > 10,000 SAR requires founder approval logged in `trust/approval_log.csv`.
- Any retainer beyond 12 months requires the same.

## Tracking
- All proposals enter `sales/proposal_tracker.csv` with status `Draft` first.
- Promote to `Sent` when delivered to the buyer.
- Always set `follow_up_date`.

## Follow-up cadence
- Day 0: send.
- Day 3: a soft check-in.
- Day 7: an explicit "are you in?" close.
- Day 14: "should we close this out?" close-or-park decision.

## Bad proposal patterns to avoid
- Vague outcome ("we will help you grow").
- No fixed price (only an hourly rate).
- No timeline.
- "Discount if you sign this week" pressure tactics.

## Capital asset
Every won proposal is recorded as a capital asset row in `evidence/execution_evidence_ledger.csv`.
