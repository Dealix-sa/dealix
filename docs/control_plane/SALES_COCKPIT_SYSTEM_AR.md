# قمرة قيادة المبيعات

> النسخة الإنجليزية القانونية: [`SALES_COCKPIT_SYSTEM.md`](./SALES_COCKPIT_SYSTEM.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #5.
- القرارات المثبّتة: الموافقة-أولًا.

## الغرض

تعطي المؤسس عرضًا تشغيليًا واحدًا لكل التنفيذ التجاري. القمرة تُظهر **قرارات اليوم**، مو بيانات، مو تحليلات تاريخية، عشان المؤسس يقفل لفافات اليوم قبل ما يفتح جديدة.

## الـ Panels

- ذكاء العملاء (Lead Intelligence)
- موافقات التواصل
- متابعات مستحقة اليوم
- ردود إيجابية
- طابور العينات
- طابور العروض
- تحصيل الدفع
- إطلاق التسليم
- طابور الاحتفاظ
- مخاطر الثقة

## أفعال المؤسس على القمرة

اعتمد دفعة تواصل، ارفض عميلًا غير مناسب، اعتمد عرضًا، اطلب عينة، ادفع متابعة دفع، ابدأ التسليم، اطلب احتفاظًا، صعّد مخاطرة ثقة. كل فعل يكتب `AuditLogRecord`.

## القواعد الجوهرية

- القمرة تُظهر **قرارات**، مو لوحات بيانات. كل panel يعرض الفعل التالي الممكن للإنسان.
- ما يبحث المؤسس في CSVs أو يقفز بين موديولات.
- لا panel يُظهر رقمًا بدون رابط مصدر للسجلات.
- تجاوزات SLA تتصدّر الـ digest اليومي.
- القمرة ما تنفّذ أفعالًا خارجية بنفسها — هي سطح تحكم، مو طيار آلي.

## الربط بالتشغيل

- `dashboard/app.py` (Streamlit) مع صفحات في `dashboard/pages/` (Overview, Leads, Approvals, Evidence, Costs, Audit).
- `api/routers/command_center.py`, `api/routers/business_now.py`.
- وثائق Founder Command Center: `docs/company/FOUNDER_COMMAND_CENTER.md`, `docs/company/CEO_OPERATING_SYSTEM.md`.
- `.github/workflows/daily_digest.yml`، `make v5-digest`، `make v5-status`، `make v5-snapshot`.
- الواجهة المستقبلية (Next.js): `frontend/src/`.

## روابط ذات صلة

- [`./APPROVAL_CENTER_V2_AR.md`](./APPROVAL_CENTER_V2_AR.md)
- [`../runtime/REVENUE_FACTORY_RUNTIME_AR.md`](../runtime/REVENUE_FACTORY_RUNTIME_AR.md)
- [`../founder/REVENUE_WAR_ROOM_OS_AR.md`](../founder/REVENUE_WAR_ROOM_OS_AR.md)
- [`../founder/BOARD_LEVEL_KPI_STACK_AR.md`](../founder/BOARD_LEVEL_KPI_STACK_AR.md)
- [`../product/COMMAND_CENTER_PRODUCT_SPEC_AR.md`](../product/COMMAND_CENTER_PRODUCT_SPEC_AR.md)

## بنود مفتوحة

- صفحات الـ Streamlit ما تغطي بعد طابور العينات، العروض، تحصيل الدفع، الاحتفاظ كـ panels من الدرجة الأولى.
- قمرة موحدة في `frontend/src/` ما زالت stub.
- مؤقتات SLA عبر الـ panels: مفاهيمية.
- panel "مخاطر الثقة" يحتاج محرك السياسات يُصدر تيار أحداث مهيكل.
