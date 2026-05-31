# إطار التميز في التسليم — Delivery Excellence Framework

> الغرض: تحديد المعايير التشغيلية التي تجعل كل تسليم في ديلكس قابلاً للتحقق، موثَّقاً، وقادراً على تحمل أي مراجعة. هذا الإطار يعمل جنباً إلى جنب مع [`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md).
>
> Purpose: Define the operational standards that make every Dealix delivery verifiable, documented, and audit-ready. This framework operates alongside the Sprint Delivery Playbook.
>
> وثائق ذات صلة: [`docs/07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md) | [`docs/04_data_os/SOURCE_PASSPORT.md`](../04_data_os/SOURCE_PASSPORT.md) | [`docs/05_governance_os/APPROVAL_POLICY.md`](../05_governance_os/APPROVAL_POLICY.md)

---

## 1. كتاب التشغيل اليومي لسبرنت الإيرادات — 7-Day Revenue Intelligence Sprint Playbook

### اليوم الأول — الانطلاق وجواز المصدر

**المسؤول:** المؤسس + مالك سير العمل من طرف العميل.

**الأنشطة الإلزامية:**
- مكالمة انطلاق مدتها 45 دقيقة: تعريف سير العمل المستهدف بدقة (مثال: إحياء الحسابات الخاملة).
- توثيق اسم مالك سير العمل من طرف العميل في سجل المشروع.
- إصدار معرِّف المشاركة (Engagement ID) وإنشاء المجلد.
- توقيع جواز المصدر (Source Passport): يجب أن يُحدِّد نوع المصدر (`client_upload`, `crm_export`, `manual_entry`) — مصدر `scraped` مرفوض دائماً.

**بوابة الجودة (لا تُكمِل اليوم الأول دون هذا):**
- [ ] جواز المصدر موقَّع من الطرفين.
- [ ] مالك سير العمل من طرف العميل محدَّد باسم ودور.
- [ ] سير العمل المستهدف مكتوب في جملة واحدة واضحة.
- [ ] معرِّف المشاركة مُسجَّل في سجل الإثبات.

---

### اليوم الثاني — استيراد البيانات وفحص الجودة

**الأنشطة الإلزامية:**
- قراءة عيِّنة أولية (Preview) لا تدمير بيانات.
- احتساب DQ Score عبر الأبعاد الستة: الاكتمال، الصلاحية، التفرُّد، الاتساق، الحداثة، المطابقة.
- توثيق النتيجة في سجل الإثبات.

**قواعد التصعيد:**
- DQ < 40: توقَّف. اقترح حزمة البيانات (1,500 ريال) بدلاً من الاستمرار في السبرنت. أعِد 80% من رسوم السبرنت.
- DQ 40–70: استمر مع توثيق التحفظات بوضوح في الحزمة النهائية.
- DQ ≥ 70: استمر بشكل نظيف.

**بوابة الجودة:**
- [ ] نتيجة DQ مُسجَّلة في سجل الإثبات.
- [ ] لم تُنفَّذ أي إجراءات خارجية.
- [ ] مسار التصعيد الصحيح متَّبَع بناءً على النتيجة.

---

### اليوم الثالث — ترتيب الحسابات

**الأنشطة الإلزامية:**
- تشغيل خوارزمية الترتيب على البيانات المستوردة المنقَّحة.
- مراجعة أفضل 10 نتائج: كل ترتيب يجب أن يمتلك تفسيراً مقروءاً للإنسان.
- تسجيل أي ميزة ترتيب قابلة للإعادة استخدام كأصل رأسمالي محتمل.

**بوابة الجودة:**
- [ ] كل حساب من أفضل 10 يمتلك تفسيراً مكتوباً.
- [ ] لا ترتيبات مبهمة أو غير قابلة للتفسير مُشحونة.
- [ ] سجل الإثبات: `scoring_completed = true`.

---

### اليوم الرابع — توليد المسودات والمراجعة المُحوكَمة

**الأنشطة الإلزامية:**
- توليد مسودات ثنائية اللغة (عربي + إنجليزي): 8 عربية + 4 إنجليزية على الأقل.
- تطبيق قرارات الحوكمة: `ALLOW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `RATE_LIMIT`.
- مراجعة كل قرار `BLOCK` و`REDACT` من المؤسس شخصياً.

**قاعدة غير قابلة للتفاوض:** لا تُرسَل أي رسالة من بنية تحتية ديلكس. كل مسودة مُصنَّفة `draft_only` حتى يُعطي العميل موافقته الصريحة على كل مسودة على حدة.

**بوابة الجودة:**
- [ ] سجل الإثبات: `drafts_generated`, `governance_decisions`, `blocked_count`, `redacted_count`.
- [ ] لا إرسال خارجي حدث.
- [ ] كل مسودة محمولة كـ `draft_only`.

---

### اليوم الخامس — تجميع حزمة الإثبات

**الأنشطة الإلزامية:**
- تجميع الـ 14 قسماً الإلزامية لحزمة الإثبات.
- احتساب نقاط الإثبات (Proof Score).
- إذا كان Proof Score < 70: لا تسليم. إما تمديد (دون تحميل العميل تكاليف إضافية) أو استرداد جزئي.

**بوابة الجودة:**
- [ ] 14 قسماً موجودة — لا أقسام ناقصة.
- [ ] Proof Score مُسجَّل.
- [ ] لا عناصر نائبة (Placeholders) في حزمة الإثبات.

---

### اليوم السادس — التسليم وتقييم جاهزية الاحتفاظ

**الأنشطة الإلزامية:**
- مكالمة تسليم مدتها 60 دقيقة: مراجعة حزمة الإثبات قسماً بقسماً.
- تقييم جاهزية العميل للانتقال إلى العمليات المُدارة (2,999–4,999 ريال/شهر).
- عرض الانتقال فقط عند اكتمال معايير الأهلية (Proof Score ≥ 80، Adoption Score ≥ 70، جواز المصدر قابل للتجديد).

**بوابة الجودة:**
- [ ] سجل الإثبات: `handoff_completed = true`.
- [ ] درجة تقييم الانتقال مُسجَّلة.
- [ ] القرار (عرض، تأجيل، إغلاق) موثَّق.

---

### اليوم السابع — تسجيل الأصل الرأسمالي والملخص الآمن

**الأنشطة الإلزامية:**
- تسجيل أصل رأسمالي واحد على الأقل قابل للإعادة استخدام (قاعدة ترتيب، قالب مسودة، قاعدة حوكمة، رؤية قطاعية).
- كتابة ملخص آمن مجهَّل باستخدام قالب [`docs/case-studies/`](../case-studies/).
- إغلاق سجل المشاركة بحالة `status = delivered`.

**بوابة الجودة:**
- [ ] معرِّف الأصل الرأسمالي مُسجَّل في سجل رأس المال.
- [ ] الملخص الآمن: لا اسم عميل، لا أرقام إيرادات محددة، لا مجموعات (قطاع + مدينة + حجم) تُعيد التعريف.
- [ ] حالة المشاركة `delivered`.

---

## 2. قائمة التحقق من عدم الادعاءات الزائفة — No Fake Claims Verification Checklist

### العربية

قبل شحن أي تسليم، يُوقِّع المؤسس على هذه القائمة الست:

- [ ] **مصدر البيانات موثَّق:** كل مدخل له جواز مصدر موقَّع ومصنَّف. لا بيانات من مصادر مجهولة.
- [ ] **الإثبات مُصنَّف بدقة:** كل ادعاء في التقرير مُصنَّف بوضوح كـ "مُقدَّر" أو "مُرصَد" أو "مُتحقَّق". لا ادعاء يُعلَّق في الهواء.
- [ ] **لا أرقام عائد مضمونة:** أي رقم ROI أو توفير تكاليف في التقرير مُلابَس بـ "تقديري" أو "بناءً على نمط القطاع" — لا "مضمون" أو "متوقَّع بيقين".
- [ ] **لا إرسال خارجي غير مُصرَّح به:** التحقق من سجل الحوكمة أن صفر إجراءات خارجية نُفِّذت دون موافقة العميل المسجَّلة.
- [ ] **التكافؤ الثنائي محقَّق:** القسم العربي والإنجليزي من التقرير يحملان نفس المعنى والبنية — ليس أحدهما ملخصاً للآخر.
- [ ] **بيانات PII مُتعاملة وفق PDPL:** كل حقل PII في التقرير النهائي إما مُحجَّب أو مُبرَّر بموافقة موثَّقة.

### English

This checklist is not optional. It is the minimum gate before any deliverable leaves Dealix's production environment. A sprint that passes all seven delivery days but fails this checklist is not delivered — it is returned to Day 5 for remediation.

The six items represent the operational translation of Dealix's non-negotiables into a per-engagement verification step.

---

## 3. قائمة تعامل البيانات وفق PDPL لكل سبرنت — PDPL Data Handling Checklist

### العربية

قانون حماية البيانات الشخصية السعودي (PDPL) يُلزِم بمعالجة البيانات لغرض محدد معلوم مُوافَق عليه. في كل سبرنت، يُطبَّق ما يلي:

| المرحلة | الإجراء المطلوب |
|---------|----------------|
| الاستيراد | تصنيف كل حقل: `non_pii`, `pii_low`, `pii_high` |
| المعالجة | استخدام البيانات للغرض المُعلَن في جواز المصدر فقط |
| التخزين | تشفير البيانات في حالة التخزين والنقل |
| التقارير | إزالة أو إخفاء PII من الحزمة النهائية إلا بموافقة صريحة |
| الإغلاق | حذف البيانات الخام بعد انتهاء فترة الاحتجاز المُتفَق عليها في جواز المصدر |
| الانتهاك | اتباع إجراء التبليغ خلال 72 ساعة وفق [`docs/ops/PDPL_BREACH_RUNBOOK.md`](./PDPL_BREACH_RUNBOOK.md) |

**تحديدات البيانات الشخصية عالية الحساسية (PII_HIGH):**
- الاسم الكامل مع رقم الجوال.
- الرقم الوطني أو رقم الإقامة.
- البيانات المالية المرتبطة بشخص محدد.
- البيانات الصحية.

هذه الفئة تتطلب موافقة صريحة مكتوبة من العميل قبل أي معالجة، حتى إذا كان العميل هو مُزوِّد البيانات أصلاً.

### English

PDPL compliance is not a one-time setup. It is a per-engagement verification step that runs at each stage of the sprint. The checklist above must be reviewed at Days 1, 2, and 5 specifically.

Any request from a client to process PII_HIGH data without documented consent triggers an immediate pause and a governance review before work resumes. This is a non-negotiable boundary, not a negotiating point.

---

## 4. نماذج التواصل مع العميل — Client Communication Templates

### 4.1 رسالة انطلاق السبرنت — Sprint Kickoff Message

**العربية:**

> موضوع: انطلاق سبرنت الإيرادات — [معرِّف المشاركة]
>
> مرحباً [اسم مالك سير العمل]،
>
> نُؤكِّد انطلاق سبرنت الإيرادات المُحوكَم لشركتكم. سير العمل المستهدف: [وصف سير العمل]. مدة السبرنت: 7 أيام عمل تبدأ اليوم.
>
> ستتلقون تحديثاً يومياً موجزاً يُحدِّد ما تم، ما هو قادم، وأي قرار يحتاج منكم موافقة. لن يُنفَّذ أي إجراء خارجي دون موافقتكم الصريحة.
>
> إذا طرأ تغيير على توفر البيانات أو على مالك سير العمل من طرفكم، أخبرونا فوراً — قد يؤثر ذلك على جدول التسليم.
>
> يُسعدنا بدء العمل.

**English:**

> Subject: Revenue Intelligence Sprint Kickoff — [Engagement ID]
>
> Hello [Workflow Owner Name],
>
> We confirm the start of your Governed Revenue Intelligence Sprint. Target workflow: [workflow description]. Sprint duration: 7 working days beginning today.
>
> You will receive a brief daily update specifying what ran, what is next, and any decision requiring your approval. No external action will be taken without your explicit sign-off.
>
> If your data availability or workflow owner changes, please notify us immediately — it may affect the delivery schedule.
>
> We are ready to begin.

---

### 4.2 تحديث منتصف السبرنت — Mid-Sprint Update

**العربية:**

> موضوع: تحديث اليوم [X] — سبرنت [معرِّف المشاركة]
>
> ما اكتملنا منه: [وصف مختصر لما أُنجِز — مثال: استيراد البيانات، DQ Score = 72].
>
> ما هو قادم اليوم: [وصف مختصر — مثال: ترتيب الحسابات وتوليد أفضل 10].
>
> ما يحتاج قراراً منكم: [إذا لم يوجد: "لا شيء حالياً — سنُخبركم عند الحاجة"].
>
> السبرنت على المسار الصحيح. تاريخ التسليم المتوقع: [التاريخ].

**English:**

> Subject: Day [X] Update — Sprint [Engagement ID]
>
> Completed: [brief description — e.g., data imported, DQ Score = 72].
>
> Next: [brief description — e.g., account scoring and top 10 generation].
>
> Decision needed from you: [if none: "Nothing at this time — we will inform you when needed"].
>
> Sprint is on track. Expected delivery date: [date].

---

### 4.3 رسالة التسليم النهائي — Final Delivery Message

**العربية:**

> موضوع: تسليم سبرنت الإيرادات — [معرِّف المشاركة]
>
> مرحباً [اسم مالك سير العمل]،
>
> يسعدنا إعلامكم باكتمال سبرنت الإيرادات المُحوكَم. حزمة الإثبات جاهزة وتحتوي على [عدد الأقسام] قسماً مكتملاً.
>
> ملخص ما أنجزناه:
> - DQ Score: [النتيجة] (خط أساس: [النتيجة الأولية])
> - أفضل 10 حسابات مُرتَّبة مع تفسيرات مكتوبة
> - [عدد المسودات] مسودة ثنائية اللغة جاهزة للمراجعة
> - سجل قرارات الحوكمة: [عدد القرارات] قراراً موثَّقاً
> - نقاط الإثبات: [النتيجة]
>
> جميع القيم أعلاه تقديرية. القيمة التقديرية ليست قيمة مُتحقَّقة.
>
> نقترح جلسة مراجعة مدتها 60 دقيقة لمناقشة النتائج والخطوات التالية.

**English:**

> Subject: Revenue Sprint Delivery — [Engagement ID]
>
> Hello [Workflow Owner Name],
>
> Your Governed Revenue Intelligence Sprint is complete. The Proof Pack is ready and contains [number] complete sections.
>
> Delivery summary:
> - DQ Score: [score] (baseline: [initial score])
> - Top 10 accounts ranked with written justifications
> - [number] bilingual outreach drafts ready for your review
> - Governance decision log: [number] documented decisions
> - Proof Score: [score]
>
> All figures above are estimates. Estimated value is not Verified value.
>
> We recommend a 60-minute review session to discuss findings and next steps.

---

## 5. قالب مراجعة ما بعد السبرنت — Sprint Post-Mortem Template

### العربية

يُكتَب هذا القالب خلال 48 ساعة من إغلاق المشاركة.

**معلومات أساسية:**
- معرِّف المشاركة:
- تاريخ الانطلاق / التسليم:
- الخدمة المقدَّمة:
- Proof Score النهائي:

**ما سار بشكل جيد:**
(3 نقاط على الأقل — محددة لا عامة)

**ما يمكن تحسينه:**
(3 نقاط على الأقل — مع إجراء محدد لكل نقطة)

**حوادث أثناء التسليم:**
(إن وجدت — وصف، سبب جذري، قرار الإغلاق)

**أصل رأسمالي جديد تم تسجيله:**
(معرِّف الأصل + وصف الاستخدام المحتمل)

**رسالة للمؤسس من المؤسس:**
(ما الذي يجب أن تعرفه قبل بداية السبرنت التالي؟)

### English

The post-mortem is not a performance review. It is an evidence record. The three "what can improve" items must each carry a specific next action — not a general statement. If the sprint produced a new capital asset, the post-mortem is the record that makes it findable and reusable for future engagements.

---

## 6. مصفوفة التصعيد — Escalation Matrix

### العربية

| نوع المشكلة | المُصعَّد إليه | الإجراء الأول | الإطار الزمني |
|------------|--------------|--------------|---------------|
| DQ < 40 عند اليوم 2 | المؤسس | إيقاف السبرنت، اقتراح حزمة البيانات، إعلام العميل خلال 4 ساعات | فوري |
| > 50% من المسودات محجوبة | المؤسس | مراجعة نطاق سير العمل مع العميل قبل الاستمرار | خلال 24 ساعة |
| العميل لا يستطيع تسمية مالك سير العمل | المؤسس | إيقاف السبرنت، لا فواتير من اليوم 3+، إعادة التقييم | فوري |
| طلب عميل لخدمة مرفوضة (تجريف، واتساب بارد...) | المؤسس | رفض، توثيق في سجل الحوكمة، إغلاق المشاركة، استرداد الجزء غير المكتسب | فوري |
| Proof Score < 70 عند اليوم 5 | المؤسس | تمديد أو استرداد جزئي — الخيار للعميل، التكلفة على ديلكس | خلال 24 ساعة |
| انتهاك محتمل لـ PDPL | المؤسس + مسؤول PDPL | إيقاف المعالجة، بروتوكول الانتهاك خلال 72 ساعة | فوري |
| تأخر في التسليم بسبب طاقة المؤسس | المؤسس | تمديد بدون تحميل إضافي على العميل + إعلام فوري | خلال 4 ساعات من اكتشاف التأخر |

### English

The escalation matrix defines owner and action for every failure mode. Two principles govern all escalations: first, the client is never penalized for Dealix's operational gaps; second, every escalation is logged in the engagement governance record, not handled verbally and forgotten.

---

## 7. مقاييس نجاح التسليم — Delivery Success Metrics

### العربية

تُقاس جودة التسليم عبر أربعة مقاييس رئيسية يُحتسب كل منها لكل مشاركة وتُجمَّع بشكل ربعي:

| المقياس | التعريف | الهدف |
|--------|---------|-------|
| **Proof Score** | نقاط حزمة الإثبات من 100 | ≥ 80 |
| **درجة رضا العميل (CSAT)** | تقييم العميل للتسليم (0–10) | ≥ 8 |
| **التسليم في الوقت المحدد** | نسبة المشاركات المُسلَّمة في 7 أيام أو أقل | ≥ 90% |
| **معدل تسجيل الأصول الرأسمالية** | نسبة المشاركات التي سجَّلت أصلاً رأسمالياً | 100% |

درجة جودة التسليم الإجمالية تُحسَب ربعياً وتُقارَن مع البيانات السابقة. أي تراجع في Proof Score المتوسط بأكثر من 5 نقاط يستدعي مراجعة تشغيلية فورية.

### English

Delivery quality is not a trailing metric. It is tracked per engagement and surfaced in the quarterly founder review. The 100% capital asset registration requirement is intentional: every engagement must produce something reusable — if it does not, the sprint produced a transaction, not an investment in Dealix's compounding capability.

---

> **القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**

---

*آخر مراجعة: 2026-05-31 | Last reviewed: 2026-05-31*
*يُقرأ جنباً إلى جنب مع: [`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [`docs/07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md)*
