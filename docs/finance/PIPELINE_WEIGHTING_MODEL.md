# Pipeline Weighting Model — Dealix

## الدور — Role

نموذج محافظ لتوزين الـ pipeline. الفلسفة: **underweight by default**.

## الأوزان — Weights

| Stage | تعريف | Weight |
| --- | --- | --- |
| `discovery` | ≥1 مكالمة 30 دقيقة | 0.10 |
| `sample_sent` | عينة معتمدة + مُسلَّمة | 0.25 |
| `proposal_sent` | proposal مُرسل بعد sample | 0.40 |
| `verbal_yes` | الزبون قال "نعم" شفهياً | 0.60 |
| `invoice_issued` | فاتورة ZATCA صادرة | 0.80 |
| `paid` | كاش مُحصَّل | 1.00 |

## قاعدة الـ Cap

- لا حالة تتجاوز 0.80 قبل دخول الكاش الفعلي.
- صفقات stalled (>14 يوم بدون رد) تُخصم 50% من وزنها.
- صفقات لم تُمسس >30 يوم تُحوَّل إلى `dormant` بوزن 0.05.

## المصدر — Source

- `<private_ops>/sales/proposal_log.csv`
- `<private_ops>/sales/meetings.csv`
- `<private_ops>/finance/cash_collected.csv`

## القواعد — Rules

- لا تعديل أوزان بدون evidence من ≥10 صفقات تاريخية.
- لا "Promotion" مرحلة بدون artefact في `<private_ops>`.

## الملكية — Ownership

- Owner: Founder.
