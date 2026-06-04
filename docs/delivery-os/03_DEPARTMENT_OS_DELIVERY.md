# Department OS Delivery — تسليم نظام القسم

The Department OS tier (SAR 25,000–150,000; Enterprise 150,000+ uses this as its base). A built, governed operating system for an entire department workflow — multiple steps, multiple roles, documented controls. This is productionization, not a one-off.

نظام القسم عرض يبني نظام تشغيل مُحوكَم لمسار عمل قسم كامل، بعدة خطوات وأدوار وضوابط موثّقة. هذه مرحلة إنتاج، لا تجربة.

## Inputs — المدخلات

- A signed scope mapping the department workflow end to end.
- A successful Pilot or an equivalent diagnostic baseline.
- Named roles on the client side (workflow owner, reviewers, data owner).
- A data agreement and Source Passport covering all sources in scope.
- Integration details for the client's CRM and tools (read/write boundaries defined).

## Outputs — المخرجات

- A governed multi-step pipeline: drafting, ranking, recommendation, and a defined human review gate at each external boundary.
- Role-based review queues so the right person approves the right artifact.
- A policy registry instance for the department. See [05_governance_os/POLICY_REGISTRY.md](../05_governance_os/POLICY_REGISTRY.md).
- A run ledger, a value ledger, and a dashboard. See [08_value_os/VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md).
- Documentation and a trained client team.

## Timeline — الجدول الزمني

- Department OS: 6–12 weeks depending on workflow breadth.
- Phase 1: workflow mapping and controls design.
- Phase 2: build and integrate.
- Phase 3: supervised operation with the client team.
- Phase 4: documentation, training, handover.

## Acceptance criteria — معايير القبول

Delivered only when: each workflow step has a working draft-review-approve loop; controls are documented in the policy registry; the client team has run the system supervised for the agreed period; the dashboard is live; and the engagement is set to `department_os_delivered`.

## Human approval boundary — حدود الموافقة البشرية

Every external boundary has a named human approver. The system drafts, ranks, and recommends across the whole department; it never sends externally. Role-based queues make the approver explicit at each step.

## Security boundary — حدود الأمان

Integrations are scoped with least privilege; read/write boundaries are written into the scope. PII classification, redaction, and retention follow [06_llm_gateway/REDACTION_POLICY.md](../06_llm_gateway/REDACTION_POLICY.md) and [04_data_os/DATA_RETENTION_POLICY.md](../04_data_os/DATA_RETENTION_POLICY.md). Access is logged.

## Handover — التسليم

Full documentation set, policy registry export, dashboard access, trained-team sign-off, run/value ledger exports, and explicit limitations. Template: [06_HANDOVER_TEMPLATE.md](06_HANDOVER_TEMPLATE.md).

## Upsell path — مسار الترقية

Department OS → Retainer (operate and maintain) and Department OS → additional departments (replicate the motion into the next workflow). Enterprise engagements bundle several Department OS builds under one governance frame. See [07_EXPANSION_PLAYBOOK.md](07_EXPANSION_PLAYBOOK.md).

## Retainer trigger — مُحفِّز الاشتراك الشهري

A Department OS almost always triggers a Retainer: a built system needs ongoing tuning, review-loop operation, and policy updates. The Retainer scope is proposed at handover and is optional, never auto-renewing.

## Client success metrics — مقاييس نجاح العميل

- Workflow coverage (steps governed vs. total steps).
- Review yield across all steps.
- Observed value at department scale (Estimated → Observed → Verified labeling).
- Client team independence (supervised runs completed before handover).
- Safety violations and compliance rejections (target: trending down).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
