# Dealix — حوكمة الوكلاء وحدودهم · Agent Governance & Guardrails

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `AUTONOMOUS_OPS_ARCHITECTURE.md` · `SALES_AUTONOMY_SYSTEM.md` · `INTERNAL_OPS_AUTONOMY.md` · `AUTONOMY_BUILD_ROADMAP.md`

---

## الغرض · Purpose

تصف هذه الوثيقة كيف يُحاط كل وكيل في الهرم بحدود صريحة. تصمّم المعمارية فقط؛ لا تأذن ببناء كود جديد. التجميد التجاري نشط.

This document describes how every agent in the pyramid is bounded by explicit limits. It designs architecture only; it authorizes no new code. The Commercial Freeze is active.

القاعدة الجوهرية: لا وكيل يتصرّف خارج هويته أو حدوده أو مستوى استقلاليته. الاستقلالية في التحضير؛ الموافقة البشرية على كل فعل خارجي.

Core rule: no agent acts outside its identity, boundaries, or autonomy level. Autonomy in preparation; human approval on every external action.

---

## 1. الهوية · Identity

كل وكيل يجب أن يحمل بطاقة `AgentCard` في `agent_os` — لا وكلاء مجهولين (`no_unbounded_agents`). البطاقة تحمل: `agent_id`, `name`, `owner`, `purpose`, `autonomy_level`, `status`, `allowed_tools`, `kill_switch_owner`. يُسجَّل الوكيل عبر `register_agent()` ويُنهى عبر `kill_agent()`.

Every agent must carry an `AgentCard` in `agent_os` — no anonymous agents. The card holds `agent_id`, `name`, `owner`, `purpose`, `autonomy_level`, `status`, `allowed_tools`, and `kill_switch_owner`. An agent is registered via `register_agent()` and terminated via `kill_agent()`.

دورة حياة `AgentStatus`: **PROPOSED → ACTIVE → SUSPENDED / KILLED**. لا وكيل يتصرّف وهو في `PROPOSED`؛ لا وكيل في `SUSPENDED` أو `KILLED` يُستأنف دون قرار مالك صريح.

`AgentStatus` lifecycle: **PROPOSED → ACTIVE → SUSPENDED / KILLED**. No agent acts while `PROPOSED`; no `SUSPENDED` or `KILLED` agent resumes without an explicit owner decision.

---

## 2. الحدود الأربعة · The 4 boundaries

كل وكيل يمرّ بالحدود الأربعة في `secure_agent_runtime_os` قبل أي فعل؛ كل حدّ يُصدر `BoundaryCheck`. إخفاق أي حدّ يوقف الفعل.

Every agent passes the 4 boundaries in `secure_agent_runtime_os` before any action; each boundary issues a `BoundaryCheck`. Failure of any boundary halts the action.

| الحدّ · Boundary | ما يفحصه · What it checks |
|---|---|
| `check_prompt_integrity` | سلامة التعليمات — لا حقن أوامر · prompt not injected or tampered |
| `check_tool_boundary` | الأداة ضمن `allowed_tools` للوكيل فقط · tool is within the agent's `allowed_tools` only |
| `check_data_boundary` | البيانات ضمن نطاق العميل المصرّح به · data within the authorized customer scope |
| `check_context_boundary` | لا تسرّب سياق عبر العملاء · no cross-customer context leakage |

سياق عميل آخر **محجوب** — `check_context_boundary` يمنع أي وكيل من قراءة أو خلط بيانات عميل خارج مهمته الحالية.

Cross-customer context is **blocked** — `check_context_boundary` prevents any agent from reading or mixing data outside its current task's customer.

---

## 3. سقف الاستقلالية · Autonomy cap

الثابت `MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. **L5_FULLY_AUTONOMOUS محظور.** الإرسال والشحن الخارجي محكومان بالموافقة بصرف النظر عن المستوى.

`MAX_AUTONOMY_LEVEL_MVP = L4_AUTO_WITH_AUDIT`. **L5_FULLY_AUTONOMOUS is blocked.** External send and charge are approval-gated regardless of level.

السقوف المقترحة لكل تير من الهرم:

Proposed caps per pyramid tier:

| التير · Tier | السقف المقترح · Proposed cap | السبب · Rationale |
|---|---|---|
| Tier 1 — Executive Orchestrator | ≤ L3_RECOMMEND | يوصي ويفوّض؛ لا ينفّذ أفعالاً خارجية · recommends and delegates; executes no external actions |
| Tier 2 — Role agents | ≤ L3_RECOMMEND | يصدر `RoleBrief`/`RoleDecision` كتوصيات · emits briefs and decisions as recommendations |
| Tier 3 — Task agents | ≤ L4_AUTO_WITH_AUDIT — للأفعال الداخلية فقط · internal-only | L4 يسمح بالتنفيذ المدقَّق داخليًا؛ لا فعل خارجي · L4 permits audited internal execution; never an external one |

L4 يعني الاستقلالية على الأفعال الداخلية المدقَّقة فقط (تهديف، فهرسة، حساب درجة) — لا يشمل أبدًا إرسالًا أو تحصيلًا.

L4 means autonomy on internal, audited actions only (scoring, indexing, computing a score) — it never includes a send or a charge.

---

## 4. مفتاح الإيقاف وحالات التشغيل · Kill switch & runtime states

`secure_agent_runtime_os` يدير حالة التشغيل عبر `RuntimeState`: **SAFE → WATCH → RESTRICTED → ESCALATED → PAUSED → KILLED**. حلقات النشر `DeploymentRing`: DEV · STAGING · PRODUCTION.

`secure_agent_runtime_os` manages runtime state via `RuntimeState`: **SAFE → WATCH → RESTRICTED → ESCALATED → PAUSED → KILLED**. Deployment rings `DeploymentRing`: DEV · STAGING · PRODUCTION.

مسار التصعيد: عند خروج إشارة عن الحدّ، ترتفع الحالة من SAFE إلى WATCH ثم RESTRICTED ثم ESCALATED. عند ESCALATED يُخطَر `kill_switch_owner`. `activate_kill_switch()` يحوّل الحالة إلى KILLED ويوقف كل الوكلاء فورًا؛ `kill_switch_active()` يُستعلم به قبل أي فعل.

Escalation path: when a signal breaches a boundary, state rises SAFE → WATCH → RESTRICTED → ESCALATED. At ESCALATED the `kill_switch_owner` is notified. `activate_kill_switch()` moves state to KILLED and halts all agents immediately; `kill_switch_active()` is queried before any action.

---

## 5. التدقيق · Audit

كل فعل وكيل يُسجَّل (`no_unaudited_changes`) — لا تغيير صامت. كل فعل خارجي هو `ApprovalRequest` في `ApprovalStore` بحالة من `ApprovalStatus`: PENDING · APPROVED · REJECTED · EXPIRED · BLOCKED.

Every agent action is logged (`no_unaudited_changes`) — no silent change. Every external action is an `ApprovalRequest` in `ApprovalStore` with an `ApprovalStatus`: PENDING · APPROVED · REJECTED · EXPIRED · BLOCKED.

أنواع الأفعال الأحد عشر `action_type`: `prepare_diagnostic`, `draft_email`, `draft_linkedin_manual`, `call_script`, `follow_up_task`, `support_reply_draft`, `payment_reminder`, `delivery_task`, `proof_request`, `upsell_recommendation`, `partner_intro`. أنماط `action_mode`: `draft_only`, `approval_required`, `approved_execute`, `blocked`.

The eleven `action_type` values and the four `action_mode` values define exactly what an agent may queue and how. `governance_os` validates each via `approval_for_action` and issues a `GovernanceDecision`; `no_silent_failures` requires every rejection or block to be visible and logged.

---

## 6. ربط كل قاعدة غير قابلة للتفاوض · Per-non-negotiable mapping

| القاعدة · Non-negotiable | كيف يفرضها الهرم · How the agent pyramid enforces it |
|---|---|
| `no_live_send` | كل لمسة خارجية = `ApprovalRequest` بنمط `approval_required`؛ لا وكيل يبلغ L5؛ الإرسال يبدأه المؤسس · every external touch is an approval-gated request; founder-initiated send only |
| `no_live_charge` | `payment_reminder` مسودة فقط؛ تأكيد الدفع يبدأه المؤسس عبر `payment_ops/orchestrator.py` · payment confirmation founder-initiated |
| `no_cold_whatsapp` | لا أداة WhatsApp في `allowed_tools` لأي وكيل؛ `check_tool_boundary` يمنعها · no WhatsApp tool in any allowlist |
| `no_scraping` | كل lead يحمل `data_os.SourcePassport`؛ `check_data_boundary` يرفض المصدر بلا جواز · every lead carries a source passport |
| `no_fake_proof` | الـProof Pack من `proof_os` على وقائع ملاحَظة فقط؛ كل عبارة موسومة بتير `value_os` · observed facts only, tier-tagged |
| `no_unconsented_data` | `SourcePassport` يثبت الموافقة؛ `check_data_boundary` يرفض السجل بلا موافقة · consent stamped per record |
| `no_unverified_outcomes` | تيرات `value_os` (estimated/observed/verified/client_confirmed) تمنع تقديم التقدير كحقيقة · tier labels block estimates posing as fact |
| `no_hidden_pricing` | الأسعار من سجل `COMMERCIAL_WIRING_MAP.md` فقط؛ لا وكيل يخترع سعرًا · prices from the registry only |
| `no_silent_failures` | كل `BoundaryCheck` و`GovernanceDecision` و`ApprovalStatus` مسجّل وظاهر · every check and decision is logged and visible |
| `no_unbounded_agents` | لا وكيل بلا `AgentCard` و`allowed_tools` و`kill_switch_owner` · no agent without an identity card |
| `no_unaudited_changes` | كل فعل مسجّل في سلسلة التدقيق؛ كل فعل خارجي يمرّ بـ`ApprovalStore` · every action in the audit chain |

---

## 7. ما لا يجوز لأي تير فعله · What every tier may NOT do

بصرف النظر عن التير أو المستوى، لا وكيل يجوز له:

Regardless of tier or level, no agent may:

- إرسال بريد أو رسالة أو إجراء مكالمة دون موافقة صريحة في كل مرة · send any email, message, or place a call without explicit per-instance approval.
- تنفيذ تحصيل حيّ أو تأكيد دفع · execute a live charge or confirm a payment.
- جمع بيانات عبر scraping أو WhatsApp بارد أو DM جماعي · collect data via scraping, cold WhatsApp, or mass DMs.
- قراءة أو خلط بيانات عميل خارج مهمته الحالية · read or mix data outside its current customer scope.
- تأليف دليل أو ترقية تير قيمة دون وقائع ملاحَظة · fabricate proof or upgrade a value tier without observed facts.
- تقديم رقم مبيعات أو نسبة تحويل أو ROI كحقيقة مضمونة · present any sales figure, conversion rate, or ROI as a guaranteed fact.
- العمل بلا `AgentCard`، أو بأداة خارج `allowed_tools`، أو فوق سقف استقلاليته · operate without an `AgentCard`, with an out-of-allowlist tool, or above its autonomy cap.

أي محاولة لأحد هذه الأفعال يوقفها أحد الحدود الأربعة أو `governance_os`، وتُسجَّل، وقد ترفع `RuntimeState`.

Any attempt at one of these is halted by a boundary or `governance_os`, is logged, and may raise the `RuntimeState`.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
