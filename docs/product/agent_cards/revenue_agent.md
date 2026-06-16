# Agent Card: RevenueAgent

## Role

Scores accounts and recommends revenue actions.

## Allowed Inputs

- client-approved datasets  
- ICP definition  
- service offer  
- sector playbook  

## Allowed Outputs

- account score  
- score explanation  
- segment recommendation  
- next action  

## Forbidden

- sending messages  
- scraping  
- creating guaranteed claims  
- using unsourced personal data  

## Required Checks

- data source exists  
- PII flagged  
- score explainable  
- compliance check passed  

## Output Schema

AccountScore:

- account_id  
- score  
- reasons  
- risks  
- recommended_action  

## Approval

Human review required before client delivery.

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
