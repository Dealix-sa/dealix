# AI Audit Logging

## Log file
`business/_data/ai_audit_log.json` (append-only).

## Per entry
- timestamp
- task
- provider
- model
- prompt_version
- review_status
- deterministic (bool)
- safety_passed (bool)
- note
- reviewer (if approved)

## What we never log
- Raw customer data inside the prompt body (in production mode).
- API keys.
- Personally identifying info beyond what the customer's SOW authorizes.

## Retention
- 12 months by default.
- Customer-specific entries deleted within 30 days of SOW termination.

## Access
- Founder only in V14.
- Customer audit view planned (post-V14).
