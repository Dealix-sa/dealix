---
title: Delegation Rules
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Delegation Rules — قواعد التفويض

## Purpose
What can be delegated, what cannot, and which approval level each delegated action requires. Pairs with `docs/governance/APPROVAL_MATRIX.md`, `docs/governance/AI_ACTION_LEVELS.md`, and `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.

## Delegable actions and A-level mapping

| Action | Delegate-to | A-level | Reference |
|---|---|---|---|
| Draft a weekly client report | Delivery analyst | A1 (founder approves before send) | [`docs/client_success/WEEKLY_REPORT_TEMPLATE.md`](../client_success/WEEKLY_REPORT_TEMPLATE.md) |
| Draft an invoice | Delivery analyst or Ops Manager | A1 (founder approves before send) | [`docs/finance/BILLING_POLICY.md`](../finance/BILLING_POLICY.md) |
| Schedule client meetings | Ops Manager | A1 | — |
| Vendor renewal under SAR 5k/month | Ops Manager | A1 | [`docs/finance/CASH_CONTROL.md`](../finance/CASH_CONTROL.md) |
| Outbound message send (cold) | SDR/VA per approved template | A2 (founder approves template; SDR sends within voice rules) | [`docs/sales/SALES_MESSAGES.md`](../sales/SALES_MESSAGES.md) |
| Sector-report data pull | Delivery analyst | A1 | [`docs/content/SECTOR_REPORT_SYSTEM.md`](../content/SECTOR_REPORT_SYSTEM.md) |
| Publish post (LinkedIn/X) | Founder | A2 self-approval | [`docs/content/CONTENT_COMMAND_CENTER.md`](../content/CONTENT_COMMAND_CENTER.md) |
| Case study publication | Founder | A2 + client consent | [`docs/content/CASE_STUDY_SYSTEM.md`](../content/CASE_STUDY_SYSTEM.md) |
| Pricing exception (within floor) | Founder | A2 written | [`docs/sales/PROPOSAL_SYSTEM.md`](../sales/PROPOSAL_SYSTEM.md) |
| Refund | Founder | A2 written | [`docs/finance/REFUND_POLICY.md`](../finance/REFUND_POLICY.md) |

## Non-delegable actions (founder only)
- Signing a customer contract.
- Setting or changing pricing floor.
- Approving a new partner.
- Approving an A2-or-above release per [`docs/product/RELEASE_POLICY.md`](../product/RELEASE_POLICY.md).
- Approving a refund.
- Approving a case study with client name.
- Hiring decisions and termination decisions.
- Capital allocation changes per [`docs/finance/CAPITAL_ALLOCATION.md`](../finance/CAPITAL_ALLOCATION.md).
- Anything that would imply Dealix sends external messages on a customer's behalf.

## Rules
- Delegation is by writing, scoped to action class, time-bound where appropriate.
- A1 actions execute then log; A2 actions require approval before execution.
- A delegated action that fails its acceptance criteria reverts to founder for the next instance.
- Delegation does not transfer accountability. Founder remains accountable for outcomes.
- A delegate cannot sub-delegate without written founder authorization.

## Operations
- Each delegation logged in `docs/people/delegations_log.md` (created on first delegation): what, to whom, scope, expiry.
- Quarterly: founder reviews active delegations and renews, revokes, or scopes down.

## Evidence
- Delegations log + signed delegation entries are the evidence trail.

## Owner & cadence
- Owner: Founder.
- Cadence: per delegation; quarterly review.

## Cross-links
- [`docs/governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)
- [`docs/governance/AI_ACTION_LEVELS.md`](../governance/AI_ACTION_LEVELS.md)
- [`docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`](../governance/HUMAN_IN_THE_LOOP_MATRIX.md)
- [`DELEGATION_COMMAND_CENTER.md`](DELEGATION_COMMAND_CENTER.md)

---

## القسم العربي

**القابل للتفويض ومستوى A:**
- صياغة التقرير الأسبوعي — للمحلل، A1 (المؤسس يعتمد قبل الإرسال).
- صياغة الفاتورة — للمحلل أو مدير العمليات، A1.
- جدولة اجتماعات العملاء — لمدير العمليات، A1.
- تجديد مورد دون 5000 ريال/شهر — لمدير العمليات، A1.
- إرسال رسالة خارجية ضمن قالب معتمد — لـSDR، A2 (المؤسس يعتمد القالب).
- جلب بيانات تقرير قطاعي — للمحلل، A1.
- نشر منشور — للمؤسس، A2 ذاتية.
- نشر case study — للمؤسس، A2 + موافقة العميل.
- استثناء تسعير ضمن السقف — للمؤسس، A2 مكتوبة.
- استرداد — للمؤسس، A2 مكتوبة.

**غير القابل للتفويض (المؤسس فقط):** توقيع عقد عميل، تغيير سقف السعر، اعتماد شريك جديد، اعتماد إطلاق A2+، اعتماد استرداد، اعتماد case study مُسمّى، التوظيف والإنهاء، تغييرات تخصيص رأس المال، أي شيء يوحي بإرسال رسائل خارجية بالنيابة عن العميل.

**القواعد:** التفويض كتابي ومُحدد ومحدود زمنيًا. A1 ينفّذ ثم يُسجّل، A2 يحتاج اعتمادًا قبل التنفيذ. فشل المعايير يعيد الإجراء للمؤسس. المسؤولية لا تنتقل بالتفويض. لا تفويض فرعي بدون إذن مكتوب.

**المالك:** المؤسس. **الإيقاع:** مراجعة ربعية للتفويضات النشطة.
