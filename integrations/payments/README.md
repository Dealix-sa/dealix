# integrations/payments

Stubs only. Real payments handled by the customer's accounting system.

| File | Purpose |
| --- | --- |
| `base.py` | Common interface every provider stub implements. |
| `moyasar_stub.py` | Moyasar surface. No live calls. |
| `stripe_stub.py` | Stripe surface. No live calls. |

To activate a stub, see `docs/payments/PAYMENT_SECURITY_BOUNDARIES.md` § Activation gates.
