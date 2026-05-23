# Launch Command Center — Dealix

## الدور — Role

غرفة قيادة واحدة تربط كل ماكينات Dealix بالواقع التشغيلي اليومي حتى لا تعمل الأنظمة في عزلة عن السوق.

A single command surface that ties every Dealix machine, agent, and asset to its market reality — so nothing runs in isolation from the customer outcome.

## الغرض — Purpose

- إظهار جاهزية الإطلاق رقم واحد في كل لحظة.
- ربط كل قرار يومي بمصدر واحد للحقيقة.
- منع التشغيل الصامت لأي ماكينة بدون قيمة سوقية واضحة.
- توحيد لوحة القيادة بين Founder / Sales / Growth / Trust / Finance.

## ما تعرضه واجهة Launch — What `/launch` surfaces

- `readiness_score` — مجموع تقييم الجاهزية الفعلي.
- `launch_blockers` — قائمة blockers مفتوحة مرتبة بالأثر.
- `next_ceo_action` — أهم action يجب أن يفعله المؤسس اليوم.
- `active_campaign` — الحملة الحالية الفعالة فقط.
- `target_sector` — القطاع المستهدف هذا الأسبوع.
- `approved_assets` — الأصول الجاهزة للتوزيع.
- `distribution_queues` — حجم الطوابير المعتمدة بانتظار النشر اليدوي.
- `trust_risks` — مخاطر ثقة مفتوحة بحاجة إلى قرار.
- `revenue_forecast` — كاش مُحصَّل + قيمة pipeline موزونة.
- `source` — `api` أو `fallback` (شفافية كاملة).

## مصادر الحقيقة — Sources of truth

| Field | Source |
| --- | --- |
| readiness_score | `scripts/verify_launch_readiness.py` |
| launch_blockers | `<private_ops>/launch/blockers.csv` |
| next_ceo_action | `<private_ops>/founder/ceo_daily_brief.md` |
| active_campaign | `<private_ops>/launch/active_campaign.yaml` |
| target_sector | `<private_ops>/launch/target_sector.yaml` |
| approved_assets | `<private_ops>/launch/approved_assets.csv` |
| distribution_queues | `<private_ops>/distribution/queues.json` |
| trust_risks | `<private_ops>/trust/open_risks.csv` |
| revenue_forecast | `<private_ops>/finance/revenue_forecast.md` |

## واجهة الـ API الداخلية — Internal API

- `GET /api/v1/internal/launch/summary` — admin-key gated, JSON projection of the fields above with `source: "api" | "fallback"`.

## المخالفات الممنوعة — Hard rules

- لا يعرض هذا الـ command center أي رسالة "مضمونة" أو وعد بدخل.
- لا يدفع المستخدم لأي action خارجي تلقائي.
- لا يكشف أي secret أو بيانات عميل خام.
- كل cell تقرأ من مصدر يومي حقيقي — لا قيم ثابتة في الكود.

## الملكية — Ownership

- Owner: Founder.
- Substitute owner: Sales Lead (مؤقتاً).
- Last review: حدث يوميًا بواسطة `scripts/generate_ceo_daily_brief.py`.

## الروابط — Links

- [MARKET_ENTRY_READINESS_GATE.md](./MARKET_ENTRY_READINESS_GATE.md)
- [LAUNCH_SCORECARD.md](./LAUNCH_SCORECARD.md)
- [LAUNCH_OPERATING_RHYTHM.md](./LAUNCH_OPERATING_RHYTHM.md)
- [GO_TO_MARKET_MASTER_PLAN.md](./GO_TO_MARKET_MASTER_PLAN.md)
