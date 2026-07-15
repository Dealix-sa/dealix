# مواصفة منتج مركز القيادة

> النسخة الإنجليزية القانونية: [`COMMAND_CENTER_PRODUCT_SPEC.md`](./COMMAND_CENTER_PRODUCT_SPEC.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #3، #5.
- القرارات المثبّتة: الموافقة-أولًا.

## الغرض

تحديد مركز قيادة Dealix داخل المنتج: الواجهة التنفيذية اللي تخلي المؤسس أو مشغّل العميل يتحكم بـ Dealix من مكان واحد. هذي الوثيقة هي **مواصفة المنتج**. الجانب التشغيلي للمؤسس في `docs/control_plane/SALES_COCKPIT_SYSTEM_AR.md`.

## العروض

- **عرض المؤسس** — صفحة واحدة لإيرادات وثقة وتكلفة وقرارات اليوم.
- **عرض المبيعات** — ذكاء العملاء، التواصل، الردود، العينات، العروض.
- **عرض التسليم** — تفاعلات نشطة، Milestones، QA، ملاحظات.
- **عرض الثقة** — طوابير الموافقة، الإيقاف، الحوادث، التقييمات.
- **عرض المالية** — النقد، المستحقات، MRR، التكلفة لكل نتيجة.
- **عرض الوكلاء** — سجل الوكلاء، التقييمات، إصدارات prompt، سجلات الأفعال.

## الأفعال الأساسية

اعتمد تواصلًا، اعتمد عرضًا، راجع عينة، راجع علامات ثقة، راقب النقد، افحص بطاقة قطاع، افحص حزمة دليل AI، أرجع prompt وكيل لإصدار سابق.

## قاعدة دليل المصدر

كل رقم في المركز عنده click-through للسجلات اللي أنتجته. لا عرض يُظهر مؤشرًا بدون مسار رجوع لبيانات المصدر.

## قاعدة العزل بين المستأجرين

المستخدم يرى ويتصرف فقط على بيانات نطاق مستأجره. الـ Router والـ ORM يفرضان هذا. المركز ما يجمّع عبر المستأجرين لمستخدم مستأجر.

## القواعد الجوهرية

- المركز ما ينفّذ أثرًا خارجيًا بنفسه. هو سطح تحكم.
- "نتيجة مضمونة" ممنوع كرسم؛ الأرقام المستقبلية تحمل نطاق ثقة صريحًا.
- عرض يعتمد على مخرج وكيل يُظهر آخر نتيجة تقييم له.
- موافقة محجوبة (لنقص دليل) تخبر المستخدم بالدليل المطلوب.

## الربط بالتشغيل

- Streamlit الحالي: `dashboard/app.py`, `dashboard/pages/`.
- `api/routers/command_center.py`, `api/routers/business_now.py`.
- Next.js: `frontend/src/` (stub).
- `docs/company/FOUNDER_COMMAND_CENTER.md`, `docs/company/CEO_OPERATING_SYSTEM.md`.
- [`../control_plane/SALES_COCKPIT_SYSTEM_AR.md`](../control_plane/SALES_COCKPIT_SYSTEM_AR.md).

## روابط ذات صلة

- [`../control_plane/SALES_COCKPIT_SYSTEM_AR.md`](../control_plane/SALES_COCKPIT_SYSTEM_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)
- [`../runtime/REVENUE_FACTORY_RUNTIME_AR.md`](../runtime/REVENUE_FACTORY_RUNTIME_AR.md)
- `docs/company/FOUNDER_COMMAND_CENTER.md`
- `docs/company/CEO_OPERATING_SYSTEM.md`
- [`../founder/BOARD_LEVEL_KPI_STACK_AR.md`](../founder/BOARD_LEVEL_KPI_STACK_AR.md)
- [`../trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md`](../trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md)

## بنود مفتوحة

- واجهة Next.js stub فقط.
- عرض الوكلاء يعتمد على سجل الوكلاء وإصدارات prompt الجزئية.
- اختبارات end-to-end لعزل المستأجرين تغطي الحالات الشائعة؛ سيناريو red team لـ Command Center مفتوح في نظام التقييم.
- Telemetry للـ click-through على روابط الدليل: غير موصول.
