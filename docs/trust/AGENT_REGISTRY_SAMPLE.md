# Agent Registry — Sample — سجل الوكلاء (عيّنة)

> **Sample — illustrative entries.** This is the format Dealix uses to declare every deployed agent. Each customer engagement maintains its own registry; this sample is for review only.
>
> **عيّنة توضيحية.** هذا التنسيق الذي يستخدمه ديلكس لتسجيل كل وكيل منشور. لكل ارتباط عميل سجل خاص؛ هذه العيّنة للمراجعة فقط.

---

## 1. Registry Summary Table — جدول ملخّص السجل

| agent_id | Owner | Capability Scope | Approval Class | Kill-Switch Owner | Last Audit |
|---|---|---|---|---|---|
| `revenue_hunter` | Commercial Lead | Inbound discovery, opportunity drafting, no external send | Reviewer | Founder | 2026-05-12 |
| `trust_agent` | Risk & Compliance | Policy compliance checks, evidence pack assembly | Reviewer | Founder | 2026-05-12 |
| `proposal_drafter` | Sales Ops | Proposal drafting from approved templates; no send | Reviewer | Founder | 2026-05-10 |
| `follow_up_agent` | Commercial Lead | Internal reminders only; external messages require explicit approval | Founder | Founder | 2026-05-08 |
| `evidence_pack_assembler` | Risk & Compliance | Assemble Evidence Pack from logged artifacts | Auto | Founder | 2026-05-12 |

---

## 2. Detailed Entries — البطاقات التفصيلية

### 2.1 `revenue_hunter`

```yaml
agent_id: revenue_hunter
display_name: "Revenue Hunter"
owner: Commercial Lead
capability_scope:
  - Inbound discovery research from public sources
  - Opportunity drafting against internal templates
  - Pipeline annotation in CRM (write access via Reviewer approval)
tool_permissions:
  ref: TOOL_PERMISSION_MATRIX_SAMPLE.md#revenue_hunter
data_boundaries:
  classes_allowed: [public, internal, customer_tenant]
  classes_forbidden: [regulated, secret]
  residency: KSA
approval_class: Reviewer
kill_switch_owner: Founder
last_audit_date: 2026-05-12
incidents_open: 0
```

### 2.2 `trust_agent`

```yaml
agent_id: trust_agent
display_name: "Trust Agent"
owner: Risk & Compliance
capability_scope:
  - Policy compliance checks on agent actions
  - Evidence Pack drafting from log sources
  - Flag-raising on PDPL or boundary violations
tool_permissions:
  ref: TOOL_PERMISSION_MATRIX_SAMPLE.md#trust_agent
data_boundaries:
  classes_allowed: [public, internal, customer_tenant, regulated]
  classes_forbidden: [secret]
  residency: KSA
approval_class: Reviewer
kill_switch_owner: Founder
last_audit_date: 2026-05-12
incidents_open: 0
```

### 2.3 `proposal_drafter`

```yaml
agent_id: proposal_drafter
display_name: "Proposal Drafter"
owner: Sales Operations
capability_scope:
  - Generate proposal drafts from approved templates
  - Populate variables from CRM (read-only)
  - Output to internal storage only; no external send
tool_permissions:
  ref: TOOL_PERMISSION_MATRIX_SAMPLE.md#proposal_drafter
data_boundaries:
  classes_allowed: [public, internal, customer_tenant]
  classes_forbidden: [regulated, secret]
  residency: KSA
approval_class: Reviewer
kill_switch_owner: Founder
last_audit_date: 2026-05-10
incidents_open: 0
```

### 2.4 `follow_up_agent`

```yaml
agent_id: follow_up_agent
display_name: "Follow-up Agent"
owner: Commercial Lead
capability_scope:
  - Internal reminders for pending actions
  - Draft external follow-up messages (never send autonomously)
  - Surface stuck items to the human operator
tool_permissions:
  ref: TOOL_PERMISSION_MATRIX_SAMPLE.md#follow_up_agent
data_boundaries:
  classes_allowed: [internal, customer_tenant]
  classes_forbidden: [regulated, secret]
  residency: KSA
approval_class: Founder
kill_switch_owner: Founder
last_audit_date: 2026-05-08
incidents_open: 0
note: External send requires Founder-class approval per action.
```

### 2.5 `evidence_pack_assembler`

```yaml
agent_id: evidence_pack_assembler
display_name: "Evidence Pack Assembler"
owner: Risk & Compliance
capability_scope:
  - Collect logged artifacts (scope memo, registry snapshot, permission snapshot)
  - Compile approvals log, outcome graph excerpt, attribution table
  - Produce Evidence Pack PDF/MD bundle
tool_permissions:
  ref: TOOL_PERMISSION_MATRIX_SAMPLE.md#evidence_pack_assembler
data_boundaries:
  classes_allowed: [internal, customer_tenant, regulated]
  classes_forbidden: [secret]
  residency: KSA
approval_class: Auto
kill_switch_owner: Founder
last_audit_date: 2026-05-12
incidents_open: 0
```

---

## 3. Registry Rules — قواعد السجل

- No agent runs in production without an entry in this registry.
- Capability scope is enumerative; anything not listed is not permitted.
- Approval class downgrades (Founder → Reviewer → Auto) require founder sign-off.
- Last audit date older than 90 days suspends the agent automatically.
- Kill-switch ownership defaults to the founder office; delegations are explicit and logged.

**AR.** لا يعمل وكيل في الإنتاج دون مدخل في السجل. النطاق حصري؛ ما لم يُذكر لا يُسمح به. تخفيض فئة الموافقة يستوجب اعتماد المؤسس. تاريخ تدقيق أقدم من 90 يومًا يوقف الوكيل تلقائيًا. ملكية مفتاح الإيقاف افتراضيًا لدى مكتب المؤسس، وأي تفويض صريح ومُسجَّل.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md` · `/home/user/dealix/docs/trust/AI_USE_POLICY_SAMPLE.md` · `/home/user/dealix/docs/trust/EVIDENCE_PACK_SAMPLE.md`
