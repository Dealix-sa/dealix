# Cash Control

> The bank account is the company. Treat it like one.

## Bank Accounts

- One operating account (SAR).
- One reserve account (SAR) — minimum balance = 1 month operating costs.
- (Optional) one USD account once international invoicing is recurring.

All accounts are in the legal entity name. None are in the founder's
personal name.

## Signatories

- Single signatory currently (founder).
- Add a second signatory when the team grows (T3 decision).

## Transfers

- Outbound transfers > 5,000 SAR require a written line in
  `dealix-ops-private/finance/transfers_log.md` with: amount, recipient,
  purpose, evidence link.
- Outbound transfers > 25,000 SAR require T3 decision + 24h cool-off
  (founder writes the decision, sleeps on it, then executes).
- We do **not** transfer to personal accounts of the founder except
  documented salary / dividend distributions.

## Reserve Discipline

- Reserve = minimum 1 month operating costs at all times.
- If operating account falls below 1 month operating costs:
  - Stop discretionary spending.
  - Founder reviews `CAPITAL_ALLOCATION.md`.
  - Escalate cash collection efforts.

## Founder Compensation

- Founder draws a fixed monthly salary, documented in
  `dealix-ops-private/finance/founder_compensation.md`.
- Variable distributions (dividends) require an annual decision in the
  monthly strategy review of December (or fiscal year end).

## Tax

- Saudi corporate tax / zakat handled by external accountant.
- Monthly: founder confirms accountant has the necessary inputs.
- Annual: founder confirms filings are on time.

## Bank Audit

- Monthly: founder reconciles bank statement to `cash_collected.csv` and
  `expenses.csv`. Discrepancies are investigated and logged.

## Anti-Patterns

- Paying expenses from personal card without reimbursement workflow.
- Holding customer payments on personal account.
- Withdrawing cash with no documented purpose.
- Skipping the reconciliation because "it has been a busy month".
