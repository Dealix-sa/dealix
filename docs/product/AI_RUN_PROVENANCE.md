# AI Run Provenance

Every client-facing AI output must include provenance.

## Provenance fields

- ai_run_id  
- agent_id  
- model  
- prompt_version  
- input_sources  
- redaction_status  
- governance_status  
- qa_score  
- human_reviewer  
- output_version  
- delivered_at  

## Rule

No provenance → no delivery.

## Why

Traceability: when the client asks where a recommendation came from, the answer is knowable.

See: [`AI_RUN_LEDGER.md`](../ledgers/AI_RUN_LEDGER.md).

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
