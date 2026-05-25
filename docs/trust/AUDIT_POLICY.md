---
title: Audit Policy
owner: Trust Lead
status: active
last_review: 2026-05-23
---

# Audit Policy — سياسة التدقيق

## Purpose

Define what Dealix audits, how often, who reviews, and how long evidence is retained. Aligns with the NIST AI RMF *Govern* function as a practical floor.

## Scope of audit

| Domain | What is audited | Frequency |
|---|---|---|
| Approvals | Sample of A1/A2/A3 files vs. claimed actions | Monthly |
| AI Run Ledger | Completeness, schema, redaction | Monthly |
| Public repo | Boundary scan for PII or unapproved claims | Quarterly |
| Delivery evidence | Random closed deal, walk the chain | Weekly |
| Incidents | All open + 90-day rolling review | Monthly |
| Controls | One live test per control | Quarterly |
| Refunds & invoices | Reconciliation against approvals | Monthly |
| Public claims | Active LinkedIn posts and case studies vs. NO_OVERCLAIM list | Quarterly |

## Reviewers

- Internal: Trust Lead runs the audit. Founder counter-signs the monthly summary.
- External: an advisor (named in `dealix-ops-private/advisors.md`) reviews annually.

## Retention

| Artifact | Minimum retention |
|---|---|
| Approval files | 7 years |
| AI Run Ledger | 3 years (rolling); summaries archived |
| Incident files + postmortems | 7 years |
| Delivery evidence packs | 5 years |
| Invoices and refunds | 10 years (ZATCA-aligned) |
| Public-repo doc history | git permanence |

## Operational steps

1. Monthly audit produces `dealix-ops-private/audits/YYYY-MM.md`.
2. Each finding is one of: pass, gap, breach.
3. Gaps get a fix ticket with owner and deadline.
4. Breaches escalate via [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md).
5. Quarterly summary maps controls to the NIST AI RMF *Govern* subcategories used (GV-1 policies, GV-3 accountability, GV-4 culture, GV-6 third parties).

## Reference framework

- NIST AI Risk Management Framework (AI RMF 1.0), *Govern* function. Used as a floor, not a label. We do not claim full certification.

## Evidence

- Monthly audit file with findings and owner sign-off.
- Quarterly external-ready summary suitable for procurement diligence.

## Cross-links

- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md)
- [EVIDENCE_SYSTEM.md](./EVIDENCE_SYSTEM.md)
- [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md)
- [docs/05_governance_os/RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md)

## Owner & cadence

- Trust Lead. Annual external review.

## AR — ملخّص

سياسة التدقيق تحدّد ما يُراجَع، ومتى، ومَن يراجع، ومدة الحفظ. مراجعة شهرية، فحص ربعي، اختبار حيّ لكل ضابط في الربع، ومراجعة سنوية من مستشار خارجي. الإطار المرجعي هو NIST AI RMF بوصفه حدًّا أدنى لا شهادة. القيمة التقديرية ليست قيمة مُتحقَّقة.
