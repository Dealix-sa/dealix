# نظام تشغيل شركة Dealix (Company OS)

## الغرض (Purpose)

نظام تشغيل شركة Dealix هو المرجع الموحّد الذي يربط الاستراتيجية بالمبيعات والتسليم والامتثال والتعلم. يوضّح هذا الملف كيف تعمل الشركة كآلة واحدة موجّهة لخدمة شركات B2B في السوق السعودي بأنظمة ذكاء اصطناعي تشغيلية — وليس كأداة دردشة أو وكالة تسويق. يغطّي النظام: Revenue Command Room OS، Company Brain OS، WhatsApp/Inbox Follow-up OS، AI Outreach & Targeting OS، AI Trust & Compliance OS، Client Delivery OS، Controlled Live Outbound OS، Founder Decision Desk، Proposal+Contract+Payment OS، Executive Proof Pack OS، Offer Intelligence OS، Market & Competitor Watch OS، Customer Pain Radar، Operations Bottleneck Scanner.

## المالك (Owner)

المؤسس / الرئيس التنفيذي (CEO). مسؤول يومي عن تحديث النظام والتزام الفريق به.

## الاستخدام اليومي (Daily Usage)

- صباحًا (30 دقيقة): تشغيل `make company-day`، مراجعة غرفة القيادة، مراجعة مسودات اليوم في `outbox/YYYY-MM-DD/`.
- أثناء اليوم: إرسال المسودات المعتمدة يدويًا، تحديث سجل الإرسال `ledgers/outreach_log.csv`، تسجيل الردود في `ledgers/reply_log.csv`.
- مساءً (15 دقيقة): تحديث `ledgers/deals_pipeline.csv`، مراجعة تقرير اليوم `reports/revenue/YYYY-MM-DD/daily_ceo_report.md`.

## المُدخلات (Inputs)

- `ledgers/prospects.csv` — الفرص
- `ledgers/deals_pipeline.csv` — الأنابيب
- `ledgers/outreach_log.csv` — الإرسال
- `ledgers/reply_log.csv` — الردود
- `data/outreach/saudi_icp_segments.json` — شرائح ICP
- `scripts/revenue/run_daily_revenue_machine.py` — الآلة اليومية

## المخرجات (Outputs)

- `outbox/YYYY-MM-DD/*.md` — مسودات معتمدة للإرسال اليدوي
- `reports/revenue/YYYY-MM-DD/` — تقارير الإيرادات والتشغيل
- `reports/command_room/index.html` — لوحة غرفة القيادة
- قرارات تشغيلية موثّقة في سجل المؤسس

## سير العمل (Workflow)

1. تشغيل الآلة اليومية لجمع البيانات وتوليد المسودات.
2. مراجعة غرفة القيادة وتحديد أولويات اليوم.
3. اعتماد المسودات يدويًا قبل أي إرسال (approval-first).
4. إرسال يدوي عبر القنوات المعتمدة فقط.
5. تسجيل كل رد وكل اجتماع وكل عرض.
6. مساءً: تحديث الأنابيب وتقرير اليوم وتدوين blockers.
7. أسبوعيًا: مراجعة استراتيجية وتحديث مصدر الحقيقة.

## معايير القبول (Acceptance Criteria)

- كل عملية إرسال موثّقة في `outreach_log.csv` قبل المغادرة.
- لا توجد مسودة تُرسل دون اعتماد صريح.
- غرفة القيادة تُبنى يوميًا دون أخطاء.
- تقرير اليوم يُحفظ قبل نهاية اليوم.
- كل صفقة في الأنابيب لها مالك وتاريخ إجراء تالي.

## المخاطر (Risks)

- الاعتماد على إرسال آلي دون اعتماد بشري قد يضرّ العلامة والامتثال.
- تراكم بيانات غير محدّثة في السجلات يؤدي لقرارات خاطئة.
- تجاوز خطوات الاعتماد يكسر الثقة مع العميل والجهات التنظيمية.
- فجوة بين الاستراتيجية والتسليم اليومي.

## ما لا يجب فعله (What Not To Do)

- لا تُرسل أي مسودة دون اعتماد.
- لا تدّعِ إيرادات مضمونة أو عوائد مؤكدة.
- لا تستخدم شهادات أو نتائج ملفّقة.
- لا تصف Dealix كأداة دردشة أو CRM أو وكالة تسويق.
- لا تتجاوز متطلبات PDPL أو الاعتماد الأول (approval-first).

## الإجراء التالي (Next Action)

تشغيل `make company-day` ثم مراجعة `reports/command_room/index.html` وتحديد أصحاب الإجراءات لليوم.

## الملفات المرتبطة (Related Files)

- `docs/company/DEALIX_COMPANY_OS_EN.md`
- `docs/company/COMMAND_ROOM_RUNBOOK_AR.md`
- `docs/company/FOUNDER_OPERATING_SYSTEM_AR.md`
- `docs/company/DEALIX_SOURCE_OF_TRUTH.md`
- `docs/brand/DEALIX_BRAND_OS.md`