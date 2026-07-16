# حزمة معالجة البيانات والأمن لأول Pilot — Dealix

> الحالة: `draft_only / counsel_approval_required / customer_specific`  
> المالك: Privacy Owner + Security Owner + Founder  
> المرجع التنفيذي: GitHub #918  
> هذا قالب تشغيل ومراجعة، وليس رأيًا قانونيًا أو ادعاء امتثال.

## 1. قاعدة المنع

لا بيانات عميل حقيقية، ولا جهات اتصال، ولا رسائل، ولا Prompts شخصية تدخل Dealix قبل اكتمال:

1. نطاق Pilot وأمر العمل.
2. تحديد Controller/Processor لكل تدفق بواسطة مستشار سعودي.
3. الغرض، الحقول، المصدر، الصلاحية/الإذن، والاحتفاظ.
4. قائمة Subprocessors والمناطق.
5. قرار مكتوب بشأن النقل عبر الحدود.
6. اختبار tenant isolation والحذف والتصدير وsuppression.
7. موافقة العميل والمالك الداخلي.

## 2. الحقيقة الحالية التي تحتاج قرارًا

- سجل GitHub #918 يوثق أن لقطة المؤسس أظهرت Postgres الإنتاجي في **US West**. يجب إعادة التحقق من المنطقة والإعدادات وقت الاعتماد.
- لا نستنتج أن الاستضافة خارج المملكة ممنوعة دائمًا، ولا نقبلها صامتًا؛ القرار يحتاج خريطة تدفق ومراجعة مستشار سعودي.
- منصة حوكمة البيانات الوطنية توفر التسجيل، تقييم الأثر، إشعار تسرب البيانات، أداة تحديد إلزامية مسؤول حماية البيانات، والتقييم الذاتي: https://dgp.sdaia.gov.sa/wps/portal/pdp/home
- لا يوصف Dealix بأنه «متوافق 100%»؛ الجاهزية تعتمد على العميل والغرض والبيانات والعقد والتشغيل الفعلي.

## 3. أطراف المعالجة — تُملأ لكل عميل

| البند | القرار | الدليل |
|---|---|---|
| العميل Controller أم Joint Controller | TBD by counsel | رأي/عقد |
| Dealix Processor أم Controller لغرض محدد | TBD by counsel | DPA |
| نقطة اتصال الخصوصية لدى العميل | TBD | اسم وظيفي فقط |
| Privacy Owner لدى Dealix | TBD | قرار تكليف |
| هل DPO مطلوب؟ | TBD | أداة NDGP + رأي |
| هل DPIA مطلوب؟ | TBD | تقييم الأثر |
| هل التسجيل مطلوب؟ | TBD | NDGP/رأي |
| آلية النقل عبر الحدود | TBD | تقييم/ضمانات |

## 4. نطاق البيانات المسموح مبدئيًا

بعد الاعتماد فقط:

- معرف حساب العميل الداخلي.
- حقول workflow الدنيا المتفق عليها.
- حالة الفرصة ومالكها وخطوتها التالية.
- أحداث الموافقة والإثبات.
- مقاييس baseline المجمعة أو المعرّفة بأقل قدر ممكن.

ممنوع في cohort الأول دون مراجعة مستقلة:

- أرقام هوية، بطاقات، حسابات مالية كاملة.
- بيانات صحية أو فئات حساسة.
- كلمات مرور، مفاتيح، أسرار أو ملفات اعتماد.
- قوائم جهات اتصال مجهولة المصدر.
- نسخ محادثات واسعة غير لازمة للنطاق.
- أي بيانات خارج Purpose المحدد.

## 5. سجل Subprocessors

| المزود | الغرض | البيانات | المنطقة | الاحتفاظ | الحذف | العقد/DPA | القرار |
|---|---|---|---|---|---|---|---|
| Railway | تطبيق/قاعدة بيانات | TBD | re-verify | TBD | TBD | Missing | Block |
| Vercel | Web/Functions/Logs | TBD | provider-specific | TBD | TBD | Missing | Block personal data |
| Model provider(s) | تحليل/توليد | minimized | provider-specific | TBD | TBD | Missing | Block personal prompts |
| Email provider | transactional/drafts | TBD | TBD | TBD | TBD | Missing | No live send |
| WhatsApp/BSP | consented messaging | TBD | TBD | TBD | TBD | Missing | No send |
| Moyasar | payment | payment minimum | verify | legal | verify | Missing | Checkout off |
| Analytics/error tools | reliability | minimized | verify | short | verify | Missing | No raw content |

لا يتحول `TBD` إلى قبول تلقائي.

## 6. القنوات

### WhatsApp

حسب سياسة WhatsApp Business الحالية، لا تواصل إلا إذا قدم الشخص الرقم وتم تسجيل opt-in، ويجب احترام opt-out؛ المحادثة التي يبدأها النشاط تستخدم Template معتمد، وخارج نافذة خدمة 24 ساعة يلزم Template معتمد، مع مسار تصعيد بشري: https://whatsappbusiness.com/policy/

بوابة Dealix: `no opt-in evidence = no draft/send eligibility`.

### LinkedIn

لا scraping، ولا bots، ولا رسائل/تفاعل آلي. المسموح بحث يدوي ضمن الشروط وتسجيل URL كسؤال discovery، وليس كإذن تواصل: https://www.linkedin.com/legal/user-agreement

### Email

دافئ/inbound أو مسار يعتمد المستشار فقط؛ هوية مرسل واضحة، صلة مباشرة، approval، suppression، ولا blast.

## 7. الأمن الأدنى قبل Pilot

- أقل صلاحية وحسابات منفصلة.
- Tenant/RLS test موجب وسالب.
- تشفير النقل والتخزين بحسب المزود.
- تدوير الأسرار وعدم ظهورها في Git/logs.
- Audit trail للموافقة والوصول والتغيير.
- لا PII في logs أو analytics أو error payloads.
- Backup/restore test مع تعريف الحذف من النسخ.
- Incident owner وشجرة تصعيد وقالب إخطار.
- Export/delete/suppression drill بنتيجة مرفقة.

## 8. الاحتفاظ والحذف

لكل فئة في `PILOT_DATA_FLOW_REGISTER.csv`:

- مدة وقاعدة واضحة.
- حذف عند انتهاء الغرض ما لم يوجد احتفاظ نظامي موثق.
- suppression مستقل حتى لا يعاد الاستيراد أو التواصل.
- مسار Export/Delete واختبار evidence.
- Legal hold لا يُفترض؛ يُوثق مع مالك وسبب.

## 9. ملحق Pilot مع العميل

يُرفق بالعقد:

- الغرض والنطاق والحقول.
- تعليمات العميل الموثقة.
- السرية والوصول والمقاولون الفرعيون.
- المنطقة والنقل عبر الحدود.
- الاحتفاظ والحذف والنسخ الاحتياطية.
- المساعدة في حقوق أصحاب البيانات.
- الحوادث والإخطار.
- التدقيق والأدلة.
- إعادة/حذف البيانات عند الإنهاء.
- منع استخدام البيانات لتدريب عام ما لم يعتمد صراحة.

## 10. بوابة الاعتماد

- [ ] Data-flow register مكتمل بلا TBD حرج.
- [ ] قائمة Subprocessors/regions معتمدة.
- [ ] رأي سعودي بشأن الأدوار والنقل.
- [ ] NDGP self-assessment/DPIA/DPO decision محفوظ.
- [ ] DPA وSOW موقعان.
- [ ] Tenant isolation + delete/export/suppression + breach drills ناجحة.
- [ ] Security pack يطابق البيئة الفعلية.
- [ ] موافقة Founder + Privacy + Security + Customer owner.

حتى اكتمالها: `NO_REAL_CUSTOMER_DATA`.
