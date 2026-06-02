# Job Signal Playbook — دليل إشارات التوظيف

> جزء من: Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
>
> **الجمهور:** المؤسس + فريق العمليات.
> **الفكرة:** الشركة التي تنشر وظيفة في عمليات المبيعات أو إدارة CRM أو الدعم أو النمو، تكشف — علناً — عن احتياج تشغيلي قابل للمطابقة مع عرض من عروض Dealix.
> **المصدر:** إعلانات وظائف منشورة علناً، تُراجَع يدوياً، وكل تواصل يحتاج موافقة المؤسس. لا كشط، لا أتمتة.
> مراجع: [reports/signals/JOB_SIGNAL_REPORT.md](../../reports/signals/JOB_SIGNAL_REPORT.md) · المخطط: [schemas/job_signal.schema.json](../../schemas/job_signal.schema.json) · [docs/content/CONTENT_ENGINE_AR.md](../content/CONTENT_ENGINE_AR.md)

---

## لماذا إشارة التوظيف ذات قيمة — Why a hiring post is a signal

حين تفتح شركة وظيفة، فهي تُقرّ بأمرين: أن العمل الحالي يفوق الطاقة الحالية، وأن الميزانية متاحة. الوظيفة المنشورة ليست بياناً شخصياً، بل إعلان تجاري عام عن نيّة. هذه النية أصدق من أي قائمة مشتراة، لأن الشركة هي من نشرها بنفسها.

الإشارة لا تعني فرصة مؤكَّدة. تعني سياقاً يستحق رسالة واحدة، مكتوبة بعناية، بموافقة المؤسس. القيمة التقديرية للإشارة ليست قيمة مُتحقَّقة حتى يردّ الطرف الآخر.

When a company opens a role, it admits two things: current work exceeds current capacity, and budget exists. A public job post is a commercial declaration of intent, not personal data. It is more honest than any purchased list because the company published it itself. A signal is context for one careful message — not a confirmed opportunity.

---

## الحدود الأخلاقية — Hard boundaries (non-negotiable)

- **المصدر علني فقط.** الإعلان منشور على لوحة وظائف عامة. لا نصل إلى أي مصدر مغلق.
- **مراجعة يدوية.** يقرأ إنساناً كل إشارة قبل أن تدخل التقرير. لا التقاط آلي.
- **موافقة لكل تواصل.** لا رسالة تخرج باسم Dealix أو باسم العميل دون اعتماد المؤسس المُسجَّل.
- **لا كشط، لا LinkedIn automation، لا قوائم مشتراة، لا واتساب بارد آلي.** هذه خطوط حمراء ثابتة في عقيدة Dealix.
- **رسالة واحدة، لا حملة.** الإشارة تبرّر تواصلاً واحداً ذا صلة، لا تتابعاً ضاغطاً.

Source is public only. A human reads every signal before it enters the report. No message leaves under the Dealix or client name without logged founder approval. No scraping, no LinkedIn automation, no purchased lists, no automated cold WhatsApp. One relevant message, never a campaign.

---

## جدول المطابقة — Role → pain → offer

| الوظيفة المنشورة / Posted role | الألم المُرجَّح / Likely pain | عرض Dealix / Matched offer |
|---|---|---|
| Sales Operations / عمليات المبيعات | بيانات حسابات مبعثرة، لا منهجية أولوية، تقارير يدوية | **Revenue OS Starter** — درجة جودة، حسابات مُرتَّبة، سجل قرارات |
| CRM Manager / مدير CRM | تكرارات، حقول ناقصة، قُمع غير نظيف | **CRM / Funnel Cleanup** — دمج، تطبيع، خريطة قُمع |
| Marketing Coordinator / منسّق تسويق | حملات بلا متابعة، تسريب عملاء بين القنوات | **Campaign Follow-up Workflow** — مسودات متابعة محوكَمة |
| Customer Support / دعم العملاء | ردود متأخرة، نبرة غير متسقة، لا مكتبة جاهزة | **Support Draft OS** — مسودات ردود تُراجَع قبل الإرسال |
| Growth Manager / مدير النمو | تجارب بلا تصميم، لا معيار خروج، لا توثيق | **Growth Experiment OS** — هيكل تجربة + معيار خروج مكتوب |

كل صف يربط ملاحظة علنية بألم متكرر بعرض من السلّم القانوني. العرض الأول دائماً منخفض الالتزام: تشخيص مجاني (0) ثم سبرنت ذكاء الإيرادات (499). لا قفز مباشر إلى عقد شهري.

Each row maps a public observation to a recurring pain to a ladder offer. The first offer is always low-commitment: Free Diagnostic (0), then Revenue Intelligence Sprint (499). No leap straight to a retainer.

---

## السلّم المرجعي — Reference ladder

التشخيص المجاني (0) · سبرنت ذكاء الإيرادات (499؛ بريميوم 3,500–15,000) · حزمة البيانات إلى الإيراد (1,500) · عمليات إيراد مُدارة (2,999–4,999/شهر) · إعداد ذكاء اصطناعي مخصّص (5,000–25,000) · مراجعة حوكمة المؤسسات (25,000–50,000).

العروض الخمسة في الجدول أعلاه كلها أبواب دخول تنتهي عند التشخيص المجاني أو السبرنت. الترقية إلى ما بعدهما تحتاج إثباتاً مُسلَّماً، لا وعداً.

---

## قالب رسالة الزاوية — The angle message template

تُرسَل بعد موافقة المؤسس فقط، ومرة واحدة، وبصياغة بشرية تُعدَّل لكل حالة:

> «لاحظت أنكم تبحثون عن [role]. غالبًا هذا يعني احتياج في [CRM/follow-up/reporting]. Dealix لا يستبدل الشخص، لكنه يجهّز operational layer يساعده يشتغل أسرع من أول يوم.»

ثم خطوة تالية واضحة: «إذا رغبتم، نبدأ بتشخيص مجاني خلال 24 ساعة — صفحتان، باعتماد المؤسس، ولا التزام بعده.»

نبرة القالب: ملاحظة محترمة، لا ادعاء معرفة داخلية. لا «سمعنا من مديركم»، لا وعد بصفقات، لا إلحاح. الرسالة تفتح باباً، والتشخيص هو الخطوة التالية.

Sent only after founder approval, once, and rephrased per case. The tone is a respectful observation — never a claim of inside knowledge, never "we heard from your manager," never a deal promise. The message opens a door; the Free Diagnostic is the next step.

---

## دورة العمل — The operating loop

1. **رصد علني** — مراجعة يدوية لإعلانات منشورة ذات صلة بالقطاعات المستهدفة.
2. **تسجيل** — إدخال الإشارة وفق [schemas/job_signal.schema.json](../../schemas/job_signal.schema.json): الشركة، الوظيفة، الألم المُرجَّح، العرض المُطابَق، الحالة.
3. **مطابقة** — اختيار العرض من الجدول، وكتابة مسودة رسالة زاوية بشرية.
4. **بوابة الموافقة** — يراجع المؤسس الإشارة والمسودة. القرار: اعتماد / تعديل / رفض، مُسجَّل بالوقت.
5. **تواصل واحد** — رسالة واحدة فقط بعد الاعتماد. لا تتابع آلي.
6. **توثيق النتيجة** — تُحدَّث الحالة في [reports/signals/JOB_SIGNAL_REPORT.md](../../reports/signals/JOB_SIGNAL_REPORT.md)، وتُحوَّل الأنماط المتكرّرة إلى محتوى عبر [docs/content/CONTENT_ENGINE_AR.md](../content/CONTENT_ENGINE_AR.md).

كل خطوة قابلة للتدقيق. كل تواصل له صاحب قرار مُسمّى. كل إشارة لها خطوة تالية محدّدة.

Observe publicly, log per schema, match an offer, pass the founder approval gate, send one message, document the outcome. Every step is auditable; every outreach has a named decision owner; every signal has a defined next step.

---

## ما الذي لا نفعله — What this is not

- ليس قائمة مبيعات تُشترى أو تُكشط.
- ليس تتابعاً مؤتمتاً عبر LinkedIn automation أو واتساب.
- ليس ادعاء أن الإشارة تساوي صفقة.
- ليس إرسالاً نيابة عن العميل دون موافقته الصريحة.

This is not a purchased or scraped list, not automated follow-up over LinkedIn automation or WhatsApp, not a claim that a signal equals a deal, and not sending on a client's behalf without explicit approval.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.**
