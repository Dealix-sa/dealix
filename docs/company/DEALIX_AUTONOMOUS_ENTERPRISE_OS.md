# Dealix Autonomous Enterprise OS

> The single source of truth for what Dealix is at the ultimate level.
> Everything else in this repository — code, docs, workflows, agents, dashboards — exists to advance the company through the layers defined here.

---

## 1. Purpose

Turn Dealix into an **autonomous, trust-gated, founder-controlled Saudi B2B revenue operating company**.

Dealix is not a dashboard, not a single product, and not a service company. It is a company-as-a-system:

- The system **prepares** the work (research, scoring, drafts, plans, reports).
- The system **routes** decisions to the founder when they exceed an approval class.
- The system **executes** approved actions through trusted, auditable workers.
- The system **measures** outcomes and learns from them.
- The founder **decides** the high-impact moves and reviews the company through one console.

This file is the constitution for that operating company. Every other Ultimate document (`docs/*/ULTIMATE_*.md`) is a chapter of this constitution.

---

## 2. Ultimate Principle

> The system prepares, routes, scores, drafts, monitors, follows up, and reports.
> The founder approves high-impact actions.
> Trust gates external impact.
> Audit records decisions.
> Revenue evidence decides scale.

Reading this principle line-by-line:

| Sentence                                            | What it means in practice                                                                 |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------|
| The system prepares…                                | All preparation work (research, scoring, drafting, planning) is performed by workers.     |
| The founder approves high-impact actions.           | Anything that touches money, customers, or external parties needs explicit approval.      |
| Trust gates external impact.                        | Even an approved action passes a policy check before it leaves the building.              |
| Audit records decisions.                            | Every approval, rejection, edit, escalation, and external action is an immutable record.  |
| Revenue evidence decides scale.                     | We expand a layer only after the previous layer has produced measurable revenue evidence. |

---

## 3. Core Operating Layers

Dealix Ultimate is composed of **ten operating layers**. Each layer is independently buildable, independently testable, independently observable, and has a single owner.

### 3.1 Founder Command Layer
The single internal interface a founder/CEO uses to operate the company.

- CEO Console (`/ceo`) — one top action, company score, bottleneck, risk, cash.
- Sales Cockpit (`/sales-cockpit`) — funnel from lead to payment.
- Approval Center (`/approvals`) — every pending decision in one queue.
- Trust Center (`/trust`) — policy flags, suppression, AI risk, incidents.
- Worker Health (`/workers`) — every background machine, with retry + disable.
- Finance Center (`/finance`) — cash, MRR, pipeline, runway, margin.

Detailed contract: `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`.

### 3.2 Revenue Factory Layer
Repeatable, measurable movement from market to cash.

- Lead intelligence (discovery, enrichment, dedupe).
- Scoring (sector × fit × signal × intent).
- Outreach drafts.
- Approval queue.
- Follow-ups.
- Reply routing.
- Sample creation.
- Proposal creation.
- Payment capture.

Detailed contract: `docs/revenue/ULTIMATE_REVENUE_FACTORY.md`.

### 3.3 Trust & Governance Layer
Every action that affects external parties must pass this layer.

- Policy evaluator (approval class, reversibility, sensitivity, evidence).
- Approval classes A0–A3.
- Suppression list (do-not-contact, do-not-mention).
- No-overclaim policy.
- AI evals (prompt, output, regression, red-team).
- Audit log (immutable, append-only).
- Incident response procedure.

Detailed contract: `docs/trust/ULTIMATE_TRUST_PLANE.md`.

### 3.4 Worker Mesh Layer
The set of background machines that do the actual work.

- Scheduled (cron) workers.
- Queue workers.
- Durable workflows.
- Autonomous-but-gated agents.
- Worker metadata, retry policy, disable switch.

Detailed contract: `docs/runtime/ULTIMATE_WORKER_MESH.md`.

### 3.5 Data Platform Layer
The system of record for every fact that matters.

- Phase 1: private ops CSV (bootstrappable, today).
- Phase 2: Postgres primary (operational source of truth).
- Phase 3: Event log (immutable append-only).
- Phase 4: Metrics layer (business, DORA, AI, finance).
- Phase 5: Warehouse (historical analysis, forecasting).

Detailed contract: `docs/data/ULTIMATE_DATA_PLATFORM.md`.

### 3.6 Delivery & Client Success Layer
Convert paid work into client value, proof, retention, and referrals.

- Client intake.
- Delivery plan.
- QA scoring.
- Handoff.
- Feedback.
- Health score.
- Retainer ask.
- Referral ask.
- Proof approval.

Detailed contract: `docs/delivery/ULTIMATE_DELIVERY_OS.md`.

### 3.7 Finance & Capital Layer
Make the company financially controlled from day one.

- Pricing, invoicing, payment capture.
- MRR, gross margin, runway.
- Tool cost, AI unit economics.
- Decisions: raise price, kill bad revenue, scale channel, pause channel.

Detailed contract: `docs/finance/ULTIMATE_FINANCE_OS.md`.

### 3.8 Product Platform Layer
Turn repeated service workflows into productized modules.

- Reusable workflows, templates, internal tools.
- Command center modules.
- Customer + partner portals.
- Integrations + APIs.

Detailed contract: `docs/product/ULTIMATE_PRODUCT_PLATFORM.md`.

### 3.9 Distribution Portfolio Layer
A balanced set of channels feeding the Revenue Factory.

- Outbound (sector machines).
- Inbound (content → demand).
- Partner referrals.
- ABM strategic accounts.
- Events, ecosystem.

(See "Distribution Portfolio Machine" in `docs/revenue/ULTIMATE_REVENUE_FACTORY.md`.)

### 3.10 Enterprise Readiness Layer
Everything required to be operated by a real company.

- Security, compliance, backups.
- Observability, SLAs, incident management.
- Support, access control.
- Branch protection + required checks (see `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`).

---

## 4. North Star

> **Cash collected from qualified Saudi B2B revenue operations.**

This is the only top-line metric that decides whether the company is winning or losing this week. Every other metric exists to **explain** the North Star, not to **replace** it.

Supporting metrics, by layer:

| Layer            | Supporting metric                                                |
|------------------|------------------------------------------------------------------|
| Founder Command  | Time-to-approve, approvals-per-day                               |
| Revenue Factory  | Approved sends, replies, samples, proposals, payment follow-ups  |
| Trust            | Suppression violations, A3 attempts, eval pass rate, incidents   |
| Worker Mesh      | Worker success rate, queue latency, failed jobs, stale reports   |
| Data Platform    | Source freshness, record count, schema drift, lineage coverage   |
| Delivery         | Delivery cycle time, QA pass rate, health score, NPS, feedback   |
| Finance          | MRR, cash, margin, runway, AI unit economics                     |
| Product          | Repeated workflow count, paid customer usage, time saved         |
| Distribution     | Channel cost, channel reply rate, channel conversion             |
| Enterprise       | Uptime, MTTR, change-fail rate, deploy frequency (DORA)          |

---

## 5. Rule

> **Autonomy increases only when trust, audit, evidence, and recovery are stronger than manual operation.**

A worker, agent, or workflow may move to a higher autonomy class **only after**:

1. **Trust** — a policy gate exists and has been exercised.
2. **Audit** — every action of that worker is recorded.
3. **Evidence** — at least 14 consecutive days of clean operation with measurable revenue or operational benefit.
4. **Recovery** — a rollback / disable path exists and has been tested.

Without all four, autonomy is downgraded — never upgraded.

---

## 6. Document Map (this file's chapters)

| Layer                | Document                                                       |
|----------------------|----------------------------------------------------------------|
| Maturity Model       | `docs/company/DEALIX_MATURITY_MODEL.md`                        |
| Architecture         | `docs/architecture/ULTIMATE_ARCHITECTURE_MAP.md`               |
| Founder Console      | `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`                    |
| Internal API         | `docs/api/ULTIMATE_INTERNAL_API.md`                            |
| Data Platform        | `docs/data/ULTIMATE_DATA_PLATFORM.md`                          |
| Trust Plane          | `docs/trust/ULTIMATE_TRUST_PLANE.md`                           |
| Worker Mesh          | `docs/runtime/ULTIMATE_WORKER_MESH.md`                         |
| Revenue Factory      | `docs/revenue/ULTIMATE_REVENUE_FACTORY.md`                     |
| Delivery OS          | `docs/delivery/ULTIMATE_DELIVERY_OS.md`                        |
| Finance OS           | `docs/finance/ULTIMATE_FINANCE_OS.md`                          |
| Product Platform     | `docs/product/ULTIMATE_PRODUCT_PLATFORM.md`                    |
| Observability + DORA | `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`              |
| Security Governance  | `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`                |

---

## 7. How to use this document

- Read this file first.
- Before changing anything, check which **layer** you are operating on.
- Before merging a change, confirm it advances the layer's maturity (or maintains it) — see `DEALIX_MATURITY_MODEL.md`.
- Verify the blueprint is intact: `make ultimate-level`.
- CI gate: `.github/workflows/dealix-ultimate-level.yml`.

---

## 8. Non-negotiables

- No external action without trust gate.
- No trust record, no action.
- No autonomous decision in approval class A2/A3.
- No layer scales until the previous layer has revenue evidence.
- No metric is celebrated unless it advances the North Star.
- No level upgrade without verification, evidence, trust gate, rollback path, and owner.

This is the company. Build accordingly.
