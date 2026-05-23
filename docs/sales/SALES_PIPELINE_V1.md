# Sales Pipeline v1

## Stages

1. Targeted  
2. Researched  
3. Contact Drafted  
4. Contacted Manually  
5. Discovery Booked  
6. Diagnostic Proposed  
7. Diagnostic Paid  
8. Sprint Proposed  
9. Sprint Paid  
10. Pilot Proposed  
11. Retainer Won  
12. Lost / Nurture  

## Required fields

- company_name  
- sector  
- city  
- pain_hypothesis  
- offer_fit  
- source  
- relationship_status  
- next_action  
- owner  
- last_touch  
- compliance_status  

## Rules

```text
Any lead without source or next_action = not ready.
Any external touch = manual, consented, and reviewable.
```

See also: [`CRM_PIPELINE_SCHEMA.md`](../growth/CRM_PIPELINE_SCHEMA.md), [`SALES_PLAYBOOK.md`](SALES_PLAYBOOK.md).

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

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
