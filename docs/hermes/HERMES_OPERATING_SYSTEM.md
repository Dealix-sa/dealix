# Hermes Agents Operating System

Hermes is the Dealix founder operating layer. It organizes agent roles, governance, review cadence, artifacts, and implementation phases so the system can grow safely from review-only intelligence into approved operational workflows.

## Design principles

1. Founder benefit first: every agent must produce a useful artifact or decision aid.
2. Review-first operation: Hermes starts by preparing recommendations and evidence, not by changing live systems.
3. Strong separation of duties: revenue, operations, security, product, finance, and content agents have distinct roles.
4. Provider resilience: route model calls through the AI gateway and fallback configuration.
5. Traceability: every run should leave a durable artifact.
6. Saudi/GCC specialization: prioritize Dealix verticals and founder workflows.

## Agent layers

### Layer 1: Supervisor

The Hermes Supervisor receives signals from all agents, ranks priorities, and prepares founder-facing summaries.

Primary outputs:

- Daily founder digest.
- Weekly priority queue.
- Escalation summary.
- Cross-agent conflict notes.

### Layer 2: Commercial agents

Commercial agents focus on revenue, proposals, content, market intelligence, and customer proof.

Agents:

- Revenue Scout.
- Proposal Architect.
- Market Intel Analyst.
- Content Growth Operator.
- Finance Unit Economics Agent.

### Layer 3: Reliability agents

Reliability agents protect the repo, product quality, release readiness, and compliance posture.

Agents:

- Ops Guardian.
- Security Compliance Sentinel.
- Product QA Agent.

## Review-first workflow

```text
Signal -> Agent review -> Artifact -> Supervisor summary -> Founder decision -> Issue/PR/manual task
```

Hermes should not hide decisions. The output of every run should be readable by the founder without needing to inspect logs.

## Artifact contract

Each artifact should include:

- `agent_id`
- `run_id`
- `created_at`
- `input_scope`
- `finding`
- `confidence`
- `risk_level`
- `recommended_next_step`
- `evidence`

## Implementation phases

### Phase 0: Foundation

- Manifest.
- Governance policy.
- Cadence plan.
- Local verifier.
- Review-only runner.

### Phase 1: Local artifacts

- Generate daily digest drafts.
- Generate review records.
- Keep outputs local or as CI artifacts.

### Phase 2: Pull-request intelligence

- Add PR review summaries.
- Add regression checklist suggestions.
- Add security notes as review artifacts.

### Phase 3: Founder cockpit

- Add dashboard data files.
- Add charts for opportunity status, review backlog, cost, and readiness.

### Phase 4: Approved workflows

Only after the review layer is reliable, add approved workflows for specific low-risk tasks. Keep higher-risk items manual.

## Agent selection strategy

| Work type | Recommended agent | Model alias |
| --- | --- | --- |
| Code and test review | Product QA Agent | dealix-code |
| Architecture and business logic | Hermes Supervisor | dealix-smart |
| Revenue watchlist | Revenue Scout | dealix-code |
| Proposal drafting | Proposal Architect | dealix-smart |
| Market notes | Market Intel Analyst | dealix-fast |
| Content drafts | Content Growth Operator | dealix-fast |
| Cost and pricing notes | Finance Unit Economics Agent | dealix-smart |
| Security and policy notes | Security Compliance Sentinel | dealix-smart |

## What “24/7” means at this stage

Hermes can run continuously as a review and monitoring layer:

- Check signals.
- Produce artifacts.
- Rank priorities.
- Prepare founder decisions.
- Track unresolved items.

It should not perform irreversible or customer-facing actions without an explicit approval workflow.

## Next implementation targets

1. Add JSONL review store.
2. Add daily digest generator.
3. Add PR review generator.
4. Add cost telemetry adapter.
5. Add optional LangGraph review checkpoints.
6. Add optional Agents SDK guardrail hooks.
7. Add founder cockpit data export.
