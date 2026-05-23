# Webhook Retry + DLQ Strategy

## Current Implementation
Webhooks from Moyasar land at `/api/v1/webhooks/moyasar`.

## Retry Policy
- 3 retry attempts with exponential backoff (1s, 10s, 60s)
- After 3 failures: mark as dead-letter, alert via Sentry

## DLQ Storage
Failed webhook events stored in DB table `webhook_dlq`:
- payload
- received_at
- attempts
- last_error
- status (pending|retrying|abandoned|replayed)

## Replay Script
```bash
python scripts/replay_webhook.py --id <dlq_id>
```

## Monitoring
- Alert if DLQ count > 5 in 1 hour
- Weekly DLQ cleanup review

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
