# Consent, Suppression & Lawful Basis System

## Doctrine Anchor
- Non-negotiables touched: #1 (no external high-risk action without approval), #2 (no value claim without source evidence), #3 (no cross-tenant operational access), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external and irreversible actions, control-plane verification scripts as release blockers.

## Purpose

Control how Dealix handles contact data and outreach permissions. Every account, contact, and outreach record carries a documented lawful basis, a consent state, and a suppression state. No external outreach proceeds against a suppressed record.

## Regulatory Anchor

Saudi Arabia's Personal Data Protection Law (PDPL), supervised by SDAIA, governs how personal data is collected, processed, and contacted. Dealix is a controller for its own outreach data and a processor when running outreach on a client's behalf. Both roles are documented per workflow.

This document is operational; it is not legal advice. Legal documents live in `docs/legal/`.

## Record Fields

Every contact record (or surrogate, where the contact is a public business role) carries:

| Field | Description |
|-------|-------------|
| `data_source` | Where the record came from (public business page, RFP, referral, opt-in form, partner intro) |
| `public_business_context` | Whether the record is a business role (e.g. "Procurement at X") or a personal identifier |
| `lawful_basis_assessment` | The basis Dealix relies on for outreach (legitimate business interest with public role, or explicit consent) |
| `consent_status` | None / Implied (B2B public role) / Explicit (form opt-in) / Withdrawn |
| `opt_out_status` | None / Requested / Confirmed |
| `suppression_reason` | If suppressed, why (see list below) |
| `last_reviewed` | When a human last reviewed this record's status |
| `tenant_id` | For multi-tenant isolation |

## Suppression Reasons

Suppress a record when any of the following are true:

- **Opt-out**: explicit unsubscribe or "stop" signal received.
- **Not interested**: explicit "not interested" from the buying unit.
- **Bad fit**: confirmed outside ICP after research.
- **Duplicate**: another active record covers the same buying unit.
- **Risky source**: the source's terms of use prohibit contact, or the data origin is unclear.
- **Complaint**: a deliverability or trust complaint was raised.
- **Personal data uncertainty**: the record looks personal rather than a business role and Dealix cannot establish a clear lawful basis.

## Core Rules

- A record in `SuppressionRecord` cannot receive an outreach draft, follow-up, or sample. The queue worker enforces this before writing.
- Opt-out requests are honored within one business day and confirmed in writing.
- A record without a `lawful_basis_assessment` is treated as suppressed by default until reviewed.
- Cross-tenant suppression is enforced: tenant A's opt-outs do not leak into tenant B's outreach decisions, and vice versa.
- An overridden suppression (very rare; founder-only) requires an `AuditLogRecord` entry with a written justification.
- Public proof, case studies, and named claims about a client require the client's written approval recorded as a source-evidence link.

## Runtime Wiring

- Suppression table: `db/models.py::SuppressionRecord`.
- Outreach window enforcement: `auto_client_acquisition/outreach_window.py`.
- Outreach queue (must check suppression before write): `db/models.py::OutreachQueueRecord`.
- Approval policy engine (rejects drafts to suppressed records): `auto_client_acquisition/approval_center/approval_policy.py`.
- Audit log: `db/models.py::AuditLogRecord`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Drafts attempted against suppressed records | 0 (must be caught by policy) | policy engine logs |
| Opt-out requests honored within 1 business day | 100% | `SuppressionRecord` timestamps |
| Records without lawful_basis_assessment | trending to 0 | `LeadRecord` join |
| Cross-tenant suppression bleed incidents | 0 | `AuditLogRecord` |
| Complaints per 1000 sends | < threshold (set by deliverability system) | deliverability metrics |

## Cross-Links

- `docs/data/GROWTH_DATABASE_MODEL.md`
- `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/legal/COMMERCIAL_CONTRACT_PACK.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- A bulk reviewer UI for records lacking `lawful_basis_assessment` is not yet built.
- The exact field shape on `SuppressionRecord` versus a separate `consent_state` table is open; today they are conflated.
- Cross-tenant isolation tests for the suppression layer exist in `tests/`, but a dedicated red-team scenario for "opt-out bleed" is open in the eval system (see `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`).
- Public-claim approval workflow (for proof and case studies) needs a dedicated approval queue item type.
