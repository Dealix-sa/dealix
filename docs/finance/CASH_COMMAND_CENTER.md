# Cash Command Center — Dealix

## الدور — Role

نظرة واحدة على وضع الكاش — لا حسابات معقدة، فقط الأرقام التي تحدد البقاء.

## الأرقام — Numbers

| Metric | Definition | Source |
| --- | --- | --- |
| `cash_in_bank_sar` | كاش متوفر | manual entry يومي في `cash_collected.csv` |
| `monthly_burn_sar` | الإنفاق الشهري الفعلي | `<private_ops>/finance/burn.csv` |
| `runway_months` | `cash_in_bank / monthly_burn` | محسوب |
| `cash_collected_this_week_sar` | حاصل الأسبوع | `cash_collected.csv` |
| `next_payment_action` | follow-up #1 | `forecast` |

## قواعد القراءة — Reading rules

- `runway_months < 3` → red alert في Daily Brief.
- `runway_months 3–6` → yellow alert.
- `runway_months ≥6` → green.

## القواعد — Rules

- لا تشغيل حملة paid acquisition بدون runway ≥3 شهور.
- كل sample/proposal يحدد deadline دفع واضح في النص.
- ZATCA invoice يُصدر فوراً بعد القبول الشفهي.

## الملكية — Ownership

- Owner: Founder.
- Updated by: `scripts/generate_revenue_forecast.py`.
