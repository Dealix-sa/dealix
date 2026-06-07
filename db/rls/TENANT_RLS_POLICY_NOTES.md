# Tenant RLS Policy Notes

هذه ملاحظات تصميم وليست تفعيلًا نهائيًا.

## الهدف
أي query لبيانات العميل يجب أن تكون scoped بـ tenant/workspace.

## قاعدة عامة
- API يتحقق من session/membership.
- DB يستخدم tenant_id في كل جدول عميل.
- audit_events تسجل كل عملية حساسة.

## أمثلة جداول تحتاج tenant_id
- leads
- accounts
- opportunities
- interactions
- proof_items
- agent_runs
- usage_events
- audit_events

## اختبار إلزامي
أي endpoint جديد يجب أن يفشل إذا لم يوجد tenant context.
