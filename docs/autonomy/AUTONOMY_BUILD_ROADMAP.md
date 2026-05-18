# Dealix — خارطة بناء الاستقلالية · Autonomy Build Roadmap

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `AUTONOMOUS_OPS_ARCHITECTURE.md` · `AGENT_GOVERNANCE_AND_GUARDRAILS.md` · `../commercial/COMMERCIAL_GATES.md` · `../launch/LAUNCH_READINESS_SCORECARD.md`

---

## الغرض · Purpose

تصف هذه الوثيقة خارطة متدرّجة لتحقيق هرم الوكلاء — تحترم التجميد التجاري. تصمّم المعمارية فقط؛ لا تأذن ببناء كود منتج جديد. البناء مُبوَّب على أول pilot مدفوع + Proof Pack.

This document describes a staged roadmap to realize the agent pyramid — and it respects the Commercial Freeze. It designs architecture only; it authorizes no new product code. Build is gated on the first paid pilot + Proof Pack.

---

## ثلاثة أعمدة للحالة · Three columns of status

| الحالة · Status | المعنى · Meaning |
|---|---|
| موجود اليوم · Exists today | كود مبني ويعمل في الريبو والمنصة الحية · code built and running in the repo and the live platform |
| آمن للتوصيل الآن · Safe to wire now | تنسيق / إعداد / جدولة بلا كود محفوف بالمخاطر · orchestration, config, scheduling — no risky code |
| يحتاج كودًا جديدًا — بعد التجميد · Needs new code — post-freeze | مُبوَّب على أول pilot مدفوع + Proof Pack · gated on the first paid pilot + Proof Pack |

### موجود اليوم · Exists today

`agent_os` (`AgentCard`, `register_agent`, `kill_agent`) · `secure_agent_runtime_os` (الحدود الأربعة، مفتاح الإيقاف، `RuntimeState`) · `role_command_os` (`RoleName`, `build_role_brief`, `RoleBrief`, `RoleDecision`) · وكلاء `auto_client_acquisition/agents/` التسعة · وكلاء `autonomous_growth/agents/` الخمسة + `GrowthOrchestrator` · `approval_center` (`ApprovalStore`, 11 `action_type`) · وظائف ARQ في `core/queue/tasks.py` (`lead_score`, `proposal_draft`, `outreach_batch`, `embedding_index`, `commercial_sprint_report`) · وحدات OS (`data_os`, `governance_os`, `proof_os`, `value_os`, `capital_os`, `adoption_os`, `client_os`, `sales_os`) · `delivery_factory/delivery_sprint.py` `run_sprint()` · `payment_ops/orchestrator.py`.

### آمن للتوصيل الآن · Safe to wire now

ملفات cron / جدولة الإيقاع المُضافة فعلًا · إعداد أدوار وأسقف الاستقلالية في `AgentCard` · سجل الوكلاء وتوثيق المعمار · ربط الوثائق المرافقة.

### يحتاج كودًا جديدًا — بعد التجميد · Needs new code — post-freeze

أي كود تنسيق وكلاء جديد · طبقة التنفيذ الذاتي · واجهة cockpit للعمليات.

---

## Phase A — الآن، آمن مع التجميد · Now, freeze-safe

**النطاق · Scope:** المعمار + سجل الوكلاء + الجدولة الآمنة. توثيق الهرم، تثبيت `AgentCard` لكل وكيل قائم، ضبط أسقف الاستقلالية لكل تير، تفعيل ملفات الجدولة (cron workflows) المُضافة فعلًا فوق الوكلاء الموجودين. لا كود منتج جديد.

**Scope:** architecture + agent roster + safe scheduling. Document the pyramid, fix an `AgentCard` for every existing agent, set per-tier autonomy caps, and enable the already-added cron workflows over existing agents. No new product code.

**المتطلبات · Prerequisites:** لا شيء — هذه المرحلة آمنة مع التجميد · none — this phase is freeze-safe.

**القواعد الملزِمة · Non-negotiables that still bind:** الأحد عشر جميعًا · all eleven — مع تركيز على `no_unbounded_agents` (كل وكيل ببطاقة) و`no_unaudited_changes`.

**القاعدة الصريحة · Explicit rule:** الإرسال والشحن الخارجي يبقيان محكومين بالموافقة — إلى الأبد · external send and charge stay approval-gated — forever.

---

## Phase B — بعد أول pilot مدفوع · After the first paid pilot

**النطاق · Scope:** توصيل المنسّق التنفيذي (Executive Orchestrator) فوق `RoleBrief`s القائمة عبر `role_command_os`؛ تنسيق أعمق بين Tier 1 و Tier 2 و Tier 3؛ تركيب طابور قرارات المؤسس من بريفات الأدوار.

**Scope:** wire the Executive Orchestrator over existing role briefs via `role_command_os`; deeper orchestration across Tier 1, 2, and 3; compose the founder decision queue from role briefs.

**المتطلبات · Prerequisites:** اجتياز Gate 2 و Gate 3 في [`../commercial/COMMERCIAL_GATES.md`](../commercial/COMMERCIAL_GATES.md) — أول دفعة موثّقة + Proof Pack مُسلَّم خلال 48 ساعة. مراجعة [`../launch/LAUNCH_READINESS_SCORECARD.md`](../launch/LAUNCH_READINESS_SCORECARD.md) بحالة GO.

**Prerequisites:** Gate 2 and Gate 3 in `../commercial/COMMERCIAL_GATES.md` cleared — first documented payment + a 48h Proof Pack. The launch scorecard at GO.

**القواعد الملزِمة · Non-negotiables that still bind:** الأحد عشر جميعًا — مع تركيز على `no_silent_failures` (كل قرار تنسيق ظاهر) و`no_unverified_outcomes` (تيرات `value_os` تحكم كل عبارة قيمة).

**القاعدة الصريحة · Explicit rule:** الإرسال والشحن الخارجي يبقيان محكومين بالموافقة — إلى الأبد · external send and charge stay approval-gated — forever.

---

## Phase C — بعد 3 pilots مدفوعة / رفع التجميد · After 3 paid pilots / freeze lifts

**النطاق · Scope:** طبقة التنفيذ الذاتي للأفعال الداخلية المدقَّقة (L4) وواجهة cockpit للعمليات. تبقى L5 محظورة؛ يبقى الإرسال والشحن خارج نطاق التنفيذ الذاتي.

**Scope:** the autonomous-execution layer for internal audited actions (L4) and the ops cockpit code. L5 stays blocked; send and charge stay outside autonomous execution.

**المتطلبات · Prerequisites:** اجتياز Gate 5 (القابلية للتكرار) في [`../commercial/COMMERCIAL_GATES.md`](../commercial/COMMERCIAL_GATES.md) — 3 workflows مكرّرة بنفس الألم والمشتري وصيغة الـProof. القاعدة الحاكمة هناك: لا يُبنى module جديد قبل Gate 5.

**Prerequisites:** Gate 5 (Repeatability) cleared — 3 repeated workflows with the same pain, buyer, and proof format. The governing rule there: no new module before Gate 5.

**القواعد الملزِمة · Non-negotiables that still bind:** الأحد عشر جميعًا — مع تركيز على `no_live_send`, `no_live_charge`, و`no_unbounded_agents` (سقف L4، لا L5).

**القاعدة الصريحة · Explicit rule:** الإرسال والشحن الخارجي يبقيان محكومين بالموافقة — إلى الأبد، حتى بعد رفع التجميد · external send and charge stay approval-gated — forever, even after the freeze lifts.

---

## ملخّص المراحل · Phase summary

| المرحلة · Phase | البوابة المسبقة · Prerequisite gate | المخرج · Exit artifact |
|---|---|---|
| A — الآن · Now | لا شيء · none | معمار موثّق + سجل وكلاء + جدولة آمنة · documented architecture + roster + safe scheduling |
| B — بعد أول pilot · After first pilot | Gate 2 + Gate 3 | Executive Orchestrator موصول فوق `RoleBrief`s · orchestrator wired over role briefs |
| C — بعد 3 pilots · After 3 pilots | Gate 5 | طبقة تنفيذ ذاتي L4 + ops cockpit · L4 execution layer + ops cockpit |

---

## القاعدة الثابتة عبر كل المراحل · The constant across every phase

البناء يتبع الدليل، لا الحدس. كل مرحلة مُبوَّبة على بوابة تجارية موثّقة. وفي كل مرحلة — وبعدها — يبقى كل فعل خارجي (إرسال / شحن) `ApprovalRequest` ينتظر موافقة المؤسس. الأتمتة تعني التحضير، لا الإرسال.

Build follows evidence, not intuition. Each phase is gated on a documented commercial gate. In every phase — and after them all — every external action (send / charge) stays an `ApprovalRequest` awaiting founder approval. Automation means preparation, never sending.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
