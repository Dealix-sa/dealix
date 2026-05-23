# Revenue Forecasting System — Dealix

## الدور — Role

نظام توقع كاش أسبوعي مبني على bookings فعلية + pipeline موزون. ليس "حلم"، بل حساب.

## المخرج — Output

```
<private_ops>/finance/revenue_forecast.md
```

## الأقسام — Sections

1. **Cash collected** — كاش مُحصَّل فعلاً (مصدر: `cash_collected.csv`).
2. **Open proposal value** — مجموع قيمة proposals لم تُغلق (مصدر: `proposal_log.csv`).
3. **Weighted pipeline** — قيمة موزونة (انظر `PIPELINE_WEIGHTING_MODEL.md`).
4. **Payment risk** — proposals ≥14 يوم بدون رد.
5. **Next cash action** — الـ action #1 لزيادة الـ cash هذا الأسبوع.
6. **Forecast confidence** — `low | medium | high`.

## واجهة API الداخلية

- `GET /api/v1/internal/finance/forecast` — admin-key gated.

## التوليد — Generation

```bash
make revenue-forecast PRIVATE_OPS=/opt/dealix-ops-private
```

Script: `scripts/generate_revenue_forecast.py`.

## القواعد — Rules

- لا تضمين إيرادات لم تُحصَّل في `Cash collected`.
- `Weighted pipeline` يستخدم أوزان موثقة في `PIPELINE_WEIGHTING_MODEL.md`.
- forecast confidence ينخفض مع زيادة `open_risks` في Risk Register.
- forecast لا يدّعي اليقين — يكتب صراحة "estimate".

## الملكية — Ownership

- Owner: Founder.
- Cadence: يومي + مراجعة شهرية (forecast vs actual).
