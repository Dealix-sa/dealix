# عملية طلب الميزات والتغذية الراجعة للمنتج — Feature Request and Product Feedback Process

> **الغرض / Purpose:** تحديد كيفية تقديم العملاء لطلبات الميزات، ومعايير تقييمها، ومسار اتخاذ القرار من التقديم إلى التسليم أو الرفض المُبرَّر.
>
> Define how clients submit feature requests, how those requests are evaluated, and the decision path from submission to delivery or reasoned rejection.
>
> **مرجع متقاطع / Cross-references:** [FEATURE_PRIORITIZATION.md](./FEATURE_PRIORITIZATION.md) · [FEATURE_BACKLOG.md](./FEATURE_BACKLOG.md) · [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) · [SPRINT_DELIVERY_CHECKLIST.md](../ops/SPRINT_DELIVERY_CHECKLIST.md)

---

## كيف يُقدِّم العملاء طلبات الميزات — How Clients Submit Feature Requests

قناة التقديم المعتمدة الوحيدة هي مدير نجاح العميل (CSM) أو المراجعة الشهرية المجدولة.
The only approved submission channel is the CSM or the scheduled monthly review.

**القنوات المعتمدة / Approved channels:**
- مدير نجاح العميل خلال أي تواصل مُجدوَل. / CSM during any scheduled communication.
- قسم التغذية الراجعة للمنتج في المراجعة الشهرية للصحة (انظر: قسم حلقات التغذية الراجعة). / The product feedback section of the monthly health review (see: Feedback Loops section).

**القنوات غير المعتمدة / Channels not accepted:**
- مشكلات GitHub المباشرة (Issues) من جانب العملاء الخارجيين. / Direct GitHub Issues from external clients.
- رسائل صوتية عبر WhatsApp. / WhatsApp voice messages.
- رسائل WhatsApp النصية خارج التواصل المجدوَل. / WhatsApp text messages outside scheduled communication.
- البريد الإلكتروني غير الرسمي. / Informal email without a structured template.

**السبب:** الطلبات غير المُوثَّقة لا تُقيَّم بعدالة ولا تُتابَع بدقة. القناة الرسمية تضمن أن كل طلب يدخل مسار التقييم الموحَّد.
**Reason:** Undocumented requests cannot be evaluated fairly or tracked accurately. A formal channel ensures every request enters the standardised evaluation path.

---

## معايير تقييم الميزة — Feature Evaluation Criteria

كل طلب ميزة يُقيَّم على أربعة معايير قبل دخوله قائمة الانتظار.
Every feature request is evaluated against four criteria before entering the backlog.

**المعيار الأول: الانتشار / Criterion 1 — Reach**
هل الميزة تخدم 3 عملاء أو أكثر بحالة استخدام موثَّقة؟ الميزة التي تخدم عميلاً واحداً هي تخصيص، لا منتج — وتخضع لمسار العقد المخصص (Custom AI).
Does the feature serve 3 or more clients with a documented use case? A feature serving one client is a customisation, not a product — it follows the Custom AI contract path.

**المعيار الثاني: توافق المعمارية / Criterion 2 — Architecture Alignment**
هل الميزة متوافقة مع مبدأ APPROVAL_FIRST؟ أي ميزة تُتيح إجراءات خارجية تلقائية بدون موافقة مُسجَّلة لا تدخل قائمة الانتظار.
Is the feature consistent with the APPROVAL_FIRST architecture? Any feature that enables automated external actions without a logged approval does not enter the backlog.

**المعيار الثالث: الامتثال / Criterion 3 — Compliance**
هل الميزة متوافقة مع ZATCA المرحلة الثانية و PDPL؟ الامتثال شرط لا مقايضة.
Is the feature compatible with ZATCA Phase 2 and PDPL? Compliance is a requirement, not a trade-off.

**المعيار الرابع: قيمة حزمة الإثبات / Criterion 4 — Proof Pack Value**
هل الميزة تُنتج قيمة قابلة للقياس تُضاف لحزمة الإثبات؟ الميزات الجمالية البحتة التي لا تُنتج أدلة قابلة للتدقيق تُؤجَّل.
Does the feature generate measurable value that contributes to the Proof Pack? Purely cosmetic features that produce no auditable evidence are deferred.

---

## مصفوفة الأولوية — Prioritization Matrix

| | **جهد منخفض / Low Effort** | **جهد مرتفع / High Effort** |
|---|---|---|
| **تأثير مرتفع / High Impact** | **فوز سريع / Quick Win** — ابنِ الآن / Build now | **استراتيجي / Strategic** — جدوِل في الخارطة الزمنية / Schedule on roadmap |
| **تأثير منخفض / Low Impact** | **تكملة / Fill-in** — افعل عند توافر السعة / Do when capacity allows | **تجنَّب / Avoid** — لا تبنِ ما لم يتغير الوضع / Do not build unless conditions change |

يُضاف عامل "انتشار الميزة عبر 3+ عملاء" كمُعامِل تصحيح: ميزة ذات تأثير متوسط ولكنها تخدم 5 عملاء تتقدم على ميزة عالية التأثير لعميل واحد.
The "3+ client reach" factor applies as a correction multiplier: a medium-impact feature serving 5 clients advances ahead of a high-impact feature for a single client.

---

## مسار العملية — Process (5 Steps)

**الخطوة 1: التقديم / Step 1 — Submit**
يُقدِّم العميل الطلب لمدير نجاح العميل أو في المراجعة الشهرية. المدير يوثّق الطلب بالمعلومات الإلزامية: الميزة المطلوبة، حالة الاستخدام، عدد المستخدمين المتأثرين، الأثر التجاري المتوقَّع (تقديري).
Client submits the request to the CSM or during the monthly review. The CSM documents it with required fields: requested feature, use case, affected user count, estimated business impact.

**الخطوة 2: التقييم / Step 2 — Evaluate**
يُقيَّم الطلب على المعايير الأربعة وتُحسَب درجة الأولوية (انظر: [FEATURE_PRIORITIZATION.md](./FEATURE_PRIORITIZATION.md)). الدرجة 80+ بناء فوري؛ 60–79 في قائمة الانتظار؛ أقل من 60 لا يُبنى.
Request evaluated against the four criteria and a prioritization score calculated (see: [FEATURE_PRIORITIZATION.md](./FEATURE_PRIORITIZATION.md)). Score 80+: build now; 60–79: backlog; below 60: do not build.

**الخطوة 3: الخارطة الزمنية أو الرفض / Step 3 — Roadmap or Reject**
الطلبات التي تجتاز التقييم تُضاف لخارطة الطريق الفصلية. الطلبات المرفوضة تُوثَّق بسبب واضح محدد، لا عبارة مبهمة.
Requests passing evaluation are added to the quarterly roadmap. Rejected requests are documented with a specific, clear reason — not a vague phrase.

**الخطوة 4: إشعار العميل / Step 4 — Notify Client**
يتلقى العميل ردوداً على طلبه في غضون 5 أيام عمل (تقديري). الرد يتضمن: هل دخل الطلب قائمة الانتظار؟ الربع الزمني المتوقَّع (تقديري، لا ملزِم)؟ أم رُفض مع السبب؟
Client receives a response within 5 business days (estimated). The response includes: did the request enter the backlog? The estimated quarter (estimated, not binding)? Or was it rejected and with what reason?

**الخطوة 5: التسليم وإضافة لحزمة الإثبات / Step 5 — Deliver + Proof Pack**
عند تسليم الميزة، تُضاف القيمة المقيسة (قبل وبعد) لحزمة إثبات العميل ذات الصلة. لا يُدَّعى تأثير الميزة قبل وجود بيانات مقيسة.
When the feature is delivered, the measured value (before and after) is added to the relevant client's Proof Pack. No feature impact is claimed before measured data exists.

---

## ما تلتزم به Dealix — What Dealix Commits To

- الردّ على كل طلب ميزة في غضون 5 أيام عمل (تقديري). / Acknowledge every feature request within 5 business days (estimated).
- تحديث خارطة الطريق الفصلية وإشعار العملاء المعنيين. / Quarterly roadmap update with notification to relevant clients.
- "لا" صريحة عند عدم التوافق — بدون صياغة مبهمة أو تأجيل غير محدد. / An honest "no" when a request is not aligned — without vague phrasing or indefinite deferral.
- توثيق سبب رفض الطلب في السجل حتى يمكن مراجعته إذا تغيّرت الظروف. / Documentation of every rejection reason in the record so it can be revisited if conditions change.

---

## ما لا تلتزم به Dealix — What Dealix Does NOT Commit To

- **أي تاريخ إطلاق محدد** بدون موافقة صريحة مُسجَّلة من المؤسس وفق مبدأ APPROVAL_FIRST. / **Any specific release date** without explicit logged founder approval per APPROVAL_FIRST.
- **ميزات مخصصة** بدون عقد Custom AI موقَّع (Tier 5: 5,000–25,000 ريال). التخصيص خارج نطاق الخطط المعيارية. / **Custom features** without a signed Custom AI contract (Tier 5: 5,000–25,000 SAR). Customisation is outside standard plan scope.
- **أولوية الطلبات** بناءً على حجم العميل أو مدة العلاقة وحدهما. الأولوية تحكمها المعايير الأربعة، لا الضغط. / **Request priority** based solely on client size or tenure. Priority is governed by the four criteria, not by pressure.
- **إتمام طلبات** تتعارض مع مبادئ الحوكمة أو متطلبات الامتثال بصرف النظر عن أهميتها التجارية. / **Fulfilling requests** that conflict with governance principles or compliance requirements regardless of their commercial importance.

---

## حلقات التغذية الراجعة — Feedback Loops

**المراجعة الشهرية للصحة / Monthly Health Review**
كل مراجعة شهرية تتضمن قسماً ثابتاً للتغذية الراجعة على المنتج يشمل:
Every monthly health review includes a standing product feedback section covering:

- ما الذي يعمل بشكل جيد في المنتج الحالي؟ / What is working well in the current product?
- ما الذي يسبب احتكاكاً في سير العمل اليومي؟ / What is causing friction in daily workflows?
- هل هناك طلبات ميزات جديدة للتسجيل في هذا الشهر؟ / Are there new feature requests to register this month?

ملاحظات هذا القسم تُحفَظ في سجل المشاريع وتُغذّي تقييم [FEATURE_BACKLOG.md](./FEATURE_BACKLOG.md) كل ربع سنة.
Notes from this section are stored in the engagement record and feed the quarterly [FEATURE_BACKLOG.md](./FEATURE_BACKLOG.md) review.

**الأنماط المتكررة / Recurring Patterns**
إذا ظهر طلب ميزة من 3+ عملاء في ربع واحد، يُعامَل تلقائياً كمرشح ذو أولوية عالية في الخارطة الزمنية القادمة.
If a feature request appears from 3+ clients in one quarter, it is automatically treated as a high-priority candidate for the next roadmap cycle.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
