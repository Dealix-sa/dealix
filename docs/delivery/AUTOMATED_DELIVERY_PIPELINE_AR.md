# خط التسليم الآلي
# Automated Delivery Pipeline

---

## المبدأ — Principle

كل Sprint يمر بـ 7 مراحل واضحة. لا مرحلة تُتخطى. لا تسليم بدون Sign-Off. كل خطوة تُسجَّل في `reports/delivery/DELIVERY_PIPELINE_STATUS.md`.

Every Sprint passes through 7 clear stages. No stage is skipped. No delivery without Sign-Off. Every step is logged.

---

## المرحلة 1 — Intake (جمع المدخلات)

**الهدف:** استلام كل المدخلات المطلوبة من العميل قبل بدء العمل.

**الإجراءات:**
1. إرسال قائمة المدخلات المطلوبة للعميل (من Mini Proposal)
2. تحديد موعد نهائي لاستلام المدخلات (عادة 48 ساعة)
3. تسجيل استلام كل ملف في سجل Intake

**معيار الاكتمال:** كل المدخلات المذكورة في Mini Proposal مُستلَمة.

**حالة Pipeline:** `INTAKE_PENDING` → `INTAKE_COMPLETE`

---

## المرحلة 2 — Readiness Gate (التحقق من الاكتمال)

**الهدف:** التحقق من أن المدخلات المُستلمة كافية وصالحة للمعالجة.

**الإجراءات:**
1. مراجعة كل مدخل مقابل القائمة المتفق عليها
2. اختبار صحة البيانات (هل الملف قابل للقراءة؟ هل البيانات مكتملة؟)
3. إذا كانت هناك فجوات: إخطار العميل وتوقف الساعة حتى الاكتمال

**معيار الاكتمال:** Readiness Score = 100% (كل المدخلات صالحة)

**حالة Pipeline:** `GATE_PENDING` → `GATE_PASSED`

**ملاحظة:** وقت التسليم لا يبدأ إلا بعد GATE_PASSED.

---

## المرحلة 3 — Execution (التنفيذ)

**الهدف:** بناء النظام التشغيلي المتفق عليه.

**الإجراءات:**
1. تنفيذ الخطوات المحددة في Sprint Library
2. توثيق كل قرار تصميمي كبير
3. تحديث DELIVERY_PIPELINE_STATUS يومياً

**معيار الاكتمال:** كل المخرجات الرئيسية جاهزة للمراجعة الداخلية.

**حالة Pipeline:** `IN_EXECUTION` → `EXECUTION_COMPLETE`

---

## المرحلة 4 — Review (المراجعة الداخلية)

**الهدف:** التأكد من أن المخرجات تلبي معيار الجودة قبل عرضها على العميل.

**الإجراءات:**
1. مراجعة كل مخرج مقابل Mini Proposal
2. اختبار الـ Workflow (هل يعمل كما صُمِّم؟)
3. إزالة أي بيانات PII لا يجب ظهورها
4. التحقق من Claim Safety (لا ادعاءات غير مدعومة)

**معيار الاكتمال:** Delivery Review Agent يُصدر تقرير مراجعة بدون ملاحظات مفتوحة.

**حالة Pipeline:** `INTERNAL_REVIEW` → `REVIEW_PASSED`

---

## المرحلة 5 — Client Review (مراجعة العميل)

**الهدف:** عرض المخرجات على العميل للمراجعة وجمع التغذية الراجعة.

**الإجراءات:**
1. إرسال المخرجات للعميل مع دليل الاستخدام
2. تحديد 48 ساعة للمراجعة
3. تسجيل كل ملاحظة من العميل في سجل مراجعة

**معيار الاكتمال:** العميل قدّم تغذية راجعة (موافق أو ملاحظات محددة)

**حالة Pipeline:** `CLIENT_REVIEW` → `CLIENT_FEEDBACK_RECEIVED`

**تنبيه:** أي طلب تغيير خارج النطاق → Change Request Process.

---

## المرحلة 6 — Sign-Off (التوقيع والقبول)

**الهدف:** الحصول على قبول رسمي موثق من العميل.

**الإجراءات:**
1. إرسال `docs/delivery/DELIVERY_SIGN_OFF_TEMPLATE_AR.md` للعميل
2. الحصول على توقيع أو موافقة كتابية واضحة
3. تسجيل تاريخ Sign-Off في DELIVERY_PIPELINE_STATUS

**معيار الاكتمال:** Sign-Off موقّع أو موافقة كتابية صريحة.

**حالة Pipeline:** `AWAITING_SIGN_OFF` → `SIGNED_OFF`

---

## المرحلة 7 — Proof Pack (تجميع الأدلة)

**الهدف:** تجميع حزمة إثبات كاملة قابلة للمراجعة.

**الإجراءات:**
1. لقطات شاشة قبل/بعد (إذا وجدت)
2. قائمة المخرجات المُسلَّمة
3. Sign-Off الموقّع
4. ملاحظات تقييم العميل
5. تحديث VALUE_LEDGER

**معيار الاكتمال:** Proof Pack كامل في ملف Delivery

**حالة Pipeline:** `PROOF_PACK_BUILDING` → `DELIVERED_CLEAN`

---

## قواعد Pipeline — Pipeline Rules

1. **لا قفز:** كل مرحلة تكتمل قبل الانتقال للتالية
2. **الساعة تتوقف:** عند انتظار مدخلات من العميل، وقت التسليم يتوقف
3. **Change Request فوري:** أي طلب خارج النطاق لا يُنفَّذ قبل Change Request موقّع
4. **تحديث يومي:** DELIVERY_PIPELINE_STATUS يُحدَّث كل يوم
5. **Delivery Blockers شفافة:** أي عائق يُسجَّل فوراً في `reports/delivery/DELIVERY_BLOCKERS.md`

---

## جدول الحالات — Status Reference

| الحالة | المعنى |
|--------|--------|
| INTAKE_PENDING | ننتظر مدخلات العميل |
| INTAKE_COMPLETE | استلمنا كل المدخلات |
| GATE_PENDING | نراجع صحة المدخلات |
| GATE_PASSED | المدخلات سليمة — بدأ العمل رسمياً |
| IN_EXECUTION | نبني النظام |
| EXECUTION_COMPLETE | البناء مكتمل |
| INTERNAL_REVIEW | مراجعة داخلية |
| REVIEW_PASSED | جاهز للعميل |
| CLIENT_REVIEW | العميل يراجع |
| CLIENT_FEEDBACK_RECEIVED | تلقينا تغذية راجعة |
| AWAITING_SIGN_OFF | ننتظر التوقيع |
| SIGNED_OFF | تم التوقيع |
| PROOF_PACK_BUILDING | نجمع الأدلة |
| DELIVERED_CLEAN | تسليم كامل موثق |
| BLOCKED | عائق — انظر DELIVERY_BLOCKERS |

---

## الوثائق المرتبطة — Related Documents

- [`docs/delivery/CLIENT_DELIVERY_ACCEPTANCE_SYSTEM_AR.md`](./CLIENT_DELIVERY_ACCEPTANCE_SYSTEM_AR.md)
- [`docs/delivery/DELIVERY_SIGN_OFF_TEMPLATE_AR.md`](./DELIVERY_SIGN_OFF_TEMPLATE_AR.md)
- [`docs/delivery/WEEKLY_VALUE_REPORTS_AR.md`](./WEEKLY_VALUE_REPORTS_AR.md)
- [`reports/delivery/DELIVERY_PIPELINE_STATUS.md`](../../reports/delivery/DELIVERY_PIPELINE_STATUS.md)
- [`reports/delivery/DELIVERY_BLOCKERS.md`](../../reports/delivery/DELIVERY_BLOCKERS.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
