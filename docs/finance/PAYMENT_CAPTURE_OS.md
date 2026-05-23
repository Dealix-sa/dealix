# Payment Capture OS

The Payment Capture OS is the system that moves a signed contract to a cleared invoice. It is the most consequential gate in the Revenue Factory because every error has a financial and a legal tail.

**Source of truth:** `$PRIVATE_OPS/payments_ledger.csv`
**Owner:** Founder
**Trust gate:** A2 — any change to payment terms, refund, or invoice issuance requires explicit founder approval.

## Channels

| Channel | Use | Reconciliation source |
|---------|-----|----------------------|
| SAR bank transfer | Default for Saudi clients | Bank statement export |
| SADAD | Government and large enterprise | SADAD reference number |
| Card | Online checkout (rare) | PSP report |
| International wire | Cross-border (rare) | SWIFT advice |

Cash payments are not accepted.

## Capture flow

1. Contract signed (`docs/revenue/PROPOSAL_FACTORY.md` stage 6).
2. Invoice generated from template with reference number, VAT line, and payment instructions.
3. Founder approves invoice (A2).
4. Invoice sent to client.
5. Payment received and matched to reference number in `payments_ledger.csv`.
6. Status set to `cleared`. Delivery is unblocked.

Delivery does not begin until status is `cleared` unless the founder explicitly authorises a deposit-trigger start, logged in `$PRIVATE_OPS/early_start_exceptions.csv`.

## VAT and invoicing

Invoices comply with ZATCA e-invoicing requirements where applicable. The invoice template carries:

- Tax registration number.
- Buyer details including VAT number where supplied.
- Itemised line items.
- VAT line at the prevailing rate.
- Total in SAR.
- Payment instructions.

## Reconciliation cadence

- **Daily:** automated match against bank export. Unmatched entries surface for founder review.
- **Weekly:** founder reviews aged receivables.
- **Monthly:** full close, archived to `$PRIVATE_OPS/finance_archives/YYYY-MM/`.

## Failure modes

- **Mis-match:** payment received but reference number does not align with any open invoice. Detection: daily reconciliation job. Recovery: founder investigates; if no match within 5 business days, payment is held in suspense.
- **Double payment:** client pays twice. Detection: reconciliation. Recovery: founder authorises refund; logged in `payments_ledger.csv` with reason.
- **Refund request:** client asks for partial or full refund. Detection: inbound request. Recovery: founder reviews against contract; A2 approval required; refund executed and logged.
- **Currency mismatch:** invoice in SAR, payment in another currency. Detection: reconciliation. Recovery: founder decides whether to absorb conversion cost or invoice difference.

## Recovery path

If the payment ledger becomes inconsistent (PSP reconciliation outage, bank export schema change), the founder freezes new invoice issuance until reconciliation is restored. No delivery begins on unverified payment.

## Audit

Every row in `payments_ledger.csv` carries: `invoice_id`, `client_id`, `amount_sar`, `vat_sar`, `channel`, `reference`, `received_at`, `cleared_at`, `approved_by`, `notes`. Rows are append-only. Edits create a new row with reason.

## Metrics

- Days sales outstanding (DSO) — median and worst.
- Aged receivables buckets (0-30, 31-60, 61-90, 90+).
- Refund rate (count and SAR) over rolling 90 days.
- Reconciliation lag (median hours from bank credit to ledger match).

## Disclaimer

Payment Capture OS reports verified cash. Projected revenue is estimated only. Dealix does not guarantee specific cash collection timing. Estimated value is not Verified value.
