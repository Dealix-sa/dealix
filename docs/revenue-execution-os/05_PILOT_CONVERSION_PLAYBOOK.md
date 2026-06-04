# Pilot Conversion Playbook — دليل التحويل إلى تجربة

## الغرض (AR)
يشرح هذا الدليل كيف يتحوّل التشخيص المُسلَّم إلى تجربة مدفوعة (Pilot). التجربة هي تنفيذ محدود النطاق يثبت القيمة عمليًا قبل العقد الشهري. كل العروض شفافة، بلا ضمانات عائد، والتنفيذ والتواصل يدويان.

## Purpose (EN)
This playbook explains how a delivered diagnostic converts into a paid pilot. The pilot is a limited-scope implementation that proves value in practice before a retainer. All offers are transparent, with no guaranteed ROI, and execution and contact remain manual.

## شرط البداية / Entry Condition
- يجب أن تكون الحالة `diagnostic_delivered`.
- يجب وجود توصية تجربة واضحة من حزمة التشخيص (`pilot_recommendation.md`).

The deal must be at `diagnostic_delivered` with a clear pilot recommendation from the diagnostic pack.

## من التشخيص إلى التجربة / From Diagnostic to Pilot
1. **عرض النتائج** / Present findings: راجع خريطة سير العمل والمخاطر مع العميل.
2. **حدد تجربة واحدة** / Define one pilot: أعلى أثر وأقل تعقيد.
3. **اتفق على معايير النجاح** / Agree success criteria: قابلة للقياس وواقعية.
4. **العرض** / Propose: نطاق + مدة + سعر + معايير نجاح.
5. **الإغلاق** / Close: اتفاق مكتوب، ثم تسجيل `pilot_sold` يدويًا.

## معايير النجاح / Success Criteria
- محددة، قابلة للقياس، ومتفق عليها كتابيًا.
- لا تَعِد بأرقام لا تستطيع التحكم بها.
- اربطها بمخرجات يتحكم بها التنفيذ، لا بعائد مضمون.

Specific, measurable, and written. Tied to controllable outputs, never to a guaranteed return.

## معالجة الاعتراضات / Objection Handling

| الاعتراض / Objection | الرد / Response |
|---|---|
| "نريد كل شيء الآن" / "Want everything now" | التجربة تقلّل المخاطر وتثبت القيمة أولًا. |
| "السعر مرتفع" / "Price high" | اربطه بنطاق محدد ومخرجات ملموسة. |
| "هل ستنجح؟" / "Will it work?" | نقيس النجاح بمعايير متفق عليها؛ لا ضمانات عائد. |

## السلامة / Safety
- لا ضمان عائد، لا جذب وهمي، لا ادعاءات غير مثبتة.
- العقد والفاتورة يدويان ومعتمدان من المؤسس.

No guaranteed ROI, no fake traction, no unproven claims. Contract and invoice are manual and founder-approved.

## التسجيل / Recording
سجّل `pilot_proposed` ثم `pilot_sold` مع `amount_sar` في سجل الأحداث اليدوية.
Record `pilot_proposed` then `pilot_sold` with `amount_sar` in the ledger.
