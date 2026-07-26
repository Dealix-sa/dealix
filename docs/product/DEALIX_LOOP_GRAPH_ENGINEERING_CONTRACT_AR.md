# عقد Loop + Graph Engineering داخل Dealix

## الهدف

تحويل مهام Dealix من طلبات منفردة إلى نظام تشغيل يتحسن مع كل دورة، مع إبقاء الحالة والقرارات والصلاحيات والأدلة ضمن بنية صريحة قابلة للمراجعة.

هذا العقد لا يضيف runtime جديدًا. إنه يحدد كيف تستخدم طبقات Dealix الحالية حلقات تنفيذ bounded ورسوم علاقات evidence-backed، بغض النظر عن الموديل المستخدم: Kimi أو Codex أو Claude أو GLM أو موديل محلي.

---

## 1. الرسم القانوني Company Graph

العقد الأساسي:

```text
Tenant
→ Company Brain
→ Goal / Strategy
→ Company / Contact / Signal
→ Opportunity
→ Action
→ Owner / Agent
→ Draft
→ Approval
→ Controlled Execution
→ Outcome Event
→ Proof Event
→ Learning Event
→ Playbook Version
```

### قواعد العقد

- كل node له `id` ثابت وtenant ownership واضح.
- كل edge له سبب ومصدر ووقت إنشاء.
- لا تُشتق مرحلة فرصة أو حالة إيراد من النص الحر وحده.
- كل claim مهم يحمل evidence أو يُوسم كـhypothesis.
- كل node حساس يلتزم data classification والاحتفاظ والحذف.
- لا يوجد node باسم مختلف يكرر كيانًا قانونيًا موجودًا.

### العلاقات المطلوبة

```text
Goal owns Opportunity intent
Opportunity selects Action
Action has one accountable owner
Draft belongs to Action
Approval gates external Action
Outcome records what actually happened
Proof links Outcome to evidence
Learning changes a future rule only after evidence
```

---

## 2. حلقة التنفيذ القانونية Execution Loop

```text
Observe
→ Normalize
→ Prioritize
→ Plan
→ Draft / Internal Execute
→ Safety Check
→ Approval Gate
→ Controlled Execute
→ Measure Outcome
→ Record Proof
→ Learn
→ Improve Playbook
→ Observe again
```

### Observe

يقرأ فقط من مصادر مصرح بها، مع timestamps وsource identity وconfidence.

### Normalize

يحول المدخلات إلى كيانات Dealix القانونية بدل تمرير نصوص غير منظمة بين agents.

### Prioritize

يستخدم أثر العمل، الاستعجال، الثقة، قابلية إعادة الاستخدام، إزالة البلوكر، الجهد، والمخاطر.

### Plan

ينتج خطوات محدودة وdefinition of done وverification وstop conditions.

### Draft / Internal Execute

ينفذ الآمن داخليًا، ويجهز الخارجي في Approval Queue.

### Safety Check

يتحقق من الصلاحية، tenant boundary، القناة، claims، البيانات الحساسة، budget، ووجود evidence.

### Approval Gate

الإرسال والنشر والدفع والدمج وتغيير production لا تتجاوز البوابة دون موافقة action-specific.

### Controlled Execute

ينفذ connector أو operator الإجراء الموافق عليه فقط، مع idempotency key وaudit metadata.

### Measure Outcome

يسجل النتيجة الواقعية، لا النتيجة المتوقعة.

### Record Proof

يربط الحدث بدليل قابل للمراجعة دون secrets أو بيانات زائدة.

### Learn

يولّد hypothesis أو improvement proposal. لا يعتبر pattern متعلمًا من عينة صغيرة دون وسم confidence.

### Improve Playbook

التغيير الداخلي منخفض المخاطر يمكن تجربته bounded. السعر والسياسة والرسائل الخارجية والإنتاج تحتاج موافقة.

---

## 3. ما يملكه الكود وما يملكه الموديل

### deterministic code يملك

- routing.
- permission checks.
- tenant isolation.
- budgets and limits.
- idempotency.
- state transitions.
- evidence requirements.
- approval enforcement.
- retries and stop conditions.
- audit and proof writes.

### LLM يملك فقط

- classification مع confidence.
- reasoning proposals.
- summaries.
- draft generation.
- option comparison.
- root-cause hypotheses.
- recommended next action.

الموديل لا يملك سلطة ضمنية على الإرسال أو الدفع أو production أو حذف البيانات.

---

## 4. حدود كل حلقة

كل loop يجب أن يحدد:

```text
loop_id
objective
owner
tenant_id
inputs
allowed_actions
blocked_actions
max_steps
max_retries
timeout
cost_budget
token_budget
approval_required_for
success_metric
stop_conditions
proof_required
```

الافتراض الافتراضي:

- `max_retries`: محدود.
- لا loop recursive غير محدد.
- لا agent يعيد تفويض المهمة لنفسه عبر دورة غير مرئية.
- كل إعادة محاولة تسجل السبب.
- الوصول للحد يوقف الحلقة ويصدر blocker report.

---

## 5. منع runaway agents

يجب إيقاف الحلقة عند:

- تكرار نفس action fingerprint.
- تجاوز budget أو timeout.
- انخفاض confidence تحت الحد.
- نقص required evidence.
- رفض approval.
- conflict مع policy.
- connector error متكرر.
- tenant mismatch.
- طلب secret أو صلاحية غير متاحة.
- محاولة external action غير معتمدة.

لا يُسمح للموديل بتوسيع scope أو إنشاء صلاحيات جديدة لتجاوز التوقف.

---

## 6. Proof وLearning

كل دورة تنتج على الأقل:

```text
Action Plan
Action/Approval Queue
Outcome Events
Proof Events
Failure/Blocker Report
Learning Notes
Next-cycle recommendation
```

### قاعدة التعلم

```text
Observation ≠ Fact
Fact ≠ Causal proof
One result ≠ Stable pattern
Draft improvement ≠ Approved playbook
```

تُحفظ:

- العينة.
- الظروف.
- القناة.
- النسخة المستخدمة.
- النتيجة.
- confidence.
- ما تغير بعد التجربة.

---

## 7. تطبيقه على الإيراد

```text
Company Brain
→ real/warm target
→ signal
→ opportunity score
→ offer match
→ outreach draft
→ approval
→ controlled/manual send
→ reply/meeting/proposal event
→ payment evidence
→ delivery evidence
→ Proof Pack
→ expansion or stop decision
```

لا revenue state من:

- رسالة جاهزة.
- invoice draft.
- test checkout.
- verbal intent.
- payment يخص شركة مختلفة.
- proof يخص فرصة مختلفة.

---

## 8. تطبيقه على الهندسة

```text
CI/log signal
→ failure classification
→ root-cause hypothesis
→ smallest patch
→ focused test
→ broader verification
→ Draft PR
→ review outcome
→ regression rule
```

لا تُضعف assertions لمجرد الحصول على green check، ولا تُغيّر production قبل proof محلي/CI وموافقة محددة.

---

## 9. تطبيقه على واجهة Company Command

واجهة `/{tenant}/command` هي view فوق الرسم والحلقة، وليست مصدر الحقيقة.

تعرض:

- ماذا يحدث الآن.
- ما الذي يحتاج قرارًا.
- ما الحركات المتاحة.
- ما آخر outcome/activity.

ولا تقوم بـ:

- simulation لنتائج العميل.
- إنشاء revenue أو success metrics.
- إرسال أو نشر أو دفع.
- تشغيل local CLI من المتصفح.
- تغيير state خارج APIs القانونية.

---

## 10. دور Kimi K3

Kimi يمكن أن يعمل كـreasoning/coding adapter ضمن نفس العقد:

- تحليل المهمة.
- اقتراح decomposition.
- كتابة patch أو draft.
- critique/evaluation.
- تلخيص outcome.

لكنه لا يصبح:

- قاعدة بيانات الشركة.
- Approval Center.
- Proof Ledger.
- مصدر الهوية والصلاحيات.
- runtime وحيدًا لا يمكن استبداله.

الهدف هو provider-neutral Company OS: يمكن استبدال الموديل دون فقدان حالة الشركة أو evidence أو governance.

---

## 11. معايير النجاح

يُعتبر Loop + Graph صالحًا عندما:

- يمكن تتبع كل قرار مهم إلى node وedge ودليل.
- rerun لا يكرر external action.
- إيقاف الموديل لا يفقد حالة الشركة.
- تغيير provider لا يغيّر الصلاحيات.
- كل external action يظهر في Approval Queue.
- كل outcome مهم يظهر في Proof Ledger.
- كل تحسين يوضح الدليل والنسخة السابقة والجديدة.
- التقارير لا تعرض بيانات محاكاة كحقيقة.

هذا العقد هو المرجع قبل إضافة أي agent أو workflow أو memory أو graph أو command surface جديد داخل Dealix.
