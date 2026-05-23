# Launch Operating Rhythm — Dealix

## الدور — Role

إيقاع تشغيلي يومي/أسبوعي/شهري يربط الـ Company OS بالواقع التجاري.

## الإيقاع اليومي — Daily rhythm

| الوقت | النشاط | الأمر |
| --- | --- | --- |
| 08:30 | CEO Daily Brief | `make ceo-daily-brief PRIVATE_OPS=...` |
| 08:45 | Revenue Forecast | `make revenue-forecast PRIVATE_OPS=...` |
| 09:00 | افتح `/launch`, `/approvals`, `/ceo` | متصفح |
| 09:15 | قرر action واحد فقط لليوم | كتابة في `<private_ops>/founder/today.md` |
| 17:30 | إغلاق طوابير + تحديث `conversation_log` | يدوي |

## الإيقاع الأسبوعي — Weekly rhythm

| اليوم | النشاط | الأمر |
| --- | --- | --- |
| الاثنين 09:00 | Weekly Growth War Room | `make weekly-growth-review PRIVATE_OPS=...` |
| الاثنين 09:30 | قرار Kill / Fix / Scale | تحديث `<private_ops>/learning/decisions.csv` |
| الخميس 14:00 | Trust risk review | فتح `/risk` + مراجعة `open_risks.csv` |
| الجمعة 11:00 | Learning loop sync | تحديث `learning/*.csv` |

## الإيقاع الشهري — Monthly rhythm

| التاريخ | النشاط |
| --- | --- |
| اليوم الأول | Machine ownership review |
| اليوم 15 | Risk register full review |
| اليوم 28 | Forecast accuracy review (مقارنة forecast vs cash) |

## قواعد الإيقاع — Rules

- لا يوم بدون CEO daily brief.
- لا أسبوع بدون weekly growth review.
- لا قرار Kill / Fix / Scale بدون evidence في `learning/*.csv`.
- لا تعديل forecast دون mark "manual override" في الملف.

## الملكية — Ownership

- Owner: Founder.
- Backup: Sales lead.
- Cadence verifier: `scripts/verify_execution_launch_layer.py`.
