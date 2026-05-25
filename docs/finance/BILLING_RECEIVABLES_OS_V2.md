# Billing & Receivables OS v2

## Relationship to existing docs
Operationalizes:
- `docs/00_constitution/NON_NEGOTIABLES.md` — "no proof, no claim" and "no growth without governance".
- `dealix/registers/compliance_saudi.yaml` — Saudi compliance constraints that gate payment paths (ZATCA Phase 2).
- `auto_client_acquisition/revops/invoice_state.py` and related modules — existing revops primitives.

## Purpose
Make sure proposals convert to paid work or clear PO / written approval.

## Objects
- quote
- invoice
- payment link
- receipt
- webhook event
- payment status
- refund request
- revenue recognition note

## Rules
- every proposal has payment path
- every payment has status
- webhook failures alert
- refund is A3 (per `dealix/trust/approval.py` classification)
- no delivery without start condition
- payment follow-ups logged daily
