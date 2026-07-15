# Dealix — Level Max System Spec (AR)

> هذه الوثيقة هي **المرجع السيادي** لبنية Dealix كنظام كامل: Control Plane وليس مجرد تطبيق.
> الكود في `dealix/control_plane/` يطبّق هذه الأقسام (51–80) حرفاً حرفاً، سطراً سطراً.
> أي تغيير في النظام يجب أن يبدأ من هنا، ثم ينعكس في الكود والاختبارات.

السيادة المطلقة لـ **سامي** — لا Agent ولا Tool ولا شريك يتجاوز هذه الطبقة.

---

## 51. النظام لازم يكون Control Plane وليس App فقط

**الفكرة الأقوى:**

> Dealix ≠ تطبيق
> Dealix = Control Plane

يعني Dealix لا يكون مجرد شاشة فيها leads وproposals. يكون طبقة تحكم فوق:

- Agents
- Tools
- Data
- Approvals
- Customers
- Partners
- Products
- Outcomes
- Assets
- Ventures

هذا مهم لأن agentic AI الحقيقي يحتاج حوكمة مستمرة، وليس مجرد تشغيل prompt.
نموذج AAGATE البحثي يطرح agentic AI governance كـ control plane مبني على
zero-trust، policy engine، behavioral analytics، وaccountability hooks،
ومتوافق مع NIST AI RMF. هذا يؤكد أن Dealix يجب أن يُبنى كطبقة تحكم لا كمساعد عادي.

**الشكل:**

```
Sami Sovereign Console
└── Dealix Control Plane
    ├── Agent Control
    ├── Tool Control
    ├── Data Control
    ├── Approval Control
    ├── Outcome Control
    ├── Asset Control
    └── Commercial Control
```

---

## 52. طبقة Identity & Access

لازم من البداية يكون عندك نظام هويات وصلاحيات.

### أنواع الهويات

1. **Sami** — أعلى صلاحية، Sovereign Owner.
2. **Internal Operator** — شخص يساعدك داخلياً لاحقاً.
3. **Customer Admin** — مسؤول حساب العميل.
4. **Customer User** — مستخدم محدود داخل حساب العميل.
5. **Partner Admin** — مسؤول شريك أو وكالة.
6. **Agent Identity** — كل Agent له identity.
7. **Tool Identity** — كل tool له identity.
8. **API Client** — لاحقاً للتكاملات.

### قاعدة السيادة

```
Sami > Internal > Customer > Partner > Agent > Tool
```

ولا يوجد أي Agent أو Tool يتجاوز Sami.

### Permissions

- `read_signal`
- `create_opportunity`
- `draft_message`
- `create_proposal`
- `request_approval`
- `approve_external_action`
- `register_tool`
- `enable_tool`
- `export_data`
- `launch_api`
- `launch_marketplace`

### أهم قاعدة

- `approve_external_action` = Sami أو من تفوضه صراحة فقط
- `enable_tool` = Sami فقط
- `launch_api` = Sami فقط
- `export_sensitive_data` = ممنوع تلقائياً إلا بمذكرة سيادية

---

## 53. Tenant & Workspace Model

النظام لازم يكون جاهز للتوسع بدون اختلاط بيانات.

### الهيكل

```
Tenant
├── Workspace
│   ├── Users
│   ├── Agents
│   ├── Tools
│   ├── Data
│   ├── Opportunities
│   ├── Outcomes
│   └── Assets
```

### أنواع الـ Workspaces

- `sovereign_workspace`
- `internal_dealix_workspace`
- `customer_workspace`
- `partner_workspace`
- `trust_workspace`
- `venture_workspace`
- `marketplace_workspace`

### القاعدة

كل signal وopportunity وoutcome وasset لازم يكون له:

- `tenant_id`
- `workspace_id`
- `owner_id`
- `sensitivity_level`

### لماذا؟

حتى إذا كبرت Dealix وصار عندك عملاء وشركاء وwhite-label، لا تختلط البيانات ولا الصلاحيات.

---

## 54. Data Classification

كل بيانات تدخل النظام لازم تصنف.

### مستويات البيانات

- **PUBLIC** — محتوى عام، أخبار، صفحات عامة.
- **INTERNAL** — تشغيل داخلي لديلكس.
- **CONFIDENTIAL** — بيانات عميل أو شريك.
- **RESTRICTED** — بيانات حساسة، عقود، مالية، بيانات شخصية، مفاتيح API.
- **SOVEREIGN** — قرارات سامي، الاستراتيجية، الصلاحيات العليا، العلاقات الحساسة.

### قواعد البيانات

| المستوى | من يراه؟ | هل يدخل Agent؟ | هل يخرج خارجياً؟ |
|---|---|---|---|
| PUBLIC | حسب الحاجة | نعم | نعم |
| INTERNAL | Dealix فقط | نعم بضوابط | لا إلا بموافقة |
| CONFIDENTIAL | Workspace محدد | نعم بسياق محدود | لا إلا بموافقة |
| RESTRICTED | محدود جداً | فقط agents مصرحين | ممنوع غالباً |
| SOVEREIGN | سامي فقط | لا إلا sovereign agents | لا |

### القاعدة الذهبية

> كل Agent يأخذ أقل سياق ممكن، وليس كل السياق.

---

## 55. Context Feed Engine

هذه من أهم الطبقات.

### المشكلة

إذا أعطيت الوكيل كل شيء، يزيد الخطر والهلوسة والتسريب.

### الحل

**Context Feed Engine** — يعطي كل Agent فقط ما يحتاجه.

### مثال

- **RevenueHunterAgent** يأخذ: sector، ICP، offer، previous winning messages، allowed lead sources، pricing range.
- **ProposalFactoryAgent** يأخذ: approved opportunity، offer card، pricing boundaries، delivery terms، exclusions، trust constraints.
- **TrustAgent** يأخذ: action payload، data sensitivity، agent card، tool card، policy rules.
- **SovereignBriefAgent** يأخذ: top opportunities، pending approvals، risks، cash actions، scale/kill recommendations.

### القاعدة

```
No raw unrestricted context.
Only scoped context packets.
```

---

## 56. Context Packet Format

كل Agent لا يأخذ DB عشوائي. يأخذ **Context Packet**.

```json
{
  "context_id": "ctx_001",
  "agent_id": "proposal_factory",
  "purpose": "draft_proposal",
  "sensitivity": "CONFIDENTIAL",
  "allowed_use": ["draft_only"],
  "expires_at": "timestamp",
  "data": {
    "opportunity": {},
    "offer": {},
    "pricing_limits": {},
    "trust_constraints": []
  }
}
```

### ضمانات

- `expires_at`
- `allowed_use`
- `sensitivity`
- `workspace_id`
- audit trail

---

## 57. Memory System

لازم تفرق بين أنواع الذاكرة.

### أنواع الذاكرة

1. **Personal Memory** — تفضيلات سامي، أسلوبه، قراراته.
2. **Company Memory** — استراتيجية Dealix، العروض، الأسعار، playbooks.
3. **Customer Memory** — لكل عميل، لا تختلط.
4. **Partner Memory** — لكل شريك.
5. **Outcome Memory** — ما نجح وما فشل.
6. **Market Memory** — إشارات السوق والقطاعات.
7. **Trust Memory** — المخاطر، incidents، approvals.

### القاعدة

- **Outcome Memory** هي الأهم تجارياً.
- **Personal/Sovereign Memory** هي الأكثر حساسية.

---

## 58. Policy Engine

لا تعتمد على if statements مبعثرة. ابنِ **Policy Engine**.

### أنواع السياسات

- Sovereignty Policy
- Data Policy
- Tool Policy
- External Action Policy
- Pricing Policy
- Partner Policy
- Customer Data Policy
- MCP Policy
- Marketplace Policy

### مثال Policy

```json
{
  "policy_id": "external_action_policy_v1",
  "if": { "external_action": true },
  "then": {
    "requires_approval": true,
    "approval_role": "Sami",
    "audit_required": true,
    "outcome_required": true
  }
}
```

### لماذا؟

لأنك لاحقاً بتضيف أدوات ووكلاء وشركاء. لو الصلاحيات مبعثرة، النظام ينهار.

---

## 59. Approval Center

Approval Center هو **صمام الأمان**.

### أنواع الموافقات

- External message approval
- Proposal approval
- Pricing approval
- Partner agreement approval
- Tool activation approval
- MCP server approval
- Sensitive data workflow approval
- Public API approval
- Marketplace listing approval

### Approval Card

```json
{
  "approval_id": "appr_001",
  "requested_by": "proposal_factory",
  "action_type": "external_proposal",
  "sovereignty_level": "S2_SAMI_APPROVAL",
  "risk_level": "medium",
  "summary": "Proposal for Agency White-label Kit",
  "payload_preview": {},
  "trust_check": {},
  "evidence_pack_id": null,
  "decision": "pending"
}
```

### أزرار

- Approve
- Deny
- Request Changes
- Escalate to Sovereign Memo
- Kill Workflow

---

## 60. Audit & Evidence

كل شيء مهم يجب أن يترك أثراً.

### Audit Event

```json
{
  "audit_id": "aud_001",
  "actor_type": "agent",
  "actor_id": "proposal_factory",
  "action_type": "draft_proposal",
  "tool_id": null,
  "risk_level": "medium",
  "sovereignty_level": "S2_SAMI_APPROVAL",
  "result": "approval_requested",
  "timestamp": "..."
}
```

### Evidence Pack

ينشأ عند:

- Enterprise proposal
- AI Trust Kit
- MCP Review
- Partner agreement
- New vertical
- Public API
- Marketplace
- Sensitive data workflow

### Evidence Pack يحتوي

- decision
- context
- signals
- opportunity score
- alternatives
- risks
- policies applied
- trust checks
- approvals
- recommended action

---

## 61. Agent Runtime Lifecycle

كل Agent Run لازم له lifecycle واضح.

```
Created
→ Context Loaded
→ Policy Checked
→ Tools Authorized
→ Execution Started
→ Guardrails Applied
→ Output Validated
→ Trust Checked
→ Approval Requested if needed
→ Outcome Required
→ Completed / Blocked
```

### Agent Run Object

```json
{
  "run_id": "run_001",
  "agent_id": "revenue_hunter",
  "workspace_id": "dealix_internal",
  "input_hash": "...",
  "context_id": "ctx_001",
  "tools_requested": [],
  "tools_allowed": [],
  "guardrails_result": "passed",
  "trust_result": "passed",
  "approval_status": "not_required",
  "output_id": "outp_001",
  "outcome_required": true,
  "status": "completed"
}
```

---

## 62. Tool Runtime Lifecycle

كل Tool Call لازم له lifecycle.

```
Requested
→ Tool Registry Check
→ Permission Check
→ Data Scope Check
→ Approval if needed
→ Execute / Block
→ Audit
→ Outcome
```

### Tool Call Object

```json
{
  "tool_call_id": "tc_001",
  "tool_id": "gmail_send",
  "agent_id": "followup_agent",
  "risk_level": "high",
  "data_scope": "customer_workspace",
  "approval_required": true,
  "status": "blocked_pending_approval"
}
```

MCP أصبح معياراً متزايد الاستخدام لربط النماذج بالأدوات والأنظمة، لكن هذا
يفتح مخاطر مثل prompt injection، tool permissions المركبة التي قد تؤدي
لتسريب بيانات، وlookalike tools التي تستبدل أدوات موثوقة؛ لذلك registry
وapproval وaudit ليست رفاهية.

---

## 63. MCP Gateway

لا تجعل كل Agent يتصل بـ MCP مباشرة.

### الشكل الصحيح

```
Agent
→ Hermes Tool Gateway
→ MCP Gateway
→ Approved MCP Server
→ Tool Call
→ Audit
```

### MCP Gateway يفعل

- server allowlist
- manifest/hash check
- tool descriptor scan
- semantic vetting
- data scope enforcement
- per-call approval
- runtime anomaly detection
- kill switch

أبحاث MCP الحديثة ركزت على Tool Poisoning وShadowing وRug Pulls،
واقترحت manifest signing، semantic vetting، وruntime guardrails
لتقليل استدعاء الأدوات غير الآمنة.

---

## 64. Security Modes

النظام يحتاج أوضاع تشغيل.

### Mode 1 — Draft-Only

- لا إرسال خارجي
- لا tool execution خطير
- كل شيء drafts
- **أفضل وضع البداية**

### Mode 2 — Approval-Gated

- يسمح بأفعال خارجية فقط بعد موافقة

### Mode 3 — Low-Risk Autonomy

- أفعال منخفضة الخطر ضمن allowlist

### Mode 4 — Enterprise Controlled

- سياسات لكل عميل
- audit كامل
- evidence packs

### Mode 5 — Sovereign Lockdown

- إيقاف كل external actions
- إيقاف tools
- تشغيل read-only

### القاعدة

> ابدأ بـ **Draft-Only**.
> لا تنتقل إلى Approval-Gated إلا بعد ثبوت الـ audit والـ outcomes.

---

## 65. Incident Response

لازم يكون عندك **incident system**.

### Incident Types

- `prompt_injection_detected`
- `tool_policy_violation`
- `sensitive_data_attempt`
- `unapproved_external_action`
- `overclaim_detected`
- `mcp_descriptor_changed`
- `agent_behavior_anomaly`
- `customer_data_boundary_violation`

### Incident Flow

```
Detect
→ Block
→ Log
→ Notify Sami
→ Evidence Pack
→ Remediate
→ Policy Update
→ Asset/Learning
```

### Incident Object

```json
{
  "incident_id": "inc_001",
  "type": "overclaim_detected",
  "severity": "high",
  "agent_id": "proposal_factory",
  "action_id": "exe_001",
  "blocked": true,
  "recommended_fix": "Rewrite claim as non-guaranteed outcome.",
  "created_at": "..."
}
```

---

## 66. Money Command System

Money Command ليس dashboard عادي. هو **"CFO + Head of Sales"**.

### يعرض

- cash now
- pipeline
- expected revenue
- probability weighted revenue
- open proposals
- stuck deals
- pending payments
- upsells
- partner revenue
- best next action

### Probability Weighted Revenue

```
Expected Revenue = Deal Value × Close Probability
```

### Deal Room لكل صفقة

```json
{
  "deal_id": "deal_001",
  "target": "Agency X",
  "offer": "Agency White-label Kit",
  "deal_value_sar": 20000,
  "floor_price_sar": 5000,
  "target_price_sar": 15000,
  "pain": "Needs AI offer for clients",
  "objections": [],
  "next_step": "Send proposal",
  "walkaway_conditions": [
    "requires exclusivity",
    "asks for data ownership",
    "wants unsupported guarantees"
  ]
}
```

---

## 67. Offer System

Offer هو **وحدة أساسية**.

### Offer States

- `draft`
- `internal_review`
- `pilot_ready`
- `active`
- `productized`
- `scaled`
- `paused`
- `retired`

### Offer Metrics

- views
- messages_sent
- replies
- calls
- proposals
- wins
- losses
- revenue
- delivery_time
- margin
- assets_created

### Offer Rule

أي Offer لا يملك: `buyer`, `pain`, `promise`, `deliverables`, `price`, `metric`, `upsell`, `trust risks` — **لا يخرج**.

---

## 68. Asset Library

هذه **مكتبة الأصول**.

### أنواع الأصول

- `message_template`
- `proposal_template`
- `objection_playbook`
- `case_study`
- `training_deck`
- `policy_template`
- `sector_kit`
- `partner_pack`
- `workflow_template`
- `agent_template`
- `market_report`

### Asset Score

- `reuse_count`
- `revenue_influenced`
- `conversion_impact`
- `quality_score`
- `trust_score`
- `commercializable`

### القاعدة

- Asset بلا استخدام يعاد تقييمه.
- Asset يجيب فلوس يتحول Product.

---

## 69. Intelligence Graph

هذا **عقل Dealix التراكمي**.

### Nodes

- signals
- opportunities
- offers
- customers
- partners
- sectors
- messages
- proposals
- outcomes
- assets
- agents
- tools
- risks

### Edges

- `signal_created_opportunity`
- `opportunity_used_offer`
- `offer_generated_proposal`
- `proposal_led_to_outcome`
- `outcome_created_asset`
- `partner_generated_customer`
- `agent_used_tool`
- `tool_created_risk`

### أسئلة يجاوب عليها

- ما أفضل قطاع؟
- ما أفضل رسالة؟
- ما العرض الأكثر ربحاً؟
- من أفضل شريك؟
- أي Agent ينتج مال؟
- أي Tool خطر؟
- أي اعتراض يتكرر؟
- أي سعر يقبل السوق؟

---

## 70. Scale/Kill Operating Board

هذه **صفحة قرارات**.

### تعرض

- Offers to scale
- Offers to pause
- Agents to improve
- Tools to disable
- Partners to double down
- Verticals to test
- Verticals to kill
- Assets to productize

### Scale Score

- `revenue_score`
- `repeatability_score`
- `margin_score`
- `data_moat_score`
- `partner_score`
- `trust_score`
- `delivery_score`

### Kill Reasons

- no demand
- low margin
- high risk
- high delivery burden
- no data moat
- no channel
- too much founder time

---

## 71. Customer Value Loop

لكل عميل:

```
Onboard
→ Define desired outcomes
→ Execute
→ Log outcomes
→ Monthly value report
→ Renewal/upsell
→ Case study
```

### Customer Value Report يجب أن يحتوي

- activities
- outputs
- outcomes
- estimated value
- risks reduced
- assets created
- next actions
- upsell recommendation

هذا يحول العميل إلى **علاقة شهرية**.

---

## 72. Partner Value Loop

لكل شريك:

```
Scout
→ Fit Score
→ Pitch
→ Agreement
→ Onboard
→ First client
→ Revenue share
→ Performance review
→ Scale or remove
```

### Partner Risk

- brand risk
- delivery risk
- data risk
- claim risk
- commercial risk

كل شريك white-label لازم تمر مخرجاته **Trust Check**.

---

## 73. Venture Value Loop

لكل vertical:

```
Sector signal
→ Pain map
→ Offer
→ First 50 targets
→ Pilot
→ Outcomes
→ Assets
→ Scale/Kill
```

### Venture Rule

لا تبني منتج vertical قبل: ردود حقيقية، ألم واضح، عرض مفهوم، قائمة leads، outcomes.

---

## 74. Public API Readiness

قبل public API:

- auth
- rate limits
- billing
- tenant isolation
- audit
- abuse detection
- terms
- kill switch
- developer docs
- **S4 approval**

### API Products لاحقاً

- Trust Check API
- Opportunity Score API
- Proposal API
- Evidence Pack API
- Outcome API
- Pricing API
- Partner Match API

---

## 75. Marketplace Readiness

قبل marketplace:

- asset quality review
- trust review
- versioning
- payments
- partner agreements
- refund/dispute policy
- ratings
- liability limits
- security review
- **S4 approval**

### Marketplace Listings

- Agent template
- Workflow
- Policy pack
- Training kit
- Sector kit
- MCP connector
- Partner service

---

## 76. UI Design Philosophy

لا تبدأ بواجهة ضخمة. ابدأ بـ **Command-first UI**.

### كل صفحة يجب أن تقول

- ما الذي يحدث؟
- ما الذي يجب أن أفعله؟
- ما الخطر؟
- ما النتيجة؟
- ما القرار؟

### أفضل UI Sections

- Action Required
- Recommended Next Actions
- Risks
- Outcomes
- Assets
- Approvals

---

## 77. System Health Dashboard

النظام نفسه يحتاج **health**.

### Metrics

- signals captured
- opportunities created
- executions completed
- outcomes logged
- assets created
- approvals pending
- risks blocked
- agent runs
- tool calls
- cost
- latency
- revenue influenced

### Red Flags

- executions بدون outcomes
- external actions بدون approval
- tools without owner
- agents without KPIs
- assets not reused
- customers without value reports
- partners without revenue

---

## 78. Commercial Packaging

داخلياً النظام ضخم. خارجياً بسيط.

### Entry Offers

- Revenue Hunter Pilot
- AI Trust Kit
- Agency White-label Kit

### Expansion Offers

- Founder OS
- Market Radar
- Executive PMO
- Partner OS
- Customer Health OS
- AI Governance OS

### Enterprise Offers

- Governed AI Workforce
- Agent Governance OS
- Executive Agentic PMO
- AI Control Plane

---

## 79. النهائي: كيف يكون النظام في جملة واحدة

> **Dealix is a sovereign control plane that turns signals into governed execution, measurable outcomes, reusable assets, and scalable revenue.**

وبالعربي:

> **Dealix هو طبقة سيادية تحوّل أي إشارة إلى تنفيذ محكوم، نتيجة مقاسة، أصل قابل لإعادة الاستخدام، وإيراد قابل للتوسع.**

---

## 80. أقوى نسخة مختصرة

```
Sami Sovereign Layer
→ Identity & Access
→ Data Classification
→ Context Feed
→ Policy Engine
→ Approval Center
→ Hermes Orchestrator
→ Agent Runtime
→ Tool Gateway
→ Outcome Graph
→ Asset Library
→ Money/Product/Partner/Market Engines
→ Scale/Kill Board
→ Platform/API/Marketplace/Ventures
```

هذا هو النظام الكامل.
ليس مجرد منتج.
ليس مجرد agents.
إنه **سيادة + حوكمة + مال + بيانات + أصول + توسع**. بدون توقف أبداً.
