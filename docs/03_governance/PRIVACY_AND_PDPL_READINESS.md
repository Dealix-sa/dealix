# جاهزية الخصوصية و PDPL — Privacy & PDPL Readiness — Dealix

> **توضيح حاسم:** هذه وثيقة **جاهزية (readiness)**، **وليست شهادة امتثال قانونية (NOT a legal certification)**.
> الصياغة المعتمدة الوحيدة في مواد العملاء: **"PDPL-aware / approval-first"**. راجع [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md).
> أي التزام قانوني تعاقدي يمر على المؤسس + مستشار (فئة **A4**).

الجمهور: المؤسس، التشغيل، DPO، فِرق Enterprise. النطاق: وضعية الخصوصية في Dealix.
تكامل قائم في المستودع: [`integrations/pdpl.py`](../../integrations/pdpl.py).

---

## 1. الوضعية — Posture

Dealix تُشغّل الخصوصية **داخل المنتج** (operationalize)، لا تعدها لاحقًا. وضوح الخصوصية ليس عبئًا تنظيميًا؛ هو **عامل تمييز للثقة (trust differentiator)** في السوق السعودي.

> EN: Dealix operationalizes privacy inside the product. Privacy clarity is a trust differentiator, not a checkbox.

---

## 2. سياق خارجي — External Context

> *(سياق خارجي للتأطير — external context, not a Dealix claim.)*

دراسة حديثة فحصت **100 موقع تجارة إلكترونية سعودي** ووجدت أن **31% فقط** أفصحوا عن العناصر الأربعة التالية. هذه الفجوة هي فرصة تمييز مباشرة:

1. **مدة الاحتفاظ** (retention period)
2. **الحق في المحو** (right to erasure)
3. **الحق في الحصول على نسخة** (right to obtain a copy)
4. **آلية الشكاوى** (complaints mechanism)

**التزام Dealix:** الإفصاح عن **العناصر الأربعة كاملة** في صفحة الخصوصية العامة وفي مواد Enterprise — لا ثلاثة من أربعة.

> EN: A recent study of 100 Saudi e-commerce sites found only 31% disclosed retention period, right to erasure, right to a copy, and a complaints mechanism. Dealix commits to disclosing all four.

---

## 3. قائمة الجاهزية — Readiness Checklist

| العنصر | الالتزام | المرجع |
|---|---|---|
| **التقاط الموافقة** (consent capture) | موافقة مُلتقطة ومربوطة بالسجل قبل المعالجة التي تتطلبها | [`integrations/pdpl.py`](../../integrations/pdpl.py) |
| **الأساس القانوني** (lawful basis) | لكل غرض أساس معلن (عقد · موافقة · التزام نظامي) | [`DATA_RETENTION.md`](DATA_RETENTION.md) |
| **حقوق صاحب البيانات** (data subject rights) | وصول · نسخة · تصحيح · محو · تقييد · سحب موافقة، بـ SLA 30 يومًا | [`DATA_RETENTION.md`](DATA_RETENTION.md) |
| **الإفصاحات الأربعة** | مدة الاحتفاظ · المحو · النسخة · الشكاوى — منشورة كاملة | صفحة الخصوصية العامة |
| **الاستجابة للخرق** (breach response pointer) | مسار استجابة موثّق + إشعار SDAIA خلال 72 ساعة | [`../PDPL_BREACH_RESPONSE_PLAN.md`](../PDPL_BREACH_RESPONSE_PLAN.md) |
| **DPA للمؤسسات** (enterprise DPA) | اتفاقية معالجة بيانات + قائمة sub-processors محدّثة | فئة A4 |
| **لا تدريب على بيانات العميل** | بيانات العميل لا تُستخدم لتدريب النماذج | [`DATA_RETENTION.md`](DATA_RETENTION.md) |

> EN checklist: consent capture · lawful basis · data subject rights · four disclosures · breach response pointer · enterprise DPA · no model training.

---

## 4. أدوار المعالجة — Processing Roles

- **Controller (المتحكّم):** عادة العميل، يحدّد **لماذا** تُعالج البيانات في سياق أعماله.
- **Processor (المعالج):** Dealix عندما تعالج بتعليمات العميل لتوصيل الخدمة المتعاقد عليها.

يُحدَّد الدور صراحةً في كل عرض/DPA: من يملك الغرض، ومن يملك علاقة الأفراد.

---

## 5. ما لا يُقال — Claim Boundaries

- **"PDPL-aware / approval-first"** ✅ — الصياغة المعتمدة.
- **"PDPL-compliant / PDPL-certified"** ❌ — الجاهزية ليست شهادة.
- **"آمن 100%"** ❌ — يُستبدل بضوابط موثّقة + خطة استجابة.

كل ذلك يُفرض عبر [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md).

---

## روابط مرجعية — Related

- [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md)
- [`DATA_RETENTION.md`](DATA_RETENTION.md)
- [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)
- [`../PDPL_BREACH_RESPONSE_PLAN.md`](../PDPL_BREACH_RESPONSE_PLAN.md)
- [`../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`](../02_saudi_positioning/PDPL_AWARE_LANGUAGE.md)
- [`integrations/pdpl.py`](../../integrations/pdpl.py)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
