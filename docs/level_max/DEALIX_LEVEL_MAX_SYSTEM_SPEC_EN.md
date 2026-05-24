# Dealix — Level Max System Spec (EN)

> This document is the **sovereign reference** for Dealix as a complete system:
> a Control Plane, not just an app.
> The Python implementation in `dealix/control_plane/` mirrors sections 51–80
> line-for-line. Any change to the system must start here, then reflect into
> code and tests.

Absolute sovereignty belongs to **Sami** — no Agent, Tool, or partner may
override this layer.

---

## 51. The system must be a Control Plane, not just an app

**The strongest framing:**

> Dealix ≠ App
> Dealix = Control Plane

Dealix is not a screen full of leads and proposals; it is a control layer
sitting above:

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

Agentic AI needs continuous governance, not just prompts. The AAGATE research
model proposes agentic AI governance as a control plane built on zero-trust, a
policy engine, behavioural analytics, and accountability hooks aligned with the
NIST AI RMF — Dealix follows this principle.

**Shape:**

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

## 52. Identity & Access

Identities are first-class. Eight kinds, six sovereignty tiers, explicit
permissions.

### Identity kinds

1. **Sami** — highest authority, Sovereign Owner.
2. **Internal Operator** — internal helpers.
3. **Customer Admin** — customer account owner.
4. **Customer User** — restricted seat in the customer account.
5. **Partner Admin** — partner or agency lead.
6. **Agent Identity** — every Agent has an identity.
7. **Tool Identity** — every Tool has an identity.
8. **API Client** — future external integrations.

### Sovereignty rule

```
Sami > Internal > Customer > Partner > Agent > Tool
```

No Agent or Tool overrides Sami.

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

### Hard rules

- `approve_external_action` = Sami or an explicitly delegated identity only.
- `enable_tool` = Sami only.
- `launch_api` = Sami only.
- `export_sensitive_data` = blocked by default; requires sovereign memo.

---

## 53. Tenant & Workspace Model

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

### Workspace kinds

- `sovereign_workspace`
- `internal_dealix_workspace`
- `customer_workspace`
- `partner_workspace`
- `trust_workspace`
- `venture_workspace`
- `marketplace_workspace`

Every signal, opportunity, outcome, and asset must carry `tenant_id`,
`workspace_id`, `owner_id`, and `sensitivity_level`.

---

## 54. Data Classification

Five classes: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, `SOVEREIGN`.

| Class | Who sees | Agent feed | External exit |
|---|---|---|---|
| PUBLIC | as needed | yes | yes |
| INTERNAL | Dealix only | yes (bounded) | only with approval |
| CONFIDENTIAL | specific workspace | yes (scoped) | only with approval |
| RESTRICTED | very limited | only cleared agents | usually blocked |
| SOVEREIGN | Sami only | only sovereign agents | no |

**Golden rule:** every Agent receives the *least* context possible.

---

## 55. Context Feed Engine

No raw, unrestricted context. Only scoped `ContextPacket`s — built per
`(agent_id, purpose)` and stamped with sensitivity, allowed_use, expiry, and
workspace.

---

## 56. Context Packet Format

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

---

## 57. Memory System

Seven memory kinds: Personal, Company, Customer, Partner, Outcome, Market,
Trust. Outcome Memory is the most commercially important; Personal/Sovereign
Memory is the most sensitive.

---

## 58. Policy Engine

Named, typed, data-driven policies. Categories: Sovereignty, Data, Tool,
External Action, Pricing, Partner, Customer Data, MCP, Marketplace.

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

---

## 59. Approval Center

Every escalation materialises as an `ApprovalCard`:

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

Buttons: Approve · Deny · Request Changes · Escalate to Sovereign Memo · Kill.

---

## 60. Audit & Evidence

`AuditEvent`s record every meaningful action. Eight triggers create full
`EvidencePack`s: enterprise proposal, AI Trust Kit, MCP review, partner
agreement, new vertical, public API, marketplace, sensitive data workflow.

Each pack contains: decision, context, signals, opportunity score,
alternatives, risks, policies applied, trust checks, approvals, recommended
action.

---

## 61. Agent Runtime Lifecycle

```
Created → Context Loaded → Policy Checked → Tools Authorized
→ Executing → Guardrails Applied → Output Validated → Trust Checked
→ Approval Requested if needed → Outcome Required → Completed / Blocked
```

A run cannot be marked `COMPLETED` while its `outcome_required` flag is true
and no outcome was logged.

---

## 62. Tool Runtime Lifecycle

```
Requested → Tool Registry Check → Permission Check → Data Scope Check
→ Approval if needed → Execute / Block → Audit → Outcome
```

MCP standardised tool access for models but also opened risks: prompt
injection, layered tool permissions leaking data, lookalike tools replacing
trusted ones. Registry, approval, and audit are not optional.

---

## 63. MCP Gateway

```
Agent → Hermes Tool Gateway → MCP Gateway → Approved MCP Server
→ Tool Call → Audit
```

Capabilities: server allowlist, manifest hash check, tool descriptor scan,
semantic vetting, data scope enforcement, per-call approval, runtime anomaly
detection, kill switch.

Recent MCP research focused on Tool Poisoning, Shadowing, and Rug Pulls;
manifest signing, semantic vetting, and runtime guardrails are the mitigations.

---

## 64. Security Modes

1. **Draft-Only** — no external sends, no high-risk tools. *Start here.*
2. **Approval-Gated** — externals only after approval.
3. **Low-Risk Autonomy** — low-risk allowlist runs automatically.
4. **Enterprise Controlled** — per-customer policies, full audit, evidence packs.
5. **Sovereign Lockdown** — all externals + tools off, read-only.

Only Sami may switch modes. Do not exit Draft-Only until audit + outcomes are
proven.

---

## 65. Incident Response

Types: `prompt_injection_detected`, `tool_policy_violation`,
`sensitive_data_attempt`, `unapproved_external_action`, `overclaim_detected`,
`mcp_descriptor_changed`, `agent_behavior_anomaly`,
`customer_data_boundary_violation`.

Flow: Detect → Block → Log → Notify Sami → Evidence Pack → Remediate →
Policy Update → Asset/Learning.

---

## 66. Money Command System

A "CFO + Head of Sales" surface. Tracks Deal Rooms, computes
probability-weighted expected revenue (`deal_value × close_probability`), and
recommends the **best next action**.

---

## 67. Offer System

States: draft, internal_review, pilot_ready, active, productized, scaled,
paused, retired. No offer leaves `internal_review` without: buyer, pain,
promise, deliverables, price, metric, upsell, trust risks.

---

## 68. Asset Library

Types: message_template, proposal_template, objection_playbook, case_study,
training_deck, policy_template, sector_kit, partner_pack, workflow_template,
agent_template, market_report. An asset that earns money becomes a Product.

---

## 69. Intelligence Graph

Dealix's accumulating brain. Nodes: signals, opportunities, offers, customers,
partners, sectors, messages, proposals, outcomes, assets, agents, tools,
risks. Edges record causal relationships and revenue impact.

---

## 70. Scale/Kill Operating Board

Decisions: which offers, agents, tools, partners, verticals, and assets to
**scale**, **pause**, or **kill**. Kill reasons: no demand, low margin, high
risk, high delivery burden, no data moat, no channel, too much founder time.

---

## 71. Customer Value Loop

Onboard → Define outcomes → Execute → Log outcomes → Monthly value report →
Renewal/upsell → Case study. The Customer Value Report converts the
relationship into a monthly cadence.

---

## 72. Partner Value Loop

Scout → Fit Score → Pitch → Agreement → Onboard → First client → Revenue
share → Performance review → Scale or remove. Every white-label partner output
passes a Trust Check.

---

## 73. Venture Value Loop

Sector signal → Pain map → Offer → First 50 targets → Pilot → Outcomes →
Assets → Scale/Kill. No vertical product is built before *real replies*, clear
pain, defined offer, target list, and outcomes.

---

## 74. Public API Readiness

Checklist: auth, rate limits, billing, tenant isolation, audit, abuse
detection, terms, kill switch, developer docs, **S4 approval**.

API products to follow: Trust Check API, Opportunity Score API, Proposal API,
Evidence Pack API, Outcome API, Pricing API, Partner Match API.

---

## 75. Marketplace Readiness

Checklist: asset quality review, trust review, versioning, payments, partner
agreements, refund/dispute policy, ratings, liability limits, security review,
**S4 approval**.

Listings: agent template, workflow, policy pack, training kit, sector kit,
MCP connector, partner service.

---

## 76. UI Design Philosophy

Command-first UI. Every screen answers: *What is happening? What must I do?
What is the risk? What is the result? What is the decision?* Sections:
Action Required · Recommended Next Actions · Risks · Outcomes · Assets ·
Approvals.

---

## 77. System Health Dashboard

Metrics: signals captured, opportunities created, executions completed,
outcomes logged, assets created, approvals pending, risks blocked, agent runs,
tool calls, cost, latency, revenue influenced.

Red flags: executions without outcomes, external actions without approval,
tools without owner, agents without KPIs, assets not reused, customers
without value reports, partners without revenue.

---

## 78. Commercial Packaging

Inside complex; outside simple.

- **Entry:** Revenue Hunter Pilot · AI Trust Kit · Agency White-label Kit.
- **Expansion:** Founder OS · Market Radar · Executive PMO · Partner OS ·
  Customer Health OS · AI Governance OS.
- **Enterprise:** Governed AI Workforce · Agent Governance OS · Executive
  Agentic PMO · AI Control Plane.

---

## 79. The system in one sentence

> **Dealix is a sovereign control plane that turns signals into governed
> execution, measurable outcomes, reusable assets, and scalable revenue.**

---

## 80. Strongest condensed form

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

This is the full system: not a product, not a bundle of agents — sovereignty +
governance + money + data + assets + scale. **Without stopping, ever.**
