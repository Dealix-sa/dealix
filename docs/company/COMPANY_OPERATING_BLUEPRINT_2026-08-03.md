# Dealix Company Operating Blueprint

## Purpose

The Company Operating Blueprint converts verified company context into a phased Dealix engagement. It is designed to make Dealix useful across the company while avoiding a broad, high-risk enterprise rollout.

Dealix remains an operating and intelligence layer. Existing CRM, ERP, finance, support, HR, and delivery systems remain systems of record unless a client explicitly changes that architecture through a separate approved program.

## Enterprise coverage

The blueprint assesses fourteen company functions:

1. Executive strategy and performance.
2. Market and company intelligence.
3. Marketing and demand.
4. Sales and revenue operations.
5. Customer success and renewal.
6. Operations and service delivery.
7. Support and incident management.
8. Product and service innovation.
9. Engineering, data, and AI governance.
10. Finance and management reporting.
11. Procurement and supplier management.
12. People and workforce productivity.
13. Partnerships and market access.
14. Risk, compliance, privacy, and security.

Each function is connected to a primary operating loop, expected business outcomes, diagnostic questions, canonical outputs, and one commercial module.

## Maturity assessment

Each function is classified from level 0 to level 5:

- **0 — Unverified:** no reliable evidence.
- **1 — Manual / fragmented:** work exists but depends on people or disconnected tools.
- **2 — Defined:** owners, stages, and outputs are documented.
- **3 — Governed:** approvals, risks, and evidence boundaries are enforced.
- **4 — Measured:** baselines, operating metrics, outcomes, and exceptions are reviewed.
- **5 — Learning:** verified outcomes improve approved playbooks.

A maturity level is not a marketing claim. The blueprint only records it when source references, an owner, and a named problem are available.

## Priority model

The builder ranks each verified function using:

- business impact;
- urgency;
- owner readiness;
- data readiness;
- current maturity gap;
- execution or compliance risk.

The initial engagement is restricted to at most two functions, and the pilot is restricted to one primary loop. This prevents a big-bang implementation and makes time-to-value, proof, and support capacity measurable.

## Commercial path

### 1. Diagnostic

Outputs:

- company context;
- maturity assessment;
- highest-priority function;
- risk map;
- recommended bounded pilot.

### 2. Pilot

Outputs:

- one primary company loop;
- baseline and target metric;
- action and approval queues;
- proof plan;
- stop or rollback rule.

### 3. Implementation

Outputs:

- Company Brain;
- selected function modules;
- roles and ownership;
- connector adapters;
- approval and evidence governance;
- Daily Command.

### 4. Managed service

Outputs:

- weekly executive command;
- risk and exception management;
- approval review;
- proof and learning review;
- renewal readiness.

## Saleability

The blueprint makes Dealix easier to sell because the conversation starts with the client's operating problem rather than a generic AI platform pitch.

A buyer receives a clear sequence:

`verified problem -> function assessment -> one priority -> bounded pilot -> evidence -> modular expansion`

This supports different buyers without creating separate products:

- CEO: strategy, decisions, and executive command.
- Sales leader: qualification, opportunity actions, and forecast evidence.
- Operations leader: handoffs, checkpoints, exceptions, and delivery proof.
- Customer success leader: onboarding, adoption, risk, value, and renewal.
- Technology leader: architecture, source authority, safe automation, and verification.
- Finance leader: reconciliation, cash visibility, approvals, and management reporting.
- Risk leader: controls, privacy, security, and audit evidence.

## Expansion gates

Enterprise expansion remains blocked until all of the following are supported:

- verified delivery;
- owner adoption;
- measured outcome or an explicit no-go;
- support capacity;
- security and privacy review;
- unit economics review.

The following are forbidden:

- big-bang enterprise rollout;
- unbounded custom automation;
- parallel sources of truth;
- unsupported autonomy claims.

## Usage

```bash
python scripts/commercial/build_company_operating_blueprint.py \
  --input company_evidence.json \
  --output reports/company_os/company_operating_blueprint.json
```

The output is internal and draft-only. It does not issue a quote, contact a customer, enable production automation, or claim readiness or value.

## Relationship to other Dealix assets

The blueprint composes existing canonical assets:

- Company Brain;
- Company Intelligence entities;
- Company Loops registry;
- Sale-Ready Pack;
- Action Queue;
- Approval Queue;
- Outcome and Proof contracts;
- Learning Events;
- Daily Command.

It does not create a second orchestrator, proof ledger, CRM, or commercial catalog.
