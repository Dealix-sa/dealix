# Payment architecture

Dealix does NOT process payments. The customer's accounting system does. This document explains the boundary.

## Status today (V12)

- No PCI scope.
- No card data handled.
- No payment links generated automatically.
- Stubs in `integrations/payments/` show the intended contract; they do not call any provider.

## When a customer pays

1. Founder issues an invoice from the customer's accounting system (Zoho, QuickBooks, Wafeq, etc.).
2. Customer pays via their normal channel (bank transfer, Moyasar link, Stripe link).
3. Customer's accounting system records the receipt.
4. Founder marks the deal `won` in `business/_data/deals.ledger.json` via `scripts/mark_deal_won.py`.

## Future state (out of V12 scope)

Two providers under consideration:
- **Moyasar** — Saudi-first, ZATCA-aware. Preferred for KSA-domiciled customers.
- **Stripe** — international, cross-border. For customers paying in foreign currency.

See `MOYASAR_INTEGRATION_PLAN.md` and `STRIPE_INTEGRATION_PLAN.md`.

## PCI boundary

Dealix:
- Never stores card numbers.
- Never logs card numbers.
- Never accepts card data through its own surfaces.
- Only stores customer-supplied invoice IDs and amounts.

## Refunds

Handled by the customer's accounting system. Dealix does not push refunds programmatically.
