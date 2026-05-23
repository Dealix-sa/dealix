---
title: Trust Command Center
owner: Founder / Trust Lead
status: active
last_review: 2026-05-23
---

# Trust Command Center — مركز قيادة الثقة

## Purpose

Single index for every trust control in Dealix. Answers: who owns what, what runs daily, what runs weekly, where the evidence lives. If a regulator, investor, or enterprise procurement officer asks "show me your safety system," this is the door they walk through.

## Owned-by map

| Domain | Doc | Owner |
|---|---|---|
| Controls inventory | [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) | Trust Lead |
| Approval gates | [APPROVAL_MATRIX.md](./APPROVAL_MATRIX.md) | Founder |
| Agent boundaries | [AUTONOMY_POLICY.md](./AUTONOMY_POLICY.md) | Trust Lead |
| Claim discipline | [NO_OVERCLAIM_POLICY.md](./NO_OVERCLAIM_POLICY.md) | Content Lead |
| Approved phrasing | [SAFE_LANGUAGE_LIBRARY.md](./SAFE_LANGUAGE_LIBRARY.md) | Content Lead |
| Repo split | [PUBLIC_PRIVATE_BOUNDARY.md](./PUBLIC_PRIVATE_BOUNDARY.md) | Founder |
| Evidence chain | [EVIDENCE_SYSTEM.md](./EVIDENCE_SYSTEM.md) | Delivery Lead |
| Incidents | [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md) | Founder |
| Audit | [AUDIT_POLICY.md](./AUDIT_POLICY.md) | Trust Lead |

Related: [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), [docs/05_governance_os/GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md).

## Daily ritual (15 min)

1. Open the approval queue. Clear any A1 items waiting on the founder.
2. Scan AI Run Ledger for failed schema validations or flagged outputs.
3. Confirm no public commit contains a client name, contact, or unapproved claim.

## Weekly ritual (45 min, Sundays)

1. Review evidence completeness for every delivery shipped that week.
2. Rotate one random closed deal — pull its evidence pack, verify it would survive an audit.
3. Read the week's incident log (even if zero — confirm zero is true).
4. Update `last_review` on any doc you touched.

## Monthly ritual

- Reconcile the controls inventory against actual practice. Anything drifted gets a fix ticket or a doc update — never both ignored.

## Evidence

Every ritual outputs a dated note in `dealix-ops-private/trust/rituals/YYYY-MM-DD.md`. Missing rituals are themselves auditable.

## Owner & cadence

- Trust Lead owns this page.
- Reviewed every Sunday. `last_review` updated whenever a linked doc changes.

## AR — ملخّص

مركز قيادة الثقة هو الفهرس الموحّد لكل ضوابط الأمان في ديليكس. يحدّد المالك، والإيقاع اليومي والأسبوعي والشهري، ومكان الأدلة. أي مراجع خارجي يبدأ من هنا. الطقوس مكتوبة، والأدلة محفوظة في المستودع الخاص. القيمة التقديرية ليست قيمة مُتحقَّقة.
