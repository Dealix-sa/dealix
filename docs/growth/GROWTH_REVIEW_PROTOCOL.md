# Growth Review Protocol — Dealix

## الدور — Role

بروتوكول جلسة Growth Review الأسبوعية — كيف تُدار حرفياً.

## ترتيب الجلسة — Agenda (60 min)

| الدقائق | البند |
| --- | --- |
| 00–05 | قراءة Scorecard من `LAUNCH_SCORECARD.md` |
| 05–15 | What moved / What stalled |
| 15–25 | Sector & channel performance |
| 25–35 | Message / offer learning |
| 35–45 | Experiments closed → Kill/Fix/Scale |
| 45–55 | Next week target (1 رقم فقط) |
| 55–60 | تأكيد القرارات + كتابتها في `decisions.csv` |

## المدخلات المطلوبة — Required inputs

- `<private_ops>/finance/cash_collected.csv`
- `<private_ops>/sales/proposal_log.csv`
- `<private_ops>/sales/meetings.csv`
- `<private_ops>/learning/experiments.csv`
- `<private_ops>/distribution/queues.json`

## القواعد — Rules

- إذا كان أي مدخل مفقود → الجلسة تُؤجَّل وتُسجَّل ملاحظة في `<private_ops>/launch/blockers.csv`.
- لا "vibe-based" قرارات — كل قرار يستند لـ row في CSV.
- لا تجاوز 60 دقيقة. إذا لم نصل لقرار → القرار = "Fix next week".

## المخرجات — Outputs

- `weekly_growth_review.md`
- صف جديد لكل قرار في `<private_ops>/learning/decisions.csv`.
- تحديث `<private_ops>/launch/active_campaign.yaml` إذا تغيرت الحالة.

## الملكية — Ownership

- Owner: Founder.
- Cadence: أسبوعي.
