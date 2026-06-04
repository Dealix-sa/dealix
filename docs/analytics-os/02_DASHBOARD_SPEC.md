# Dashboard Spec — مواصفات لوحة المعلومات

The live commercial dashboard layout. It visualizes the funnel from [01_EVENT_TAXONOMY.md](01_EVENT_TAXONOMY.md). Every panel sources from a defined metric; none display invented values.

تخطيط لوحة المعلومات التجارية المباشرة. تعرض القمع من تصنيف الأحداث. كل لوحة تستمد من مقياس محدد، ولا تعرض قيمًا مُختلَقة.

## Panels — اللوحات

### 1. Funnel overview — نظرة القمع
A top-to-bottom funnel: website_visitors → cta_clicks → audit_requests → leads_created → ... → retainer_starts. Show absolute counts and step-to-step conversion. Conversions are descriptive of the period, not forecasts.

### 2. Draft-to-send governance — حوكمة المسودات
drafts_generated, founder_review_count, manual_sends side by side. This panel makes the governing rule visible: drafts always exceed sends, and every send passed review.

### 3. Response quality — جودة الاستجابة
replies and positive_replies, with positive-reply share. Definition is fixed per the taxonomy so the trend is comparable.

### 4. Revenue — الإيراد
pipeline_sar and realized_revenue_sar as two distinct series, never summed together. Label both in SAR.

### 5. Conversion to paid — التحويل إلى مدفوع
booked_diagnostics → paid_diagnostics → pilots_proposed → pilots_sold → retainer_starts.

### 6. Safety strip — شريط الأمان
safety_violations and compliance_rejections, always visible at the top of the dashboard, never hidden in a sub-tab.

## Layout rules — قواعد التخطيط

- The safety strip is pinned and always on screen.
- pipeline_sar and realized_revenue_sar are visually separated and color-distinct.
- Any panel with no data this period shows `—`, not a zero-filled fake trend.
- Each panel footer names its source: `auto` ledger/analytics or `manual` entry.

## Panel schema — مخطط اللوحة

```json
{
  "panel_id": "string",
  "title_en": "string",
  "title_ar": "string",
  "metrics": ["metric_name"],
  "viz": "funnel | bar | line | counter",
  "source": "auto | manual",
  "empty_state": "—",
  "pinned": false
}
```

## Refresh and entry — التحديث والإدخال

- `auto` panels refresh on ledger/analytics update.
- `manual` panels reflect the latest founder entry with `entered_by` and timestamp.
- No panel projects future values. Trends describe history only.

## Forbidden on the dashboard — ممنوع على اللوحة

No "guaranteed", "100%", projected ROI tiles, or fabricated growth curves. No blending of pipeline and realized revenue.

## Related — مراجع

- Metrics: [01_EVENT_TAXONOMY.md](01_EVENT_TAXONOMY.md)
- Value dashboard: [../08_value_os/VALUE_DASHBOARD.md](../08_value_os/VALUE_DASHBOARD.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
