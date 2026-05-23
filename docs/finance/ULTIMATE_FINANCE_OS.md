# Ultimate Finance OS

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Focused on Results.

The Finance OS is the discipline by which Dealix turns won deals
into cash and tracks the cost of producing those deals. It is owned
by the Finance Copilot agent (A2 max), governed by the policy
adapter, and surfaced via the Founder Console.

## Scope

| Concern                            | Owner                                                       |
| ---------------------------------- | ----------------------------------------------------------- |
| Invoicing                          | Finance Copilot + Founder (commitment gate)                  |
| Payment capture                    | Finance Copilot                                             |
| Cash reconciliation                | Finance Copilot                                             |
| AI unit economics                  | Finance Copilot                                             |
| Revenue recognition                | Founder + Finance Copilot                                   |
| Payment-term changes                | Founder (policy-gated)                                      |
| Refunds                            | Founder (policy-gated)                                      |
| ZATCA / invoicing compliance        | Founder + Finance Copilot                                  |

## Source files

The Finance OS reads and writes a small set of CSVs in the private
ops runtime:

| File                                  | Purpose                                                            |
| ------------------------------------- | ------------------------------------------------------------------ |
| `finance/payment_capture_queue.csv`    | Invoices issued and their status (issued, sent, paid, overdue).    |
| `finance/cash_collected.csv`           | Cash receipts, one row per receipt.                                |
| `finance/ai_unit_economics.csv`        | AI spend USD vs. deals supported; cost per deal USD.               |

The schema is detailed in `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`.

## Founder Console endpoints

| Endpoint                            | What it shows                                          |
| ----------------------------------- | ------------------------------------------------------ |
| `GET /finance/summary`              | 30-day cash collected, pipeline value, AI cost, margin health. |
| `GET /finance-ops/summary`           | Invoices open, invoices overdue, AI cost per deal.    |

Both endpoints are read-only. Mutations to terms, refunds, or
write-offs happen through founder approval, not the API.

## The cash flow

```
Won deal → Invoice issued → Invoice sent → Customer pays → Cash collected
                                       │
                                       └── overdue (>terms) → collection cadence
```

Each stage produces a row in the relevant CSV. The Finance Copilot
moves rows through the stages by appending updated rows; it does not
edit existing rows.

## Invoicing

| Aspect                          | Practice                                                       |
| ------------------------------- | -------------------------------------------------------------- |
| Trigger                         | Proposal status flips to `won` in `sales/proposal_queue.csv`.   |
| Issue                           | Finance Copilot drafts the invoice; founder approves.          |
| Send                            | Sent via the application (not via the agent directly).         |
| ZATCA                           | Saudi e-invoicing alignment per `docs/INVOICING_ZATCA_READINESS.md`. |
| Currency                        | SAR by default; USD only with founder approval.                |
| Terms                           | Default Net 14 unless contracted otherwise.                     |

A payment-term change is a policy-gated action
(`payment_terms_require_escalation`). The Finance Copilot may
propose; the founder approves.

## Payment capture

The capture queue tracks invoices through to cash. The lifecycle:

```
issued → sent → (paid | overdue)
                  │
                  └── partially_paid → paid (after remaining receipt)
```

| State              | Action                                                                 |
| ------------------ | ---------------------------------------------------------------------- |
| `issued`            | Invoice number assigned; ZATCA flow if applicable.                      |
| `sent`              | Customer notified.                                                     |
| `paid`              | Cash receipt recorded in `finance/cash_collected.csv`.                 |
| `partially_paid`    | Receipt recorded; remaining tracked.                                   |
| `overdue`           | Past terms. Collection cadence in `docs/REFUND_SOP.md` / collection SOP. |
| `write_off`         | Disallowed without founder approval recorded in audit.                  |

## Cash collection

`finance/cash_collected.csv` is the SAR-denominated ledger of cash
in. The `amount_sar` column is the primary financial signal.

| Column          | Notes                                                       |
| --------------- | ----------------------------------------------------------- |
| `id`            | Receipt id.                                                 |
| `client`        | Display name.                                               |
| `amount_sar`    | SAR amount.                                                  |
| `collected_at`  | ISO ts of receipt.                                          |
| `method`        | `bank_transfer`, `moyasar_card`, `manual_invoice`, etc.     |

The Founder Console computes the 30-day cash collected from this
file:

```
cash_collected_30d_sar = sum(amount_sar for row in rows if row.collected_at >= now - 30 days)
```

## Revenue recognition

Revenue recognition is documented in
`REVENUE_RECOGNITION_NOTES.md`. Brief summary:

- Subscription revenue is recognized over the service period.
- One-time sprint revenue is recognized on completion.
- Sample sprint revenue is recognized on milestone.
- Reservation fees are deferred until contracted scope completes.

The Finance Copilot does not auto-recognize revenue. The founder
signs off on recognition entries during the monthly close.

## AI unit economics

The AI unit economics row schema (`finance/ai_unit_economics.csv`):

| Column                | Notes                                                       |
| --------------------- | ----------------------------------------------------------- |
| `ts`                  | ISO ts of measurement.                                       |
| `ai_cost_usd`         | USD AI spend in the period.                                  |
| `deals_supported`     | Count of deals the AI motion supported.                      |
| `cost_per_deal_usd`   | Derived: `ai_cost_usd / deals_supported`.                    |

Detail is in `AI_UNIT_ECONOMICS_SYSTEM.md`. The Founder Console
surfaces the latest `cost_per_deal_usd` in the finance-ops summary.

## Cost discipline

| Cost line               | Source                                                  | Owner                |
| ----------------------- | ------------------------------------------------------- | -------------------- |
| AI inference            | Provider invoices; `finance/ai_unit_economics.csv`.     | Finance Copilot      |
| Delivery cost            | Per-sprint cost tracking (private ops, ad hoc).         | Delivery Copilot     |
| Platform infra           | Hosting invoices.                                       | Engineering          |
| Founder time             | Implicit; valued at a fixed hourly rate for analysis.   | Founder              |

The gross margin per deal is computed in the monthly close.

## Refunds

Refunds are policy-gated (`pricing_commit_requires_approval` and the
refund SOP in `docs/REFUND_SOP.md`). The Finance Copilot may propose;
the founder approves and records the approval in the audit ledger.

## ZATCA and Moyasar

- Saudi e-invoicing readiness: `docs/INVOICING_ZATCA_READINESS.md`.
- Payment integration runbook: `docs/BILLING_MOYASAR_RUNBOOK.md` and
  `docs/MOYASAR_E2E_GUIDE.md`.

The Finance OS treats the application's billing module as the
official invoicing surface. The CSV tier is the operating mirror.

## Monthly close

| Step                                 | Owner                          |
| ------------------------------------ | ------------------------------ |
| Cash collected reconciled to bank    | Finance Copilot + Founder.     |
| Invoices outstanding reviewed         | Finance Copilot.               |
| AI cost reconciled to provider invoices | Finance Copilot.            |
| Revenue recognition entries recorded  | Founder.                       |
| Margin computed                       | Founder.                       |
| Founder brief includes the close      | CEO Copilot.                   |

## What the Finance OS will not do

- Commit pricing externally without founder approval.
- Change payment terms without escalation.
- Issue a refund without policy-gated approval.
- Auto-write off an invoice.
- Send a payment reminder externally without approval.

## Discipline

1. SAR is the operating currency; USD is for AI cost only.
2. Cash collected is the truth; invoices are the path.
3. AI cost per deal is tracked at a defined threshold (see
   `AI_UNIT_ECONOMICS_SYSTEM.md`).
4. Refunds, terms, and write-offs are founder decisions.
5. The Finance OS is auditable end to end.
