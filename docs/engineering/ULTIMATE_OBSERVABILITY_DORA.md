# Ultimate Observability + DORA

Operational signals tracked by the Operating Layer:

- worker last-run + failures (`runtime/worker_state.csv`)
- trust flag count (`trust/trust_flags.csv`)
- audit events (`trust/approval_decisions.csv`)
- security status (`security/security_status.csv`)

DORA-style metrics (lead time, deployment frequency, MTTR, change fail
rate) are out of scope for this layer — they belong to the existing
engineering observability stack.
