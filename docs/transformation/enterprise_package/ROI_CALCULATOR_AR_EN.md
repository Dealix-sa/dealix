# ROI Calculator — Worksheet / ورقة عمل تقدير العائد

> **Estimates, not guarantees.** تقديرات وليست أرقامًا مُتحقَّقة. The numbers are
> bounded ranges; actuals depend on data quality, adoption, and scope.

Pairs with the governed calculator `dealix/commercial/roi_calculator.py`
(`POST /api/v1/commercial/roi/estimate`) and the
[roi_realization_narrative_template.md](roi_realization_narrative_template.md)
(used post-pilot to convert estimates → measured outcomes via Proof events).

## Inputs / المدخلات

| Input | حقل | Notes |
|---|---|---|
| `manual_hours_per_week` | ساعات يدوية/أسبوع | Repetitive work the system offloads |
| `hourly_cost_sar` | تكلفة الساعة (ر.س) | Loaded cost of the staff time |
| `lost_leads_per_month` | فرص ضائعة/شهر | Leads dropped due to slow/no follow-up |
| `avg_deal_value_sar` | متوسط قيمة الصفقة | Average closed-deal value |
| `recovered_conversion_pct` | نسبة التحويل المُستعادة | Conservative % of recovered leads that close |
| `setup_cost_sar` / `monthly_cost_sar` | الإعداد / الشهري | From the catalog ranges |

## Method / المنهجية (conservative bands)

- **Time savings/yr** = hours/wk × 52 × hourly cost × **40–70%** capture band.
- **Recovered revenue/yr** = lost_leads × 12 × avg_deal × conversion% × **50–100%** band.
- **Gross value** = time + recovered. **Net** = gross − (setup + 12×monthly).
- **Payback (months)** = setup ÷ monthly net benefit.

Bands stay **below the theoretical ceiling** on purpose — transformation rarely
captures 100%. النطاقات أقل من السقف النظري عمدًا.

## Worked example / مثال

20 h/wk · 80 SAR/h · 10 lost leads/mo · 5,000 SAR/deal · 15% · setup 35k · 8k/mo:
the calculator returns a **gross/net range** + **payback window**, all stamped
`is_estimate=true`, with no guarantee language.

## Rule / القاعدة

Estimated value is **not** verified value. Convert to measured ROI only via Proof
events (see realization narrative). القيمة التقديرية ليست قيمة مُتحقَّقة.
