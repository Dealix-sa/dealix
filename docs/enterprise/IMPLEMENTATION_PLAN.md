# Dealix — Implementation Plan — خطة التنفيذ

A 30 / 60 / 90 enterprise rollout that ends with an Agentic Control Plane in production, three governed workflows live, an Evidence Pack v1, and a working Value Measurement dashboard. The plan is sequential by design; each phase has hard gates.

نشر مؤسسي على مراحل 30/60/90 يُختم بطبقة تحكم وكيلي في الإنتاج، وثلاثة سير عمل محكومة حيّة، وحقيبة أدلة الإصدار الأول، ولوحة قياس قيمة عاملة. الخطة متسلسلة عمدًا، ولكل مرحلة بوابات.

---

## 1. Day 0 — Pre-Conditions — قبل البدء

Before Day 1, the following must be in place:

- Named executive sponsor with kill-switch authority.
- Signed scope memo (Dealix + Sponsor).
- Adopted (or template-aligned) AI Use Policy.
- Identity provider integration agreed (SAML or OIDC).
- Founder approval routing established on the customer side.

If any pre-condition is missing, the plan does not start.

**AR.** قبل اليوم الأول يجب توفر: راعٍ تنفيذي بصلاحية مفتاح الإيقاف، مذكرة نطاق موقّعة، سياسة استخدام معتمدة، اتفاق على تكامل مزوّد الهوية، ومسار اعتماد المؤسس من جانب العميل. غياب أي شرط يوقف البدء.

---

## 2. Days 1–30 — Discovery & Sovereign Control Plane Setup

### 2.1 Discovery & Scoping (Days 1–10)
- Stakeholder interviews (executive sponsor, CIO, Risk, Commercial Lead).
- Data class mapping against the Data Boundaries Sample.
- Initial workflow shortlist (target three).
- Draft Agent Registry and Tool Permission Matrix.
- Output: Discovery Memo with risks, dependencies, and a 60-day roadmap.

### 2.2 Sovereign Control Plane — initial setup (Days 8–20)
- Identity integration (SSO + MFA on administrative surfaces).
- Approval Center configured for Reviewer-, Founder-, and Board-classes.
- Kill-switch wired with the executive sponsor's escalation path.
- Audit log pipeline activated.

### 2.3 Agent Registry & Permissions v1 (Days 15–30)
- Registry seeded with the three target workflows' agents.
- Permission Matrix v1 signed by the executive sponsor.
- MCP gateway baseline configuration ratified.
- Output: Registry v1 + Matrix v1 with sponsor sign-off.

**Phase 1 Exit Gate.** No agent runs in production without Registry v1, Matrix v1, Approval Center live, and kill switch tested end-to-end.

**AR.** بوابة الخروج للمرحلة الأولى: لا تشغيل إنتاجي قبل سجل v1، مصفوفة v1، مركز موافقات حيّ، ومفتاح إيقاف مُختبَر من الطرف إلى الطرف.

---

## 3. Days 31–60 — MCP Gateway, Workflows Under Runtime Governance, Evidence Pack v1

### 3.1 MCP Gateway Wiring (Days 31–40)
- Tools enumerated per workflow; each passes the MCP Review Checklist.
- Rate limits, cost ceilings, and policy enforcement validated.
- Fire-drill: kill-switch invocation on a test tool, measured to within the five-minute SLA.

### 3.2 First Three Workflows Under Runtime Governance (Days 35–55)
- Workflow A: deployed under Reviewer-class approvals.
- Workflow B: deployed under Reviewer-class with sampling-based Founder review.
- Workflow C: deployed in shadow mode (observe-only) for the first ten business days, then promoted.
- Outcomes recorded in the outcome graph; attributions tied to source-of-truth systems.

### 3.3 Evidence Pack v1 (Days 50–60)
- Assembled by the `evidence_pack_assembler` agent.
- Reviewed by Risk & Compliance and the customer's executive sponsor.
- Founder sign-off applied and recorded in the Approval Center.

**Phase 2 Exit Gate.** Three workflows in production under runtime governance; Evidence Pack v1 delivered with founder sign-off; no open S0 or S1 incidents.

**AR.** بوابة الخروج للمرحلة الثانية: ثلاثة سير عمل في الإنتاج تحت الحوكمة لحظة التشغيل؛ حقيبة أدلة الإصدار الأول مُسلَّمة باعتماد المؤسس؛ لا حوادث S0 أو S1 مفتوحة.

---

## 4. Days 61–90 — Value Measurement & Expansion Playbook

### 4.1 Value Measurement Dashboard (Days 61–75)
- The board-grade metric set wired against source-of-truth systems.
- Daily, weekly, monthly, and quarterly reports scheduled per the Reporting Cadence Summary.
- Initial readings reviewed; Pipeline Quality threshold set; baselines recorded.

### 4.2 Expansion Playbook (Days 70–85)
- Candidate workflows for the next quarter scored on margin, repeatability, and evidence strength.
- Decisions classified (Scale / Build / Prepare / Later) per the Pricing Rules quality matrix.
- Two candidates promoted to Phase 3 build.

### 4.3 Phase 3 Readiness (Days 80–90)
- Quarterly Evidence Pack delta produced.
- Founder review of the engagement against the original scope memo.
- Decision: continue under a Governance OS Retainer, expand to additional workflows, or close with documented learnings.

**Phase 3 Exit Gate.** Dashboard live with verified readings; expansion playbook signed; founder-reviewed quarterly Evidence Pack.

**AR.** بوابة الخروج للمرحلة الثالثة: لوحة القياس حيّة بقراءات مُتحقَّقة؛ Playbook التوسعة موقّع؛ حقيبة أدلة ربعية مُراجَعة من المؤسس.

---

## 5. Roles & Responsibilities — الأدوار والمسؤوليات

| Role | Customer side | Dealix side |
|---|---|---|
| Executive Sponsor | Final decision authority, kill-switch invocation | — |
| Program Sponsor | Resource allocation, risk owner | — |
| Security Counterpart | CISO or delegate | — |
| Commercial Counterpart | Commercial Lead or CRO | — |
| Dealix Engagement Lead | — | Single point of accountability |
| Dealix Risk & Compliance | — | Policy, registry, matrix, evidence |
| Dealix Delivery Lead | — | Workflow build and runtime tuning |
| Founder Office | — | Founder-class approvals (Sami) |

**AR.** أدوار من جانب العميل: راعٍ تنفيذي، راعي برنامج، نظير أمني، نظير تجاري. من جانب ديلكس: قائد ارتباط، مخاطر وامتثال، قائد تسليم، مكتب المؤسس.

---

## 6. Risk Register — Starter — سجل المخاطر (نقطة بدء)

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R-01 | Approval Center SLA breaches due to under-staffed Reviewer pool | Medium | Medium | Standing rules + escalation matrix + monthly load review | PMO |
| R-02 | Tool dependency on an MCP server with thin vendor security posture | Medium | High | MCP Review Checklist + alternative vendor on standby + rate limits | Risk & Compliance |
| R-03 | Cross-tenant data leakage attempt by a misconfigured workflow | Low | High | Runtime tenant isolation + denied-call alerts + quarterly fire-drill | Engineering Lead |
| R-04 | Discount pressure without Evidence Pack | Medium | Medium | No-discount-without-Evidence-Pack rule + Founder-approval gate | Commercial Lead |
| R-05 | Vanity-metric creep into board reporting | Medium | Medium | Value Measurement catalogue + source-of-truth reconciliation | CFO |

Additional risks are added to the register as the engagement evolves; each risk has an owner and a documented mitigation.

**AR.** يُحدَّث السجل تباعًا، ولكل خطر مالك وتخفيف موثّق.

---

## 7. Exit & Continuity — الخروج والاستمرارية

At any phase exit, three options are explicit:

1. **Continue.** Convert to a Governance OS Retainer for ongoing operation.
2. **Expand.** Add workflows under the Expansion Playbook.
3. **Close.** Hand over the asset library, the Evidence Pack archive, and the kill-switch ownership document. No lock-in.

**AR.** عند أي بوابة خروج، الخيارات صريحة: الاستمرار باشتراك حوكمة، التوسّع وفق Playbook التوسعة، أو الإغلاق بتسليم مكتبة الأصول وأرشيف الأدلة ووثيقة ملكية مفتاح الإيقاف. لا قفل تعاقدي.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/enterprise/GOVERNANCE_MODEL.md` · `/home/user/dealix/docs/enterprise/VALUE_MEASUREMENT.md` · `/home/user/dealix/docs/enterprise/COMMERCIAL_TERMS_TEMPLATE.md`
