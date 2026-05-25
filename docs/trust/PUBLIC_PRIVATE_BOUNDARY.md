---
title: Public / Private Boundary
owner: Founder
status: active
last_review: 2026-05-23
---

# Public / Private Boundary — حدود العام والخاص

## Purpose

Define what lives in the public Dealix repository and what lives in `dealix-ops-private`. A single mistake here leaks a client. The boundary is enforced by rule, not by memory.

## Public repo (this one)

May contain:

- Doctrine: constitution, category, positioning, policies.
- Method: SOPs, playbooks, templates, schemas.
- Anonymized case-safe summaries explicitly labeled.
- Sector reports built from public methodology and aggregated patterns.
- Public posts after A2 approval.

May NOT contain:

- Client names, logos, contacts.
- Real lead tables.
- Internal financials, MRR, pipeline value as numbers.
- Internal approval files.
- AI Run Ledger snapshots.
- Any credential, key, or token.

## Private repo (`dealix-ops-private`)

Contains:

- Client records, intake forms, signed contracts.
- Lead tables with real names and contacts.
- Invoices, payments, refunds.
- Approval files (A1, A2, A3).
- Incident files.
- Evidence packs per delivery.
- The AI Run Ledger.

## Boundary check rules

1. Pre-commit hook scans every public commit for: client names, phone patterns, email patterns, national ID patterns, known secret patterns, and banned claim phrases.
2. Any case study in the public repo must carry the label "Hypothetical / case-safe template" or "Anonymized — consent on file."
3. Any number that looks like a revenue or ROI claim requires A3 evidence in the private repo.
4. Sector reports cite methodology and use ranges. No single-client metric.

## What if a real metric is needed publicly?

- Get written client consent in the private repo.
- Run the metric through [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
- Publish only the band (e.g., "estimated 5–15% pipeline lift, reviewed at handover"), never the exact figure tied to a named entity.

## Operational steps

1. Before every public commit, the hook runs.
2. If blocked, the contributor reviews the offending lines.
3. If a leak ships despite the hook, follow [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md) immediately.

## Evidence

- `pre_commit.log` in the public repo.
- Incident files for any leak.
- Quarterly sweep of recent commits sampled for boundary compliance.

## Cross-links

- [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md)
- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) — C-09 pre-commit scan.
- [docs/04_data_os/PII_CLASSIFICATION.md](../04_data_os/PII_CLASSIFICATION.md)

## Owner & cadence

- Founder owns the boundary. Quarterly sweep.

## AR — ملخّص

المستودع العام يحوي العقيدة والأساليب والقوالب وملخّصات مُجمَّعة آمنة فقط. أما العملاء والإيرادات والموافقات وسجلات الذكاء فتعيش في المستودع الخاص. خطّاف ما قبل الالتزام يفحص كل عملية دفع، وأي تسريب يفتح حادثة فورية. القيمة التقديرية ليست قيمة مُتحقَّقة.
