# Production Go / No-Go

## Go إذا
- readiness checks OK.
- env contract كامل.
- RLS/tenant guard موثق.
- E2E smoke ناجح.
- rollback واضح.
- أول عميل managed محدد.

## No-Go إذا
- يوجد secrets في repo.
- API يكتب بدون tenant context.
- لا يوجد audit logs.
- migration غير موثق.
- لا يوجد owner للمتابعة بعد النشر.
