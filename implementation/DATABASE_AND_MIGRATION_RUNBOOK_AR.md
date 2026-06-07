# Database and Migration Runbook

## الهدف
جعل قاعدة البيانات قابلة للتحديث بدون كسر الإنتاج.

## القواعد
1. migration لكل تغيير schema.
2. لا حذف عمود مستخدم قبل backfill وdeprecation window.
3. كل جدول tenant-facing يحتاج tenant_id/workspace_id.
4. RLS أو tenant guard مطلوب قبل أي client access.
5. seed data يجب ألا يحتوي أسرارًا أو بيانات عملاء حقيقية.

## أمر مقترح للإنتاج

```bash
python scripts/dealix_migration_plan.py
# ثم أداة migration الفعلية حسب stack المشروع
```

## قبل الدمج
- هل migration id واضح؟
- هل يوجد rollback note؟
- هل يوجد index للأعمدة tenant_id وworkspace_id؟
- هل تم اختبار seed؟
