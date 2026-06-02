# Content Production OS — Case Study System — نظام دراسات الحالة

> How to turn a delivered engagement into a case-safe story without leaking client data. Mandatory rule: a case study is labeled "Hypothetical / case-safe template" unless a real customer signed publish permission. No PII, no real names without signed permission, no sales numbers stated as fact.
>
> Cross-link: [CONTENT_ENGINE_AR.md](./CONTENT_ENGINE_AR.md) · [PROOF_CONTENT_SYSTEM_AR.md](./PROOF_CONTENT_SYSTEM_AR.md) · [LINKEDIN_SYSTEM_AR.md](./LINKEDIN_SYSTEM_AR.md) · [../commercial/operations/CASE_STUDY_TEMPLATE_AR.md](../commercial/operations/CASE_STUDY_TEMPLATE_AR.md) · [../commercial/operations/PROOF_STACK_ORDER_AR.md](../commercial/operations/PROOF_STACK_ORDER_AR.md) · [../07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md) · [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)

---

## المبدأ — The principle

دراسة الحالة ليست إعلاناً، بل إثباتاً مُهيكلاً. تأخذ التزاماً سُلِّم فعلاً وتحوّله إلى قصة آمنة: تشرح **النمط** دون كشف **العميل**. القصة تبيع المنهجية، لا اسم الشركة. هذا الملف يصف **كيف** نكتبها؛ القالب التشغيلي الكامل (Metadata، segment، motion، proof_level) في [../commercial/operations/CASE_STUDY_TEMPLATE_AR.md](../commercial/operations/CASE_STUDY_TEMPLATE_AR.md)، وقاعدة «Verified فقط» في [../07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md).

---

## القواعد الإلزامية — Mandatory rules

هذه ليست توصيات. خرق أي منها يمنع النشر:

1. **الوسم الافتراضي إلزامي.** كل دراسة حالة تُوسم في أعلاها **«Hypothetical / case-safe template — حالة افتراضية / قالب آمن»** ما لم يوقّع عميل حقيقي إذن نشر صريحاً. الوضع الافتراضي افتراضي.
2. **لا اسم عميل بلا إذن موقّع.** لا اسم شركة، لا شعار، لا اسم شخص، لا منصب يكشف الهوية — إلا بإذن نشر مكتوب ومحفوظ. هذا من بنود عدم التفاوض (لا PII).
3. **لا أرقام بيع كحقيقة.** «أغلقنا له صفقات بـ X» ممنوع. كل رقم إمّا «تقديري» أو «نمط آمن» أو رقم منهجي بمصدر. النتائج «فرص مُثبتة بأدلة»، لا مبيعات مضمونة.
4. **لا رقم بلا مصدر.** كل رقم في الجدول يحمل `source_ref` (proof_pack، CRM مُستورد في KPI، لقطة مُخفّاة). لقطة لوحة بلا `source_id` لا تُعدّ دليلاً.
5. **التعميم قبل الكشف.** نصف القطاع بدل الشركة («وسيط تأمين متوسط» لا «شركة كذا»)، والحجم بنطاق لا بعدد دقيق يكشف الهوية.
6. **الإذن يرفع المستوى، لا يُسقط القواعد.** حتى مع إذن موقّع، تبقى قواعد «لا أرقام بيع كحقيقة» و«لا رقم بلا مصدر» سارية.

---

## بنية القالب الآمن — The case-safe template structure

خمسة مقاطع، بهذا الترتيب. هذا هيكل السرد العام؛ يُعبّأ من القالب التشغيلي:

```text
[وسم إلزامي في الأعلى]
Hypothetical / case-safe template — حالة افتراضية / قالب آمن
(أو: Published with signed permission — منشور بإذن موقّع — إن وُجد)

case_id:      CS-YYYY-MM-NNN
sector:       القطاع (مُعمَّم)
proof_level:  L0–L5  (انظر PROOF_CONTENT_SYSTEM_AR.md)
anonymized:   true | false
permission:   none | signed (ref)
```

1. **السياق / Context** — القطاع المُعمَّم، الحجم بنطاق، والـ Trigger: لماذا الآن؟ بلا أي معرّف هوية.
2. **التسرّب المُكتشَف / Leakage found** — الألم الواحد القابل للقياس: حسابات راكدة، تأخر متابعة، تكرار، غياب مالك. مُسنَد بمصدر إن كان رقماً.
3. **الـ Workflow** — العلاج الواحد الذي شغّلناه: العرض، المدة، والحوكمة (approval-first · Decision Passport). خطوة واحدة واضحة، لا قائمة قدرات.
4. **النتيجة المُثبتة بأدلة / Evidenced result** — قبل/بعد بمصدر لكل رقم. النتائج فرص مُثبتة بأدلة، لا أرقام بيع. مستوى الإثبات معلن.
5. **الخطوة التالية / Next step** — العرض المرتبط (Sprint / Retainer / التوقف عند التشخيص) و CTA واحد.

ثم سطر الإخلاء. للنسخة المنشورة على لينكدإن، تتبع البنية والحرفة في [LINKEDIN_SYSTEM_AR.md](./LINKEDIN_SYSTEM_AR.md) (ثنائية اللغة، قسمان متطابقان).

---

## متى تُنشر — Publish timing

تتبع ترتيب طبقة الأدلة في [../commercial/operations/PROOF_STACK_ORDER_AR.md](../commercial/operations/PROOF_STACK_ORDER_AR.md): الحالة الآمنة بأسماء (طبقة 5) لا تُرسل ولا تُنشر إلا بعد `payment_received` **و** بإذن كتابي. قبل ذلك، تبقى القصة افتراضية وموسومة كذلك. الحالات الافتراضية يمكن إنتاجها في أي وقت لأنها لا تكشف عميلاً.

---

## من الافتراضي إلى الحقيقي — From hypothetical to real

التحوّل خطوة بخطوة، ولا يحدث صدفة:

1. **تسليم مكتمل** — يوجد `proof_pack_delivered` بمستوى إثبات واضح.
2. **طلب إذن** — يُعرض على العميل نص النشر النهائي قبل أي طلب توقيع.
3. **إذن موقّع ومحفوظ** — `permission: signed (ref)` يُسجَّل ويُربَط بالحالة.
4. **استبدال الوسم** — يُرفع وسم «Hypothetical» ويُستبدل بـ «Published with signed permission».
5. **بقاء القواعد** — لا أرقام بيع كحقيقة، لا رقم بلا مصدر، حتى بعد الإذن.

بلا الخطوات الأربع الأولى، الحالة تبقى افتراضية وموسومة. لا اختصار.

---

## بوابة الجودة لدراسة الحالة — Case study quality gate

- [ ] الوسم في الأعلى: «Hypothetical / case-safe template» أو «Published with signed permission».
- [ ] لا اسم عميل / شعار / شخص / منصب كاشف بلا إذن موقّع.
- [ ] القطاع والحجم مُعمَّمان.
- [ ] كل رقم يحمل `source_ref`؛ لا لقطة لوحة بلا `source_id`.
- [ ] لا رقم بيع كحقيقة؛ النتائج «فرص مُثبتة بأدلة».
- [ ] `proof_level` معلن ولا يُبالَغ فيه (انظر [PROOF_CONTENT_SYSTEM_AR.md](./PROOF_CONTENT_SYSTEM_AR.md)).
- [ ] العرض ضمن النطاق المعتمد و CTA واحد.
- [ ] لا ذكر scraping أو إرسال بارد أو أتمتة لينكدإن كخدمة.
- [ ] سطر الإخلاء في النهاية.
- [ ] موافقة المؤسس مسجَّلة قبل النشر، والنشر يدوي.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
