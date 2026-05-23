# API Governance

Every HTTP **endpoint** must declare behavior before it becomes a “shadow product.”

## Required (per route)

- **purpose**
- **input schema** (body/query; validation rules)
- **output schema** (stable fields for clients if public)
- **auth** requirement (public / user / admin / service)
- **audit** requirement (yes/no + event shape)
- **PII handling** (none / flag / redact / never log raw)
- **error states** (machine-readable codes where possible)
- **tests** (smoke + boundary)

## Example

**`POST /api/v1/data/import-preview`** (illustrative)

| Aspect | Policy |
|--------|--------|
| Purpose | Preview and validate a client dataset before heavy processing |
| Auth | Authenticated client or internal operator |
| Audit | Yes — who uploaded, file hash/filename, row counts (no raw cell PII) |
| PII | Flag columns; do **not** log raw PII lines |
| Errors | missing required column · unsupported encoding · empty file · size limit |

Future consolidation: align with “readiness API” vision in [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).

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
