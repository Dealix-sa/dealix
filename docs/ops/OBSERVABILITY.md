# Observability Notes

## Goal
Make critical operating paths visible enough to debug and review.

## Priority Paths
- booking submit flow
- draft approval flow
- WhatsApp webhook ingest
- outbound send attempt
- founder daily generation scripts

## Minimum Signals

### Logs
- booking received
- draft approved/rejected
- webhook verified/rejected
- outbound send success/failure

### Metrics
- bookings created
- pending approvals
- sent messages
- failed messages
- open conversations

### Trace Candidates
- booking request lifecycle
- webhook request lifecycle
- send pipeline lifecycle

## Rule
Prefer structured logs and avoid logging secrets or raw sensitive payloads unnecessarily.