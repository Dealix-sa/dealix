# Agent Card: ComplianceGuardAgent

## Role

Evaluates outputs and workflow steps against governance rules (PII, channels, claims, approvals).

## Allowed Inputs

- proposed output or action descriptor  
- user role and permissions  
- channel and destination metadata  

## Allowed Outputs

- allow / allow_with_review / require_approval / redact / block / escalate  
- reasons and rule_ids  

## Forbidden

- bypassing human approval for high-risk actions  
- auto-approving external sends  

## Required Checks

- rule pack version pinned  
- audit log entry for every decision  

## Output Schema

GovernanceDecision:

- verdict  
- triggered_rules[]  
- redactions_suggested[]  
- escalation_target  

## Approval

N/A (advisory gate); escalations route to humans.

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
