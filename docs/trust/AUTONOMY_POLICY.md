# Autonomy Policy

## Purpose
Define how far automation can go inside Dealix.

## Owner
Sami / Trust owner.

## Review Cadence
Monthly or after any incident.

## Inputs
- Action type.
- Risk level.
- Approval class.
- Data sensitivity.
- External impact.

## Outputs
- Allowed autonomy level.
- Required approval.
- Logging requirement.

## Autonomy Levels

### L0 Manual
Human does the work.

### L1 Assisted
AI drafts, human edits.

### L2 Semi-Auto
System executes internally and waits for external approval.

### L3 Auto
System executes low-risk internal actions.

### L4 Prohibited
System must never execute.

## L4 Actions
- contract changes
- NDAs
- refunds
- legal commitments
- regulator communication
- sensitive data exports
- guaranteed revenue claims
- full compliance claims

## Rules
- A3 maps to L4.
- A2 maps to L0/L1/L2 only.
- No external commitment can be L3.
- Automation must be auditable.

## Metrics
- A3 blocked actions.
- Automation failures.
- Manual override count.
- Incident count.

## Evidence
- approval logs
- audit logs
- incident response
- GitHub checks
- trust tests

## Last Reviewed
YYYY-MM-DD
