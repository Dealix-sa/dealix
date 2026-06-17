# Commercial Contract Pack

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action — contracts are external commitments), #2 (no value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external and irreversible actions.

## Purpose

Standardize Dealix's commercial documents so every engagement, retainer, partner, refund, scope change, and data arrangement runs on a known template — with founder approval and legal review as appropriate. This document is the **index and scope** for the contract pack; the documents themselves live across `docs/legal/`.

## Documents in the Pack

| Document | Purpose | Owner |
|----------|---------|-------|
| Revenue Sprint terms | Standard terms for a productized sprint engagement | Founder |
| Retainer terms | Standard recurring-scope terms | Founder |
| Proof approval | Client written approval template for public proof or case study | Founder |
| Data processing notes | When Dealix acts as processor for a client | Founder + legal review |
| Refund policy | Conditions and process for refunds | Founder |
| Partner referral terms | Commission, attribution, and conduct for partners | Founder |
| Scope change policy | How a scope change is requested, priced, approved, recorded | Founder |
| Confidentiality (NDA) template | Standard mutual NDA | Founder |
| Pilot / engagement letter | Lightweight letter of intent for early-stage engagements | Founder |

## Core Rules

- No custom legal commitment without founder approval and, where the doctrine requires it, recorded legal review.
- A public claim about a client (case study, named proof, public quote) requires the **Proof approval** document signed and recorded as a source-evidence link.
- A scope change is documented and signed; a verbal scope change is not a scope change.
- A refund is A3 (irreversible) per `docs/finance/BILLING_RECEIVABLES_OS.md`; the refund document is signed and recorded.
- A partner relationship is recorded under the **Partner referral terms** before commissions accrue.
- "Guaranteed outcome" language is not allowed in any commercial document.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Per engagement | The appropriate engagement letter or terms document is signed |
| Per scope change | A change note is signed |
| Per refund | The refund document is signed |
| Per public proof | The proof approval is signed |
| Quarterly | Template review: are the terms still right; any edge cases that bit us |

## Runtime Wiring

- Existing legal cluster: `docs/legal/` (7 files).
- Approval Center (the gate for contractual commitments): `docs/control_plane/APPROVAL_CENTER_V2.md`.
- Billing / receivables: `docs/finance/BILLING_RECEIVABLES_OS.md`.
- Audit log: `db/models.py::AuditLogRecord`.
- Templates directory: `templates/`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Engagements signed using a pack template | 100% | review |
| Public client claims with recorded proof approval | 100% | proof queue |
| Refunds processed without signed refund document | 0 | refund records |
| Scope changes invoiced without signed scope change | 0 | review |
| Template revisions per quarter | non-zero (templates are living documents) | release notes |

## Cross-Links

- `docs/legal/` (existing legal docs)
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/finance/BILLING_RECEIVABLES_OS.md`
- `docs/partners/PARTNER_REVENUE_MACHINE.md`
- `docs/client_success/CUSTOMER_LIFECYCLE_OS.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`
- `templates/`

## Open Items

- Several pack documents listed here exist across `docs/legal/` and `templates/` but are not yet labeled as the canonical version. A canonical-version sweep is open.
- A "contract sign-off" approval queue item type is conceptual today; signing happens externally and the record links back to the audit log manually.
- The data-processing notes need a one-page Arabic explainer suitable for buyers' procurement teams.
