# Dealix Launch Package V2 — Founder Execution Layer

هذه الحزمة تكمل حزمة الإطلاق الأولى وتحوّل Dealix إلى نظام مواقعي/تشغيلي أوضح:

- صفحات موقع إضافية: industries, pricing, case-studies, contact, privacy, terms.
- نظام تشغيل يومي: lead scoring, pipeline, daily command center.
- مواد بيع جاهزة: سكربت مكالمة، واتساب، إيميل، objection handling، proposal، SOW.
- جاهزية قانونية أولية: Privacy/Terms عربية بصيغة عامة تحتاج مراجعة قانونية قبل النشر النهائي.
- ملفات قياس: KPIs، UTM، event taxonomy، CRM stages.

## أوامر الدمج

```bash
cp -R dealix_launch_package_v2/* .
python scripts/dealix_launch_readiness_check.py
python scripts/dealix_daily_prospect_drafts.py
python scripts/dealix_lead_scoring.py --input data/prospects/icp_seed_accounts_saudi.csv --output data/prospects/scored_prospects.csv
python scripts/dealix_daily_command_center.py
```

## قاعدة التشغيل

لا إرسال آلي للعملاء. كل المسودات للمراجعة البشرية فقط. استخدم المصادر العامة المصرح بها، سجلاتك الداخلية، ونماذج consent واضحة.
