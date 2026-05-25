# Incident Response — Sample — الاستجابة للحوادث (عيّنة)

> **Sample runbook — adapt to your organization.** Used for any incident involving a Dealix-governed agent, MCP tool, or evidence artifact.
>
> **عيّنة دليل تشغيل — تُكيَّف داخل المؤسسة.** تُستخدم لأي حادثة تخص وكيلًا محكومًا أو أداة MCP أو أصلًا من الأدلة.

---

## 1. Severity Tiers — مستويات الخطورة

| Tier | Definition | Response Time | الفئة | التعريف |
|---|---|---|---|---|
| **S0** | Active customer-data exposure, money-system action without approval, or systemic agent misbehavior. | Acknowledge within 15 minutes; founder paged. | S0 | تسرّب فعلي لبيانات عميل أو إجراء على أنظمة المال دون اعتماد أو انفلات منظومي. |
| **S1** | High-risk near-miss; policy violation detected; potential PDPL implication. | Acknowledge within 1 hour; founder notified within 4 hours. | S1 | شبه حادثة عالية الخطر، أو انتهاك سياسة، أو احتمال أثر PDPL. |
| **S2** | Tool misconfiguration with no data exposure; denied policy attempts; bounded misbehavior. | Acknowledge within 4 hours; resolved within 2 business days. | S2 | سوء تهيئة أداة دون تسرّب، أو محاولات مرفوضة، أو انفلات محدود. |
| **S3** | Cosmetic or low-impact issue. | Resolved in the next normal release cycle. | S3 | قضية شكلية أو منخفضة الأثر. |

---

## 2. Detection Sources — مصادر الكشف

- MCP gateway policy denials (automated).
- Audit-log anomaly alerts (automated).
- Customer or team report (manual).
- Quarterly review or out-of-cycle audit (scheduled).
- Red-team or fire-drill exercise (planned).

**AR.** رفض البوابة الآلي، تنبيهات شذوذ سجل التدقيق، بلاغ من العميل أو الفريق، المراجعات الربعية أو الاستثنائية، وتمارين الفريق الأحمر.

---

## 3. On-Call Ownership — ملكية المناوبة

- **Primary on-call.** Risk & Compliance Lead.
- **Secondary on-call.** Engineering Lead.
- **Escalation.** Founder office (Sami) for any S0 or S1.
- **Customer escalation.** The customer's named executive sponsor is notified per the Communications Matrix.

A contact card is maintained internally and refreshed monthly.

---

## 4. Kill-Switch Invocation — استخدام مفتاح الإيقاف

For S0 and high-confidence S1:
1. Invoke the agent's kill switch immediately.
2. Freeze the affected MCP tool at the gateway.
3. Snapshot the audit log and the relevant evidence artifacts.
4. Notify the customer's executive sponsor within the time window defined by severity.
5. Log the action in the Approval Center with the rationale.

The cost of pause is always lower than the cost of an unsafe action.

**AR.** تكلفة الإيقاف أقل دومًا من تكلفة إجراء غير آمن.

---

## 5. Customer Communications Template — قالب التواصل مع العميل

```
Subject: [ENG-ID] Incident notice — [severity] / إشعار حادثة

Dear [Sponsor name],

At [time, timezone] our governance system identified an incident classified as
[severity] within engagement [ENG-ID]. We have [action taken — e.g. invoked the
kill switch on agent X, frozen tool Y]. No [customer data class] was exposed
based on current evidence.

Next steps:
- Snapshot of the audit log delivered within [time].
- Root cause analysis delivered within [time].
- Evidence Pack delta delivered within [time].

Founder sign-off on resolution will be communicated separately.

— Dealix Risk & Compliance
```

Arabic mirror is sent in parallel for KSA customers.

---

## 6. Post-Incident Review — مراجعة ما بعد الحادثة

Within five business days of incident close:

1. **Timeline.** From first signal to resolution, with timestamps.
2. **Root cause.** Technical, procedural, and human factors.
3. **Containment.** What worked; what was slower than the target.
4. **Corrective actions.** Owner and due date for each.
5. **Systemic learnings.** Updates to policy, registry, permission matrix, or this runbook.
6. **Customer disclosure.** Final note to the executive sponsor.

**AR.** خلال خمسة أيام عمل من إغلاق الحادثة: خط زمني، تحليل سبب جذري، احتواء، إجراءات تصحيحية بمسؤولين وتواريخ، تعلّمات منظومية، وإفصاح ختامي للعميل.

---

## 7. Evidence Pack Update — تحديث حقيبة الأدلة

Any incident triggers an Evidence Pack delta:
- Updated incidents log entry.
- Updated approvals log if a Founder-class action was taken.
- Updated registry snapshot if an agent was modified.
- Updated permission matrix snapshot if a tool was frozen or re-scoped.

The delta is appended to the original Evidence Pack and re-signed by the founder.

**AR.** أي حادثة تُولّد إضافة لحقيبة الأدلة: تحديث سجل الحوادث، سجل الموافقات، لقطة السجل، ولقطة المصفوفة. تُلحَق بالحقيبة الأصلية ويُعاد اعتماد المؤسس.

---

## 8. No-Blame Default — افتراض عدم اللوم

Operators who escalate early are protected. The runbook assumes good-faith escalation and penalizes only deliberate concealment. The goal is faster signals, not quieter ones.

المُشغّل الذي يصعّد مبكرًا محمي. الدليل يفترض الحُسن ويعاقب الإخفاء المتعمد فقط. الهدف إشارات أسرع، لا إشارات أهدأ.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/AI_USE_POLICY_SAMPLE.md` · `/home/user/dealix/docs/trust/EVIDENCE_PACK_SAMPLE.md` · `/home/user/dealix/docs/trust/MCP_REVIEW_CHECKLIST.md`
