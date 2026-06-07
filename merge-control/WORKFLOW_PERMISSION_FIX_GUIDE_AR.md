# إصلاح صلاحيات GitHub Actions

## القاعدة
كل workflow غير مخصص للنشر يجب أن يحتوي:

```yaml
permissions:
  contents: read
```

## متى نحتاج صلاحيات أكثر؟
فقط عند:
- إنشاء release.
- رفع artifact يحتاج write.
- deployment job مرتبط ببيئة محمية.
- PR comment bot مصمم بعناية.

## طريقة المراجعة
شغل:

```bash
python scripts/dealix_workflow_permission_audit.py
```

ثم أضف permissions للملفات التي تظهر في التحذير.
