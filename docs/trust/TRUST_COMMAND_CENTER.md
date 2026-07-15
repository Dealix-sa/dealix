# Trust Command Center

## Purpose
Protect Dealix from unsafe automation, overclaims, data leakage, and uncontrolled external commitments.

## Owner
Sami / Trust owner.

## Review Cadence
Daily for approvals, weekly for policies.

## Inputs
- outbound messages
- proposal drafts
- public claims
- client delivery reports
- data exports
- AI outputs
- approval logs

## Outputs
- approve
- reject
- rewrite
- escalate
- block
- log

## Rules
- A3 actions never auto-execute.
- A2 actions require explicit founder approval.
- No guaranteed revenue claim.
- No full compliance claim unless legally reviewed.
- No sensitive data export without approval.
- No real client/lead data in public repo.
- Every external claim needs evidence.

## A3 Never Auto-Execute
- refunds
- contract changes
- legal commitments
- regulator communication
- sensitive data exports
- guaranteed revenue claims
- full compliance claims

## Metrics
- approvals pending
- A3 blocked actions
- claims reviewed
- incidents
- public safety pass rate

## Evidence
- approval_log.csv
- claim_approval_log.csv
- incident log
- public safety check
- GitHub Actions

## Last Reviewed
2026-05-23
