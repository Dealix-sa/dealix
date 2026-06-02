# Dealix Business Metrics — مؤشرات الأعمال

> **القاعدة الصلبة (Article 8):** الإيراد المؤكَّد يُقرأ **فقط** من حالة `payment_confirmed`. **نية الفاتورة (`invoice_intent`) ليست إيراداً.** لا vanity metrics، ولا `payment_received` وهمي.
>
> **Hard rule (Article 8):** confirmed revenue reads ONLY from `payment_confirmed`; invoice intent is NOT revenue. No vanity metrics.

**مصدر الحقيقة (Source of truth):**
- محرك المؤشرات: `auto_client_acquisition/business_metrics_board/computer.py` (12 مؤشراً، deterministic) + `schemas.py`.
- Scorecards: `scripts/founder_daily_scorecard.py` · `scripts/founder_weekly_scorecard.py` · `scripts/dealix_growth_scorecard.py`.
- السجلات: [`docs/ledgers/`](ledgers/README.md) — Proof · Value · Capital · Client · Delivery.
- استيراد KPI تجاري: `scripts/apply_kpi_founder_commercial.py` (**لا تُختلق أرقام CRM** في الأتمتة).

**مرتبط:** [`docs/BUSINESS_AUTOPILOT_OS.md`](BUSINESS_AUTOPILOT_OS.md) · [`reports/company_os/weekly/GROWTH_SCORECARD.md`](../reports/company_os/weekly/GROWTH_SCORECARD.md).

---

## 1) مؤشرات الإيراد (Revenue)

| المؤشر | المصدر | قاعدة النزاهة |
|--------|--------|----------------|
| `confirmed_revenue_sar` | `payment_confirmed` فقط | الفاتورة المعلّقة لا تُحتسب |
| `monthly_recurring_estimate_sar` | retainers نشطة | تقدير معلّم بوضوح |
| `pipeline_estimate_sar` | War Room | تقدير لا إيراد |
| Reply rate / Demos / Proposals | War Room + CRM | من بيانات حقيقية فقط |
| `sprint_to_partner_conversion` | partner_conversions ÷ sprint_count | — |

## 2) مؤشرات التسليم (Delivery)

- زمن الـ onboarding · زمن أول workflow حي · `proof_events_total` · `case_studies_published` · `churn_risk_count` · رضا العميل (NPS responses).

## 3) مؤشرات المنتج (Product)

- تشغيلات أتمتة ناجحة/فاشلة · مهام يدوية أُزيلت · استخدام لوحة المؤسس · bugs.

## 4) مؤشرات المالية (Finance)

- `gross_margin = (revenue − direct_cost) / revenue` (0 إن لا إيراد) · `estimated_direct_cost_sar` · `estimated_founder_hours` · تكلفة API/أدوات لكل عميل · payback. المرجع: `auto_client_acquisition/operating_finance_os/`.

## 5) رافعة المؤسس (Founder leverage)

- قرارات وُضِّحت · متابعات يدوية أُزيلت · تقارير وُلّدت · ساعات مؤسس مُوفَّرة (تقدير).

---

## 6) كيف تُملأ المؤشرات (How populated)

`compute_customer_metrics(...)` دالة نقية؛ الـ router يسحب البيانات الحقيقية من `payment_ops` / `proof_ledger` / `customer_success`. الأرقام التجارية (CRM) تُستورد من ملف gitignored عبر `apply_kpi_founder_commercial.py` — **النظام لا يخترع أرقاماً** (القانون 4/7).

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
