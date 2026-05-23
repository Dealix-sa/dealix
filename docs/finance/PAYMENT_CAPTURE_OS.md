# Payment Capture OS | نظام تحصيل المدفوعات

## Purpose | الغرض
Move accepted proposals into invoices, payment links, captured payments, and
reconciled cash. Run polite payment follow-ups when overdue. Never commit to
pricing or terms outside what the founder has explicitly approved.

## Inputs | المدخلات
- Accepted proposal (from Proposal Factory)
- Client billing details (legal name, VAT, address, contact email)
- Payment method preference (bank transfer, card via Moyasar, other)
- Standard invoice & payment-terms template
- ZATCA / VAT readiness data

## Outputs | المخرجات
- `finance.invoices`: invoice_id, client_id, proposal_id, amount, currency,
  zatca_id, payment_link, state, issued_at, paid_at
- `finance.payments`: payment_id, invoice_id, method, captured_at,
  reconciliation_state
- Payment follow-up drafts (queued for founder approval)
- Per-payment reconciliation note

## Invoice lifecycle | دورة حياة الفاتورة
1. Proposal accepted → invoice drafted
2. Founder approves invoice (A2)
3. Invoice issued to client (email draft + payment link)
4. Payment captured via provider
5. Reconciliation: amount, currency, FX rate, VAT, ZATCA confirmation
6. Marked paid; engagement may proceed to Delivery

## Payment follow-up | متابعة الدفع
- Day 0: invoice issued
- Day 7: gentle reminder draft (if unpaid)
- Day 14: follow-up draft, founder reviews
- Day 21: founder-personal note draft
- Day 30: escalation draft, possibly pause delivery pending payment
- All drafts founder-approved before send

## Refund handling | معالجة الاسترداد
- Refund requests routed to founder immediately
- Refund decision is always A2 (founder approval)
- Refund execution logged + reconciled
- Refund reasons categorized for monthly review

## Data source | مصدر البيانات
`finance.invoices`, `finance.payments`, `finance.reconciliations`,
`crm.proposals`.

## Approval class | فئة الموافقة
- A1: drafting invoices, drafting reminders, reconciliation calculations
- A2: every invoice issue, every payment-link creation, every reminder send,
  every refund
- A3: any non-standard term, any pricing deviation, any payment > stated cap

## Trust gate | بوابة الثقة
- Invoice amount must match accepted proposal (or have founder note)
- VAT/ZATCA correctness check before issue
- No payment link generated outside founder-approved processor
- No promises in reminder language ("guaranteed delivery on payment")
- Policy snapshot + audit row per state transition

## Owner | المالك
Founder approves every external finance touch.

## Worker name
`finance.payment_capture_os`

## KPI | المؤشرات
- DSO (Days Sales Outstanding) — target ≤ 21
- % invoices paid on time (≤ 14 days)
- % invoices requiring follow-up beyond 30 days
- Refund rate (should remain low)
- Reconciliation accuracy (target 100%)

## Failure mode | حالات الفشل
- Invoice amount drifts from proposal due to manual override
- Payment captured but not reconciled within 48h
- Reminder cadence sends despite payment having landed

## Recovery path | مسار الاسترداد
- Pre-issue diff check: invoice ↔ proposal; mismatch blocks issue
- Daily reconciliation sweep; unreconciled > 48h surfaces to founder
- Payment-state recheck immediately before any reminder send
