# Audit Policy

> How Dealix audits itself, and how clients/regulators can audit us.

## What's Audited

| Layer | What | Frequency | Auditor |
|---|---|---|---|
| Approvals | Every external action logged in `trust/approval_log.csv` | Daily review | Founder |
| Claims | Every published claim → evidence pack on file | Per-publish + monthly sweep | Founder + claim_guard |
| Suppression | Every send blocked or allowed | Per-send + weekly count | Code + founder |
| Data retention | Deletion runs + log | Monthly | Founder + data_retention.py |
| Incidents | Every incident logged + post-mortem | Per-incident + quarterly trend | Founder + advisor |
| Agent decisions | Logged per agent per call | Per-call + monthly aggregate | Founder + agent owner |
| Financial | Invoices, payments, MRR | Monthly | Founder |
| Trust scorecards | Composite | Weekly | Founder |
| Code (CI) | Tests, security scan, public safety | Per-PR | CI bots + reviewer |

## Audit Trails Must Be

- Append-only (no editing past entries)
- Timestamped
- Identifiable (who did what)
- Linked (decision → action → outcome)
- Retained per `DATA_RETENTION_POLICY.md`

## Internal Audit Cadence

- **Daily** — approval log review (10 min, founder)
- **Weekly** — full Weekly CEO Review (scorecards + audit summary)
- **Monthly** — pattern analysis (incidents, claim_guard catches, suppression growth)
- **Quarterly** — full trust posture review with advisor
- **Annually** — third-party review (when budget allows)

## Audit Findings Workflow

For every finding:
1. Severity assessed (per `INCIDENT_RESPONSE.md` if Trust-related)
2. Root cause documented
3. Rule change committed (file → change)
4. Test added if applicable
5. Closed only after rule change merged

## External Audit Readiness

Dealix can produce on request:
- Approval log for a specific date range
- Claim evidence for a specific public statement
- Suppression list status for a specific identifier
- Deletion proof for a specific data set
- Incident log for a specific period (redacted as needed)
- Agent inventory + risk levels
- Code SHA + test results for any production behavior

This is the "client audit kit". Lives as a script: `scripts/generate_audit_kit.py` (planned).

## Client Audit Rights

- Managed Ops clients: quarterly written audit summary on request
- Revenue Desk clients: per-DPA, may include integration audit
- All clients: full disclosure of their own data on request (24 hr response SLA)

## Regulator Audit Posture (Saudi)

- PDPL: data inventory + retention proof
- SDAIA: AI governance summary + human-in-the-loop evidence
- ZATCA: financial records per Saudi requirements
- Any official inquiry: founder + Saudi counsel within 24 hr

## Tools

- `dealix/trust/audit.py` — utilities for log compaction, query, export
- `dealix/trust/policy_engine.py` — policy enforcement layer
- `dealix/trust/evidence_pack.py` — generates evidence pack manifests
- `tests/trust/` — every trust policy has a test

## Common Audit Failures (and how to prevent)

- **Missing approval log entry** — automate logging; never rely on manual entry
- **Claim without evidence pack** — block at publish; never override
- **Suppression breach** — code-level check; can't be bypassed in UI
- **Stale data past retention** — scheduled deletion + monthly review
- **Untraceable agent decision** — every agent call logs request + response + version

## What This Policy Refuses

- "We can audit later" — auditability must be built in from day one
- "It's too small to log" — every external action is logged, regardless of size
- "Just delete the old log" — logs are append-only
- "We trust ourselves" — internal trust is what audit verifies, not replaces
- Outsourcing audit while still owning the trust posture
