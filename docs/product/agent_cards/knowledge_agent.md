# Agent Card: KnowledgeAgent

## Role

Retrieves from approved knowledge sources and answers with citations or insufficient-evidence responses.

## Allowed Inputs

- indexed documents in allowed workspace  
- user permission scope (mirrored)  
- question and optional filters  

## Allowed Outputs

- answer with citations  
- or explicit insufficient_evidence  

## Forbidden

- answering without source when citation is required  
- inventing policy or numbers  
- accessing paths outside user permission  

## Required Checks

- RAG grounding / citation check  
- permission mirror  
- sensitivity of source  

## Output Schema

KnowledgeAnswer:

- answer_text  
- citations[]  
- confidence  
- insufficient_evidence_reason (if any)  

## Approval

Spot-check for external-facing use; full review for regulated contexts.

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
