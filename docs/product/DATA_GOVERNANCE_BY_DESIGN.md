# Data Governance by Design

Every **dataset** processed for AI ops carries explicit metadata—traditional data management is not enough when models amplify error and leakage ([Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk)).

## Required metadata

- **source** (system, export, manual upload)
- **owner** (client DRI)
- **purpose** (proportionality)
- **sensitivity** (public / internal / confidential / regulated)
- **retention** (align with [`../governance/DATA_RETENTION.md`](../governance/DATA_RETENTION.md))
- **allowed uses** (model training? reporting? drafts only?)
- **blocked uses** (e.g. resale, unapproved outbound)
- **lawful basis** if personal data exists (PDPL)
- **redaction status** (raw / redacted / synthetic)

## Dealix default

- Client-provided **only** unless contract says otherwise
- **Minimize** PII; prefer aggregates in client-facing reports
- Log **governance decisions** in [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md)

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
