---
title: Cash Control
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Cash Control — التحكم النقدي

## Purpose
Define who has authority over cash outflows and where dual-control is required. The founder is signer-of-record; dual-control above the threshold prevents a single compromised credential from draining accounts.

## Authority

| Outflow type | Single-signer limit | Dual-control above |
|---|---|---|
| Vendor / SaaS subscription | SAR 5,000 per month | SAR 5,000 |
| Contractor / agency payment | SAR 10,000 per invoice | SAR 10,000 |
| Marketing / content spend | SAR 5,000 per item | SAR 5,000 |
| Refunds | SAR 5,000 | SAR 5,000 (still A2 written per `REFUND_POLICY.md`) |
| Capital allocation transfers | Zero | All transfers require dual-control |
| Owner draw | Per `CAPITAL_ALLOCATION.md` schedule | Off-schedule: dual-control |

Dual-control = founder + one named delegate (initially: trusted bookkeeper or partner) on a co-signing channel.

## Rules
- No outflow without a purpose, vendor name, category, and matching invoice or receipt.
- No personal expenses paid from the business account, and no business expenses paid from the personal account. If accidentally swapped, reconcile within 7 days.
- Card and online banking credentials are not shared. Delegate signs under their own credentials.
- Monthly bank reconciliation is mandatory.
- Any outflow categorized as "miscellaneous" triggers a follow-up to recategorize within 7 days.

## Reserves
- Maintain a minimum operating reserve of 3 months of fixed cost in a separate sub-account.
- Reserves are not used for growth experiments. Growth experiments come from the growth allocation per [`CAPITAL_ALLOCATION.md`](CAPITAL_ALLOCATION.md).

## Operations
- Founder reviews bank position daily (1-minute glance).
- Weekly: founder reviews outflow categories vs budget.
- Monthly: full reconciliation; reserves verified against minimum.

## Evidence
- Every outflow has a source document (invoice, receipt) attached in the bookkeeping system.
- Reconciliation reports stored monthly.

## Owner & cadence
- Owner: Founder.
- Cadence: daily glance; weekly category review; monthly reconciliation.

## Cross-links
- [`CAPITAL_ALLOCATION.md`](CAPITAL_ALLOCATION.md)
- [`REFUND_POLICY.md`](REFUND_POLICY.md)
- `docs/governance/APPROVAL_MATRIX.md`

---

## القسم العربي

**السلطة:** اشتراكات SaaS حتى 5000 ريال/شهر بتوقيع واحد، فوقها تحكم مزدوج. مدفوعات مقاولين/وكالات حتى 10000 ريال/فاتورة بتوقيع واحد. صرف تسويق حتى 5000 ريال. الاسترداد حتى 5000 ريال (مع موافقة A2 دائمًا). تحويلات تخصيص رأس المال — تحكم مزدوج دائمًا. سحب المالك خارج الجدول — تحكم مزدوج.

**التحكم المزدوج:** المؤسس + مفوّض مُسمّى (كمحاسب موثوق أو شريك).

**القواعد:** لا تدفق بدون غرض ومورد وفئة ومستند. لا خلط بين الشخصي والتجاري. لا مشاركة بيانات اعتماد. مصاريف "متفرقات" تُعاد تصنيفها خلال 7 أيام.

**الاحتياطي:** 3 أشهر من التكلفة الثابتة في حساب فرعي منفصل، لا يُستخدم لتجارب النمو.

**المالك:** المؤسس. **الإيقاع:** نظرة يومية، مراجعة فئات أسبوعية، مطابقة شهرية.
