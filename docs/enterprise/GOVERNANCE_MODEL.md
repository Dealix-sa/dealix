# Dealix — Governance Model — نموذج الحوكمة

> **EN-primary, AR summaries.** This document describes how Dealix governs AI agents at runtime: the loop, the rules, the approval surfaces, and the kill-switch. Where it cites external frameworks (e.g., AGENTSAFE-style framing), the reference is paraphrased context; we do not invent citations.
>
> **بالإنجليزية أصلًا وملخّصات بالعربية.** تصف هذه الوثيقة كيف يحوكم ديلكس وكلاء الذكاء الاصطناعي لحظة التشغيل: الحلقة، والقواعد، وواجهات الاعتماد، ومفتاح الإيقاف. الإشارات الخارجية مُعاد صياغتها كسياق، بلا اقتباسات مفترَضة.

---

## 1. Runtime Governance Loop — حلقة الحوكمة لحظة التشغيل

Every agent action passes through a five-step loop:

1. **Observe.** The agent's intent and inputs are captured.
2. **Decide.** The Governance Loop maps the intended action to its policy, data class, and approval class.
3. **Approve.** If the action requires Reviewer-, Founder-, or Board-class approval, it is routed and paused until a recorded decision.
4. **Act.** The action executes through the MCP gateway with policy enforcement and rate limits.
5. **Log.** The action is recorded in the append-only audit log; the outcome is linked to the Evidence Pack pipeline.

The loop is not optional. An agent that bypasses it is, by definition, ungoverned and is denied execution.

**AR.** كل إجراء يمر بحلقة من خمس خطوات: ملاحظة، قرار، اعتماد، تنفيذ، تسجيل. الحلقة غير اختيارية، وأي وكيل يتجاوزها يُعدّ غير محكوم ويُرفض تنفيذه.

---

## 2. Policy, Agent, Governance, Runtime, Ledger (PAGRL) — العناصر الخمسة

Dealix governance rests on five elements; together they form the PAGRL spine.

- **P — Policy.** A written, versioned set of allowed and forbidden actions per agent, per data class.
- **A — Agent.** A declared entity in the registry with a named owner, capability scope, and approval class.
- **G — Governance.** The runtime loop above plus the Approval Center and the kill-switch surface.
- **R — Runtime.** A sandboxed execution environment that enforces tenant isolation and tool scope.
- **L — Ledger.** A tamper-evident audit log linked to the Evidence Pack assembly pipeline.

If any element is missing, the agent does not deploy.

**AR.** ترتكز الحوكمة في ديلكس على خمسة عناصر تُلخَّص في الاختصار P-A-G-R-L: سياسة، وكيل، حوكمة، تشغيل، سجل. غياب أي عنصر يُلغي النشر.

---

## 3. Authenticated Workflows — سير العمل المُصدَّق عليه

A workflow is authenticated when:

1. Its scope memo is signed by both Dealix and the customer's executive sponsor.
2. The agents executing it are present in the registry with current audit dates.
3. The tools it invokes are present in the Tool Permission Matrix and the MCP gateway.
4. Its data classes are enumerated and bounded.
5. Its outcomes map to source-of-truth systems for verification.

Unauthenticated workflows do not run. There is no "shadow" path.

**AR.** يُعدّ سير العمل مُصدَّقًا عليه عندما: تُوقَّع مذكرة نطاقه، تُسجَّل وكلاؤه، تُدرَج أدواته في المصفوفة والبوابة، تُحدَّد فئات بياناته، وتُربط نتائجه بأنظمة المصدر للتحقق. لا تشغيل بلا تصديق ولا مسار خفيّ.

---

## 4. Agent-to-Agent Rules — قواعد التفاعل بين الوكلاء

When agents call agents, additional constraints apply:

- The calling agent's approval class is the floor; the callee cannot operate under a lower class.
- Tool permissions of the callee must intersect with the caller's scope; no privilege escalation through delegation.
- Cross-agent calls are logged with the full chain (initiator → intermediate → terminal).
- Cycles in agent-to-agent graphs are detected and broken automatically; cycle attempts are S1 incidents.
- An agent may not call another agent across tenants.

**AR.** عند استدعاء وكيل لوكيل: فئة الاعتماد للمستدعي هي الحدّ الأدنى، تتقاطع صلاحيات المُستدعَى مع نطاق المُستدعِي، تُسجَّل السلسلة كاملة، تُكتشف الدورات وتُقطع تلقائيًا، ولا استدعاء عابرًا للمستأجرين.

---

## 5. The Approval Center — مركز الموافقات

The Approval Center is the single surface where pending actions wait for a decision. It exposes:

- **Pending queue.** Actions waiting on Reviewer, Founder, or Board approval.
- **Decision record.** Every approval or rejection is logged with rationale, approver identity, and timestamp.
- **Standing rules.** Approvers may define rules that pre-authorize categories of action; rule changes themselves are Founder-approved.
- **SLA timers.** Each class has a target decision window; breaches surface as operational metrics.

The Approval Center is integrated with the audit ledger; a decision recorded there is itself an auditable artifact.

**AR.** مركز الموافقات هو الواجهة الوحيدة لانتظار القرار. يعرض: قائمة المعلّق، سجل القرارات، القواعد الدائمة (والتغييرات عليها باعتماد المؤسس)، ومؤقّتات SLA لكل فئة. القرار فيه نفسه أصل قابل للتدقيق.

---

## 6. The Kill Switch — مفتاح الإيقاف

- Every agent and every tool has a documented kill switch.
- The default owner is the Founder office (Sami); delegations to a customer's executive sponsor are explicit and logged.
- Invocation freezes the agent or tool within five minutes across all in-flight invocations.
- A kill-switch event automatically generates an Evidence Pack delta entry.
- Quarterly fire-drills exercise the switch end-to-end.

**Principle.** The cost of pause is always lower than the cost of an unsafe action.

**AR.** لكل وكيل وأداة مفتاح إيقاف موثّق. المالك الافتراضي مكتب المؤسس (سامي)؛ التفويض للراعي التنفيذي صريح ومُسجَّل. التفعيل يجمّد التنفيذ خلال خمس دقائق على كل النداءات الجارية، ويولّد إضافة في حقيبة الأدلة. تدريبات ربعية. مبدأ: تكلفة الإيقاف أقل دومًا من تكلفة إجراء غير آمن.

---

## 7. Founder-Class Approval — اعتماد فئة المؤسس

Founder-class approval is required for:

1. Discounts on enterprise-tier offers.
2. Scope changes that touch data boundaries, residency, or kill-switch ownership.
3. New MCP servers or external tools wired to deployed agents.
4. Cross-tenant or cross-border data flows.
5. Code execution by any agent on a non-sandboxed surface.
6. Modifications to the Tool Permission Matrix or Agent Registry that lower an approval class.

Founder-class approvals are not ceremonial. Each is recorded with rationale, evidence, and signature, and is auditable in the Approval Center.

**AR.** فئة المؤسس مطلوبة لـ: خصومات فئات المؤسسات، تغييرات نطاق تمسّ الحدود أو الإقامة أو مفتاح الإيقاف، توصيل خوادم MCP وأدوات جديدة، تدفقات عابرة للمستأجرين أو الحدود، تنفيذ شيفرة خارج الصندوق الرملي، وتعديلات تخفّض فئة الاعتماد. غير شكلية؛ تُسجَّل ببرّر ودليل وتوقيع.

---

## 8. AGENTSAFE-Style Framing (Paraphrased Context) — إطار شبيه بـ AGENTSAFE

Industry-aligned framings such as AGENTSAFE-style guidance describe agent governance through risk categories (privilege, persistence, side-effects, deception, escalation). The Dealix Governance Model maps to those categories as follows:

| Category | Dealix Surface |
|---|---|
| Privilege | Approval class + Tool Permission Matrix |
| Persistence | Sandbox boundaries + secret-handling rules |
| Side-effects | MCP gateway policy enforcement + rate limits |
| Deception | Prompt-injection quarantine + trusted/untrusted content classification |
| Escalation | Founder-class approval + cross-agent privilege rules |

This mapping is paraphrased context; we do not claim a formal AGENTSAFE certification.

**AR.** الأُطُر الصناعية تصنّف مخاطر الوكلاء عبر فئات (الامتياز، الاستمرار، التأثير الجانبي، الخداع، التصعيد). يربط ديلكس كل فئة بسطح تشغيلي محدد. الإشارة سياقية مُعاد صياغتها، بلا ادعاء شهادة رسمية.

---

## 9. What This Model Refuses — ما يرفضه هذا النموذج

- Agents that act on sensitive systems without an approval class.
- Cold outreach automation as a service (cold email, cold WhatsApp, LinkedIn automation, scraping).
- Vanity metrics displayed as outcomes.
- Cross-tenant data leakage of any size.
- Confidential customer metrics inside sector reports.
- Discounts granted without a delivered Evidence Pack.

**AR.** يرفض النموذج: وكلاء يعملون على أنظمة حسّاسة بلا فئة موافقة؛ التواصل البارد كخدمة؛ مؤشرات شكلية كنتائج؛ تسرّب بيانات بين المستأجرين؛ مؤشرات سرية للعملاء في تقارير القطاعات؛ خصومات بلا حقيبة أدلة مُسلَّمة.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/enterprise/SECURITY_OVERVIEW.md` · `/home/user/dealix/docs/enterprise/VALUE_MEASUREMENT.md` · `/home/user/dealix/docs/trust/AGENT_REGISTRY_SAMPLE.md`
