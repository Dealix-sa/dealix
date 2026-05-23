# إدارة عائد التسعير

> النسخة الإنجليزية القانونية: [`PRICING_YIELD_MANAGEMENT.md`](./PRICING_YIELD_MANAGEMENT.md).

## مرجع الدوكترين
- الالتزامات: #2، #5.
- القرارات المثبّتة: معمارية العرض تبقى خمسة أبواب بسلالم خدمات منتجة.

## الغرض

تحسين تسعير Dealix بناءً على الطلب وجهد التسليم والمخاطر والتحويل. هذي الوثيقة **لا تعيد** قائمة الأسعار — قائمة الأسعار في `docs/PRICING_STRATEGY.md` و`docs/OFFER_LADDER_AND_PRICING.md`. هذي الوثيقة تحدّد **قرار العائد الأسبوعي**.

## المراجعة الأسبوعية

لكل سلّم عرض نشط، راجع:

- نسبة تحويل العرض → دفع.
- متوسط حجم الصفقة.
- ساعات التسليم لكل تفاعل.
- الهامش الإجمالي (بعد تكلفة AI/أدوات).
- احتمالية الـ retainer.
- أثر الخصومات.
- إيرادات سيئة الملاءمة.

## القرارات الممكنة

ارفع السعر، قلّص النطاق، اقسم العرض، أوقف عرضًا ضعيفًا، أنشئ شريحة premium، انقل إلى retainer.

## القواعد الجوهرية

- قرار تسعير يحتاج دليل مصدر: بيانات التحويل، ساعات التسليم، حسبة الهامش.
- لا استثناء تحت الحد بدون موافقة المؤسس وسبب مسجّل.
- خصم يحوّل = يُدرَس قبل ما يصير عرضًا قائمًا.
- تفاعل سيئ الملاءمة بِيع = يُسلَّم، ثم العرض/البوابة يُصلَح للمرة القادمة.
- "إذا الطلب عالي والقدرة على التسليم مقيّدة، ارفع السعر قبل التوظيف."

## الربط بالتشغيل

- `docs/PRICING_STRATEGY.md`, `docs/OFFER_LADDER_AND_PRICING.md`.
- `docs/UNIT_ECONOMICS_AND_MARGIN.md`, `docs/company/UNIT_ECONOMICS.md`.
- معمارية العرض: `docs/transformation/01_doctrine_lock.md`.
- مصادر البيانات: revenue events, `AuditLogRecord`.

## روابط ذات صلة

- `docs/PRICING_STRATEGY.md`
- `docs/OFFER_LADDER_AND_PRICING.md`
- `docs/company/UNIT_ECONOMICS.md`
- [`./AI_UNIT_ECONOMICS_AR.md`](./AI_UNIT_ECONOMICS_AR.md)
- [`./BILLING_RECEIVABLES_OS_AR.md`](./BILLING_RECEIVABLES_OS_AR.md)
- [`../founder/REVENUE_WAR_ROOM_OS_AR.md`](../founder/REVENUE_WAR_ROOM_OS_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)

## بنود مفتوحة

- ملف سجل قرارات التسعير في `docs/finance/` غير موجود.
- الربط بين استثناء سعر في مركز الموافقات ومراجعة الأسبوع القادم: غير رسمي.
- حسبة الهامش لكل سلّم تعتمد على بيانات تكلفة AI/أداة لكل نتيجة، الموصولة جزئيًا.
