# قالب نطاق عمل وقبول — Revenue Command Pilot (30 يومًا)

> الحالة: `draft_only / founder_legal_finance_approval_required`  
> لا سعر، لا عرض ملزم، ولا تفويض دفع في هذا القالب.

## 1. الأطراف

- العميل: `[LEGAL_NAME]`
- Dealix entity: `[LEGAL_NAME]`
- صاحب القرار لدى العميل: `[ROLE]`
- المالك التشغيلي: `[ROLE]`
- Privacy/Security contacts: `[ROLES]`

لا يوقّع قبل التحقق من الكيانات والصلاحيات.

## 2. الهدف

اختبار workflow إيراد واحد خلال 30 يومًا باستخدام بيانات first-party محدودة ومصرح بها، لإنتاج baseline وتدخل تشغيلي واحد وProof Pack وقرار `stop / redesign / expand`.

لا يهدف إلى استبدال CRM/ERP، ولا يضمن مبيعات أو إيرادًا أو ROI.

## 3. النطاق

- ICP/workflow: `[ONE_WORKFLOW]`
- النظام المصدر: `[ONE_SOURCE_SYSTEM]`
- الحقول المعتمدة: `[MINIMUM_FIELDS]`
- المقياس: `[ONE_PRIMARY + UP_TO_2_GUARDRAILS]`
- baseline window: `[DATE_RANGE]`
- العينة: `[AUTHORIZED_SAMPLE]`
- الإجراء الخارجي: `draft_only`

## 4. المخرجات ومعايير القبول

| الأسبوع | المخرج | معيار القبول | المالك |
|---|---|---|---|
| 0 | RACI + data map + access approval | توقيع الأطراف والحقول والغرض | الطرفان |
| 1 | Baseline Pack | المصدر والتاريخ والتعريف وفجوات الدليل واضحة | العميل |
| 2 | Workflow/Decision intervention | قاعدة owner/next action وموافقة قابلة للاختبار | Dealix |
| 3 | Weekly executive readout | قرار ومخاطر واستثناءات موثقة | العميل |
| 4 | Proof Pack + final decision | before/after وحدود attribution وقرار صريح | الطرفان |

القبول لا يعني تحقق نتيجة مالية؛ يعني تسليم النطاق وفق الدليل المتفق عليه.

## 5. مسؤوليات العميل

- امتلاك الحق في البيانات وتزويدها بطريقة معتمدة.
- تعيين صاحب قرار ومالك تشغيلي.
- اعتماد baseline والمقاييس والمخرجات في الوقت المحدد.
- عدم طلب بيانات/قنوات/تكاملات خارج النطاق.
- عدم نشر مخرجات أو ادعاءات دون موافقة متبادلة.

## 6. مسؤوليات Dealix

- أقل وصول ونطاق.
- فصل الحقيقة والفرضية والمجهول.
- إبقاء الرسائل والأسعار والخصومات والنشر `approval_required`.
- سجل موافقات وإثبات.
- الإفصاح عن blockers والحوادث وحدود الدليل.
- عدم استخدام بيانات العميل خارج تعليماته المعتمدة.

## 7. السعر والدفع والفوترة

- السعر قبل الضريبة: `[FOUNDER_APPROVED_SAR]`
- VAT: `[FINANCE_CONFIRMED]`
- جدول الدفع: `[MILESTONES]`
- شروط الاسترداد/الرصيد: `[APPROVED_ORDER_FORM_TERMS]`
- مسؤول ZATCA/e-invoice: `[OWNER]`

ZATCA توضح أن الفوترة الإلكترونية مطبقة على مرحلتين وتوفر مواصفات واشتراطات أمنية للمطورين: https://zatca.gov.sa/en/E-Invoicing/Pages/default.aspx

لا Checkout أو charge قبل اعتماد #917 واختبار sandbox والفاتورة والمصالحة.

## 8. التغيير والتوسّع

أي طلب يغيّر workflow أو البيانات أو التكامل أو المدة أو المخرجات يحتاج Change Request مكتوبًا يحدد الأثر والسعر والمخاطر. الصمت لا يعد موافقة.

## 9. البيانات والأمن

`PILOT_DATA_PROCESSING_AND_SECURITY_PACK_AR.md` وDPA جزء من العقد. لا وصول قبل إكمال #918. أي بيانات حساسة أو نقل جديد يوقف العمل حتى المراجعة.

## 10. الإتاحة والدعم

- نافذة العمل: `[BUSINESS_HOURS]`
- قناة الدعم: `[APPROVED_CHANNEL]`
- زمن الاستجابة: `[MEASURED_SERVICE_TARGET]`
- الاستثناءات: `[PLANNED_MAINTENANCE / PROVIDER_DEPENDENCY]`

لا SLA عام قبل اعتماد القدرة التشغيلية.

## 11. الملكية والنشر

- ملكية بيانات العميل تبقى للعميل.
- ملكية Dealix السابقة تبقى لـDealix.
- ترخيص المخرجات الخاصة يحدد في العقد.
- لا اسم أو شعار أو testimonial أو case study أو رقم نتيجة دون موافقة نشر مكتوبة منفصلة.

## 12. الإيقاف والإنهاء

إيقاف فوري عند:

- وصول غير مصرح أو غرض غير واضح.
- P0 أمني/خصوصي.
- طلب إرسال/كشط/ضمان مخالف.
- غياب صاحب القرار أو البيانات اللازمة.
- عدم دفع وفق العقد.

معالجة الإنهاء والحذف والاسترداد تُحدد في أمر العمل وDPA، لا عبر وعود عامة.

## 13. التوقيعات

| الدور | الاسم/الصفة | القرار | التاريخ | مرجع الدليل |
|---|---|---|---|---|
| Founder |  | approve/reject |  |  |
| Legal/Privacy |  | approve/reject |  |  |
| Finance/Tax |  | approve/reject |  |  |
| Security |  | approve/reject |  |  |
| Customer authorized signatory |  | approve/reject |  |  |
