---
title: Evidence System
owner: Delivery Lead
status: active
last_review: 2026-05-23
---

# Evidence System — نظام الأدلة

## Purpose

Every claim Dealix makes — internal or external — points to an artifact. If there's no artifact, the claim is treated as opinion. This page defines what counts as evidence and how it's stored.

## What counts as evidence

An evidence record contains four fields:

| Field | Definition |
|---|---|
| `artifact_path` | Repo path or storage URI to the underlying file. |
| `timestamp_utc` | When the artifact was produced. |
| `owner` | The human accountable for it. |
| `summary` | One sentence: what it shows. |

## Evidence categories

| Claim type | Required artifacts |
|---|---|
| Lead surfaced | `lead_table.csv` row + source URL + retrieval timestamp |
| Sprint delivered | Final report PDF + handover note + client acknowledgement |
| Refund issued | Approval file + bank transaction reference |
| Public claim made | Approval file + draft snapshot + publish link |
| Compliance posture | Policy doc + last review date + audit note |
| Revenue figure | Invoice + payment confirmation + ledger entry |
| Incident | Incident file + timeline + resolution note |

## Storage

- Private artifacts: `dealix-ops-private/evidence/<category>/<id>/`.
- Public method artifacts: in this repo under their owning docs.
- Each artifact has a stable ID — never overwritten, only superseded.

## Operational steps

1. Producer attaches evidence at the moment of the action — not at handover.
2. Delivery Lead checks evidence completeness during the QA gate ([docs/delivery/revenue_sprint/QA_CHECKLIST.md](../delivery/revenue_sprint/QA_CHECKLIST.md)).
3. Weekly trust ritual samples one closed deal and walks its evidence chain.
4. Missing evidence on a shipped deliverable opens an incident.

## Anti-patterns (do not do)

- Reconstructing evidence from memory after the fact.
- Storing PII inside a public-repo artifact.
- Citing a chat message as standalone evidence — convert it to a note with timestamp and owner.

## Cross-links

- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) — controls produce evidence.
- [AUDIT_POLICY.md](./AUDIT_POLICY.md) — what the audit checks.
- [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) — external proof pack.
- [docs/06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md)

## Owner & cadence

- Delivery Lead. Reviewed monthly.

## AR — ملخّص

كل ادّعاء يربط بأثر: مسار، زمن، مالك، ملخّص. الأدلة الخاصة في المستودع الخاص، والأدلة المنهجية في المستودع العام. غياب الدليل على تسليم منجز يُفتح حادثة. القيمة التقديرية ليست قيمة مُتحقَّقة.
