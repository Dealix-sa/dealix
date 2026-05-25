# Dealix Financial Model V1 — النموذج المالي التشغيلي

نموذج مالي **بسيط لكن قوي**. الهدف ليس نموذج مالي معقد قبل وجود الإيراد، بل أن تعرف:
كم يدخل، كم متوقّع، كم تصرف، كم runway، كم MRR، كم gross_margin.

> هذا الإصدار **V1 تشغيلي يومي** — يكمّل [`../company/FINANCIAL_MODEL.md`](../company/FINANCIAL_MODEL.md) (النموذج الاستراتيجي طويل المدى)، ولا يحلّ محله.

## الغرض — Purpose

تتبّع إيراد Dealix، النقد، runway، واقتصاديات العروض.

## المالك — Owner

Sami / Finance owner (المؤسس مؤقتاً).

## إيقاع المراجعة — Review Cadence

أسبوعي (cash + pipeline) — شهري (full review + runway).

---

## خطوط الإيراد — Revenue Lines

| Revenue Line | Type | Price Range (SAR) | Notes |
|---|---|---:|---|
| Signal Sample | one-time | 0–199 | دخول / تأهيل |
| Revenue Sprint | one-time | 2,500–7,500 | العرض الأول الأساسي |
| Managed Pilot | one-time / project | 9,500–25,000 | engagement أكبر |
| Revenue Desk | recurring | 5,000–20,000 / month | retainer |
| Dealix OS | custom | لاحقاً | فقط بعد الـ proof |

---

## المقاييس الأساسية — Core Metrics

### Cash
- `cash_collected`
- `cash_expected`
- `overdue_cash`

### Pipeline
- `pipeline_value`
- `weighted_pipeline`
- `proposals_pending`

### Recurring
- `MRR`
- `active_retainers`
- `churn_risk`

### Efficiency
- `founder_hours_per_sprint`
- `delivery_hours_per_sprint`
- `gross_margin` (estimate)

### Survival
- `monthly_expenses`
- `net_burn`
- `runway` (months)

---

## الحسابات الأساسية — Calculations

**Runway:**
```
runway = cash_on_hand / monthly_net_burn
```

**Gross Margin:**
```
gross_margin = (revenue - direct_costs) / revenue
```

**Weighted Pipeline:**
```
weighted_pipeline = Σ (deal_value * probability_by_stage)
```

**Net Burn:**
```
net_burn = max(monthly_expenses - mrr, 0)
```

> الحسابات الفعلية يُنفّذها `dealix/finance/calculator.py` ويُخرجها `scripts/generate_finance_review.py`. التشغيل: `make ceo-finance`.

---

## القواعد — Rules

- **لا تسليم كامل بدون** دفع، أو PO، أو موافقة كتابية.
- **كل proposal** له expected value و تاريخ متابعة.
- **خصم > 20%** يحتاج موافقة CEO.
- **الاسترداد (refund)** قرار A3 ولا يحدث تلقائياً.
- **مراجعة مالية** أسبوعية.

## الأدلّة — Evidence

- `dealix-ops-private/revenue/cash_collected.csv`
- `dealix-ops-private/revenue/pipeline_value.csv`
- `dealix-ops-private/revenue/mrr_tracker.csv`
- `dealix-ops-private/finance/expenses.csv`
- `dealix-ops-private/finance/runway_estimate.md`
- `dealix-ops-private/finance/monthly_finance_review.md`
- المراجع البرمجية:
  - `dealix/finance/calculator.py`
  - `auto_client_acquisition/operating_finance_os/financial_metrics.py`
- المراجع الوثائقية:
  - [`FINANCIAL_CONTROL_METRICS.md`](FINANCIAL_CONTROL_METRICS.md)
  - [`../company/FINANCIAL_MODEL.md`](../company/FINANCIAL_MODEL.md)

## الجملة الختامية

**Burn rate و runway** يخبرانك كم يمكن أن تستمر قبل الحاجة لإيراد إضافي. هذا ليس ترفاً — هذا **بقاء**.

## Last Reviewed

YYYY-MM-DD
