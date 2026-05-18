# Proof Pack 2.0 — Commercial Proof Mode standard

The Proof Pack is the real first product of Dealix. Use this **client-facing**
11-section standard for every engagement: an auditable narrative + an honest
upsell bridge.

**Compat:** supersedes the minimal [`proof_pack.md`](proof_pack.md) for new
engagements. Aligned with
[`../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md`](../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md).

---

## Truth Labels — وسوم الصدق

Every claim, number, and outcome in the Proof Pack carries exactly one label.
No claim ships unlabelled. This enforces the `no_unverified_outcomes` and
`no_fake_proof` non-negotiables.

| Label | العربية | Meaning |
|---|---|---|
| **Estimate** | تقديري | A modelled / illustrative figure. Not measured. |
| **Observed** | مُلاحَظ | Seen directly in the client's data or workflow. |
| **Client-confirmed** | مؤكَّد من العميل | The client explicitly agreed this is true. |
| **Payment-confirmed** | مؤكَّد بالدفع | Backed by an `invoice_paid` event. |
| **Repeated workflow** | سير عمل متكرر | The same workflow ran successfully ≥ 2 times. |
| **Retainer-ready** | جاهز للريتينر | Proven enough to support a recurring engagement. |

Example — مثال:
> Follow-up gap: **Observed** · Potential value: **Estimate** ·
> Client pain: **Client-confirmed** · Revenue: **Payment-confirmed** only.

---

## The 11 sections — الأقسام الإحدى عشر

```markdown
# Proof Pack — [Client] — [Date]

## 1. Context
Why this engagement exists; the one primary outcome the client wanted.

## 2. Inputs reviewed
- Files / rows / documents received:
- Data sources:
- Constraints (legal, time, access):

## 3. Lead / workflow status
- Leads / opportunities reviewed:
- Current status board (per lead / per workflow):

## 4. Source quality
- Where leads originate (SOAEN — Source):
- Source clarity gaps:

## 5. Owner gaps
- Leads / steps without a clear owner (SOAEN — Owner):

## 6. Approval risks
- AI / external actions running without approval (SOAEN — Approval):

## 7. Follow-up gaps
- Missed / late / missing follow-ups (SOAEN — Next Action):
- Evidence gaps (SOAEN — Evidence):

## 8. Draft messages
- Follow-up drafts prepared (for human approval — never auto-sent):

## 9. Recommended next actions
- Prioritised, owner-assigned next steps:

## 10. Truth labels
- Each claim above tagged: Estimate / Observed / Client-confirmed /
  Payment-confirmed / Repeated workflow / Retainer-ready.

## 11. Upgrade path
- Recommended next offer (one of: Sprint / Data Pack / Retainer / Partner):
- Why:
- Expected outcome (labelled honestly):
```

---

## Rules

- Every Proof Pack must produce exactly one upgrade outcome: Sprint proposal,
  retainer candidate, referral, partner intro, anonymous insight, or a
  benchmark data point.
- The Proof Pack is also **retainer collateral** — design section 11 for a
  clear monthly story ([`../growth/EXPANSION_OFFER_SYSTEM.md`](../growth/EXPANSION_OFFER_SYSTEM.md)).
- No guarantee, no fake metric, no customer name without signed permission.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
