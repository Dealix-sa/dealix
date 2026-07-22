# Dealix Canonical Strategy & Policy Core

## الهدف

استخراج أفضل قيمة من PRs #869 و#875—Strategy Registry، Safety Gate، Model Routing، Learning Metrics—كطبقة declarative خالصة تُستهلك من Canonical Company OS #886.

هذه الطبقة لا تحتوي:

- orchestrator؛
- daily runner؛
- GitHub workflow؛
- sender أو publisher؛
- connectors؛
- production mutation؛
- merge أو payment executor؛
- استراتيجية مفعلة افتراضيًا.

# 1. عقد Strategy YAML

كل Strategy يجب أن تحتوي:

```yaml
id: revenue_sprint
name: Revenue Sprint
goal: Prepare evidence-first commercial work.
enabled: true
priority: 80
guardrails:
  - draft_only
kpis:
  - qualified_opportunities
stop_conditions:
  - production_unhealthy
steps:
  - action: prepare_daily_brief
    kind: internal_draft
    risk: 0.10
    requires_approval: false
```

التحقق strict:

- `enabled: "false"` يقرأ False فعليًا، وليس True بسبب truthiness.
- priority من 0 إلى 100.
- risk من 0 إلى 1.
- ActionKind من allowlist واضحة.
- كل Strategy تحتاج goal وخطوة واحدة على الأقل.
- IDs مكررة تفشل.
- directory مفقود أو فارغ يفشل بدل تشغيل يوم فارغ بصمت.

# 2. Autonomy & Safety

المستويات:

- 0 Observe
- 1 Analyze
- 2 Draft
- 3 Internal Write
- 4 Repo Write عبر branch/PR/tests
- 5 External/Irreversible — غير متاح تلقائيًا في هذه الطبقة

الإجراءات التالية دائمًا Approval:

- external draft/action؛
- merge؛
- publish؛
- payment؛
- production change؛
- أي external channel؛
- risk ≥ 0.40؛
- خطوة مميزة `requires_approval=true`.

إجراءات doctrine المحظورة تُرفض:

- cold/mass broadcasts؛
- contact scraping أو شراء leads؛
- bypass consent؛
- fake proof/revenue؛
- guaranteed revenue/win؛
- government-access claim؛
- auto charge/invoice.

كل SafetyDecision يحمل `external_action_allowed=false` دائمًا. التنفيذ الخارجي يحتاج مسار موافقة منفصل، وليس flag سحري داخل Strategy.

# 3. Model Routing

الـRouter declarative ولا ينفذ network call.

Local target يصبح executable فقط إذا:

```text
ENABLE_LOCAL_LLM=true
LOCAL_LLM_HEALTHY=true
```

وجود `OLLAMA_HOST` وحده لا يثبت أن الخدمة حية.

Hosted fallback يحتاج:

```text
ALLOW_HOSTED_MODEL_FALLBACK=true
<PROVIDER>_API_KEY موجود
<PROVIDER>_MODEL محدد
```

الـRouter لا يعيد قيمة أي secret. إذا لا يوجد target مثبت، يعيد:

```text
provider=none
executable=false
```

ولا يدّعي أن Ollama متاح افتراضيًا.

# 4. Transparent Learning

Learning يحسب فقط:

- internal executed؛
- drafts prepared؛
- approvals requested؛
- approved/rejected؛
- blocked؛
- outcomes recorded؛
- approval rate؛
- block rate.

لا يغير priority أو YAML أو policy تلقائيًا. أي تغيير استراتيجية يحتاج evidence ومراجعة بشرية/PR.

# 5. ترتيب الدمج

1. #898 استعادة Railway.
2. #886 canonical runner بعد موافقة الدمج وproduction verification.
3. هذه الطبقة تُعاد rebase فوق #886.
4. Strategy YAMLs تُضاف تدريجيًا بعد تحديد المصدر والـKPI والـstop conditions.
5. لا workflow يومي جديد؛ #886 يبقى نقطة التشغيل الوحيدة.

# 6. القيمة التجارية

هذه الطبقة تمنع أربعة أخطاء مكلفة:

- استراتيجية مكتوبة `enabled: false` تعمل بالخطأ؛
- خطوة high-risk تنفذ بسبب parsing ضعيف؛
- مودل محلي يُعامل كحي بدون health evidence؛
- learning loop يرفع استراتيجية بناء على كثرة drafts بدل outcomes حقيقية.
