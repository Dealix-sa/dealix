# Outreach Approval Queue / طابور اعتماد التواصل

**Owner:** Founder · **Updated:** 2026-06-06
**Rule:** every row is a **draft**. Nothing leaves until the founder approves.
**No auto-send. No spam. No cold/scraped contacts. founder approval required.**

> Policy: [`../../docs/03_governance/HUMAN_APPROVAL_POLICY.md`](../../docs/03_governance/HUMAN_APPROVAL_POLICY.md)
> Targets: [`../../data/growth/first_30_targets.csv`](../../data/growth/first_30_targets.csv)

---

## How this works

1. Draft a personalized message for a **warm** target (from the top-10
   shortlist).
2. Add it as a row below with `status = approval_required`.
3. Founder reviews → approves or rejects (records who + when).
4. Only approved messages are sent **manually** by the founder.

There is **no auto-send** path. Each draft requires founder approval.

---

## Queue

| # | Target | Channel | consent_basis | Draft summary | Status | Approved by / when |
|---|---|---|---|---|---|---|
| 1 | [Warm account A] | (warm reply) | prior_engagement | Diagnostic invite, references prior work | approval_required | — |
| 2 | [Warm account B] | (warm reply) | referred_by_partner | Intro + free Diagnostic offer | approval_required | — |
| 3 | [Warm account C] | (warm reply) | opted_in_form | Follow up on their form submission | approval_required | — |
| 4 | [Warm account D] | (warm reply) | referred_by_customer | Referral mention + Diagnostic offer | approval_required | — |
| 5 | [Warm account E] | (warm reply) | prior_engagement | Re-engage, offer Command Sprint Diagnostic | approval_required | — |

---

## Draft 1 (example, NOT sent)

> **To:** [Warm account A] — warm, prior engagement.
> **EN:** "Hi <name>, following our earlier work — I put together a quick way to
> spot where revenue might be leaking in your funnel. Free 20-min Diagnostic, no
> commitment. Worth a look? (Estimated findings, not guaranteed outcomes.)"
> **AR:** «مرحباً <الاسم>، بناءً على عملنا السابق — جهّزت طريقة سريعة لاكتشاف أين
> قد تتسرّب الإيرادات. تشخيص مجاني 20 دقيقة، بلا التزام. (نتائج تقديرية وليست
> مضمونة.)»
> **Status:** approval_required — founder approval required before sending.

---

## Guardrails

- ❌ No auto-send. ✅ Founder approval required for every message.
- ❌ No cold/scraped contacts — warm + consent_basis only.
- ❌ No guaranteed-revenue language — estimates carry `~` + disclaimer.
