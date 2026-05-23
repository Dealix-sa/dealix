---
title: Financial Dashboard (Schema)
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Financial Dashboard — لوحة المؤشرات المالية

## Purpose
Schema for the finance metrics view. One table, one source per cell, one owner. Until BI tooling is in place, markdown + a spreadsheet is enough.

## Schema (JSON)
```json
{
  "as_of_date": "YYYY-MM-DD",
  "cash_position": {
    "operating_balance_sar": 0,
    "reserves_balance_sar": 0,
    "reserves_floor_sar": 0,
    "months_runway": 0
  },
  "revenue": {
    "mrr_sar": 0,
    "new_mrr_sar": 0,
    "expansion_mrr_sar": 0,
    "contraction_mrr_sar": 0,
    "churned_mrr_sar": 0,
    "net_new_mrr_sar": 0,
    "one_time_revenue_month_sar": 0,
    "bookings_signed_not_started_sar": 0
  },
  "ar": {
    "outstanding_total_sar": 0,
    "outstanding_0_14_sar": 0,
    "outstanding_15_30_sar": 0,
    "outstanding_31_60_sar": 0,
    "outstanding_60_plus_sar": 0
  },
  "cost": {
    "fixed_monthly_sar": 0,
    "variable_month_sar": 0,
    "growth_spend_month_sar": 0
  },
  "allocation_variance_qtd_pct": {
    "reinvest": 0,
    "growth": 0,
    "owner_draw": 0,
    "buffer": 0
  },
  "customers": {
    "active_count": 0,
    "new_this_month": 0,
    "churned_this_month": 0
  },
  "refunds_month": {
    "count": 0,
    "amount_sar": 0
  }
}
```

## Source of each field

| Field | Source |
|---|---|
| cash_position.* | Bank export + reserves sub-account |
| revenue.mrr_* | MRR register per [`MRR_DEFINITION.md`](MRR_DEFINITION.md) |
| ar.* | Invoice register per [`INVOICE_WORKFLOW.md`](INVOICE_WORKFLOW.md) |
| cost.* | Outflow categories per [`CASH_CONTROL.md`](CASH_CONTROL.md) |
| allocation_variance_qtd_pct.* | Quarterly allocation per [`CAPITAL_ALLOCATION.md`](CAPITAL_ALLOCATION.md) |
| customers.* | Customer ledger |
| refunds_month.* | Refund register per [`REFUND_POLICY.md`](REFUND_POLICY.md) |

## Rules
- One source per field. No double-counting.
- Dashboard does not invent metrics. Anything reported externally must trace to a register.
- Numbers below registration cadence (e.g., daily MRR) are not published; metric remains monthly.
- All amounts in SAR.

## Operations
- Built monthly by founder; published by 5th of following month to `docs/finance/registers/YYYY-MM_dashboard.md`.

## Evidence
- Every field links to its source register.

## Owner & cadence
- Owner: Founder.
- Cadence: monthly publish; quarterly trend brief.

## Cross-links
- [`MRR_DEFINITION.md`](MRR_DEFINITION.md)
- [`INVOICE_WORKFLOW.md`](INVOICE_WORKFLOW.md)
- [`CAPITAL_ALLOCATION.md`](CAPITAL_ALLOCATION.md)

---

## القسم العربي

**الغرض:** مخطط لعرض المؤشرات المالية. حقل واحد لكل خلية، مصدر واحد، مالك واحد.

**الأقسام (JSON أعلاه):** الوضع النقدي، الإيراد (MRR ومكوناته + إيراد مرة واحدة + حجوزات موقّعة)، الذمم المدينة بفئات المُسنّ، التكاليف (ثابت/متغير/نمو)، فروقات التخصيص الربع حتى تاريخه، العملاء، الاسترداد الشهري.

**القواعد:** مصدر واحد لكل حقل، لا اختراع مقاييس، لا نشر متكرر أعلى من إيقاع التسجيل، كل المبالغ بالريال.

**المالك:** المؤسس. **الإيقاع:** نشر شهري بحلول الخامس، ملخص اتجاهات ربعي.
