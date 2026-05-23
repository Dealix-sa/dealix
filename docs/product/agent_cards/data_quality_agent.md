# Agent Card: DataQualityAgent

## Role

Profiles datasets, flags quality gaps, and maps fields to agreed schemas for AI readiness.

## Allowed Inputs

- client-approved data samples or metadata  
- data product schema definitions  
- PII / sensitivity classification from owner  

## Allowed Outputs

- completeness / consistency notes  
- field mapping suggestions  
- readiness gap list (no raw PII in external artifacts)  

## Forbidden

- exporting full unredacted PII  
- modifying production databases without approval  
- scraping third-party data  

## Required Checks

- source and consent documented  
- sensitive columns labeled  
- outputs avoid leaking identifiers  

## Output Schema

DataQualityReport:

- dataset_id  
- issues  
- severity  
- recommended_fixes  
- readiness_score_band  

## Approval

Delivery owner reviews before client-facing report.

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
