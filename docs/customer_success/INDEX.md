# Customer Success / Product Distribution — Surface Index

Read-only index for customer-success and product-distribution surface.
`scripts/verify_product_distribution.py` confirms this file exists.

## Canonical artifacts

- `auto_client_acquisition/client_os/` — delivery factory + client
  lifecycle.
- `api/routers/customer_success_scores.py` — 5-score read-only customer
  health.
- `api/routers/customer_webhooks.py` — Dealix→customer event delivery.
- `dealix/services/SERVICE_READINESS_MATRIX.yaml` — service-level rubric.

## Founder Console references

- `/internal/ceo/daily-brief` surfaces top customer-success bottlenecks.
- `/internal/audit/recent` surfaces approval decisions for case-study
  publish / scope_send / invoice_send.

## Governance

- Expansion offers must respect the **5-rung service ladder**
  (`docs/COMPANY_SERVICE_LADDER.md`); upsell from rung N to rung N+1
  requires a signed Proof Pack from rung N.
- `case_study_publish` requires approval AND customer consent.
