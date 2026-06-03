# Cash Rules

## Purpose
Protect Dealix from doing unpaid work, mispriced work, or work that hurts trust.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Core Rules
1. No full delivery without one of: payment received, PO issued, written approval from authorized buyer.
2. Free Diagnostic is the only zero-cash offer; it stops after one round per lead.
3. Discounts require founder approval and a logged reason.
4. Refunds require founder approval; the reason is logged in revenue/refund_log.csv.
5. Payment must be reconciled within 48 hours of receipt.
6. Any revenue from a known bad-fit client must be flagged in BAD_REVENUE_FILTER review.
7. Capital expense above 1,000 SAR requires explicit founder approval.

## Payment Channels
- Bank transfer (preferred for invoices >= 1,500 SAR)
- Moyasar / online payment link
- Manual receipt (with PO copy stored)

## Reconciliation
- revenue/cash_collected.csv is the source of truth for cash.
- revenue/pipeline_value.csv tracks expected (not yet cash) value.
- revenue/mrr_tracker.csv tracks recurring monthly revenue.
- Reconcile weekly against bank statement.

## Escalation
- Late payment > 14 days: founder follow-up with safe language (no threats, no fees added).
- Failed payment attempt: investigate root cause before retrying.

## Linked Systems
- docs/revenue/REVENUE_CONTROL_SYSTEM.md
- docs/revenue/BAD_REVENUE_FILTER.md
- docs/trust/APPROVAL_MATRIX.md

## Last Reviewed
2026-05-23
