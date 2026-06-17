# سجل الادعاءات — Claims Register — Dealix

> **القاعدة:** لا ادعاء عام أو موجَّه للعميل (public / customer-facing claim) يُنشر قبل المرور على هذا السجل.
> الادعاء غير المُدرَج هنا = **غير معتمد (not approved)** افتراضيًا.
> هذه ضوابط **قابلة للإنفاذ**: أي ادعاء = فئة موافقة **A2** على الأقل (راجع [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)).

الجمهور: التسويق، المبيعات، التشغيل، طبقة المحتوى. النطاق: كل نص يصل لعميل أو الجمهور.

---

## 1. جدول الضبط — Claim / Allowed? / Approved Rewrite

| الادعاء (Claim) | مسموح؟ | الصياغة المعتمدة (Approved rewrite) |
|---|---|---|
| نضمن زيادة المبيعات | **NO** | نوضح **next actions** ونرفع **جودة التشغيل (operational quality)** |
| نضمن مبيعات / guaranteed revenue | **NO** | فرص مُثبتة بأدلة — **evidenced opportunities** |
| نرسل واتساب تلقائي | **NO** | نجهّز **drafts** بموافقة بشرية — **human-approved drafts** |
| نجيب عملاء / نضمن عملاء | **NO** | نبني **targeting** و**pipeline مؤهل (qualified pipeline)** |
| ROI مضمون / نسبة تحويل محددة | **NO** | نمط case-safe + مؤشرات **تقديرية (estimated)**، ليست وعدًا |
| متوافق مع PDPL / PDPL-certified | **NO** | **PDPL-aware / approval-first** — جاهزية، **ليست شهادة قانونية** |
| آمن 100% / لا اختراق | **NO** | ضوابط أمنية موثّقة + خطة استجابة (breach response pointer) |
| نستخدم بياناتكم لتحسين النموذج | **NO** | **بيانات العميل لا تُستخدم لتدريب النماذج** (no model training) |
| نتعامل مع آلاف العملاء | **NO** (إن لم يثبت) | أرقام مُتحقَّقة فقط؛ غير ذلك "case-safe template" |
| **Proof Pack خلال 7 أيام** | **YES** | يُعرض كما هو، مشروطًا بتسليم delivery folder فعلي |
| **Business OS سعودي** | **YES** | يُعرض كما هو |
| **Approval-first operating system** | **YES** | يُعرض كما هو، مدعومًا بهذه السياسات |
| **targeting مبني على evidence لكل هدف** | **YES** | يُعرض كما هو (every target needs evidence) |
| **كل عميل مدفوع له delivery folder + proof pack** | **YES** | يُعرض كما هو |
| **PDPL-aware ومبني على approval-first** | **YES** | الصياغة المعتمدة الوحيدة للخصوصية في مواد العملاء |
| **بنية مستضافة في me-south-1 (KSA region)** | **YES** (إن صحّ تقنيًا) | يُذكر كموقع استضافة، لا كشهادة سيادة بيانات |

---

## 2. ادعاءات Enterprise / Security — قواعد خاصة

- **"PDPL-aware"** مسموح؛ **"PDPL-compliant / certified"** ممنوع. الجاهزية ليست شهادة. راجع [`PRIVACY_AND_PDPL_READINESS.md`](PRIVACY_AND_PDPL_READINESS.md).
- أي ادعاء أمني يجب أن يشير إلى ضابط فعلي قابل للإثبات (control + evidence)، لا صفة مطلقة.
- أي ادعاء قانوني/تعاقدي = فئة **A4**، يمر على المؤسس (+ مستشار).
- لا يُنشر اسم عميل أو شعاره دون موافقة موثّقة من العميل (no client name publishing without approval).

---

## 3. عملية الاعتماد — Process (no claim ships unchecked)

1. **اقترح** الادعاء بصياغته المطلوبة + الدليل المساند (evidence ref).
2. **طابِق** على هذا السجل: مُدرَج ومسموح؟ استخدم الصياغة المعتمدة حرفيًا.
3. غير مُدرَج؟ **لا يُنشر** حتى يُضاف صف هنا بقرار **A2+** من المؤسس.
4. **سجّل** القرار في Approval Register (claim_id + artifact + approver + timestamp).
5. **راجِع** كل 90 يومًا: هل أي ادعاء "YES" ما زال مدعومًا بالدليل؟ إن لا → يُعلَّق.

> Process (EN): propose → match register → if missing, block until founder approves a new row → record in Approval Register → re-verify every 90 days.

---

## 4. الإنفاذ — Enforcement

- نشر ادعاء ممنوع أو غير مُدرَج = **حادثة حوكمة** تُسجَّل وتُسحب فورًا.
- لا أدلة مزيّفة (no fake proof): كل proof point يربط بمصدر حقيقي قابل للتحقق.
- KPI: **صفر ادعاءات منشورة خارج هذا السجل**.

---

## روابط مرجعية — Related

- [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)
- [`PRIVACY_AND_PDPL_READINESS.md`](PRIVACY_AND_PDPL_READINESS.md)
- [`EXTERNAL_ACTIONS_POLICY.md`](EXTERNAL_ACTIONS_POLICY.md)
- [`../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`](../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md)
