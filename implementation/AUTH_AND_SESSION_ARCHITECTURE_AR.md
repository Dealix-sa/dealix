# Auth and Session Architecture

## الهدف
ضمان أن كل مستخدم يدخل فقط إلى tenant/workspace المسموح له، وأن أي API route لا يعمل بدون session وtenant context.

## البنية
- user_id: هوية المستخدم.
- tenant_id: الشركة أو العميل.
- workspace_id: مساحة العمل.
- role: owner/admin/member/viewer.

## Middleware / Guard
أي request داخلي يجب أن يمر بهذه القاعدة:

```text
request → session check → tenant membership check → role check → handler
```

## قواعد ممنوعة
- ممنوع الاعتماد على tenant_id من body فقط.
- ممنوع service role في browser.
- ممنوع public route يكتب في جداول tenant.
- ممنوع عرض بيانات cross-tenant حتى في logs.
