# Production Server Layout / تخطيط خادم الإنتاج

## Purpose / الغرض

Define how Dealix runs on the connected server.

تعريف كيف يعمل Dealix على الخادم المتصل.

## Paths / المسارات

```txt
/opt/dealix
/opt/dealix-ops-private
/var/log/dealix
/etc/dealix
/var/lib/dealix
```

## Services / الخدمات

### API
FastAPI app.

تطبيق FastAPI.

### Web
Next.js / landing / dashboard.

Next.js / الصفحة التعريفية / لوحة المعلومات.

### Workers
Background jobs for growth, scoring, approvals, follow-ups, reports.

مهام خلفية للنمو والتقييم والموافقات والمتابعات والتقارير.

### Database
Postgres.

قاعدة Postgres.

### Queue
Redis later.

Redis لاحقاً.

### Logs
Structured logs.

سجلات مُنظَّمة.

### Backups
Daily private ops and database backup.

نسخ احتياطية يومية للعمليات الخاصة وقاعدة البيانات.

## Non-Negotiables / غير القابل للتفاوض

- secrets stay outside repo / الأسرار تبقى خارج الريبو
- private ops outside public repo / العمليات الخاصة خارج الريبو العام
- no external sending without approval / لا إرسال خارجي بدون موافقة
- workers log every run / العاملون يسجلون كل تشغيل
- failed worker alerts CEO / فشل العامل ينبه الرئيس التنفيذي

## See Also / مراجع

- [`../docs/runtime/WORKER_MESH_OS.md`](../docs/runtime/WORKER_MESH_OS.md)
- [`../docs/runtime/CSV_TO_POSTGRES_MIGRATION_PLAN.md`](../docs/runtime/CSV_TO_POSTGRES_MIGRATION_PLAN.md)

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
