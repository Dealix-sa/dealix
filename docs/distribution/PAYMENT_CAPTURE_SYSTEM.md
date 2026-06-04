# Payment Capture System

## Purpose
Convert proposals into payment, PO, or written approval.

## Follow-Up Rules
- Day 1: Confirm received.
- Day 3: Answer questions.
- Day 7: Decision request.
- Day 14: Close / recycle.

## Payment Paths
- Bank transfer.
- Invoice.
- Purchase order.
- Written approval.

## Rules
- Proposal is not cash.
- Interest is not cash.
- PO / written approval starts delivery only if risk acceptable.
- Every follow-up is logged.

## Evidence
- `private-ops/finance/payment_capture_queue.csv`
- `private-ops/revenue/cash_collected.csv`
