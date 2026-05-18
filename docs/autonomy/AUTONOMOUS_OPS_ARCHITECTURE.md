# Dealix — معمار العمليات الذاتية · Autonomous Operations Architecture

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `AGENT_ROSTER.md` · `ORCHESTRATION_AND_AUTONOMY_LADDER.md` · `../launch/MACHINE_ORCHESTRATION_MAP.md` · `../COMMERCIAL_WIRING_MAP.md`

---

## الغرض · Purpose

هذه الوثيقة تصف الهرم الكامل من الوكلاء (agent pyramid) الذي يدير عمليات Dealix بشكل ذاتي — لكنه **محكوم بالموافقة عند كل حدّ خارجي**. المكاين تُحضّر وتحلّل وتسجّل وتصفّ؛ المؤسس يوافق على كل إرسال أو شحن. لا توجد قناة تتجاوز صندوق الموافقة.

This document describes the complete agent pyramid that runs Dealix operations autonomously — yet **approval-gated at every external boundary**. The machines prepare, analyze, score, and queue; the founder approves every send or charge. No channel bypasses the approval center.

**تجميد تجاري نشط (Commercial Freeze):** هذه الوثيقة **تصمّم** المعمار — لا تأذن ببناء كود منتج جديد. الأولوية هي البيع وإنهاء تسليم Tier 0–1 وأول Pilot مدفوع.
This document **designs** the architecture — it does not authorize new product code. Priority remains selling and closing the first paid pilot.

---

## الهرم · The Pyramid

ثلاث طبقات فوق عمود حوكمة عرضي. كل طبقة تفوّض للأسفل، وكل وكيل يمرّ بنفس عمود الحوكمة.
Three tiers above one cross-cutting governance spine. Each tier delegates downward; every agent passes the same spine.

```
                    ┌─────────────────────────────────────┐
       TIER 1       │      Executive Orchestrator          │
       تنفيذي       │  role_command_os · RoleName.CEO      │
                    │  /api/v1/founder/beast-command-center│
                    └───────────────────┬─────────────────┘
                                        │ delegates / يفوّض
        ┌───────────┬───────────┬───────┴───┬───────────┬───────────┐
   TIER 2  ┌────────┴──┐ ┌──────┴──┐ ┌──────┴──┐ ┌──────┴──┐ ┌──────┴──┐ ┌──────────┐
   وظيفي   │  CEO role │ │  SALES  │ │ GROWTH  │ │PARTNER- │ │   CS    │ │ FINANCE  │ ...
           │  agent    │ │  agent  │ │  agent  │ │  SHIP   │ │  agent  │ │  agent   │ COMPLIANCE
           └────────┬──┘ └────┬────┘ └────┬────┘ └─────────┘ └─────────┘ └──────────┘
                    │         │           │ drives GrowthOrchestrator
        ┌───────────┴─────────┴───────────┴───────────────────────────────┐
   TIER 3                          Task Agents — the doers                 │
   تنفيذ   IntakeAgent · ICPMatcherAgent · PainExtractorAgent ·            │
           QualificationAgent · BookingAgent · CRMAgent · ProposalAgent ·  │
           OutreachAgent · FollowUpAgent                                   │
           SectorIntelAgent · MarketResearchAgent · ContentCreatorAgent ·  │
           DistributionAgent · CompetitorMonitorAgent                      │
           ARQ run_agent_job: lead_score · proposal_draft · outreach_batch │
           · embedding_index · commercial_sprint_report                    │
        └───────────────────────────────────────────────────────────────┘
   ════════════════════════════════════════════════════════════════════════
   GOVERNANCE SPINE — عمود الحوكمة (cross-cutting / عرضي)
   AgentCard identity · 4 boundaries · kill switch · AutonomyLevel · ApprovalStore
```

### Tier 1 — الطبقة التنفيذية · Executive layer

منسّق تنفيذي واحد (Executive Orchestrator). مدعوم بـ`role_command_os` عبر `RoleName.CEO` وواجهة `/api/v1/founder/beast-command-center`. يضع الأولويات اليومية، يفوّض إلى Tier 2، ويركّب طابور قرارات المؤسس.
One Executive Orchestrator, backed by `role_command_os` (`RoleName.CEO`) and `/api/v1/founder/beast-command-center`. It sets daily priorities, delegates to Tier 2, and composes the founder decision queue.

### Tier 2 — الوكلاء الوظيفيون / وكلاء الأدوار · Functional / role agents

سبعة وكلاء، واحد لكل `RoleName`: CEO · SALES · GROWTH · PARTNERSHIP · CUSTOMER_SUCCESS · FINANCE · COMPLIANCE. كل واحد يصدر `RoleBrief` عبر `build_role_brief(role)`. دور GROWTH يقود إضافيًا `GrowthOrchestrator`.
Seven agents, one per `RoleName`. Each emits a `RoleBrief` via `build_role_brief(role)`. The GROWTH role additionally drives `GrowthOrchestrator`.

### Tier 3 — وكلاء المهام (المنفّذون) · Task agents (the doers)

أصناف `auto_client_acquisition/agents/` التسعة + أصناف `autonomous_growth/agents/` الخمسة + وظائف ARQ الخمس في `run_agent_job`. كل واحد ضيّق، أحادي المهمة، ومحدود.
The nine `auto_client_acquisition/agents/` classes + five `autonomous_growth/agents/` classes + the five ARQ `run_agent_job` jobs. Each is narrow, single-task, and bounded.

### عمود الحوكمة · The governance spine

عرضي على كل الطبقات. كل وكيل: له هوية `AgentCard` (no_unbounded_agents)؛ يمرّ بالحدود الأربعة؛ له `kill_switch_owner`؛ له `AutonomyLevel`؛ ويوجّه كل فعل خارجي عبر `ApprovalStore`.
Cross-cutting across all tiers. Every agent has an `AgentCard` identity, passes the 4 boundaries, has a `kill_switch_owner`, an `AutonomyLevel`, and routes external actions through `ApprovalStore`.

---

## المبدأ الجوهري · The Core Principle

**استقلالية في التحضير، موافقة بشرية على الفعل الخارجي.** الأتمتة في Dealix تعني أن المكينة تنفّذ 100% من التحضير والتحليل والصياغة والتسجيل والجدولة والمراقبة. لكن كل فعل خارجي — إرسال أو شحن — يصفّ في `ApprovalStore` وينتظر موافقة المؤسس. الأتمتة = تحضير + صفّ، وليست إرسالًا مجدولًا.

**Autonomy of preparation, human approval of external action.** Automation at Dealix means the machine does 100% of preparation, analysis, drafting, scoring, scheduling, and monitoring. Every external action — a send or a charge — queues into `ApprovalStore` and waits for founder approval. Automation = preparation + queuing, never scheduled sending.

هذا ما يُبقي القائمة غير القابلة للتفاوض سليمة: `no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_scraping`, `no_fake_proof`, `no_unconsented_data`, `no_unverified_outcomes`, `no_hidden_pricing`, `no_silent_failures`, `no_unbounded_agents`, `no_unaudited_changes`.

---

## جدول ربط الوحدات · Module Mapping Table

| المكوّن · Component | الطبقة · Tier | الوحدة الحقيقية المُسنِدة · Real backing module(s) |
|---|---|---|
| Executive Orchestrator | 1 | `auto_client_acquisition/role_command_os/` (`RoleName.CEO`, `build_role_brief`) · `/api/v1/founder/beast-command-center` |
| Role agents (×7) | 2 | `role_command_os/` — `RoleBrief`, `RoleDecision`, `RoleName` StrEnum |
| GROWTH role driver | 2 | `autonomous_growth/orchestrator.py` — `GrowthOrchestrator.run_sector_campaign()` |
| Acquisition task agents (×9) | 3 | `auto_client_acquisition/agents/` — `IntakeAgent`, `ICPMatcherAgent`, `PainExtractorAgent`, `QualificationAgent`, `BookingAgent`, `CRMAgent`, `ProposalAgent`, `OutreachAgent`, `FollowUpAgent` |
| Growth task agents (×5) | 3 | `autonomous_growth/agents/` — `SectorIntelAgent`, `MarketResearchAgent`, `ContentCreatorAgent`, `DistributionAgent`, `CompetitorMonitorAgent` |
| Background jobs (×5) | 3 | `core/queue/tasks.py` — `run_agent_job()`: `lead_score`, `proposal_draft`, `outreach_batch`, `embedding_index`, `commercial_sprint_report` |
| Agent identity | spine | `auto_client_acquisition/agent_os/` — `AgentCard`, `AgentStatus`, `register_agent`, `get_agent`, `list_agents`, `kill_agent` |
| Runtime safety | spine | `auto_client_acquisition/secure_agent_runtime_os/four_boundaries.py` — `check_prompt_integrity`, `check_tool_boundary`, `check_data_boundary`, `check_context_boundary`; `RuntimeState`, `DeploymentRing`, `activate_kill_switch`, `kill_switch_active` |
| Autonomy ceiling | spine | `agent_os/autonomy_levels.py` — `AutonomyLevel`, `MAX_AUTONOMY_LEVEL_MVP` |
| Approval routing | spine | `auto_client_acquisition/approval_center/` — `ApprovalStore`, `ApprovalStatus`, 11 `action_type`s |

وحدات OS مرافقة مستخدمة عرضيًا: `data_os`, `governance_os`, `proof_os`, `value_os`, `capital_os`, `adoption_os`, `client_os`, `sales_os`, `agentic_operations_os`, `agent_identity_access_os`.

---

## سلّم الاستقلالية · The Autonomy Ladder

الوحدة `agent_os/autonomy_levels.py` تعرّف `AutonomyLevel` كـ `IntEnum`:

| المستوى · Level | المعنى · Meaning |
|---|---|
| `L0_READ_ONLY` = 0 | قراءة فقط · read only |
| `L1_ANALYZE` = 1 | تحليل · analyze |
| `L2_DRAFT` = 2 | صياغة مسودة · draft |
| `L3_RECOMMEND` = 3 | توصية · recommend |
| `L4_AUTO_WITH_AUDIT` = 4 | تلقائي مع تدقيق — **للأفعال الداخلية فقط** · auto-with-audit, **internal actions only** |
| `L5_FULLY_AUTONOMOUS` = 5 | **محظور** · **blocked** |

الثابت `MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. **L5 محظور.** L4 يعني الاستقلالية على الأفعال الداخلية المدقَّقة فقط؛ أي إرسال أو شحن خارجي يبقى محكومًا بالموافقة. التفصيل الكامل في [`ORCHESTRATION_AND_AUTONOMY_LADDER.md`](ORCHESTRATION_AND_AUTONOMY_LADDER.md).

`MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. **L5 is blocked.** L4 means autonomy on internal, audited actions only; any external send or charge stays approval-gated. Full detail in [`ORCHESTRATION_AND_AUTONOMY_LADDER.md`](ORCHESTRATION_AND_AUTONOMY_LADDER.md).

---

## ما ليس عليه الهرم · What the Pyramid Is NOT

- **ليس مُرسِلًا تلقائيًا.** لا يرسل بريدًا ولا WhatsApp ولا LinkedIn ولا يجري مكالمات بلا موافقة صريحة في كل مرة. · Not an auto-sender.
- **ليس وكلاء بلا حدود.** كل وكيل له `AgentCard` و`kill_switch_owner` و`allowed_tools` معرّفة (no_unbounded_agents). · Not unbounded agents.
- **ليس L5.** لا يوجد وكيل مستقل تمامًا؛ السقف هو L4، والأفعال الخارجية محكومة بالموافقة. · Not L5.
- **لا يَعِد بنتائج.** يحضّر فرصًا مُثبتة بأدلة، لا إيرادًا مضمونًا. · Promises no outcomes.

---

## فهرس وثائق `docs/autonomy/` · Index of `docs/autonomy/` docs

| الوثيقة · Doc | الغرض · Purpose |
|---|---|
| [`AUTONOMOUS_OPS_ARCHITECTURE.md`](AUTONOMOUS_OPS_ARCHITECTURE.md) | هذه الوثيقة — المعمار الرئيس · this doc — master architecture |
| [`AGENT_ROSTER.md`](AGENT_ROSTER.md) | سجل كل وكيل في الهرم · full agent roster |
| [`ORCHESTRATION_AND_AUTONOMY_LADDER.md`](ORCHESTRATION_AND_AUTONOMY_LADDER.md) | التنسيق وسلّم الاستقلالية · orchestration & autonomy ladder |
| `AGENT_GOVERNANCE_AND_GUARDRAILS.md` | الحوكمة والحواجز — *لم تُنشأ بعد* · governance & guardrails — *not yet created* |

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
