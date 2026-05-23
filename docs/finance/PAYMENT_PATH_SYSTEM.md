# Payment Path System

## Purpose
A repeatable, low-friction path from accepted proposal to confirmed payment.

## Accepted methods
1. **Bank transfer (SAR)** — preferred for proposals ≥ 1,500 SAR.
2. **Moyasar / Tap / similar gateway** — for under 5,000 SAR if needed.
3. **PO + invoice 30 days** — only after explicit founder approval.

## Path steps
1. Buyer confirms acceptance in writing (email, signed proposal, or PO).
2. Founder sends a simple invoice (PDF or written-out terms).
3. Buyer pays.
4. Bank statement confirmed; row added to `revenue/cash_collected.csv` with `status=Confirmed`.
5. Evidence row added to `evidence/execution_evidence_ledger.csv`.

## SLA targets
- Invoice sent within 24 hours of acceptance.
- Payment received within 14 days for transfer, 30 days for PO.
- Receipt issued within 48 hours of confirmation.

## Trust requirements
- No "verbal yes" counts as revenue until cash is received OR a PO is on file.
- Discounts off list price logged in `finance/discount_log.csv` with approver.
- Refund or cancellation requires written record and Trust workflow approval.

## VAT
- VAT-registered as required by KSA law.
- VAT line is itemized on every invoice.

## Cash discipline
See `docs/finance/CASH_DISCIPLINE_SYSTEM.md` for monthly close routines.

## Dispute handling
- Customer dispute → immediate pause of delivery; investigate; written record.
- Bad debt → write-off process documented after 90 days unpaid.
