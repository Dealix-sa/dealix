---
title: MRR Definition
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# MRR Definition — تعريف الإيراد الشهري المتكرر

## Purpose
Define exactly what counts as Monthly Recurring Revenue at Dealix and what does not. Prevents inflated metrics in board updates, content, and decisions.

## Definitions
- **MRR** — the monthly normalised value of revenue that recurs without renegotiation.
- **ARR** — MRR × 12.
- **Active customer** — paying customer with an active recurring agreement and at least one invoice paid in the current period.

## What counts as MRR

| Item | Counts | How |
|---|---|---|
| Signed monthly retainer | Yes | Monthly fee at the contracted price |
| Signed annual contract billed monthly | Yes | Monthly fee |
| Signed annual contract billed annually | Yes | Annual fee ÷ 12 |
| Quarterly billed retainer | Yes | Quarterly fee ÷ 3 |

## What does not count as MRR

| Item | Why |
|---|---|
| Sprint or pilot fees (fixed scope, one-time) | Not recurring |
| Implementation / onboarding fees | One-time |
| Change-request fees | One-time |
| Pass-through expenses billed to client | Not Dealix revenue |
| Estimated upsell, deferred contracts, verbal commitments | Not signed |
| Discounts, write-offs, refunds | Reduce MRR or reverse it |
| Foreign currency conversion gains | Not revenue |

## Rules
- A retainer starts contributing to MRR on the first day of the first paid period.
- A retainer stops contributing to MRR on the day cancellation takes effect, not on the day notice was given.
- Mid-period upgrades/downgrades take effect on the next billing cycle for MRR purposes.
- A churned customer never appears in retroactive MRR. We do not adjust history to be flattering.
- "Bookings" (signed but not yet started) is a separate metric. Never reported as MRR.

## Operations
- Monthly MRR computation: sum of contracted monthly values of active customers on the last day of the month.
- Components reported: new MRR, expansion MRR, contraction MRR, churned MRR, net new MRR.
- Stored in `docs/finance/registers/YYYY-MM_mrr.md` (created on first cycle).

## Evidence
- Each line in the MRR register links to the underlying contract and invoice register row.
- Recomputation possible from primary records at any time.

## Owner & cadence
- Owner: Founder.
- Cadence: monthly compute on last business day; published by 5th of next month.

## Cross-links
- [`BILLING_POLICY.md`](BILLING_POLICY.md)
- [`FINANCIAL_DASHBOARD.md`](FINANCIAL_DASHBOARD.md)
- [`INVOICE_WORKFLOW.md`](INVOICE_WORKFLOW.md)

---

## القسم العربي

**يُحتسب MRR:** retainer شهري موقّع، عقد سنوي بفوترة شهرية، عقد سنوي بفوترة سنوية (يُقسّم على 12)، فوترة ربعية تُقسّم على 3.

**لا يُحتسب:** سبرنت أو تجريبي (مرّة واحدة)، رسوم تنفيذ، رسوم تغيير، مصاريف عبور، توقعات أو وعود شفهية، خصومات وشطب واسترداد، أرباح فروقات عملة.

**القواعد:** يبدأ retainer بالإسهام في MRR أول يوم فترة مدفوعة، ويتوقف يوم سريان الإلغاء. الترقية/التخفيض منتصف الفترة تسري في الدورة التالية. التاريخ لا يُعدَّل ليبدو أجمل. "الحجوزات" مقياس منفصل.

**التشغيل:** حساب آخر يوم عمل في الشهر، نشر بحلول الخامس من الشهر التالي. المكونات: MRR جديد، توسع، انكماش، churned، صافي جديد.

**المالك:** المؤسس.
