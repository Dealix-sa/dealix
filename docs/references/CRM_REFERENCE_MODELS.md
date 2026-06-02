# CRM Reference Models — نماذج CRM المرجعية

**الغرض / Purpose:** مقارنة قصيرة لأنظمة CRM مفتوحة المصدر **كنماذج مرجعية** لهيكلة pipeline في Dealix — أفكار لنموذج البيانات وسير العمل، **لا خطة هجرة (migration) ولا موصلات حيّة**.

A short comparison of open-source CRMs as **reference models** for structuring the Dealix pipeline — data-model and workflow ideas, **not a migration plan and not live connectors**.

**حدّ صريح / Hard boundary:** Dealix **لا يبني الآن أي موصلات multi-CRM حيّة**؛ هذا مؤجَّل. نقطة التكامل الحالية الوحيدة هي HubSpot كبداية (sync عند capture/تحديث) — انظر [../ops/INTEGRATION_ROADMAP_AND_VENDOR_MATRIX_AR.md](../ops/INTEGRATION_ROADMAP_AND_VENDOR_MATRIX_AR.md).

Dealix builds **no live multi-CRM connectors now**; that is deferred. The only current integration starting point is HubSpot (sync on capture/update).

**مرجع ذو صلة / Related:** مكتبة المراجع: [OPEN_SOURCE_REFERENCE_LIBRARY.md](OPEN_SOURCE_REFERENCE_LIBRARY.md) · نموذج المسودة: [../distribution/DRAFT_SYSTEM_SPEC_AR.md](../distribution/DRAFT_SYSTEM_SPEC_AR.md).

---

## 1) جدول المقارنة (مرجع فقط)

| CRM | لماذا مفيد كمرجع / Why useful as a reference |
|-----|----------------------------------------------|
| **HubSpot** | نقطة التكامل الحالية (Starting point). مرجع لنمط الكائنات (contacts/companies/deals) ومراحل الـ pipeline التي نزامن معها فعلاً اليوم عبر `HUBSPOT_ACCESS_TOKEN`. |
| **SuiteCRM** | CRM مؤسسي ناضج. مرجع لمراحل المبيعات، حقول الصفقات، وسير عمل ما بعد البيع (cases/activities). |
| **EspoCRM** | نموذج كيانات قابل للتخصيص + صلاحيات دقيقة. مرجع لتصميم الأدوار، الحقول المخصصة، وعلاقات الكيانات. |
| **Twenty** | CRM حديث (TypeScript). مرجع لنمذجة الكائنات المرنة وواجهة عمليات نظيفة وتجربة سجل/طابور. |
| **Vtiger** | CRM عملي واسع الانتشار. مرجع لربط المبيعات بالدعم والتسعير/العروض (quotes) في تدفّق واحد. |

---

## 2) ماذا نستعير من كل نموذج (أفكار، لا كود)

| نريد أن نقرّر | نستلهم من |
|---------------|-----------|
| كائنات أساسية (prospect/company/deal) | Twenty · EspoCRM · HubSpot |
| مراحل pipeline ومعايير الانتقال | SuiteCRM · HubSpot |
| أدوار وصلاحيات قراءة/كتابة | EspoCRM |
| ربط المبيعات بالعروض والدعم | Vtiger · SuiteCRM |

تُترجَم هذه الأفكار إلى نماذجنا الخاصة (مثل [نموذج المسودة](../distribution/DRAFT_SYSTEM_SPEC_AR.md)) المحكومة بسياسة Dealix — لا نستورد سكيمة CRM خارجية كما هي.

---

## 3) ما هذه الوثيقة **ليست** (حدود صريحة)

- **ليست** خطة هجرة من/إلى أي CRM.
- **ليست** خارطة موصلات multi-CRM — لا نبني الآن موصلات حيّة متعددة؛ مؤجَّل.
- **ليست** التزاماً بدعم أي CRM في المنتج؛ التكامل الحي الوحيد اليوم هو HubSpot كبداية.
- **ليست** دعوة لكشط أو استيراد بيانات تواصل خارجية — الاستيراد يبقى ضمن مصادر مشروعة وحوكمة الإدخال.

---

## 4) متى يُعاد النظر في موصلات إضافية

أي موصل CRM إضافي يُؤجَّل حتى:

1. أدلة طلب حقيقي من عملاء يدفعون (لا افتراض).
2. owner + metric لكل تكامل، مع env vars وhealth وfallback (وفق [مصفوفة التكاملات](../ops/INTEGRATION_ROADMAP_AND_VENDOR_MATRIX_AR.md)).
3. kill switch / بوابة موافقة لأي تكامل يلمس بيانات عميل أو حالة خارجية.

حتى ذلك الحين، تبقى هذه المشاريع **مراجع تعلّم** فقط.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*نماذج مرجعية — لا خطة هجرة. آخر تحديث: 2026-06-02.*
