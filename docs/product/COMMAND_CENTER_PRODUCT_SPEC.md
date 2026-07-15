# Command Center Product Spec

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #3 (no cross-tenant operational access), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Specify Dealix's in-product Command Center: the executive interface that lets a founder or client operator control Dealix from one place. This document is the **product spec** — what the UI surfaces, what actions it exposes, and what doctrine it enforces. The operational view of the same surface for the founder lives in `docs/control_plane/SALES_COCKPIT_SYSTEM.md`.

## Views

| View | Audience | Purpose |
|------|----------|---------|
| CEO View | Founder / company head | One-page revenue, trust, cost, and decision queue |
| Sales View | Commercial operator | Lead intelligence, outreach, replies, samples, proposals |
| Delivery View | Delivery lead | Active engagements, milestones, QA, feedback |
| Trust View | Trust owner | Approval queues, suppression, incidents, evals |
| Finance View | Finance owner | Cash, receivables, MRR, cost per outcome |
| Agent View | Engineering / product | Agent registry, evals, prompt versions, action logs |

## Core Actions Across Views

- Approve outreach (per draft or per batch).
- Approve proposal.
- Review and approve a sample artifact.
- Review trust flags and escalate.
- Monitor cash collected and aging.
- Inspect a sector scorecard.
- Inspect an AI evidence pack (what evidence backs a claim).
- Roll an agent prompt back to a prior version.

## Source-Evidence Rule

Every number on the Command Center has a click-through to the records that produced it. No view renders a metric without a path back to source data.

## Cross-Tenant Rule

A user can only see and act on tenant-scoped data. The router and ORM both enforce this. The Command Center never aggregates across tenants for a tenant user.

## Core Rules

- The Command Center never executes an external side effect on its own. It is a control surface.
- A "guaranteed outcome" rendering is not allowed; numbers shown as forward-looking carry an explicit confidence band.
- A view that depends on an agent output also surfaces that output's last eval pass result.
- A blocked approval (because evidence is missing) tells the user what evidence is needed.

## Runtime Wiring

- Existing operational surface (Streamlit): `dashboard/app.py`, `dashboard/pages/` (Overview, Leads, Approvals, Evidence, Costs, Audit).
- HTTP surface: `api/routers/command_center.py`, `api/routers/business_now.py`.
- Frontend home: `frontend/src/` (Next.js, currently stub).
- Existing founder command center docs: `docs/company/FOUNDER_COMMAND_CENTER.md`, `docs/company/CEO_OPERATING_SYSTEM.md`.
- Sales cockpit operational view: `docs/control_plane/SALES_COCKPIT_SYSTEM.md`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Time from "open Command Center" to "first decision recorded" | < 60 seconds for routine batches | UX timing |
| Approvals executed per active day | tracked, trending up | `AuditLogRecord` |
| Cross-tenant accidental visibility | 0 | RBAC tests |
| Evidence-link click-through on rendered metrics | tracked; a low rate indicates trust gaps | UX events |

## Cross-Links

- `docs/control_plane/SALES_COCKPIT_SYSTEM.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`
- `docs/company/FOUNDER_COMMAND_CENTER.md`
- `docs/company/CEO_OPERATING_SYSTEM.md`
- `docs/founder/BOARD_LEVEL_KPI_STACK.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`

## Open Items

- The Next.js frontend is stub-only; today the operational surface is the Streamlit dashboard.
- The Agent View depends on the agent registry and prompt version log, which are partial.
- Cross-tenant RBAC is enforced at the router level; end-to-end tests cover the common cases, but a dedicated Command Center cross-tenant red team scenario is open in the evals system.
- Evidence-link click-through telemetry is not yet wired.
