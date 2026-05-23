# Revenue Recognition Notes

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Focused on Results.

This document is the operating reference for revenue recognition at
Dealix. It is not an accounting standard; the auditor is the final
authority. It does, however, define how the Finance Copilot and the
founder reconcile the operating system's view of revenue to the
financial statements.

## Recognition principles

Dealix recognizes revenue when:

1. The customer has been delivered the agreed scope or the
   measurable milestone.
2. The price is fixed and determinable (no contingencies).
3. Collection is reasonably assured.
4. There is documented evidence of delivery and acceptance.

The Finance Copilot does not auto-recognize. The founder signs off
on recognition entries during the monthly close.

## Revenue types

Dealix has five revenue types. Each has a distinct recognition
pattern.

### 1. Subscription revenue (retainer)

| Aspect            | Practice                                                       |
| ----------------- | -------------------------------------------------------------- |
| Recognition       | Ratably over the service period (typically monthly).            |
| Triggers          | Customer pays for a month; service runs for that month.        |
| Deferred portion  | Any prepayment beyond the current period is deferred.          |
| Reversal          | If the customer cancels mid-period, refund per the SOP.        |

### 2. One-time sprint revenue

| Aspect            | Practice                                                       |
| ----------------- | -------------------------------------------------------------- |
| Recognition       | On sprint completion and customer acceptance.                  |
| Triggers          | Delivery handoff signed; QA gate passed.                       |
| Milestone splits   | A multi-milestone sprint may recognize at each milestone with documented acceptance. |
| Reversal          | If the sprint is aborted, recognize only the delivered portion. |

### 3. Sample sprint revenue

| Aspect            | Practice                                                       |
| ----------------- | -------------------------------------------------------------- |
| Recognition       | On milestone completion (the sample sprint has a single defined milestone). |
| Triggers          | Customer accepts the sample deliverable.                       |
| Deferred portion  | Booked but unrecognized until the milestone closes.            |

### 4. Reservation fees

| Aspect            | Practice                                                       |
| ----------------- | -------------------------------------------------------------- |
| Recognition       | Deferred until the contracted scope completes.                 |
| Triggers          | Scope delivery and acceptance per contract.                    |
| Refund            | Refundable if the scope does not start within the contracted window. |

### 5. Pass-through / reimbursable

| Aspect            | Practice                                                       |
| ----------------- | -------------------------------------------------------------- |
| Recognition       | Net basis; revenue equals the markup or fee.                   |
| Triggers          | When the underlying expense is incurred and re-billed.         |
| Documentation     | Original vendor invoice attached to the customer invoice.      |

## Source files

| File                                  | Used for                                                            |
| ------------------------------------- | ------------------------------------------------------------------- |
| `sales/proposal_queue.csv`             | Identifies what was won and at what value.                           |
| `sales/sample_queue.csv`               | Identifies sample sprint state.                                     |
| `finance/payment_capture_queue.csv`    | Invoice state.                                                      |
| `finance/cash_collected.csv`           | Cash receipts.                                                      |
| Customer contracts (object storage)    | Authoritative scope and term.                                        |

The CSV tier is the operating mirror; the contract is the legal source.

## Recognition pattern matrix

| Revenue type        | Cash received | Service delivered | Recognized? |
| ------------------- | ------------- | ----------------- | ----------- |
| Subscription        | Yes           | Partial            | Pro-rata.   |
| Subscription        | Yes           | Yes                | Full month. |
| Subscription        | No            | Yes                | Accrual; revenue recognized, AR open. |
| Sprint              | Yes           | Partial            | At completed milestones only. |
| Sprint              | Yes           | Yes                | Full.       |
| Sprint              | No            | Yes                | Accrual; AR open. |
| Sample sprint        | Yes           | Yes (milestone)   | Full at milestone. |
| Sample sprint        | Yes           | No                 | Deferred.   |
| Reservation         | Yes           | Not started        | Deferred.   |
| Reservation         | Yes           | Started            | Pro-rata against milestone. |

## Monthly close steps

| Step                                                              | Owner                |
| ----------------------------------------------------------------- | -------------------- |
| Reconcile cash collected to bank statement                         | Finance Copilot.     |
| Reconcile invoices issued to Postgres `invoices`                    | Finance Copilot.     |
| List sprints completed in the month                                | Delivery Copilot.    |
| Apply recognition patterns to each closed sprint                   | Founder.             |
| Apply ratable recognition for retainer customers                    | Founder.             |
| Record deferred revenue balance                                    | Founder.             |
| Generate the monthly revenue report                                | Finance Copilot.     |
| Founder signs the report                                            | Founder.             |
| The signed report is referenced in the next founder brief           | CEO Copilot.         |

## Audit trail

Each recognition entry corresponds to an audit row in
`trust/approval_decisions.csv`:

| Action                   | Payload reference                                              |
| ------------------------ | -------------------------------------------------------------- |
| `revenue_recognize`       | Sprint id or sample id or retainer period.                     |
| `revenue_defer`           | Reservation id; window.                                        |
| `revenue_reverse`         | Sprint id and reason.                                          |
| `invoice_issue`           | Invoice number; deal id.                                       |
| `invoice_write_off`       | Invoice number; reason; founder approval.                      |

## Currency

- Operating currency is SAR.
- USD invoices are allowed only with founder approval.
- AI cost is USD; reported separately in unit economics.

## Tax and compliance

- Saudi VAT applies per the registered tax position.
- ZATCA e-invoicing readiness per `docs/INVOICING_ZATCA_READINESS.md`.
- Cross-border transfers per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Refunds

Refunds reverse previously recognized revenue. The reversal is
recorded as `revenue_reverse` with `risk: medium`. The SOP is in
`docs/REFUND_SOP.md` and the policy gate is
`pricing_commit_requires_approval`.

## What the Finance Copilot will not do

- Auto-recognize revenue.
- Auto-defer revenue.
- Process refunds without founder approval.
- Change recognition timing for a closed period.

## Discipline

1. Recognize when delivered and accepted, not when invoiced.
2. Defer prepayments; never accelerate.
3. Document every entry against a sprint id, milestone id, or
   retainer period.
4. Reversals are normal; misclassification is not.
5. Auditor authority is final.

## Cross-references

- `ULTIMATE_FINANCE_OS.md` for the broader finance discipline.
- `AI_UNIT_ECONOMICS_SYSTEM.md` for the cost side.
- `RENEWAL_AND_EXPANSION_OS.md` for retainer renewals.
- `docs/INVOICING_ZATCA_READINESS.md` for ZATCA alignment.
