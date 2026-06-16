# Human Approval Gates

## Goal
No external message leaves Dealix without a human approval when required.

## Gates

### Gate 1: Draft Generation
- AI generates draft.
- Human reviews for tone, accuracy, safety.

### Gate 2: Target Verification
- Source URL confirmed.
- Contact verified.

### Gate 3: Content Safety
- No fake claims.
- No guaranteed ROI.
- Unsubscribe present for email.
- Opt-in present for WhatsApp.

### Gate 4: Send Approval
- Operator approves batch.
- `APPROVED_BY` env var or explicit approval recorded.

### Gate 5: Post-Send Review
- Bounces and replies reviewed daily.
- Suppression list updated.

## Exceptions
- None in production.
- Tests may bypass approval only in `APP_ENV=test`.
