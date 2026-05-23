# Payment Capture OS

The Payment Capture OS owns the flow from "closed-won" to "cash in
bank." It coordinates invoicing, reconciliation, payment terms, and
ZATCA-aligned record keeping. It does not move money on its own.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Capture every closed-won opportunity into a clean invoicing and
collection process. Reconcile receipts against expected payments.
Surface aging issues to the founder. Never commit to refunds, term
changes, or write-offs without approval.

## 2. Input

Sources:

- `sales/pipeline.csv` (rows at stage = closed_won).
- `contracts/{opportunity_id}/` (signed contracts).
- `product/offer_ladder.csv` (price reference).
- `finance/payment_terms_library.csv` (sanctioned terms).
- `finance/bank_statement_imports/` (bank statement files imported by
  operator).
- `finance/zatca_config.yaml` (e-invoicing configuration).

Each closed_won opportunity is automatically pushed into the capture
queue.

## 3. Output

Queues and ledgers:

- `finance/payment_capture_queue.csv` — invoices to be issued.
- `finance/cash_collected.csv` — collected payments matched to
  opportunities.
- `finance/aging_report.csv` — invoices outstanding and aging.
- `finance/refund_queue.csv` — refund requests (approval-gated).
- `finance/ai_unit_economics.csv` — AI cost reconciliation (separate
  scope).

`finance/payment_capture_queue.csv` columns:

- `invoice_id`
- `opportunity_id`
- `account_id`
- `amount`
- `currency`
- `terms_id`
- `due_at`
- `state` — drafted | issued | partial | paid | overdue | written_off
- `zatca_status` — pending | submitted | accepted | rejected
- `approval_state`
- `drafted_by`
- `issued_at`
- `paid_at`
- `notes`

## 4. Source of truth

`finance/payment_capture_queue.csv` for capture state.
`finance/cash_collected.csv` for confirmed receipts. Bank statements
remain the source of truth for cash; the queue mirrors them.

## 5. Approval class

A2 for invoice drafting and reconciliation. A3 banned. Every external
finance action — issuing the invoice, sending the e-invoice to ZATCA,
issuing a refund — is approval-gated. Policy rule
`pricing_commit_requires_approval` applies.

## 6. Trust gate

- Price integrity: amount must match the signed contract and the
  sanctioned offer/price band.
- Terms integrity: terms_id must reference a sanctioned terms entry;
  deviations require founder approval (policy rule
  `payment_terms_require_escalation`).
- ZATCA compliance: every invoice submission must pass the configured
  schema.
- Reconciliation discipline: cash without a matched invoice is held;
  invoice without a matched contract is blocked.
- Refund: every refund requires founder approval and a documented
  reason (policy rule `pricing_commit_requires_approval` covers
  refund_commit).

## 7. Owner

`finance_copilot` agent. Allowed write target: `finance/`.

## 8. Worker

`scripts/dealix_payment_capture.py` (planned). The worker:

1. Reads new closed_won opportunities.
2. Drafts invoices.
3. Submits ZATCA-side when approved.
4. Reconciles imported bank statements against the queue.
5. Updates aging and ledger states.

## 9. KPI

- Days Sales Outstanding (DSO).
- Capture Cycle Time (closed_won -> invoice issued).
- Reconciliation Accuracy (target: 100%).
- ZATCA Acceptance Rate (target: 100%).
- Refund Rate (target: low; tracked).
- Aging Overdue Count.

## 10. Failure mode

- Amount mismatch (invoice vs. contract). Worker rejects; founder
  reviews.
- Off-menu terms. Worker rejects without approval.
- ZATCA rejection. Worker captures the reason; correction sprint.
- Unmatched cash. Held; operator-assisted match.
- Refund proposed without approval. Worker blocks; founder reviews.

## 11. Recovery path

- For amount mismatch: contract authoritative; ledger entry; rewrite.
- For off-menu terms: founder approval and ledger entry, or revert to
  sanctioned terms.
- For ZATCA rejection: correction filed; root cause analysis.
- For unmatched cash: operator-assisted match; ledger entry.
- For refund without approval: blocked; ledger entry; root cause.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Reconciliation; aging update |
| Weekly | Aging review with founder |
| Monthly | DSO and refund review |
| Quarterly | ZATCA posture and terms library audit |

## 13. Saudi specifics

- ZATCA e-invoicing is the default; integration follows the local
  schema.
- VAT handling is captured per offer; the offer ladder records VAT
  posture.
- Payment terms are conservative; the library favours upfront or
  milestone billing.

## 14. Non-negotiables

- No invoice without a signed contract.
- No refund without founder approval.
- No off-menu terms without approval.
- A3 not used.
- No external finance action by an agent.

The OS does not move money. It produces a clean, reconciled record of
the money that has moved, and it surfaces decisions to the founder.
