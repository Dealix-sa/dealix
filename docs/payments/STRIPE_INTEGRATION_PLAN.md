# Stripe integration plan (future)

## When to use Stripe instead of Moyasar
- Customer pays in non-SAR currency.
- Customer's existing finance stack already uses Stripe.
- Cross-border subscription with international customer.

## Scope (when activated)
- Issue Stripe Payment Link or Checkout Session for approved quote.
- Webhook on `payment_intent.succeeded` → mark deal won.
- Webhook on `customer.subscription.deleted` → mark customer churned in CRM.

## Out of scope
- Storing card details.
- Refund automation.
- Connect / marketplace flows (no plan to operate as a marketplace).

## Prerequisites before going live
- Signed Stripe account with KSA-eligible business entity.
- `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in env vars.
- Customer SOW allows Stripe link issuance.
- Decision on ZATCA invoice issuance (Stripe does not produce KSA tax invoices; customer's accounting system must).
- Quarterly key rotation.

## Architecture sketch

```
[Approved quote]
       ↓
scripts/issue_payment_link.py (creates Stripe link)
       ↓
[Customer pays at Stripe]
       ↓
Webhook → api/routers/payments_router.py (Stripe handler)
       ↓
scripts/mark_deal_won.py
```

## Status
- `integrations/payments/stripe_stub.py` defines function signatures.
- No live calls until activation gates above are passed.
