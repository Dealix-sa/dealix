# Tenant / Workspace Model

## الكيانات
- Organization: الشركة العميلة.
- Workspace: مساحة تشغيل محددة داخل المنظمة.
- User: مستخدم داخل workspace.
- Role: صلاحيات المستخدم.
- Module: ميزة مفعلة.
- Usage Event: حدث استخدام محسوب.
- Audit Event: حدث أمني/تشغيلي.

## أدوار افتراضية
- owner
- admin
- operator
- viewer
- client_viewer

## عزل البيانات
كل record يجب أن يحتوي `tenant_id` أو `workspace_id` عندما يكون متعلقًا بعميل.

## ممنوع
- قراءة records بدون tenant scope.
- مشاركة proof أو leads بين tenants.
- استخدام API key عام بدون scope.
