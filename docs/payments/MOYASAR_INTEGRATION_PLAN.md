# Moyasar integration plan (future)

## Why Moyasar
- Saudi-licensed payment processor.
- ZATCA / Mada / Apple Pay support.
- Strong API + webhook docs.

## Scope (when activated)
- Generate a payment link for an approved quote.
- Receive a webhook on payment.
- Mark the deal `won` in `deals.ledger.json`.

## Out of scope
- Storing card details.
- Refund automation.
- Subscription billing (use Moyasar subscriptions only after dedicated security review).

## Prerequisites before going live
- Signed Moyasar merchant agreement.
- Signed customer SOW that explicitly allows Moyasar payment link issuance.
- Webhook secret stored in `MOYASAR_WEBHOOK_SECRET` env var.
- API key stored in `MOYASAR_SECRET_KEY` env var.
- Quarterly key rotation procedure.
- ZATCA-compliant invoice generation through the customer's accounting system.

## Architecture sketch

```
[Approved quote]
       ↓
scripts/issue_payment_link.py (creates Moyasar link)
       ↓
[Customer pays at Moyasar]
       ↓
Webhook → api/routers/payments_router.py
       ↓
scripts/mark_deal_won.py (auto-triggered by router)
```

## Status
- `integrations/payments/moyasar_stub.py` defines the function signatures.
- No live calls until activation gates above are passed.
