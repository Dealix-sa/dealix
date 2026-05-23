# Launch Scorecard — Dealix

## الدور — Role

بطاقة قياس واحدة تجيب على سؤال "هل نتقدم نحو السوق هذا الأسبوع؟" بدون فتح 12 لوحة.

A single weekly scorecard that answers: did we move toward market this week? Built on observable inputs only — no vanity metrics.

## مؤشرات النتائج — Outcome metrics

| Metric | Definition | Source |
| --- | --- | --- |
| `cash_collected_sar` | كاش فعلي مُحصَّل هذا الأسبوع | `<private_ops>/finance/cash_collected.csv` |
| `proposals_sent` | عدد عروض اعتمدها المؤسس وأُرسلت يدويًا | `<private_ops>/sales/proposal_log.csv` |
| `meetings_booked` | اجتماعات مؤكدة من العميل | `<private_ops>/sales/meetings.csv` |
| `samples_delivered` | عينات أُرسلت بعد اعتماد Trust | `<private_ops>/sales/samples.csv` |
| `approved_outreach` | رسائل اعتمدها المؤسس (لم تُرسل تلقائيًا) | `<private_ops>/distribution/queues.json` |

## مؤشرات الجاهزية — Readiness metrics

| Metric | Definition | Source |
| --- | --- | --- |
| `readiness_score` | نسبة الشهادات الخضراء | `scripts/verify_launch_readiness.py` |
| `open_blockers` | عدد blockers مفتوحة | `<private_ops>/launch/blockers.csv` |
| `open_trust_risks` | مخاطر ثقة بدرجة high+ | `<private_ops>/trust/open_risks.csv` |
| `failing_machines` | ماكينات حالتها `degraded` أو `down` | `<private_ops>/ops/machine_health.csv` |

## مؤشرات التعلم — Learning metrics

| Metric | Definition | Source |
| --- | --- | --- |
| `experiments_run` | تجارب أنهيت دورة قياس | `<private_ops>/learning/experiments.csv` |
| `kill_decisions` | قرارات وقف نشاطات | `<private_ops>/learning/decisions.csv` |
| `scale_decisions` | قرارات مضاعفة موارد | `<private_ops>/learning/decisions.csv` |

## قاعدة القراءة — Reading rule

- **Green week**: `cash_collected_sar > 0` AND `open_blockers == 0` AND `failing_machines == 0`.
- **Yellow week**: قيمة pipeline موزونة تقدمت لكن لم يُحصَّل كاش.
- **Red week**: blockers أو machines سقطت بدون تقدم على المعارضات.

## ما لا يُحسب — What is NOT scored

- "Impressions", views, vanity reach.
- LinkedIn likes أو followers.
- عدد المحادثات الباردة.
- عدد الملفات أو الـ commits.

## الملكية — Ownership

- Owner: Founder.
- Updated by: `scripts/generate_weekly_growth_review.py`.
- Review cadence: كل اثنين 09:00 (محلي).
