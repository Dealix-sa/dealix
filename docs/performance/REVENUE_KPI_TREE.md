# Revenue KPI Tree

A small, defensible tree. Everything ties to a ledger.

## L0 — North star

- **Compounding-Approved Revenue (CAR)** — SAR captured this quarter
  that traces back to a Dealix-approved draft or scoring run.

## L1 — Drivers

1. **Pipeline coverage** — tier-A account count × expected band.
2. **Approval throughput** — approvals / day.
3. **Approval-to-meeting rate**.
4. **Meeting-to-proposal rate**.
5. **Proposal-to-sign rate**.
6. **Sign-to-captured rate**.
7. **Retention rate** (logo + net).
8. **Referral acceptance rate**.

## L2 — Counter-metrics (must not regress)

- Voice violation rate (brand guardian).
- PDPL opt-out compliance rate (must be 100 %).
- ZATCA acceptance rate (must be 100 %).
- Time-from-reply-to-action.
- Drafts blocked by trust guardian per week.

## L3 — Source ledgers

- `growth/account_scores.csv`
- `distribution/*_queue.csv`
- `governance/approvals.csv`
- `revenue/proposal_register.csv`
- `revenue/payment_register.csv`
- `revenue/retention_register.csv`

## L4 — Refresh cadence

Weekly (Monday). The performance_analyst publishes a snapshot
PDF + JSON for the founder console.
