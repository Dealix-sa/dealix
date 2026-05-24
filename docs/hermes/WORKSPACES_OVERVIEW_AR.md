# Workspaces — نظرة شاملة على الـ 7 مساحات عمل

> المرجع: §29 من المواصفة الأصلية.

---

## القاعدة الذهبية

> **Sovereign Workspace لا يشارك أي شيء تلقائيًا مع أي workspace آخر.**

أي بيانات، قرار، أو إعداد ينشأ داخل Sovereign Workspace يبقى هناك حتى يُصدر المالك أمرًا صريحًا بنشره. لا توجد "مزامنة افتراضية"، ولا "تعرّف على بعض"، ولا "share by default".

نفس المنطق يمتد بين الـ workspaces الأخرى: كل workspace يرى ما يحتاجه فقط، ولا يرى ما لا يخصّه.

---

## لماذا 7 workspaces؟

كل workspace يمثّل **سياقًا تشغيليًا منفصلًا** له:
- مالك واحد محدد.
- غرض واحد محدد.
- جمهور وصول محدد.
- مجموعة صفحات/أدوات/أحداث ظاهرة فيه.
- مجموعة أخرى مُخفاة عنه عمدًا.

الفصل ليس تنظيميًا فقط — هو **تقني**: كل workspace له جدول صلاحيات، قاموس أحداث ظاهرة، وحدود تشغيلية يفرضها Hermes.

---

## جدول مقارن للـ 7 workspaces

| Workspace | المالك | الغرض | من يصل | ما يُعرض | ما يُخفى |
|---|---|---|---|---|---|
| **Sovereign** ([تفاصيل](SAMI_SOVEREIGN_WORKSPACE_AR.md)) | Sami (المؤسس) | حوكمة عليا + قرارات استراتيجية + ثروة شخصية | شخص واحد فقط | كل شيء (10 صفحات Command/Money/Approvals/...) | لا شيء — هذا أعلى مستوى |
| **Internal Dealix** ([تفاصيل](INTERNAL_DEALIX_WORKSPACE_AR.md)) | فريق Dealix | تشغيل الشركة اليومي | الفريق الداخلي | 11 صفحة عمليات/منتج/بيانات/جودة | السيادة الشخصية، Personal Wealth، Kill Switch |
| **Customer** ([تفاصيل](CUSTOMER_WORKSPACE_AR.md)) | العميل | استلام القيمة + Value Reports | مستخدمو العميل المعتمدون | 8 صفحات نتائج/فرص/تقارير | الاستراتيجية الداخلية، البيانات الخام، عملاء آخرون |
| **Partner** ([تفاصيل](PARTNER_WORKSPACE_AR.md)) | الشريك (وكالة white-label) | تقديم القيمة لعملاء الشريك تحت علامته | فريق الشريك | 8 صفحات تشغيل/تقارير + branding | Sovereign Layer، عملاء آخرين، Tool Registry الداخلي |
| **Trust** ([تفاصيل](TRUST_WORKSPACE_AR.md)) | مسؤول الحوكمة (قد يكون Sami أو مفوّض) | مراقبة الجودة والمخاطر | Sovereign + مفوّضو الحوكمة | 9 صفحات سياسات/تنبيهات/تدقيق/أدوات | بيانات تجارية تفصيلية لا تخص الحوكمة |
| **Venture** ([تفاصيل](VENTURE_WORKSPACE_AR.md)) | فريق Venture Studio | تجريب verticals جديدة | فريق Venture + Sovereign | 8 صفحات بطاقات قطاعات/فرضيات/قياس | عمليات الإنتاج الكاملة، عملاء راسخون |
| **Marketplace API / Public** | Sovereign (تحت إشراف Trust) | واجهات للمطورين الخارجيين والشركاء التقنيين | عام مُسجَّل | API docs، schemas، حدود الاستخدام | كل ما هو داخلي |

> الـ Marketplace/Public ليس workspace كامل بنفس مستوى الستة الأخرى — هو **سطح خارجي** تحت سيطرة Hermes، يُذكر هنا للاكتمال ولأن §29 يعدّه ضمن طبقة الـ workspaces عند الحديث عن سطوح الوصول.

---

## مبادئ تصميم Workspaces

1. **عزل افتراضي** — كل workspace معزول؛ المشاركة استثناء يحتاج قرارًا.
2. **مُسطّح في الأحداث** — كل workspace يرى نسخة مُفلترة من نفس bus الأحداث المركزي.
3. **لا backdoor** — لا توجد طريقة لقراءة workspace من آخر دون أن يُسجَّل الحدث.
4. **Sovereignty downward only** — Sovereign يرى الكل؛ لكن الكل لا يرى Sovereign.
5. **Branding قابل للتخصيص** — Partner و Customer يمكن أن يحملا branding مختلف؛ Sovereign و Trust لا.
6. **Kill propagation فوري** — أمر Kill من Sovereign يصل لكل الـ workspaces خلال زمن مضمون.

---

## ما لا تفعله أي Workspace

- لا workspace (عدا Sovereign) يستطيع تعديل سياسات Trust.
- لا workspace يستطيع إنشاء وكيل/أداة جديدة دون مرور Sovereign.
- لا workspace يستطيع رؤية بيانات workspace آخر، حتى لو طلبها برمجيًا.
- لا workspace يستطيع إخفاء سجلاته عن Sovereign — الشفافية للأعلى مضمونة.

---

## كيف تختار أين تذهب البيانات؟

| نوع البيانات | الـ workspace المنطقي |
|---|---|
| قرار رأسمالي / kill / scale | Sovereign |
| تشغيل وكيل لعميل محدد | Internal + ظهور نتيجة في Customer |
| تنبيه خرق سياسة | Trust + Sovereign |
| تجربة قطاع جديد قبل الإنتاج | Venture |
| تقديم خدمة لعميل شريك تحت اسم الشريك | Partner |
| استدعاء API خارجي للمطورين | Marketplace |

---

## English Summary

- Dealix exposes seven workspace surfaces, each with a single owner, a single purpose, and an explicit list of what is visible and what is hidden.
- The golden rule is strict: the Sovereign Workspace never auto-shares with any other workspace; sharing is always an explicit decision.
- Isolation is enforced technically through Hermes, not just organizationally — there are no backdoors between workspaces.
- Sovereignty flows downward only: Sovereign can see everything, but no other workspace can see Sovereign.
- Kill commands originating from Sovereign propagate to every workspace within a guaranteed time window.
