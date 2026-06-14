# Delivery Acceptance Criteria — معايير قبول التسليم — The Universal Done-Definition

## ما هذه الوثيقة — What this is

هذه هي **معايير القبول الكونية**: كل مُخرَج في أي Sprint — مهما كان نوعه — يجب أن يحمل تسعة حقول قبل أن يُسمَّى «جاهزًا». تُطبَّق على كل ملف في [CUSTOMER_FOLDER_TEMPLATE](CUSTOMER_FOLDER_TEMPLATE.md) وكل بند في [PROOF_PACK_TEMPLATE](PROOF_PACK_TEMPLATE.md).

> القاعدة العليا — The supreme rule: لا مُخرَج «جاهز» حتى تكتمل كل الحقول، ويُحَلّ كل بند `approval_required`. No deliverable is done until all nine fields are present and every approval gate is resolved.

## الحقول التسعة — The nine fields

كل مُخرَج (أو بند داخل مُخرَج) يحمل هذه الحقول صراحةً:

| الحقل — Field | التعريف — Definition |
|---|---|
| **source** | من أين جاءت المعلومة. مصدر عام أو ما شاركه العميل. لا رقم بلا مرجع. |
| **analysis** | ما الذي فعلناه بالمصدر — التفسير أو الاستنتاج، لا نقل خام. |
| **assumption** | الافتراض الصريح الذي يقوم عليه الاستنتاج. إن لم يوجد افتراض، اكتب «لا يوجد». |
| **confidence** | مستوى الثقة: high / medium / low. لا ثقة ضمنية. |
| **recommendation** | ما الذي نوصي به بناءً على التحليل. توصية واحدة واضحة. |
| **approval_required** | yes/no — هل يحتاج هذا البند موافقة قبل أي إجراء خارجي؟ |
| **next_action** | الخطوة التالية المحدّدة، لا نيّة عامة. |
| **owner** | المسؤول عن الخطوة التالية — دور، لا PII. |
| **due_date** | تاريخ الاستحقاق. لا «قريبًا». |

## مثال مُعبّأ — Filled example

بند من Revenue Map لشركة افتراضية (Hypothetical / case-safe template):

```
- claim: "وقت الردّ على الطلب الوارد يتجاوز يومين في القناة الرئيسية"
  source: عيّنة من سجلّ الطلبات شاركها العميل (مصدر داخلي، بإذن)
  analysis: 18 من 25 طلبًا تجاوزت 48 ساعة قبل أول ردّ
  assumption: العيّنة تمثّل الشهر الكامل (لم يُؤكَّد بعد)
  confidence: medium
  recommendation: تثبيت SLA ردّ خلال 4 ساعات على القناة الرئيسية
  approval_required: yes   # يلمس عملية تواجه العميل
  next_action: عرض مقترح SLA في Executive Command Brief لليوم 6
  owner: المؤسس (delivery lead)
  due_date: 2026-06-11
```

هذا البند **مكتمل**: تسعة حقول حاضرة، والـ `approval_required: yes` سيُحَلّ في بوابة اليوم 6.

## قاعدة الاكتمال — The completeness rule

```
deliverable.is_done == (
    كل الحقول التسعة حاضرة لكل بند
    AND كل بند approval_required: yes مربوط بقيد في 06_approval_register.md
    AND كل رقم تقديري يحمل كلمة "تقديري" (estimated)
)
```

- حقل واحد مفقود = المُخرَج **غير جاهز**. لا استثناء.
- `approval_required: yes` بلا قيد موافقة مُحَلّ = المُخرَج **محجوز (blocked)**، لا يُسلَّم ولا يُذكَر للعميل.
- لا رقم مبيعات مضمون، لا نسبة تحويل كحقيقة. تقدير أو نمط case-safe فقط — No guaranteed revenue claims.
- لا إجراء خارجي يواجه العميل دون موافقة المؤسس — No external customer-facing action without founder approval.

## أين تُفحَص — Where this is enforced

- في **acceptance check** لكل يوم من أيام الـ SLA ([COMMAND_SPRINT_DELIVERY_OS](COMMAND_SPRINT_DELIVERY_OS.md)).
- في **مراجعة المؤسس** يوم 6 قبل أي إرسال للعميل.
- في **بوابة النشر** يوم 7 قبل أي ذكر لاسم العميل.

## روابط مرجعية — Cross-links

- [COMMAND_SPRINT_DELIVERY_OS.md](COMMAND_SPRINT_DELIVERY_OS.md)
- [CUSTOMER_FOLDER_TEMPLATE.md](CUSTOMER_FOLDER_TEMPLATE.md)
- [PROOF_PACK_TEMPLATE.md](PROOF_PACK_TEMPLATE.md)
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
