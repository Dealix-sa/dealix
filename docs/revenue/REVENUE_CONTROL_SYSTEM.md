# Revenue Control System

## Purpose
Ensure every Dealix activity is connected to a verifiable revenue motion.

## Principles
- Revenue first. Systems second.
- Every lead has a stage and a next action.
- No work begins without payment, PO, or written approval.
- Evidence precedes celebration.
- Pipeline truth lives in the private ledger, not in narratives.

## Pillars

### 1. Pipeline Integrity
- Stages match `docs/revenue/PIPELINE_STAGES.md`.
- Every active record has `next_action`, `owner`, `next_action_date`.
- Stage movement requires evidence (reply, sent proposal, signed approval).

### 2. Revenue Action Discipline
- Every working day records at least one revenue-moving action.
- Revenue actions are logged in `dealix-ops-private/revenue/revenue_action_log.csv`.
- Outbound activity is counted, not estimated.

### 3. Cash Rules
- Cash rules are defined in `docs/revenue/CASH_RULES.md`.
- No customization or extension beyond scope without an approved change request.
- Refunds, discounts, and write-offs require founder approval.

### 4. Proposal Hygiene
- Every proposal has scope, price, start condition, and follow-up cadence.
- Proposals follow `sales/proposal_followup_rule.md`.
- No proposal sent without a recorded follow-up date.

### 5. Founder Sales Motion
- Founder-led DMs, calls, and proposals are the primary motion.
- No paid acquisition before product-market signal.
- Calls are anchored on the `Founder Sales Call One-Pager`.

## Daily Revenue Gate
At end of day, the founder confirms:
1. Pipeline updated.
2. At least one revenue action logged.
3. Approvals queue reviewed.
4. Tomorrow's revenue focus picked.

## Weekly Revenue Gate
At end of week, the founder confirms:
- Pipeline value updated.
- Won / lost reasons captured.
- One learning decision recorded.
- One system update committed.

## Evidence
- `dealix-ops-private/pipeline/pipeline_tracker.csv`
- `dealix-ops-private/revenue/revenue_action_log.csv`
- `dealix-ops-private/sprint/sprint_scorecard.csv`
- `dealix-ops-private/learning/weekly_intelligence_review.md`

## Last Reviewed
2026-05-23
