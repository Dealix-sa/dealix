# Audit Policy

> Trust without audit is wish.

## Audits

| Audit | Cadence | Owner | Output |
|-------|---------|-------|--------|
| Overclaim grep | Weekly | `make audit` (CI) | List of violations |
| Evidence link integrity | Monthly | Founder | Broken-link list |
| Approval log completeness | Monthly | Founder | Missing entries report |
| Public/private boundary | Monthly | Founder + CI | Private-data-in-public report |
| Autonomy tier audit | Monthly | Founder | A3 sends counted; A4 must be 0 |
| Incident drill | Quarterly | Founder | Updated incident response |
| External counsel review | Annual | External legal | Compliance memo |

## What `make audit` does

- Greps for forbidden phrases (see `NO_OVERCLAIM_POLICY.md`).
- Greps for PII patterns (emails, phone, Saudi national ID shape) in `docs/`.
- Lists evidence references with no matching ledger entry.
- Reports approval-queue age outliers (> 7 days).
- Reports risk-log freshness (last review date).

## Audit Output Disposition

| Finding | Disposition |
|---------|-------------|
| Forbidden phrase in public docs | Remove immediately, log in incident_log |
| Forbidden phrase in template | Replace with `SAFE_LANGUAGE_LIBRARY.md` equivalent |
| Private data in public | INCIDENT (S0 or S1) |
| Missing evidence link | Either add link or downgrade language |
| Approval queue stale | Founder closes within 24h |
| Risk log stale | Founder reviews within 24h |

## Audit Records

All audit outputs are stored in
`dealix-ops-private/trust/audits/yyyy-mm-dd/`.

The list of dates of recent audits is summarised in
`TRUST_COMMAND_CENTER.md`.

## External Audit (annual)

Once a year (or before any enterprise contract requires it):

- Counsel reviews PDPL handling.
- Counsel reviews contracts and proposal templates.
- Counsel reviews any "compliance" language used externally.

Findings → updates to policies + templates.

## What an audit is **not**

- A status report
- A retrospective
- A vibe-check

An audit is **adversarial**: assume the founder is trying to overclaim.
Find the overclaim. If you cannot, the audit was not done.
