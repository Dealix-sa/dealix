# Dealix Launch Package V15 — Founder Daily Execution Autopilot

V15 لا يضيف قناة جديدة فقط؛ يربط كل طبقات Dealix السابقة في تشغيل يومي للفاوندر. الهدف أن يبدأ اليوم بـ command brief واضح، ثم أعلى 10 مهام، ثم مسودات رسائل/عروض/فواتير/تقارير، ثم سجل تنفيذ ومراجعة نهاية اليوم.

القواعد:
- لا إرسال آلي خارجي.
- لا وعود نتائج مضمونة.
- لا استخدام بيانات حساسة في المخرجات العامة.
- كل outbound، invoice، proposal، أو client-facing report يحتاج مراجعة بشرية.
- كل task له next action وowner وdeadline.

أوامر التشغيل:

```bash
python scripts/dealix_v15_readiness_check.py
python scripts/dealix_founder_command_brief.py
python scripts/dealix_top10_task_ranker.py
python scripts/dealix_daily_artifact_generator.py
python scripts/dealix_execution_log.py --task "Review top 10 tasks" --status done --note "Founder reviewed"
python scripts/dealix_founder_autopilot_dashboard.py
```

أو:

```bash
make dealix-v15-daily
```
