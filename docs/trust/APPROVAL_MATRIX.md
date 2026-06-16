# Approval Matrix

## Purpose
Define what Dealix can execute automatically and what requires founder approval.

## Owner
Sami / Trust owner.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Workflow type.
- Risk level.
- Data sensitivity.
- External commitment.
- Legal/compliance implication.

## Outputs
- Approval class.
- Execution decision.
- Audit requirement.

## Approval Classes

### A0 - Fully Automatic
Allowed for low-risk internal actions:
- duplicate removal
- internal lead scoring
- CRM status update
- internal report generation

### A1 - Human Review Recommended
Requires review before important external use:
- outreach drafts
- public content drafts
- sample pack drafts
- lead list delivery drafts

### A2 - Explicit Human Approval Required
Cannot proceed without founder approval:
- proposal sending
- client delivery
- pricing exceptions
- public case studies
- customer data exports

### A3 - Never Auto-Execute
Never automatic:
- contract changes
- NDAs
- legal commitments
- regulator communication
- refunds
- sensitive data exports
- guaranteed revenue claims
- full compliance claims

## Rules
- External commitments require A1 or higher.
- Financial or legal changes require A2 or A3.
- A3 actions are blocked, not queued for automation.
- Every A2/A3 action must be logged.

## Metrics
- Approvals waiting.
- A3 blocked actions.
- Approval turnaround time.
- Sensitive action count.
- Incidents.

## Evidence
- trust/approval_log.csv
- trust/sensitive_actions.md
- claim_approval_log.csv
- incident logs

## Last Reviewed
YYYY-MM-DD
