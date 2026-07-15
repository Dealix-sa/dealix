# نظام الموافقة والإيقاف والأساس النظامي

> النسخة الإنجليزية القانونية: [`CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`](./CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #3، #5.
- القرارات المثبّتة: الموافقة-أولًا، سكربتات التحقق مانعة للإصدار.

## الغرض

ضبط كيف يتعامل Dealix مع بيانات التواصل وأذونات التواصل. كل حساب وجهة اتصال وسجل تواصل يحمل أساسًا نظاميًا موثقًا، وحالة موافقة، وحالة إيقاف. ما يطلع تواصل خارجي على سجل موقوف.

## المرجع التنظيمي

نظام حماية البيانات الشخصية في المملكة (PDPL) تحت إشراف SDAIA يحكم كيفية جمع ومعالجة البيانات الشخصية والتواصل بها. Dealix متحكم على بيانات تواصله الذاتية، ومعالج عند تشغيل عمليات تواصل بالنيابة عن عميل. الدوران موثقان حسب سير العمل.

هذي الوثيقة تشغيلية. الوثائق القانونية تعيش في `docs/legal/`.

## حقول السجل

`data_source`, `public_business_context`, `lawful_basis_assessment`, `consent_status`, `opt_out_status`, `suppression_reason`, `last_reviewed`, `tenant_id`.

## أسباب الإيقاف

- طلب إلغاء الاشتراك (opt-out) صريح.
- إجابة "غير مهتم" صريحة.
- ملاءمة غير صحيحة (بعد البحث).
- تكرار مع سجل آخر للوحدة المشترية نفسها.
- مصدر بيانات يخالف شروط استخدامه أو غير واضح.
- شكوى أو بلاغ ثقة.
- شك في كون السجل بيانات شخصية بدون أساس نظامي واضح.

## القواعد الجوهرية

- السجل في `SuppressionRecord` ما يستقبل draft تواصل أو متابعة أو عينة. الفحص يحصل قبل الكتابة في الطابور.
- طلبات opt-out تُنفّذ خلال يوم عمل وتُؤكَّد كتابيًا.
- السجل بدون `lawful_basis_assessment` يُعامل موقوفًا افتراضيًا حتى يُراجَع.
- الإيقاف معزول بين المستأجرين: opt-out في مستأجر ما يتسرّب لمستأجر آخر.
- تجاوز الإيقاف (نادر جدًا، مؤسس فقط) يحتاج `AuditLogRecord` مع تبرير مكتوب.
- الإثبات العام أو الـ case study لعميل: يحتاج موافقة كتابية مسجّلة كرابط دليل مصدر.

## الربط بالتشغيل

- `db/models.py::SuppressionRecord`.
- `auto_client_acquisition/outreach_window.py`.
- `auto_client_acquisition/approval_center/approval_policy.py`.
- `db/models.py::OutreachQueueRecord`, `AuditLogRecord`.

## روابط ذات صلة

- [`../data/GROWTH_DATABASE_MODEL_AR.md`](../data/GROWTH_DATABASE_MODEL_AR.md)
- [`../distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md`](../distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)
- [`../legal/COMMERCIAL_CONTRACT_PACK_AR.md`](../legal/COMMERCIAL_CONTRACT_PACK_AR.md)
- `docs/transformation/01_doctrine_lock.md`

## بنود مفتوحة

- واجهة مراجعة جماعية للسجلات بدون `lawful_basis_assessment` غير مبنية.
- الشكل الدقيق لـ `SuppressionRecord` مقابل جدول `consent_state` منفصل: مفتوح.
- اختبار red-team مخصص لـ "تسرب opt-out" بين المستأجرين مفتوح في `docs/evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`.
- موافقة الادعاء العام تحتاج نوع طابور موافقة مخصص.
