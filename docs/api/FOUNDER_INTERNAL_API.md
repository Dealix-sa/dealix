# Founder Internal API

## Purpose
Expose safe internal endpoints for the CEO Command Center.

## Endpoints

### CEO
- GET /api/v1/internal/ceo/summary
- GET /api/v1/internal/ceo/top-action
- GET /api/v1/internal/ceo/certification

### Sales
- GET /api/v1/internal/sales/funnel
- GET /api/v1/internal/sales/followups
- GET /api/v1/internal/sales/payment-capture

### Approvals
- GET /api/v1/internal/approvals
- POST /api/v1/internal/approvals/{id}/approve
- POST /api/v1/internal/approvals/{id}/reject
- POST /api/v1/internal/approvals/{id}/request-edit

### Distribution
- GET /api/v1/internal/distribution/channels
- GET /api/v1/internal/distribution/sectors
- GET /api/v1/internal/distribution/experiments

### Workers
- GET /api/v1/internal/workers/health
- GET /api/v1/internal/workers/logs

### Trust
- GET /api/v1/internal/trust/flags
- GET /api/v1/internal/trust/incidents
- POST /api/v1/internal/trust/evaluate

### Finance
- GET /api/v1/internal/finance/summary
- GET /api/v1/internal/finance/payment-capture
- GET /api/v1/internal/finance/runway

## Security
- Internal endpoints require auth.
- External-impact actions require approval class.
- A2 and A3 actions cannot bypass policy evaluation.

## Rule
The frontend calls API. The API calls trust. Trust gates execution.
