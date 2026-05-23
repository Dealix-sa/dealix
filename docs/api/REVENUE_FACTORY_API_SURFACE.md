# Revenue Factory API Surface

## Purpose
Define API endpoints required to operate the revenue factory.

## Endpoints

### Accounts
- GET /api/v1/accounts
- POST /api/v1/accounts/import
- POST /api/v1/accounts/enrich
- POST /api/v1/accounts/score

### Outreach
- GET /api/v1/outreach/pending
- POST /api/v1/outreach/:id/approve
- POST /api/v1/outreach/:id/reject
- POST /api/v1/outreach/:id/draft
- POST /api/v1/outreach/:id/mark-sent

### Conversations
- POST /api/v1/conversations/log
- POST /api/v1/conversations/route

### Samples
- GET /api/v1/samples/queue
- POST /api/v1/samples/generate
- POST /api/v1/samples/approve

### Proposals
- GET /api/v1/proposals/queue
- POST /api/v1/proposals/generate
- POST /api/v1/proposals/approve

### Payments
- GET /api/v1/payments/capture-queue
- POST /api/v1/payments/follow-up
- POST /api/v1/payments/mark-paid

### Delivery
- POST /api/v1/delivery/start
- GET /api/v1/delivery/queue

### Retention
- GET /api/v1/retention/queue
- POST /api/v1/retention/ask-retainer

### Trust
- GET /api/v1/trust/flags
- POST /api/v1/trust/evaluate
- POST /api/v1/trust/approval

## Rule
Every external-impacting endpoint checks trust policy and approval class.
