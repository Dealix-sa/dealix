# Multi-Tenant Security Checklist

- كل endpoint يتطلب tenant context.
- كل record عميل يحتوي tenant_id/workspace_id.
- لا يوجد global admin API بدون audit.
- roles محددة وصغيرة.
- audit لكل تعديل حساس.
- usage لا يحتوي بيانات حساسة.
- logs لا تحتوي secrets.
- feature flags حسب tenant.
- exports تحتاج approval.
