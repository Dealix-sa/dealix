# Diagnostic Sales Playbook — دليل بيع التشخيص

## الغرض (AR)
يشرح هذا الدليل كيف يحوّل المؤسس مكالمة اكتشاف إلى تشخيص مدفوع. التشخيص هو أول التزام مالي صغير يثبت الجدية ويبني الثقة قبل التجربة الأكبر. كل العروض شفافة وبلا ضمانات عائد أو ادعاءات غير مثبتة.

## Purpose (EN)
This playbook explains how the founder turns a discovery call into a paid diagnostic. The diagnostic is the first small financial commitment that proves seriousness and builds trust before the larger pilot. All offers are transparent, with no guaranteed ROI or unproven claims.

## ما هو التشخيص / What the Diagnostic Is
- نطاق محدد وزمني (مثلًا أسبوع إلى أسبوعين).
- مخرجات ملموسة: خريطة سير العمل، خريطة المخاطر، توصية تجربة.
- سعر ثابت معلن مسبقًا.

A fixed-scope, time-boxed engagement with concrete deliverables and a stated price.

## من المكالمة إلى البيع / From Call to Sale
1. **التأكيد على الألم** / Confirm the pain: أعد صياغة المشكلة بكلمات العميل.
2. **تحديد الأثر** / Quantify impact: اطلب من العميل تقدير الكلفة الحالية (بدون وعود عائد منك).
3. **عرض التشخيص** / Present the diagnostic: نطاق + مخرجات + سعر + مدة.
4. **معالجة الاعتراضات** / Handle objections: السعر، الوقت، الثقة.
5. **الإغلاق** / Close: اتفاق مكتوب وفاتورة، ثم تسجيل `diagnostic_sold` يدويًا.

## معالجة الاعتراضات الشائعة / Common Objections

| الاعتراض / Objection | الرد / Response |
|---|---|
| "مكلف" / "Too expensive" | اربط السعر بكلفة المشكلة الحالية المقدّرة من العميل نفسه. |
| "لا وقت" / "No time" | التشخيص يوفّر وقتًا لاحقًا؛ النطاق صغير ومحدد. |
| "نحتاج ضمانًا" / "Need a guarantee" | لا نضمن عائدًا؛ نضمن مخرجات واضحة وعملية موثّقة. |

## السلامة / Safety
- لا تضمن عائدًا (No guaranteed ROI) ولا تعرض جذبًا وهميًا.
- لا أرقام مخترعة عن نتائج عملاء آخرين.
- العرض والفاتورة يدويان وبموافقة المؤسس.

No guaranteed ROI, no fake traction, no invented client results. Offer and invoice are manual and founder-approved.

## التسجيل / Recording
سجّل `diagnostic_proposed` ثم `diagnostic_sold` في سجل الأحداث اليدوية مع المبلغ بالريال (`amount_sar`).
Record `diagnostic_proposed` then `diagnostic_sold` in the manual events ledger with `amount_sar`.
