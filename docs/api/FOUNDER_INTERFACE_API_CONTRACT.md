# Founder Interface API Contract

## Purpose

Define the internal API used by the Dealix founder-facing frontend.

All routes live under `/api/v1/internal/*` and are intended for the
authenticated founder console only. They are never exposed to customers
or partners.

## CEO

- `GET /api/v1/internal/ceo/summary`
- `GET /api/v1/internal/ceo/top-action`
- `GET /api/v1/internal/ceo/certification`

## Sales

- `GET /api/v1/internal/sales/funnel`
- `GET /api/v1/internal/sales/followups`
- `GET /api/v1/internal/sales/payment-capture`

## Approvals

- `GET  /api/v1/internal/approvals`
- `POST /api/v1/internal/approvals/{id}/approve`
- `POST /api/v1/internal/approvals/{id}/reject`
- `POST /api/v1/internal/approvals/{id}/request-edit`

## Workers

- `GET /api/v1/internal/workers/health`

## Trust

- `GET /api/v1/internal/trust/flags`
- `GET /api/v1/internal/trust/incidents`

## Finance

- `GET /api/v1/internal/finance/summary`

## Distribution

- `GET /api/v1/internal/distribution/channels`
- `GET /api/v1/internal/distribution/sectors`
- `GET /api/v1/internal/distribution/experiments`

## Response Shape — CEO Summary

```json
{
  "top_action": "Approve outreach batch",
  "status": "C3 Revenue Partial",
  "risk_flags": 0,
  "cash_collected_sar": 0,
  "approved_outreach": 0,
  "positive_replies": 0,
  "proposals_due": 0,
  "payment_followups_due": 0,
  "last_updated": "2026-05-23T00:00:00Z"
}
```

## Rule

- The frontend never bypasses the Trust Plane.
- All external-impacting actions require policy evaluation and an
  explicit approval class.
- Internal endpoints are read-only by default. Any write endpoint must
  record an audit entry, the actor, and the approval class used.
