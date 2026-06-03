# Trust Control System

## Purpose
Protect Dealix from overclaims, unsafe automation, data leakage, and uncontrolled external commitments.

## Owner
Sami / Trust owner.

## Review Cadence
Daily for approvals, weekly for policy.

## Inputs
- proposed outbound messages
- proposals
- client deliveries
- public claims
- data exports
- pricing exceptions
- AI outputs

## Outputs
- approval decision
- blocked action
- safer wording
- audit record
- incident response when needed

## Rules
- A3 actions never auto-execute.
- A2 actions require explicit founder approval.
- No guaranteed revenue claim.
- No full compliance claim unless legally reviewed.
- No sensitive data export without approval.
- No real client or lead data in public repo.

## Metrics
- approvals pending
- A3 blocked actions
- claims reviewed
- incidents
- public safety pass rate

## Evidence
- trust/approval_log.csv
- claim_approval_log.csv
- incident log
- public safety check
- GitHub Actions

## Linked Systems
- docs/trust/APPROVAL_MATRIX.md
- docs/trust/AUTONOMY_POLICY.md
- docs/trust/NO_OVERCLAIM_POLICY.md
- docs/trust/SAFE_LANGUAGE_LIBRARY.md
- docs/trust/PUBLIC_PRIVATE_BOUNDARY.md

## Last Reviewed
2026-05-23
