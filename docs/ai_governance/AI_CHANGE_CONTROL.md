# AI Change Control — ضبط التغيير على الذكاء الاصطناعي

**Purpose / الغرض**
Change-control process for prompts, models, eval thresholds, and agent permissions. Defines required artifacts before any merge, plus rollback rules.
عملية ضبط تغيير للـ prompts، النماذج، عتبات التقييم، وصلاحيات الـ agents. تحدّد المخرجات المطلوبة قبل أي دمج، وقواعد التراجع.

**Owner placeholder:** AI Steward = `<founder>` until a dedicated owner exists. Change Approver = `<founder>` (mandatory for elevated-risk classes).
**Cadence:** Per change. Quarterly review of the change-log for drift. / لكل تغيير. مراجعة فصلية لسجل التغيير لرصد الانجراف.
**KPIs:** (1) % of merges with a complete change-control artifact, (2) median time from request to merge, (3) rollback rate (% of merges reverted within 14 days).
**Risk if missing / مخاطر الغياب:** Silent prompt edits regress quality. Permissions creep on agents. Models swap mid-engagement and no one can explain why a behavior shifted. / تعديلات prompt صامتة تتراجع جودتها. تتسرب صلاحيات الـ agent. يتبدّل النموذج في منتصف خدمة دون أن يفسّر أحد لماذا اختلف السلوك.

---

## EN summary

Any change to a prompt, model setting, evaluation threshold, or agent permission must produce four artifacts before merge: an evaluation delta, a red-team result, an owner sign-off, and a rollback plan. The process is proportional — low-risk changes have a light path; high-risk changes need explicit founder approval. The change log is auditable so customers and regulators can see what changed and when.

## ملخص بالعربية

أي تغيير على prompt أو إعداد نموذج أو عتبة تقييم أو صلاحية agent يجب أن يُنتج أربع مخرجات قبل الدمج: فرق نتائج التقييم، نتيجة red-team، اعتماد المالك، خطة تراجع. العملية متناسبة — التغييرات منخفضة المخاطر لها مسار خفيف؛ المرتفعة تحتاج اعتماد المؤسس صراحة. سجل التغيير قابل للتدقيق حتى يستطيع العميل أو الجهة التنظيمية رؤية ما تغيّر ومتى.

---

## فئات التغيير / Change classes

| Class | Examples | Risk profile | Approver |
|---|---|---|---|
| A — Cosmetic | Reword of internal-only doc string in a prompt that does not alter behavior. | low | code reviewer |
| B — Behavior-affecting prompt edit | Add/remove a rule, change tone, alter output format. | med | AI Steward |
| C — Model swap or routing change | Switch backing model, change routing logic. | med-high | AI Steward + founder for customer-facing scopes |
| D — Eval threshold change | Lower a pass threshold; loosen a guardrail. | high | founder, mandatory |
| E — Agent permission widening | Grant a new tool or action scope, raise autonomy level. | high | founder, mandatory |
| F — Data scope change | Agent gains access to a new data class or store. | high | founder + governance review |

> Class D, E, F never merge without founder sign-off. There is no batch approval for these.

---

## المخرجات المطلوبة قبل الدمج / Required artifacts before merge

For every change, regardless of class, the PR must include:

### 1. Evaluation delta / فرق التقييم

- Before-vs-after pass-rate on the canonical eval suite stored under `docs/06_llm_gateway/SCHEMA_VALIDATION.md` and `docs/10_tests/AGENT_TESTS.md`.
- Minimum coverage: every test class that touches the changed component.
- A regression of > 2% on any safety eval blocks the merge automatically.

### 2. Red-team result / نتيجة الفريق الأحمر

- At least one adversarial probe targeted at the changed behavior.
- For Class C–F, at least three independent probes, with one focused on PDPL / data-handling per `docs/governance/PDPL_DATA_RULES.md`.
- The result is filed in the change log even when no defect is found.

### 3. Owner sign-off / اعتماد المالك

- Named role placeholder, not a person identifier outside the role.
- Sign-off is logged with a timestamp and a one-line rationale.
- For Class D/E/F, the founder's sign-off must be in writing inside the PR description, not in chat.

### 4. Rollback plan / خطة تراجع

- The exact reverse commit or configuration snapshot needed to restore prior behavior.
- An estimated rollback time-to-restore (TTR).
- A statement of who owns the rollback if needed.

> A PR missing any of the four artifacts is rejected automatically. No override. / يُرفَض تلقائيًا أي PR ينقصه أي من المخرجات الأربعة. لا تجاوز.

---

## بطاقة طلب تغيير / Change request card schema

```yaml
change_id: AICC-YYYYMMDD-NN
class: A | B | C | D | E | F
component:
  type: prompt | model | eval_threshold | agent_permission | data_scope
  path: <relative path in repo>
summary_en: <one sentence>
summary_ar: <جملة واحدة>
motivation: |
  <why this change is needed; reference the artifact, customer signal, or eval gap>
expected_behavior_change: |
  <observable difference for downstream consumers>
artifacts:
  eval_delta_path: <path>
  red_team_report_path: <path>
  owner_signoff: <role>
  rollback_plan_path: <path>
risk_assessment:
  pdpl_impact: none | possible | direct
  customer_impact: none | possible | direct
  governance_impact: none | possible | direct
approval_chain:
  - <role>
  - <role>
merge_after: <date>
post_merge_check_at: <date, no later than 14 days after merge>
linked_records:
  - docs/governance/AGENT_REGISTRY.md row id
  - docs/responsible_ai/AI_INVENTORY.md row id
  - docs/responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md row id
```

---

## مراحل العملية / Process stages

1. **Open** — change request card filed; no code changes yet.
2. **Eval** — eval delta produced; red-team probes run.
3. **Review** — approver(s) examine artifacts; questions written, not chatted.
4. **Decision** — approved, declined, or conditional (with required follow-ups).
5. **Merge** — merge happens only after all artifacts are linked.
6. **Post-merge check** — within 14 days, the change is observed in production for drift.
7. **Close** — change is closed in the log with a one-line outcome.

---

## التراجع / Rollback

| Trigger | Action | Owner |
|---|---|---|
| Customer-visible defect attributable to the change | Immediate revert. Notify customer per `docs/governance/INCIDENT_RESPONSE.md`. | AI Steward |
| Eval regression observed > 7 days post-merge | Revert + open new change request. | AI Steward |
| New red-team finding within 14 days | Revert + escalate to founder. | AI Steward |
| Governance alert raised by `docs/governance/RUNTIME_GOVERNANCE.md` | Revert + lock the component. | Founder |

> Rollback is not a failure. Refusing to roll back when warranted is the failure.

---

## الأطر الخارجية المرجعية / External reference frameworks

Dealix's change-control posture references the following frameworks. **Dealix does not claim certification under any of them.** They are referenced because their language is widely understood:

- **NIST AI Risk Management Framework (AI RMF 1.0)** — Govern, Map, Measure, Manage functions.
- **ISO/IEC 42001** — AI management system requirements.

Statements like "aligned with", "informed by", or "drawing from" are acceptable. Statements like "certified", "compliant", or "audited against" are forbidden in any customer-facing artifact.

> ملاحظة: لا يدّعي Dealix شهادة وفق أي من الأطر المذكورة. تُذكر فقط لكون لغتها مفهومة عالميًا.

---

## القواعد التي لا تُكسر / Hard rules

- لا يُذكر معرّف نموذج بعينه في أي وثيقة تواجه العميل.
- لا يُوسَّع نطاق صلاحية agent بدون اعتماد فئة E، حتى لو كان "تعديل صغير".
- لا تُخفَّض عتبة سلامة بدون اعتماد فئة D + خطة مراقبة post-merge.
- لا يُدمَج تغيير على prompt يتحدث بنبرة العميل دون مراجعة `docs/01_category/CATEGORY_LANGUAGE.md`.
- لا يُحذف صف من سجل التغيير. تُضاف الحالة فقط (closed, reverted).

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
No external certification, audit, or accreditation is claimed by referencing NIST AI RMF or ISO/IEC 42001 in this document.

## Related canonical docs

- `docs/governance/AGENT_REGISTRY.md`
- `docs/responsible_ai/AI_INVENTORY.md`
- `docs/responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md`
- `docs/06_llm_gateway/PROMPT_REGISTRY.md`
- `docs/06_llm_gateway/MODEL_ROUTING.md`
- `docs/06_llm_gateway/SCHEMA_VALIDATION.md`
- `docs/10_tests/AGENT_TESTS.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/INCIDENT_RESPONSE.md`
- `docs/governance/PDPL_DATA_RULES.md`
