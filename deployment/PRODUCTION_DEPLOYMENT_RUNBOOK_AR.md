# Production Deployment Runbook — Dealix

## قبل النشر
- تأكد من env variables.
- شغّل secret smoke.
- شغّل public exposure check.
- تأكد من sitemap/robots.
- تأكد من صفحة contact وdiagnostic.
- افحص lead route.

## Railway / Vercel / VPS
1. اربط GitHub branch.
2. اضبط build command.
3. اضبط start command.
4. أضف secrets فقط في dashboard.
5. لا تحفظ secrets في ملفات.
6. شغّل health endpoint.
7. راقب logs أول 24 ساعة.

## Rollback
- احتفظ بآخر commit stable.
- لا تدمج تعديلات homepage + API + env دفعة واحدة بدون readiness check.
- عند الفشل: disable workflow، rollback branch، راجع logs.
