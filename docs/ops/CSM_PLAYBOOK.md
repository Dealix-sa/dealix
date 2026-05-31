# كتيب مدير نجاح العملاء | Customer Success Manager Playbook

> **الغرض:** الدليل التشغيلي الكامل لمدير نجاح العملاء (CSM) في ديلكس، من الإعداد إلى التجديد.
> **Purpose:** Complete operational guide for the Dealix CSM, from onboarding to renewal.
>
> وثائق ذات صلة: [`docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md`](./CUSTOMER_ONBOARDING_DAY_BY_DAY.md) | [`docs/legal/SLA_TEMPLATE.md`](../legal/SLA_TEMPLATE.md) | [`docs/07_proof_os/PROOF_OS.md`](../07_proof_os/PROOF_OS.md) | [`docs/05_governance_os/APPROVAL_POLICY.md`](../05_governance_os/APPROVAL_POLICY.md)

---

## 1. مهمة مدير نجاح العملاء | CSM Mission

مهمة الـ CSM ثلاثية وغير قابلة للتفاوض:

The CSM mission is threefold and non-negotiable:

1. **حماية صافي معدل الاحتفاظ بالإيرادات (NRR):** لا يغادر عميل بسبب خدمة يمكن إصلاحها. Protect Net Revenue Retention (NRR): no client leaves due to a correctable service failure.
2. **قيادة التوسع:** كل عميل في مستوى يمكنه الانتقال إلى المستوى الأعلى هو فرصة توسع، وليس مجرد تجديد. Drive expansion: every client eligible for the next tier is an expansion opportunity, not just a renewal.
3. **تحويل العملاء إلى مدافعين عن Proof Pack:** العميل الذي يفهم ويستشهد بقيمه الموثَّقة هو أقوى أداة مبيعات. Make clients Proof Pack champions: a client who understands and cites their documented value is the strongest sales tool.

الـ CSM لا يعد بنتائج لم تُتحقَّق. كل رقم يُقدَّم للعميل يُصنَّف صراحةً كـ "مُقدَّر" أو "مُرصَد" أو "مُتحقَّق" وفق منهجية [`docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

The CSM does not promise unverified results. Every metric presented to a client is explicitly classified as "estimated", "observed", or "verified" per the value methodology.

---

## 2. مراحل دورة حياة العميل | Client Lifecycle Stages

| المرحلة | Stage | المحفز | Trigger | الهدف | Goal |
|---------|-------|--------|---------|-------|------|
| الإعداد | Onboarding | الدفع الأول | First payment | إكمال الإعداد التقني وتسليم جواز المصدر | Complete technical setup and Source Passport |
| التفعيل | Activation | أول تقرير مُسلَّم | First report delivered | 80% من مؤشرات الصحة خضراء خلال 30 يوماً | 80% of health indicators green within 30 days |
| النمو | Growth | درجة الصحة ≥ 75 | Health score ≥ 75 | مناقشة ترقية المستوى | Initiate tier upgrade conversation |
| التجديد | Renewal | 90 يوماً قبل الانتهاء | 90 days before expiry | تأكيد الاستمرار أو التفاوض على مستوى جديد | Confirm continuation or negotiate new tier |
| المناصرة | Advocacy | درجة الصحة ≥ 85 + NPS ≥ 8 | Health score ≥ 85 + NPS ≥ 8 | طلب شهادة أو إحالة موثَّقة | Request testimonial or documented referral |

---

## 3. جدول التواصل الشهري | Monthly Touchpoint Cadence

### الأسبوع الأول — مراجعة الصحة | Week 1 — Health Review

- استدعاء `client_health_ops` API لمراجعة درجة الصحة الحالية ومكوناتها.
- Call `client_health_ops` API to review current health score and its components.
- مراجعة DQ Score للعميل: هل تدهورت جودة البيانات منذ آخر إيداع؟
- Review client DQ Score: has data quality declined since last submission?
- تسجيل الملاحظات في سجل نظام العملاء (`client_os`) مع تاريخ المراجعة.
- Log observations in the client system record (`client_os`) with review date.
- إجراء اتصال مدته 15 دقيقة لتأكيد الأولويات التشغيلية للعميل هذا الشهر.
- Conduct a 15-minute call to confirm client's operational priorities for the month.

### الأسبوع الثاني — مراجعة التسليم وتحديث Proof Pack | Week 2 — Delivery Review + Proof Pack Update

- مراجعة جميع المخرجات المُسلَّمة في الفترة السابقة: هل اكتملت؟ هل التزمت بـ SLA؟
- Review all deliverables from the prior period: complete? SLA-compliant?
- تحديث Proof Pack بأي مقاييس مرصودة أو مُتحقَّقة جديدة.
- Update Proof Pack with any new observed or verified metrics.
- إرسال ملخص Proof Pack المُحدَّث للعميل. لا تُرسَل أرقام بدون تصنيف واضح.
- Send updated Proof Pack summary to client. No figures sent without explicit classification.
- توثيق أي اعتراض أو سؤال من العميل في سجل الحالة.
- Document any client objection or question in the case record.

### الأسبوع الثالث — محادثة التوسع (إن كانت درجة الصحة ≥ 75) | Week 3 — Expansion Conversation (if health ≥ 75)

- إذا كانت درجة الصحة ≥ 75: تُفتح محادثة التوسع (انظر القسم 6 أدناه).
- If health score ≥ 75: open expansion conversation (see Section 6 below).
- إذا كانت درجة الصحة < 75: تُعطى الأولوية لخطة الاسترداد (انظر القسم 7 أدناه).
- If health score < 75: prioritize recovery plan (see Section 7 below).
- توثيق نتيجة المحادثة: مهتم / بحاجة لمزيد من الوقت / غير مهتم حالياً.
- Document conversation outcome: interested / needs more time / not interested currently.

### الأسبوع الرابع — التحضير للتجديد (إن كان التجديد خلال 90 يوماً) | Week 4 — Renewal Preparation (if within 90 days)

- إذا كان تاريخ انتهاء العقد خلال ≤ 90 يوماً: يبدأ إجراء التجديد.
- If contract end date is ≤ 90 days away: initiate renewal procedure.
- إعداد ملخص قيمة التجديد: مجموع الأنشطة، المقاييس المُتحقَّقة، مقترح المستوى القادم.
- Prepare renewal value summary: total activities, verified metrics, proposed next tier.
- إرسال مسودة عرض التجديد للمؤسس للمراجعة قبل تقديمه للعميل. [يتطلب موافقة المؤسس]
- Send renewal proposal draft to Founder for review before client presentation. [Founder approval required]

---

## 4. محفزات التصعيد الفوري للمؤسس | Immediate Escalation Triggers to Founder

يجب إبلاغ المؤسس **فوراً** عند حدوث أي من الحالات التالية:

The Founder must be notified **immediately** upon any of the following:

| الحالة | Condition | الإجراء الفوري | Immediate Action |
|--------|-----------|----------------|------------------|
| درجة الصحة < 60 | Health score drops below 60 | تفعيل خطة الاسترداد (قسم 7) + إشعار المؤسس | Activate recovery plan (Section 7) + notify Founder |
| العميل يغيب عن جلستَي متابعة متتاليتَين | Client misses 2 consecutive check-ins | الاتصال المباشر + إبلاغ المؤسس في نفس اليوم | Direct contact attempt + same-day Founder notification |
| NPS < 7 | NPS score below 7 | مكالمة استرداد خلال 24 ساعة + إبلاغ المؤسس | Recovery call within 24 hours + Founder notification |
| إشارة إلغاء الاشتراك | Cancellation signal detected | تجميد أي إجراء توسع + تصعيد فوري للمؤسس | Freeze any expansion actions + immediate Founder escalation |

إشارات الإلغاء تشمل: طلب تصدير البيانات، عدم تجديد بيانات الدفع، رسائل مباشرة تُعبِّر عن عدم الرضا، أو غياب متكرر.

Cancellation signals include: data export request, payment method not renewed, direct messages expressing dissatisfaction, or repeated absence.

---

## 5. إجراء تسليم Proof Pack | Proof Pack Delivery SOP

**الخطوة 1 — التحقق من جاهزية البيانات**
تأكد من أن جميع مصادر البيانات المستخدمة في الفترة مُوثَّقة في جواز المصدر وأن DQ Score ≥ 40.

**Step 1 — Verify Data Readiness**
Confirm all data sources used in the period are documented in the Source Passport and DQ Score ≥ 40.

**الخطوة 2 — تصنيف المقاييس**
صنِّف كل مقياس صراحةً: مُقدَّر / مُرصَد / مُتحقَّق. لا مقياس يُرسَل بدون تصنيف.

**Step 2 — Classify Metrics**
Classify every metric explicitly: estimated / observed / verified. No metric is sent without classification.

**الخطوة 3 — توليد تقرير Proof Pack**
استخدم نقطة API `/api/v1/proof-pack/{engagement_id}/generate` لإنتاج التقرير الرسمي.

**Step 3 — Generate Proof Pack Report**
Use API endpoint `/api/v1/proof-pack/{engagement_id}/generate` to produce the formal report.

**الخطوة 4 — مراجعة المؤسس**
أرسل مسودة التقرير للمؤسس للمراجعة قبل تسليمه للعميل. [يتطلب موافقة المؤسس]

**Step 4 — Founder Review**
Send report draft to Founder before client delivery. [Founder approval required]

**الخطوة 5 — التسليم والتوثيق**
أرسل التقرير النهائي عبر القناة المُعتمَدة. سجِّل الإرسال في سجل التدقيق مع: التاريخ، اسم المرسِل، القناة، نسخة الملف.

**Step 5 — Delivery and Documentation**
Send final report via approved channel. Log delivery in the audit record with: date, sender name, channel, file version.

---

## 6. نص محادثة التوسع | Expansion Conversation Script

### النوع 1: من السبرنت إلى حزمة البيانات | Type 1: Sprint → Data Pack

**العربية:** "بناءً على تقرير السبرنت، رصدنا أن جودة بياناتكم الحالية في {X}%، وهناك {N} قطاع بيانات يحتاج تعميقاً. حزمة البيانات بـ 1,500 ريال تُتيح لنا تدقيقاً شاملاً يُحوِّل هذه البيانات إلى أصل قابل للاستخدام المتكرر. هل تودّون الاطلاع على نطاق العمل؟"

**English:** "Based on the Sprint report, we observed your current data quality at {X}%, with {N} data segments requiring deeper structuring. The 1,500 SAR Data Pack provides a full audit that converts these datasets into a reusable asset. Would you like to review the scope?"

### النوع 2: من حزمة البيانات إلى العمليات المُدارة | Type 2: Data Pack → Managed Ops

**العربية:** "حزمة البيانات أنجزت تدقيق الجودة. النتائج تُظهر {N} فرصاً مُرصَدة في {القطاع}. العمليات المُدارة بـ {2,999–4,999} ريال/شهر تُمكِّننا من متابعة هذه الفرص منهجياً مع حوكمة كاملة وتقارير شهرية. هل نعرض الخيارات؟"

**English:** "The Data Pack completed the quality audit. Results show {N} observed opportunities in {sector}. Managed Ops at {2,999–4,999} SAR/month enables systematic follow-through on these opportunities with full governance and monthly reporting. Shall we present options?"

### النوع 3: من العمليات المُدارة إلى الحلول المخصصة | Type 3: Managed Ops → Custom AI

**العربية:** "بعد {N} أشهر من العمليات المُدارة، تجاوزنا معاً ما يمكن للإطار القياسي تغطيته. فرصكم في {المجال} تستوجب وكيلاً مخصصاً وتكاملات مباشرة مع {النظام}. الحلول المخصصة تبدأ من 5,000 ريال. هل نُجدوِل جلسة تصميم؟"

**English:** "After {N} months of Managed Ops, we have collectively reached what the standard framework can cover. Your opportunity in {domain} warrants a custom agent and direct integrations with {system}. Custom AI starts at 5,000 SAR. Shall we schedule a design session?"

---

## 7. إطار استرداد العميل المعرَّض للخطر | At-Risk Client Recovery Framework

**المشغِّل | Trigger:** درجة الصحة < 60، أو أي محفز تصعيد من القسم 4 / Health score < 60, or any escalation trigger from Section 4.

**المرحلة 1 (أيام 1–7) — التشخيص | Phase 1 (Days 1–7) — Diagnosis**
- مكالمة تشخيصية استثنائية مع العميل (مُعدّة مسبقاً، لا ارتجال). Diagnostic call with client (prepared, not improvised).
- تحديد المشكلة الجذرية: تقني / توقعات / تغيير في الأولويات / ضعف تسليم. Identify root cause: technical / expectations / priority shift / weak delivery.
- تسجيل نتائج المكالمة في سجل الحالة وإبلاغ المؤسس. Log call findings in case record and notify Founder.

**المرحلة 2 (أيام 8–21) — الإجراء | Phase 2 (Days 8–21) — Action**
- وضع خطة إصلاح مكتوبة وموافَق عليها من المؤسس. Develop written remediation plan approved by Founder.
- تسليم مكيَّف: تعديل المخرجات المتبقية لتعالج المشكلة المُحدَّدة. Adapted delivery: adjust remaining deliverables to address identified issue.
- تواصل مرتفع التكرار: مكالمة أسبوعية لا أقل. High-frequency contact: weekly call minimum.

**المرحلة 3 (أيام 22–30) — التقييم | Phase 3 (Days 22–30) — Assessment**
- مراجعة درجة الصحة: هل تحسنت إلى ≥ 65؟ Review health score: improved to ≥ 65?
- نعم: استئناف الإيقاع الطبيعي مع ملاحظة الحالة في السجل. Yes: resume normal cadence with case noted in record.
- لا: تصعيد للمؤسس مع خيارات: تعديل شروط العقد، أو إنهاء مُتفاوَق عليه. No: escalate to Founder with options: contract terms adjustment, or negotiated exit.

---

## 8. المؤشرات الرئيسية لأداء الـ CSM | CSM-Owned KPIs

| المؤشر | KPI | التعريف | Definition | الهدف | Target |
|--------|-----|----------|------------|-------|--------|
| NRR % | NRR % | الإيرادات المتكررة الصافية بعد الفقدان والتوسع | Net recurring revenue after churn and expansion | ≥ 110% | ≥ 110% |
| متوسط درجة الصحة | Avg Health Score | متوسط درجات الصحة عبر المحفظة | Average health scores across portfolio | ≥ 75 | ≥ 75 |
| معدل تسليم Proof Pack | Proof Pack Delivery Rate | % تقارير Proof Pack مُسلَّمة في الموعد | % of Proof Pack reports delivered on time | ≥ 95% | ≥ 95% |
| إيرادات التوسع | Expansion Revenue | الإيرادات الإضافية من ترقية المستوى | Additional revenue from tier upgrades | [Founder review required] | [Founder review required] |

تُراجَع هذه المؤشرات أسبوعياً مع المؤسس. يُسجَّل كل انحراف > 5% في سجل قرارات الحوكمة.

These KPIs are reviewed weekly with the Founder. Any deviation > 5% is logged in the governance decision record.

---

## 9. الأدوات | Tools

| الأداة | Tool | الاستخدام | Use |
|--------|------|-----------|-----|
| `subscription_ops` API | `subscription_ops` API | إدارة الاشتراكات، تغيير المستوى، تحديث حالة العقد | Manage subscriptions, tier changes, contract status updates |
| `client_health_ops` API | `client_health_ops` API | قراءة وكتابة درجات الصحة ومكوناتها | Read and write health scores and their components |
| `onboarding_ops` API | `onboarding_ops` API | متابعة مراحل الإعداد، تأكيد إتمام الخطوات | Track onboarding stages, confirm step completion |
| `/api/v1/proof-pack/{eid}/generate` | `/api/v1/proof-pack/{eid}/generate` | توليد تقرير Proof Pack الرسمي | Generate the formal Proof Pack report |
| `/api/v1/customer-success-os/{handle}/health` | `/api/v1/customer-success-os/{handle}/health` | عرض لوحة صحة العميل الكاملة | Display full client health dashboard |

جميع الإجراءات الخارجية (إرسال تقارير، تعديل عقود، تواصل مع العميل) تخضع لسياسة APPROVAL_FIRST. لا يُرسَل أي محتوى خارجي بدون توثيق الموافقة.

All external actions (sending reports, modifying contracts, client communication) are subject to the APPROVAL_FIRST policy. No external content is sent without documented approval.

---

> **القيمة التقديرية ليست قيمة مُتحقَّقة**
> Estimated value is not Verified value.

---

*آخر مراجعة: 2026-05-31 | Last reviewed: 2026-05-31*
