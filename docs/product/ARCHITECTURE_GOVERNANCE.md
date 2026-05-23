# Architecture Governance

Every technical **module** must be intentional—no orphan code paths.

## Required fields (per module)

- **purpose**
- **service(s) supported**
- **owner** (human DRI)
- **inputs**
- **outputs**
- **tests** (or explicit risk acceptance)
- **risks** (PII, cost, misuse)
- **logging / audit** (when actions are sensitive)
- **future path** (deprecate / promote to SaaS)

## Example — Data OS (illustrative)

| Field | Content |
|-------|---------|
| Purpose | Prepare client data for AI operations safely |
| Supports | Lead Intelligence, readiness reviews, cleanup sprints |
| Inputs | CSV, spreadsheet, CRM export (client-provided) |
| Outputs | Import preview, data quality score, PII flags, source report |
| Tests | `tests/test_data_os_helpers.py` (etc.) |
| Risks | PII leakage, wrong lawful basis assumed |
| Logging | Redact PII; no raw dumps in logs |

Link modules: [`MODULE_MAP.md`](MODULE_MAP.md), [`CAPABILITY_MATRIX.md`](CAPABILITY_MATRIX.md).

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
