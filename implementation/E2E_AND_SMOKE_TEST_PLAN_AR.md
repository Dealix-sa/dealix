# E2E and Smoke Test Plan

## صفحات حرجة
- /
- /pricing
- /diagnostic
- /book
- /app/workspace
- /trust-center

## API Smoke
- POST /api/leads
- POST /api/tenants
- POST /api/usage
- POST /api/audit
- GET /api/health

## نجاح الاختبار
- الصفحة تحمل.
- CTA ظاهر.
- form validation يعمل.
- API يرجع status واضح.
- لا يظهر stack trace للمستخدم.
