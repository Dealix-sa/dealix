# Dealix — التنسيق وسلّم الاستقلالية · Orchestration & Autonomy Ladder

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `AUTONOMOUS_OPS_ARCHITECTURE.md` · `AGENT_ROSTER.md` · `AGENT_GOVERNANCE_AND_GUARDRAILS.md` · `../launch/MACHINE_ORCHESTRATION_MAP.md` · `../COMMERCIAL_WIRING_MAP.md`

---

## الغرض · Purpose

تعرّف هذه الوثيقة بدقة سلّم الاستقلالية الذي يحكم كل وكيل في الهرم، وتشرح كيف يفوّض المنسّق التنفيذي للأسفل، وكيف يصبح كل فعل خارجي طلب موافقة، وكيف تعمل حواجز وقت التشغيل (runtime). تصمّم الوثيقة المعمار فقط؛ التجميد التجاري نشط ولا يُؤذَن ببناء كود منتج جديد.

This document defines precisely the autonomy ladder governing every agent in the pyramid, how the Executive Orchestrator delegates downward, how every external action becomes an approval request, and how runtime safety operates. It designs architecture only; the Commercial Freeze is active.

---

## سلّم الاستقلالية · The Autonomy Ladder

الوحدة `agent_os/autonomy_levels.py` تعرّف `AutonomyLevel` كـ `IntEnum`. كل وكيل يحمل مستوى واحدًا، والمستوى يحدّد أقصى ما يجوز للوكيل فعله — لا أكثر.

`agent_os/autonomy_levels.py` defines `AutonomyLevel` as an `IntEnum`. Each agent carries one level; the level caps what the agent may do — never more.

| المستوى · Level | القيمة · Value | التعريف الدقيق · Precise definition |
|---|---|---|
| `L0_READ_ONLY` | 0 | قراءة فقط. الوكيل يقرأ بيانات ولا ينتج مخرجًا قابلًا للتنفيذ ولا يكتب حالة. · Reads data only; produces no actionable output, writes no state. |
| `L1_ANALYZE` | 1 | تحليل. الوكيل يقرأ ويحسب درجات/أنماط/توصيفات داخلية. لا صياغة موجَّهة لإنسان، لا فعل. · Reads and computes internal scores, patterns, classifications. No human-facing drafts, no action. |
| `L2_DRAFT` | 2 | صياغة مسودة. الوكيل ينتج مسودة موجَّهة لإنسان (بريد، نص، مقترح) — مسودة فقط، لا تُرسَل. · Produces a human-facing draft (email, script, proposal). Draft only; never sent. |
| `L3_RECOMMEND` | 3 | توصية. الوكيل يصدر قرارًا موصى به مع مبرّر (`RoleDecision`) ويرتّب الأولويات. القرار يبقى معلّقًا لموافقة. · Issues a recommended decision with rationale; ranks priorities. The decision stays pending approval. |
| `L4_AUTO_WITH_AUDIT` | 4 | تلقائي مع تدقيق — **للأفعال الداخلية المدقَّقة فقط**. الوكيل ينفّذ فعلًا داخليًا (تحديث CRM، فهرسة) ويسجّله في التدقيق. **لا يشمل أبدًا إرسالًا أو شحنًا خارجيًا.** · Auto-with-audit — **internal, audited actions only**. The agent executes an internal action (CRM write, indexing) and logs it. **Never includes an external send or charge.** |
| `L5_FULLY_AUTONOMOUS` | 5 | استقلال كامل بلا موافقة. · Fully autonomous, no approval. |

### السقف · The ceiling

الثابت `MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. لا وكيل يُسجَّل فوق L4. **`L5_FULLY_AUTONOMOUS` محظور** — موجود في الـ`IntEnum` كقيمة معرّفة فقط، ولا يُسنَد لأي وكيل. أي محاولة تسجيل وكيل على L5 تُرفض عند `register_agent()`.

`MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. No agent is registered above L4. **`L5_FULLY_AUTONOMOUS` is blocked** — it exists in the `IntEnum` as a defined value only and is assigned to no agent. Any attempt to register an L5 agent is rejected at `register_agent()`.

### الفرق الجوهري عند L4 · The critical distinction at L4

L4 يربك القراءة السطحية، فليكن صريحًا: **L4 يعني الاستقلالية على الأفعال الداخلية المدقَّقة فقط** — كتابة سجل CRM، بناء فهرس متجهات، تحديث حالة داخلية. كل واحد من هذه يُسجَّل في التدقيق (`no_unaudited_changes`). **L4 لا يعني أبدًا إرسالًا أو شحنًا خارجيًا.** أي بريد أو WhatsApp أو LinkedIn أو مكالمة أو تحصيل — مهما كان مستوى الوكيل — يبقى محكومًا بالموافقة عبر `ApprovalStore`.

L4 invites a shallow misreading, so state it plainly: **L4 means autonomy on internal, audited actions only** — a CRM write, a vector index build, an internal state update. Each is logged for audit (`no_unaudited_changes`). **L4 never means an external send or charge.** Any email, WhatsApp, LinkedIn, call, or charge — regardless of the agent's level — stays approval-gated through `ApprovalStore`.

في السجل الحالي وكيلان فقط على L4: `CRMAgent` و`embedding_index` — كلاهما داخلي بالكامل. التوزيع الكامل في [`AGENT_ROSTER.md`](AGENT_ROSTER.md).

In the current roster only two agents sit at L4: `CRMAgent` and `embedding_index` — both fully internal. Full distribution in [`AGENT_ROSTER.md`](AGENT_ROSTER.md).

---

## تدفّق التنسيق · Orchestration Flow

التنسيق ينحدر للأسفل عبر ثلاث طبقات، ثم كل فعل خارجي يصعد عبر صندوق الموافقة.

Orchestration flows downward across three tiers, then every external action rises back through the approval center.

```
   كرون · cron                Tier 1                 Tier 2                Tier 3
   ┌──────────────┐    ┌────────────────────┐   ┌──────────────┐   ┌──────────────────┐
   │ daily_lead_  │───▶│ Executive          │──▶│ role agents  │──▶│ task agents +    │
   │ prep.yml     │    │ Orchestrator       │   │ ×7 RoleBrief │   │ run_agent_job    │
   │ weekly_brief │    │ role_command_os    │   │              │   │ ARQ jobs         │
   │ monthly_     │    │ RoleName.CEO       │   │ GROWTH drives│   │                  │
   │ cadence      │    │                    │   │ Growth-      │   │ produce drafts / │
   │ daily-       │    │ sets priorities,   │   │ Orchestrator │   │ scores / reports │
   │ revenue-     │    │ delegates,         │   │              │   │                  │
   │ machine.yml  │    │ composes queue     │   │              │   │                  │
   └──────────────┘    └────────────────────┘   └──────────────┘   └────────┬─────────┘
                                                                            │
   ┌────────────────────────────────────────────────────────────────────────┘
   │  every external action  ▼
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  ApprovalStore — ApprovalRequest (one of 11 action_types, action_mode)    │
   │  founder: approve / reject / edit   ·   WhatsApp/LinkedIn/phone never auto │
   └──────────────────────────────────────────────────────────────────────────┘
```

### من التنفيذي إلى المهام · From executive to task

1. **المنسّق التنفيذي · Executive Orchestrator** — مدعوم بـ`role_command_os` (`RoleName.CEO`) و`/api/v1/founder/beast-command-center`. يقرأ حالة العمل، يضع أولويات اليوم، ويفوّض إلى وكلاء الأدوار السبعة.
2. **وكلاء الأدوار · Role agents** — كل دور يصدر `RoleBrief` عبر `build_role_brief(role)`. دور `RoleName.GROWTH` إضافيًا يشغّل `GrowthOrchestrator.run_sector_campaign()`.
3. **وكلاء المهام · Task agents** — وكلاء الأدوار يفوّضون لوكلاء المهام (`auto_client_acquisition/agents/`، `autonomous_growth/agents/`) ووظائف ARQ في `core/queue/tasks.py` عبر `run_agent_job()`: `lead_score`, `proposal_draft`, `outreach_batch`, `embedding_index`, `commercial_sprint_report`.
4. **الصعود · The rise back** — مخرجات وكلاء المهام (مسودات، درجات، تقارير) ترتفع: الداخلي يُسجَّل، والخارجي يصفّ في `ApprovalStore`، ثم يركّب المنسّق التنفيذي طابور قرارات المؤسس.

### المُطلِقات المجدولة · Scheduled triggers

كرون GitHub Actions يطلق الهرم بإيقاع يومي/أسبوعي/شهري. كل المخرجات مسودات أو تقارير — لا فعل خارجي بلا موافقة. الخريطة الكاملة في [`../launch/MACHINE_ORCHESTRATION_MAP.md`](../launch/MACHINE_ORCHESTRATION_MAP.md).

| المكينة · Machine | الإيقاع · Cadence | ما تطلقه في الهرم · What it triggers |
|---|---|---|
| `daily-revenue-machine.yml` | يوميًا · daily | تشغيل كامل للهرم — مسودات Tier 3 تصفّ في `approval_center` |
| `daily_lead_prep.yml` | يوميًا 03:30 UTC | تحضير leads — **مسودات فقط (drafts only)** عبر وكلاء الاستقبال والتهديف |
| `weekly_brief.yml` | الأحد 03:00 UTC | موجز أسبوعي لكل العملاء النشطين — يجمّع `RoleBrief` من Tier 2 |
| `monthly_cadence.yml` | أول الشهر 03:00 UTC | إيقاع شهري + جدولة تجديدات — يحرّك دور FINANCE وCS |

The cron workflows trigger the pyramid on a daily/weekly/monthly rhythm. All outputs are drafts or reports; no external action runs without approval.

---

## توجيه الموافقات · Approval Routing

كل فعل خارجي — بلا استثناء — يصبح `ApprovalRequest` في `auto_client_acquisition/approval_center/` عبر `ApprovalStore`. لا قناة تتجاوزه.

Every external action — without exception — becomes an `ApprovalRequest` in `auto_client_acquisition/approval_center/` via `ApprovalStore`. No channel bypasses it.

### الأنواع القانونية الأحد عشر · The 11 canonical action_types

`prepare_diagnostic` · `draft_email` · `draft_linkedin_manual` · `call_script` · `follow_up_task` · `support_reply_draft` · `payment_reminder` · `delivery_task` · `proof_request` · `upsell_recommendation` · `partner_intro`.

### أوضاع الفعل · action_mode

`draft_only` (مسودة لا تُنفَّذ) · `approval_required` (تنتظر قرار المؤسس) · `approved_execute` (وافق المؤسس، جاهز للتنفيذ اليدوي) · `blocked` (محظور بالحدود أو الحوكمة).

### دورة الحياة · Lifecycle

1. وكيل Tier 3 ينتج مخرجًا خارجيًا → ينشئ `ApprovalRequest` بحالة `ApprovalStatus.PENDING`.
2. المؤسس يراجع عبر `GET /api/v1/approvals/pending` ثم `ApprovalStore` يدعم: **approve / reject / edit** (مع `list_pending` و`list_history`).
3. الحالات: `PENDING` → `APPROVED` أو `REJECTED` أو `EXPIRED`؛ أو `BLOCKED` إذا منعته الحوكمة أو الحدود الأربعة.
4. **WhatsApp / LinkedIn / الهاتف لا تُوافَق تلقائيًا أبدًا** — تتطلب موافقة صريحة من المؤسس في كل مرة (`no_live_send`, `no_cold_whatsapp`). حتى بعد الموافقة، التنفيذ يدوي ولا يرسله الوكيل نيابةً عن العميل بلا موافقة صريحة.

The founder reviews pending requests and approves, rejects, or edits. WhatsApp, LinkedIn, and phone never auto-approve; each needs explicit founder approval every time, and execution stays manual.

| الحالة · `ApprovalStatus` | المعنى · Meaning |
|---|---|
| `PENDING` | بانتظار قرار المؤسس · awaiting founder decision |
| `APPROVED` | وافق المؤسس · founder approved |
| `REJECTED` | رفض المؤسس · founder rejected |
| `EXPIRED` | انتهت صلاحية الطلب بلا قرار · request expired without decision |
| `BLOCKED` | منعته الحوكمة أو الحدود الأربعة · blocked by governance or the 4 boundaries |

---

## سلامة وقت التشغيل · Runtime Safety

الوحدة `auto_client_acquisition/secure_agent_runtime_os/` تحكم سلامة كل وكيل أثناء التشغيل عبر الحدود الأربعة (`four_boundaries.py`): `check_prompt_integrity()`, `check_tool_boundary()`, `check_data_boundary()`, `check_context_boundary()` — كل واحدة تُعيد `BoundaryCheck` (`boundary`, `allowed`, `reason`). أي حدّ يفشل يوقف الوكيل ويصعّد.

`auto_client_acquisition/secure_agent_runtime_os/` governs each agent's runtime safety through the four boundaries; any failed boundary halts the agent and escalates.

### حالات وقت التشغيل · RuntimeState transitions

`RuntimeState` StrEnum: `SAFE` · `WATCH` · `RESTRICTED` · `ESCALATED` · `PAUSED` · `KILLED`.

```
   SAFE ──انحراف بسيط · minor drift──▶ WATCH
   WATCH ──تكرار · recurrence──▶ RESTRICTED ──تصعيد · escalation──▶ ESCALATED
   ESCALATED ──قرار المؤسس · founder decision──▶ PAUSED  أو · or  KILLED
   أي حالة · any state ──activate_kill_switch()──▶ KILLED
```

- **`SAFE`** — التشغيل الطبيعي؛ كل الحدود تمرّ.
- **`WATCH`** — انحراف بسيط مرصود؛ مراقبة مشدّدة.
- **`RESTRICTED`** — صلاحيات الوكيل مقيّدة؛ أفعال أقل مسموحة.
- **`ESCALATED`** — رُفع للمؤسس لقرار.
- **`PAUSED`** — موقوف مؤقتًا، قابل للاستئناف.
- **`KILLED`** — أُوقف نهائيًا.

### مفتاح الإيقاف · The kill switch

`activate_kill_switch()` يوقف وكيلًا أو الهرم بالكامل فورًا؛ `kill_switch_active()` يفحص الحالة. كل وكيل له `kill_switch_owner` في بطاقته (`AgentCard`) — وهو Sami (founder) لكل الوكلاء في السجل الحالي. عند الإيقاف، تنتقل حالة الوكيل في `agent_os` إلى `AgentStatus.KILLED` مع `killed_reason`، ولا يصفّ الوكيل أي فعل جديد. هذا يضمن `no_unbounded_agents`.

`activate_kill_switch()` halts an agent or the whole pyramid immediately; `kill_switch_active()` checks state. Every agent has a `kill_switch_owner` in its `AgentCard`. On kill, the agent's `AgentStatus` becomes `KILLED` with a `killed_reason` and queues nothing further.

### حلقات النشر · Deployment rings

`DeploymentRing` StrEnum: `DEV` · `STAGING` · `PRODUCTION`. لا وكيل يصل `PRODUCTION` قبل المرور بـ`DEV` ثم `STAGING`. الترقية تتطلب اجتياز الحدود الأربعة في كل حلقة، وموافقة المؤسس على الانتقال. هذا يحافظ على `no_unaudited_changes` و`no_silent_failures`.

```
   DEV ──اجتياز الحدود الأربعة · 4 boundaries pass──▶ STAGING
   STAGING ──موافقة المؤسس · founder approval──▶ PRODUCTION
```

No agent reaches `PRODUCTION` without passing through `DEV` then `STAGING`; promotion requires the four boundaries to pass at each ring plus founder approval.

---

## الربط بالحوكمة · Tie to Governance

سلّم الاستقلالية وحده لا يكفي — يعمل فوق عمود الحوكمة العرضي: هوية `AgentCard`، الحدود الأربعة، مفتاح الإيقاف، وتوجيه `ApprovalStore`. القواعد الكاملة للحواجز في [`AGENT_GOVERNANCE_AND_GUARDRAILS.md`](AGENT_GOVERNANCE_AND_GUARDRAILS.md)، والمعمار الكامل في [`AUTONOMOUS_OPS_ARCHITECTURE.md`](AUTONOMOUS_OPS_ARCHITECTURE.md)، وخريطة المكاين المجدولة في [`../launch/MACHINE_ORCHESTRATION_MAP.md`](../launch/MACHINE_ORCHESTRATION_MAP.md).

The ladder alone is not enough; it runs atop the cross-cutting governance spine. Full guardrail rules in [`AGENT_GOVERNANCE_AND_GUARDRAILS.md`](AGENT_GOVERNANCE_AND_GUARDRAILS.md).

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
