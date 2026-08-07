# نموذج تشغيل السيرفر

## الخدمات

| الخدمة | المنفذ | الغرض |
|---|---|---|
| FastAPI Backend | 8000 | API الرئيسي |
| PostgreSQL | 5432 | قاعدة البيانات |
| Redis | 6379 | الكاش/الطابور |
| Next.js Frontend | 3000 | واجهة المستخدم |

## تشغيل البنية المحلية

```bash
docker compose up -d postgres redis
APP_ENV=development uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## فحوصات ما قبل التشغيل

```bash
make server-preflight
make server-health
make production-smoke
```

## متغيرات البيئة المطلوبة

- `APP_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL` (اختياري لكن موصى به)
- `MOYASAR_SECRET_KEY` (عند التعامل مع المدفوعات)
- `HUBSPOT_ACCESS_TOKEN` (عند CRM)
- `GMAIL_*` (عند إنشاء drafts)

## لا تطبع الأسرار

- لا secrets في logs.
- لا secrets في git.
- استخدم env vars فقط.

## النسخ الاحتياطي

- قاعدة البيانات: يومي.
- الإعدادات: في Railway/dashboard.
