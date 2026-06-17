# Dealix Company Operating System

## ما هو؟

نظام تشغيل الشركة يجمع:
- الاستراتيجية والقياس
- المبيعات والإيرادات
- التسليم والخدمة
- الامتثال والثقة
- التعلم والتحسين

## ما الذي يتم تشغيله يوميًا

### الصباح (30 دقيقة)
1. `make company-day`
2. مراجعة `reports/command_room/index.html`
3. مراجعة المسودات في `outbox/YYYY-MM-DD/`

### أثناء اليوم
4. الإرسال اليدوي للمسودات المعتمدة.
5. تحديث `ledgers/outreach_log.csv` بعد كل إرسال.
6. تسجيل الردود في `ledgers/reply_log.csv`.

### المساء (15 دقيقة)
7. تحديث `ledgers/deals_pipeline.csv`.
8. مراجعة `reports/revenue/YYYY-MM-DD/daily_ceo_report.md`.

## ملفات المصدر

- `ledgers/prospects.csv` — الفرص
- `ledgers/deals_pipeline.csv` — الأنابيب
- `ledgers/outreach_log.csv` — الإرسال
- `ledgers/reply_log.csv` — الردود
- `data/outreach/saudi_icp_segments.json` — شرائح ICP
- `scripts/revenue/run_daily_revenue_machine.py` — الآلة اليومية

## المخرجات

- `outbox/YYYY-MM-DD/*.md` — مسودات
- `reports/revenue/YYYY-MM-DD/` — تقارير
- `reports/command_room/index.html` — لوحة القيادة

## كيف نبيع

1. نحدد الألم التشغيلي.
2. نقدم Diagnostic Sprint 4,999 ريال.
3. نقدم Pilot 14,999 ريال.
4. ننتقل للاشتراك الشهري بعد نجاح Pilot.

## كيف نسلم

- أسبوع 1: Discovery + بيانات.
- أسبوع 2: بناء النظام الصغير.
- أسبوع 3: اختبار + تعديل.
- أسبوع 4: تقرير النجاح.

## كيف نقيس

- baseline قبل Pilot.
- after بعد Pilot.
- فرق واضح موثق.

## أخطاء تتجنبها

- لا وعود بنسب محددة.
- لا تجميع بيانات حساسة.
- لا إرسال تلقائي.
