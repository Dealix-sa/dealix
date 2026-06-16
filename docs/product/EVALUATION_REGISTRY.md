# Evaluation Registry

Quality and governance must be **measurable**—tie each eval to a service and a **threshold**.

| Eval | Service | Checks | Pass threshold |
|------|---------|--------|----------------:|
| lead_scoring_eval | Lead Intelligence | relevance, explainability, consistency | 85 |
| claims_safety_eval | Outreach / drafts | no guarantees, no fake proof | **100** |
| rag_grounding_eval | Company Brain | citation, no-source-no-answer | **95** |
| arabic_quality_eval | All AR outputs | clarity, tone, Saudi business fit | 85 |
| governance_eval | All | PII, source, approval paths | **100** |

## Hard thresholds

```text
Governance eval = 100 required
Claims safety = 100 required
RAG grounding = 95+
Arabic quality = 85+
```

**YAML packs:** [`../../evals/README.md`](../../evals/README.md). Update when prompts change.

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
