# Prompt Registry

No **production** prompt without owner, schema, and eval linkage.

| Prompt ID | Version | Service | Purpose | Owner | Eval hook |
|-----------|---------|---------|---------|-------|-----------|
| lead_scoring_prompt | v1.0 | Lead Intelligence | score account fit | | lead_intelligence_eval |
| outreach_draft_prompt | v1.0 | Lead Intelligence | safe drafts | | outreach_quality_eval |
| citation_answer_prompt | v1.0 | Company Brain | answer with sources | | company_brain_eval |

## Each prompt must define

```text
purpose
input schema
output schema
forbidden behavior
examples
eval tests
version history
```

Implementation: store in repo or prompt DB with **checksum**; reference version in [`AI_RUN_LEDGER.md`](../ledgers/AI_RUN_LEDGER.md).

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
