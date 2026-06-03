# سياسة نطاق المراجعات — Revision Scope Policy

> الغرض: تحديد الحد الفاصل بين المراجعة المسموح بها ضمن النطاق الأصلي والطلب الجديد الذي يتجاوزه، مع تحديد عملية التقييم وإجراءات Change Request، وتزويد المؤسس بنماذج جاهزة للرد.
>
> المراجع المتقاطعة: [POST_DELIVERY_SUPPORT_POLICY_AR.md](./POST_DELIVERY_SUPPORT_POLICY_AR.md) | [DELIVERY_SIGN_OFF_TEMPLATE_AR.md](./DELIVERY_SIGN_OFF_TEMPLATE_AR.md) | [CHANGE_REQUEST_PROCESS.md](./CHANGE_REQUEST_PROCESS.md) | [SCOPE_CONTROL.md](./SCOPE_CONTROL.md)

---

## القسم الأول — تعريف المراجعة المسموح بها ضمن النطاق

المراجعة ضمن النطاق هي أي تعديل يستوفي المعايير الثلاثة التالية معاً:

**المعيار 1 — الوظيفة موثَّقة في النطاق الموقَّع**
الوظيفة أو المخرج موصوف صراحةً في وثيقة النطاق أو Sign-off. لا وجود لوظيفة "مفهومة ضمنياً" في هذه السياسة.

**المعيار 2 — التعديل تصحيح لا توسيع**
التعديل يجعل المخرج القائم يعمل كما وُصف — لا يضيف وظيفة جديدة أو يوسّع نطاق المخرج.

**المعيار 3 — الجهد لا يتجاوز حداً معقولاً**
التعديل يستغرق أقل من 2 ساعة عمل فني. ما يتجاوز ذلك يُقيَّم كـ Change Request حتى لو كان ضمن النطاق من حيث المبدأ.

### أمثلة على مراجعات ضمن النطاق

- تصحيح خطأ إملائي في مسودة رسالة مُسلَّمة
- تعديل اسم شركة مُدخَل بشكل خاطئ في بيانات الإدخال
- إعادة ترتيب أقسام تقرير متفق عليها في النطاق
- تصحيح صيغة تاريخ غير متوافقة في مخرج
- إصلاح رابط معطوب في وثيقة مُسلَّمة

---

## القسم الثاني — تعريف الطلب الجديد خارج النطاق

الطلب الجديد هو أي طلب يستوفي معياراً واحداً على الأقل من التالية:

- يُضيف وظيفة لم تُذكر في النطاق الأصلي
- يتطلب بيانات جديدة لم تكن ضمن بيانات الإدخال الأصلية
- يُنتج مخرجاً إضافياً لم يكن في قائمة المخرجات المتفق عليها
- يغيّر المنطق الجوهري لنظام قائم (معايير الترتيب، قواعد التصنيف)
- يستلزم أكثر من 2 ساعة عمل فني
- يربط النظام بمصدر بيانات أو أداة جديدة

### أمثلة واضحة على طلبات خارج النطاق

- إضافة 50 حساباً جديداً لم يكونوا في بيانات الإدخال
- إنشاء تقرير جديد لم يُذكَر في النطاق
- تغيير لغة جميع المخرجات من العربية للإنجليزية (أو العكس) بعد التسليم
- إضافة نظام تنبيهات لم يكن ضمن النطاق
- ربط المخرجات بنظام CRM خارجي
- إضافة لوحة بيانات تفاعلية على نظام تقارير نصي

---

## القسم الثالث — عملية تقييم الطلبات

### الخطوة 1 — استلام الطلب وتوثيقه (المؤسس — فوري)

عند وصول أي طلب تعديل أو إضافة من العميل:
1. سجّل الطلب في [POST_DELIVERY_SUPPORT_QUEUE.md](../../reports/delivery/POST_DELIVERY_SUPPORT_QUEUE.md) مع تاريخ الاستلام
2. أرسل للعميل تأكيد استلام خلال 4 ساعات عمل
3. لا تبدأ أي عمل قبل إتمام التقييم

### الخطوة 2 — تقييم الطلب (المؤسس — خلال 24 ساعة عمل)

طبّق معايير القسمين الأول والثاني:

```
هل الوظيفة موثَّقة في النطاق الموقَّع؟
  نعم → هل هو تصحيح (لا توسيع)؟
    نعم → هل يستلزم أقل من ساعتين؟
      نعم → مراجعة ضمن النطاق
      لا  → قيِّم كـ Change Request (الجهد يتجاوز الحد)
    لا  → طلب جديد خارج النطاق
  لا  → طلب جديد خارج النطاق
```

### الخطوة 3 — الرد على العميل (خلال 24 ساعة عمل)

- مراجعة ضمن النطاق → ابدأ العمل وأرسل تأكيداً بموعد الإنجاز
- طلب جديد → أرسل رد Change Request (انظر القسم الخامس)

---

## القسم الرابع — إجراءات Change Request

### متى يُرفَع Change Request؟

عند كل طلب يُصنَّف "خارج النطاق" في عملية التقييم أعلاه.

### مكوّنات نموذج Change Request

| الحقل | المحتوى |
|---|---|
| معرّف CR | CR-[معرف المشروع]-[رقم تسلسلي] |
| تاريخ الطلب | |
| وصف الطلب | ما يريده العميل بلغة محايدة |
| سبب تصنيفه خارج النطاق | مع مرجع لبند النطاق الأصلي |
| الجهد التقديري | بالساعات أو الأيام |
| التكلفة التقديرية | مع ملاحظة "تقديرية، تحتاج تأكيداً" |
| الأثر على الجدول | هل يؤثر على مشاريع أخرى؟ |
| خيارات المعالجة | Sprint إضافي / Retainer / حزمة منفردة |

### عملية الموافقة على Change Request

1. يُرسَل نموذج CR للعميل ويُشرَح شفهياً إذا لزم
2. العميل لديه 5 أيام عمل للرد: موافقة / رفض / تعديل
3. بدون موافقة كتابية لا يُنفَّذ أي عمل
4. بعد الموافقة يُجمَّد العمل الحالي ويُحدَّد موعد بدء CR
5. CR مكتمل يُضاف للنطاق ويحتاج Sign-off منفصلاً

---

## القسم الخامس — نماذج الرد على طلبات خارج النطاق

### النموذج أ — رد موجز لطلب إضافة بيانات

---

**بالعربية:**

شكراً على طلبك. بعد مراجعة النطاق الأصلي، إضافة [وصف الطلب] يقع خارج نطاق المشروع الحالي لأن [السبب المحدد].

يمكننا معالجة هذا الطلب عبر طلب تغيير (Change Request) بتكلفة تقديرية تُحدَّد بعد مراجعة مفصَّلة. هل تودّ أن أُعدّ تفاصيل طلب التغيير لمراجعتك؟

**بالإنجليزية:**

Thank you for your request. After reviewing the agreed scope, [request description] falls outside the current project scope because [specific reason].

We can address this through a Change Request with an estimated cost to be determined after detailed review. Would you like me to prepare the Change Request details for your review?

---

### النموذج ب — رد مفصَّل لطلب وظيفة جديدة

---

**بالعربية:**

تلقيتُ طلبك المتعلق بـ [وصف الطلب] وأُقدِّر وضوحك.

بعد مقارنة الطلب بوثيقة النطاق الموقَّعة في [التاريخ]، أؤكد أن هذه الوظيفة لم تُدرَج في النطاق الأصلي. النطاق الأصلي تضمّن: [قائمة موجزة بما شمله النطاق].

خياراتك للمضي قدماً:
1. **طلب تغيير (Change Request):** نُحدد النطاق الجديد والتكلفة ونُرسَل لك خلال 48 ساعة عمل.
2. **Sprint إضافي:** إذا كان الطلب واسعاً بما يكفي لتشكيل مشروع مستقل.
3. **إرجاء الطلب:** تُؤجَّل إلى دورة Retainer إذا كنت تخطط للاشتراك الشهري.

أيّ خيار يناسبك؟

**بالإنجليزية:**

I received your request regarding [request description] and appreciate the clarity.

After comparing it to the agreed scope document signed on [date], I confirm this functionality was not included in the original scope, which covered: [brief scope summary].

Your options to proceed:
1. **Change Request:** We define the new scope and cost and send it to you within 48 business hours.
2. **Additional Sprint:** If the request is substantial enough to form a standalone project.
3. **Defer to Retainer:** If you plan to subscribe to monthly operations support.

Which option suits you?

---

### النموذج ج — رد على طلب مُلحّ خارج النطاق

---

**بالعربية:**

أفهم أن هذا الطلب عاجل. لكن تنفيذه قبل توضيح النطاق والتكلفة يضع كلانا في موقف غير واضح.

ما أقترحه: نتحدث 15 دقيقة اليوم أو غداً، أُحدد لك الجهد والتكلفة التقديرية، وإذا اتفقنا نبدأ مباشرةً. هذا يضمن أن تحصل على ما تحتاجه بشروط واضحة ودون مفاجآت.

هل يناسبك [اقتراح وقت]؟

**بالإنجليزية:**

I understand this request is urgent. However, executing it before clarifying scope and cost puts us both in an ambiguous position.

What I suggest: a 15-minute call today or tomorrow so I can determine the effort and estimated cost. If we agree, we start immediately. This ensures you get what you need with clear terms and no surprises.

Does [suggested time] work for you?

---

## المراجع المتقاطعة

- سياسة الدعم بعد التسليم: [POST_DELIVERY_SUPPORT_POLICY_AR.md](./POST_DELIVERY_SUPPORT_POLICY_AR.md)
- عملية Change Request التقنية: [CHANGE_REQUEST_PROCESS.md](./CHANGE_REQUEST_PROCESS.md)
- ضبط النطاق الأصلي: [SCOPE_CONTROL.md](./SCOPE_CONTROL.md)
- قائمة طلبات الدعم: [../../reports/delivery/POST_DELIVERY_SUPPORT_QUEUE.md](../../reports/delivery/POST_DELIVERY_SUPPORT_QUEUE.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
