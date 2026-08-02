# Dealix Company Loops Execution Spine

## Executive decision

Dealix will operate companies through governed cross-department loops, not through a collection of independent agents or dashboards.

The canonical lifecycle remains:

```text
Company Brain
→ Sources and Consent
→ Company / Contact / Signal Graph
→ Opportunity / Partnership
→ Department Plan
→ Action
→ Draft
→ Approval
→ Controlled Execution
→ Outcome
→ Proof
→ Learning
→ Daily Command
```

This slice adds the missing loop registry and a deterministic synthetic runner. It does not add a second Company Brain, CRM, ERP, scheduler, Approval Center, Proof Ledger, or agent framework.

## Why Lead-to-Cash is first

Lead-to-Cash is the shortest loop that proves Dealix can coordinate multiple departments and produce a result a company values:

- Market intelligence finds an evidence-backed signal.
- Sales qualifies and prepares discovery.
- Commercial governance approves external contact and terms.
- Operations receives a bounded delivery handoff.
- Finance records invoice and payment evidence.
- Customer success records value and expansion learning.
- Executive reporting receives a proof-backed command summary.

It also exercises the hardest trust gates:

- consent and channel eligibility;
- external-action approval;
- commercial-term approval;
- payment evidence before revenue recognition;
- delivery evidence before completion claims;
- learning from verified outcomes rather than invented metrics.

## Repository additions

### Loop registry

`dealix/registers/company_loops_registry.json`

The registry defines:

- loop ownership and priority;
- department handoffs;
- ordered stages;
- canonical entity inputs and outputs;
- event types;
- autonomy level;
- external-effect and approval requirements;
- proof requirements;
- recognition effects.

### Synthetic runner

`scripts/commercial/run_company_loop_simulation.py`

The first executable path is intentionally synthetic and network-free:

```bash
python scripts/commercial/run_company_loop_simulation.py \
  --loop lead_to_cash \
  --mode synthetic
```

The runner:

- creates deterministic IDs;
- marks every record synthetic;
- simulates approvals without sending anything;
- records OutcomeEvent and ProofEvent objects;
- refuses to recognize revenue without `payment_received` proof;
- refuses to claim completed delivery without `delivery_completed` proof;
- emits a LearningEvent and DailyCommand-ready summary;
- executes zero external actions.

Draft-only mode demonstrates the real safety behavior:

```bash
python scripts/commercial/run_company_loop_simulation.py \
  --loop lead_to_cash \
  --mode draft_only
```

It must stop at the first external-effect stage until approval is provided.

## Company-loop roadmap

| Priority | Loop | Departments | Product value |
|---|---|---|---|
| P0 | Lead-to-Cash | Market intelligence, sales, approvals, operations, finance, customer success, executive | Converts opportunities into collected payment and proof |
| P0 | Customer-to-Value and Renewal | Operations, support, customer success, finance, executive | Proves adoption, value, renewal, and expansion |
| P1 | Incident-to-Resolution | Support, operations, engineering, security, executive | Resolves problems and prevents recurrence |
| P1 | Source-to-Pay | Operations, procurement, finance, executive | Controls supplier selection, delivery, and payment |
| P1 | Idea-to-Release | Product, engineering, security, customer success | Converts evidence into tested releases and adoption learning |
| P1 | Plan-to-Performance | Executive and all departments | Turns goals into bounded actions and proof-backed performance |
| P2 | Hire-to-Productivity | Executive, people, operations, finance | Connects capacity gaps to productive staffing |
| P2 | Record-to-Report | Finance, operations, executive | Produces reconciled and approved management truth |
| P2 | Signal-to-Partnership | Market intelligence, partnerships, approvals, operations | Builds governed partner and market-access motions |

## Open-source adoption decisions for company loops

The repository's existing open-source adoption delta remains the authority. This execution slice applies it to the loop architecture.

### Use now or strengthen

- **Langfuse:** strengthen one existing canonical adapter for LLM traces, evaluations, cost, and action/approval/proof lineage. Observability must remain non-blocking and redacted.
- **Docling:** run the private-document pilot for proposals, customer files, financial reports, and Company Brain candidate facts. Human review remains mandatory before knowledge is approved.
- **OpenTelemetry:** use its stable trace and metric APIs as the neutral instrumentation substrate where useful; Langfuse remains the LLM-specific engineering surface.

### Pilot behind Dealix contracts

- **Activepieces:** connector-only bridge for customer-owned integrations and human input. Signed requests, signed callbacks, idempotency, and Dealix-owned Approval and Proof events are mandatory.
- **OpenFGA:** later authorization-policy pilot for tenant, workspace, department, action, and approval access after PostgreSQL tenant isolation is proven. It may answer authorization questions but cannot own Dealix business entities.
- **Nango:** hold as an optional OAuth/integration gateway. Its Elastic License and feature boundaries require legal and commercial review; use only when a real customer connector need justifies it.

### Hold until measured failure

- **Temporal:** use its durable-workflow design patterns now, but do not add the runtime until Dealix proves a restart/resume, long approval wait, or duplicate-execution failure that the current stack cannot solve safely.
- **OPA:** policy-engine pattern only. Do not add a second policy authority while the current autonomy and approval contracts are still being consolidated.

### Reject as core

- full CRM or ERP forks;
- another canonical workflow scheduler;
- unrestricted crawlers;
- another vector database before pgvector limits are measured;
- external systems that own consent, revenue, payment, approval, or proof truth.

## Architecture boundaries

External systems may:

- authenticate a customer connector;
- fetch or write approved data through a scoped adapter;
- provide document parsing;
- provide telemetry;
- host a human-input form;
- execute an approved, idempotent task.

External systems may not:

- create canonical Dealix entity truth without an adapter and provenance;
- infer consent;
- bypass Approval;
- recognize revenue;
- mark delivery complete;
- rewrite playbooks without evidence and approval;
- execute customer communication by default.

## Phase sequence

### Phase 1 — Contract and synthetic proof

- Merge no production dependency.
- Validate registry ownership and gates.
- Run Lead-to-Cash with synthetic data.
- Produce deterministic proof output.

### Phase 2 — Dealix-on-Dealix draft-only

- Connect existing Company Brain and offer truth.
- Read only approved internal data.
- Create real internal Action and Approval queues.
- Prepare drafts but do not send.
- Record real founder decisions and operational outcomes.

### Phase 3 — Managed pilot

- One customer and one bounded pain.
- Human-operated delivery with Dealix coordination.
- No broad autonomous company promise.
- Weekly Proof Pack and measurable before/after evidence.

### Phase 4 — Department expansion

Add Customer-to-Value, Incident-to-Resolution, Source-to-Pay, Idea-to-Release, and Plan-to-Performance based on proven customer needs.

### Phase 5 — Durable and multi-tenant scale

Only after three real pilots:

- complete PostgreSQL tenant isolation;
- add fine-grained authorization;
- harden connector lifecycle;
- add long-running workflow infrastructure if measured failures justify it;
- expose a client Control Tower.

## Definition of done for this slice

- Loop registry references only canonical entities.
- Lead-to-Cash stages are ordered and unique.
- Every external-effect stage is approval-gated.
- Revenue recognition requires payment proof.
- Delivery claims require completion proof.
- Every loop closes through Outcome, Learning, and Daily Command.
- Synthetic Lead-to-Cash completes with zero external actions.
- Draft-only Lead-to-Cash blocks before external contact.
- No production, dependency, migration, secret, customer data, sending, payment, or deployment change.
