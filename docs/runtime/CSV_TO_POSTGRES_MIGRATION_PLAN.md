# CSV to Postgres Migration Plan / خطة الانتقال من CSV إلى Postgres

## Purpose / الغرض

Move Dealix from private CSV ops to production database without losing execution speed.

نقل Dealix من تشغيل CSV الخاص إلى قاعدة بيانات إنتاجية بدون فقدان سرعة التنفيذ.

## Phase 1 — CSV Control / المرحلة 1 — التحكم بالـ CSV

Use private ops CSV for:
- quick execution
- founder review
- early lead batches
- weekly learning

استخدام CSV الخاص للعمليات لأجل:
- تنفيذ سريع
- مراجعة المؤسس
- دفعات العملاء المبكرة
- تعلم أسبوعي

## Phase 2 — Shadow Database / المرحلة 2 — قاعدة بيانات ظل

Mirror CSV into Postgres:
- accounts
- outreach queue
- conversation log
- proposals
- payments
- approvals

نسخ CSV إلى Postgres بشكل ظل:
- الحسابات
- طابور التواصل
- سجل المحادثات
- العروض
- المدفوعات
- الموافقات

## Phase 3 — Database Primary / المرحلة 3 — قاعدة البيانات أساسية

Postgres becomes source of truth. CSV exports become reports.

Postgres تصبح مصدر الحقيقة. تصديرات CSV تصبح تقارير.

## Phase 4 — Command Center UI / المرحلة 4 — واجهة مركز القيادة

CEO uses UI for:
- approvals
- sales cockpit
- distribution dashboard
- finance center
- trust center

الرئيس التنفيذي يستخدم الواجهة لـ:
- الموافقات
- قُمرَة المبيعات
- لوحة التوزيع
- مركز المالية
- مركز الثقة

## Rule / القاعدة

Do not migrate for elegance. Migrate only when daily operation needs it.

لا تهاجر من أجل الأناقة. هاجِر فقط عندما يحتاج التشغيل اليومي ذلك.

## See Also / مراجع

- [`../data/UNIFIED_OPERATING_DATABASE.md`](../data/UNIFIED_OPERATING_DATABASE.md)
- [`WORKER_MESH_OS.md`](WORKER_MESH_OS.md)
- [`../../deploy/PRODUCTION_SERVER_LAYOUT.md`](../../deploy/PRODUCTION_SERVER_LAYOUT.md)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
