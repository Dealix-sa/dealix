# Restore Drill Log

Quarterly restore drill of the production database. Source: `scripts/restore_test.sh`.

| Date (UTC) | Backup tested | Time-to-restore | Rows verified | Exit | Operator | Notes |
|------------|---------------|-----------------|---------------|------|----------|-------|
| _pending_ | _to fill on first drill_ | — | — | — | — | First drill scheduled within 7 days of GA |

**Drill schedule:** 1st of January, April, July, October.

**Pass criteria:**
- Exit code 0
- `accounts` row count ≥ `EXPECTED_MIN_LEADS` (current baseline: 158, drill floor: 100)
- Total time-to-restore ≤ 60 minutes

**Failure protocol:** SEV-2 incident, page on-call, root-cause in INCIDENT_RUNBOOK.md format within 48h.

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
