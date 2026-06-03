# Approval Matrix

## Purpose
Tell every operator and every agent exactly when to act, when to ask, and when to refuse.

## Owner
Sami / Trust owner.

## Review Cadence
Weekly.

## Action Classes

### A1 — Auto-allowed
Reversible, low blast-radius, no external visibility.
Examples:
- Read internal files
- Generate draft (held in queue, not sent)
- Update internal pipeline_tracker.csv
- Run verifier scripts

### A2 — Founder approval required
External-facing or partially irreversible.
Examples:
- Send DM, email, or proposal to a lead
- Publish public content
- Apply a discount within ladder
- Export data outside the workspace

### A3 — Founder + written record required (sometimes legal)
Irreversible, high blast-radius, or regulated.
Examples:
- Sign a contract or PO
- Make a compliance claim
- Charge a customer
- Share PII with a third party
- Push to production main branch with revenue/trust impact

## Default for Unknown Actions
Treat as A3 until classified.

## Logging
All A2 and A3 decisions are logged in `trust/approval_log.csv` (private ops repo) with:
- timestamp
- actor
- action
- class
- decision
- evidence link

## Linked Systems
- docs/trust/TRUST_CONTROL_SYSTEM.md
- docs/trust/AUTONOMY_POLICY.md

## Last Reviewed
2026-05-23
