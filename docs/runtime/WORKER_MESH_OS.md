# Worker Mesh OS / نظام شبكة العاملين

## Purpose / الغرض

Run Dealix as a mesh of safe internal workers on the server.

تشغيل Dealix كشبكة من العاملين الداخليين الآمنين على الخادم.

## Worker Classes / فئات العاملين

### A. Intelligence Workers / عاملو الذكاء
- market discovery / اكتشاف السوق
- sector discovery / اكتشاف القطاع
- lead discovery / اكتشاف العملاء
- signal detection / كشف الإشارات
- competitor monitoring / مراقبة المنافسين

### B. Commercial Workers / العاملون التجاريون
- lead scoring / تقييم العملاء
- outreach drafting / صياغة التواصل
- approval queue building / بناء طابور الموافقات
- follow-up scheduling / جدولة المتابعة
- reply routing / توجيه الردود
- sample generation / توليد العينات
- proposal drafting / صياغة العروض
- payment capture / تحصيل الدفع

### C. Delivery Workers / عاملو التسليم
- client workspace creation / إنشاء مساحة عمل العميل
- delivery checklist / قائمة التسليم
- QA scoring / تقييم ضمان الجودة
- handoff generation / توليد التسليم النهائي
- feedback request / طلب التغذية الراجعة

### D. Trust Workers / عاملو الثقة
- policy evaluator / مُقيِّم السياسات
- suppression check / فحص الاستبعاد
- no-overclaim scan / مسح المبالغة
- sensitive data check / فحص البيانات الحساسة
- approval routing / توجيه الموافقات

### E. Finance Workers / العاملون الماليون
- proposal value tracking / تتبع قيمة العروض
- payment follow-up / متابعة الدفع
- MRR update / تحديث الإيراد الشهري المتكرر
- margin calculation / حساب الهامش
- pricing review / مراجعة التسعير

### F. CEO Workers / عاملو الرئيس التنفيذي
- sales cockpit / قُمرَة المبيعات
- approval center / مركز الموافقات
- stoplight report / تقرير إشارة المرور
- board KPI stack / حُزمة مؤشرات المجلس
- war room report / تقرير غرفة العمليات

## Execution Rules / قواعد التنفيذ

- Workers may prepare. / للعاملين الإعداد.
- Workers may route. / للعاملين التوجيه.
- Workers may score. / للعاملين التقييم.
- Workers may draft. / للعاملين الصياغة.
- Workers may not make external commitments without approval. / لا يحق للعاملين إنشاء التزامات خارجية بدون موافقة.

## Queue Upgrade Path / مسار ترقية الطابور

Cron → Redis Queue → Durable Workflows.

Cron ← طابور Redis ← سير عمل دائم.

## See Also / مراجع

- [`../data/UNIFIED_OPERATING_DATABASE.md`](../data/UNIFIED_OPERATING_DATABASE.md)
- [`CSV_TO_POSTGRES_MIGRATION_PLAN.md`](CSV_TO_POSTGRES_MIGRATION_PLAN.md)
- [`../agents/AGENT_GOVERNANCE_V3.md`](../agents/AGENT_GOVERNANCE_V3.md)
- [`../../deploy/PRODUCTION_SERVER_LAYOUT.md`](../../deploy/PRODUCTION_SERVER_LAYOUT.md)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
