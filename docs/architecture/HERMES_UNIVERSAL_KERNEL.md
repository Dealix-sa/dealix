# Hermes Universal Kernel

> Sovereign execution core for Dealix. Any signal — customer, partner,
> market, product, risk, finance, training, report, API, venture, legal,
> technical, personal — flows through the same loop and is governed by
> the same gate.

```
Sami Sovereign Console
└── Hermes Universal Kernel
    ├── Signal Intake
    ├── Opportunity Graph
    ├── Decision Layer
    ├── Execution Planner
    ├── Trust Check
    ├── Outcome Logger
    ├── Asset Builder
    ├── Money Dashboard
    └── Agent / Tool Registry
```

## The canonical loop

```
Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset
```

Every layer is small, deterministic, and replaceable:

| Layer        | Module                                    | Store              |
|--------------|-------------------------------------------|--------------------|
| Signal       | `dealix.hermes.core.signals`              | `SignalStore`      |
| Opportunity  | `dealix.hermes.core.opportunities`        | `OpportunityStore` |
| Decision     | `dealix.hermes.core.decisions`            | `DecisionStore`    |
| Execution    | `dealix.hermes.core.executions`           | `ExecutionStore`   |
| Trust        | `dealix.hermes.trust.guardrails`          | _stateless_        |
| Outcome      | `dealix.hermes.core.outcomes`             | `OutcomeStore`     |
| Asset        | `dealix.hermes.core.assets`               | `AssetStore`       |

The Orchestrator (`dealix.hermes.orchestrator.HermesOrchestrator`) is the
only object that needs to know the full loop.

## Sovereignty (S0..S5)

`dealix.hermes.sovereignty.classify_action` is the top of the Kernel.
Every action gets one of six levels:

- **S0 — auto-safe**: read-only computation.
- **S1 — internal**: side-effects bounded to Dealix's own systems.
- **S2 — Sami approval**: any `external_*` action.
- **S3 — sovereign memo**: anything touching sensitive data.
- **S4 — sovereign-only**: contracts, enterprise pricing, money moves,
  marketplace, public API launches, agent permissions, MCP enablement.
- **S5 — never autonomous**: legal/financial commitments, signing on
  Sami's behalf, sending sensitive customer data.

Nothing at S2+ leaves the Kernel without an explicit human approval.

## Trust layer

- `guardrails.trust_check` — blocks overclaims, surfaces sensitive data,
  forces approval on enterprise pricing and external commitments.
- `mcp_security.review_mcp_server` — MCP servers require an owner,
  narrow data scope, no broad/external execution by default; broad
  access escalates to critical risk and is rejected.
- `registry` / `tools` / `permissions` — single source of truth for what
  agents and tools exist and what sovereignty ceiling each is bounded by.
- `evidence` / `audit` — append-only record of inputs, sources, checks,
  and approvals attached to any subject.

## API surface

All endpoints are mounted under `/api/v1/hermes`:

| Method | Path                          | Purpose                                  |
|--------|-------------------------------|------------------------------------------|
| POST   | `/signals/capture`            | Ingest a signal, return opportunity + score. |
| POST   | `/opportunities/score`        | Score an opportunity.                    |
| POST   | `/decisions/create`           | Generate a decision memo.                |
| POST   | `/executions/plan`            | Generate an execution plan (gated).      |
| POST   | `/trust/check`                | Run guardrails on a draft.               |
| POST   | `/sovereignty/check`          | Classify an action.                      |
| POST   | `/mcp/review`                 | Review a proposed MCP server.            |
| POST   | `/outcomes/log`               | Record an outcome, may emit an asset.    |
| GET    | `/sovereign/brief`            | Founder one-pager.                       |
| GET    | `/money/dashboard`            | Cashflow + assets snapshot.              |

## Non-negotiables

1. Sovereignty stays with Sami — no agent may exceed its registered ceiling.
2. External actions are drafts until Sami signs them off.
3. Every outcome with a learning or a win is promoted to an asset.
4. MCP servers require an owner, narrow scope, and per-call approval for
   external execution.
5. Guardrails are non-bypassable — forbidden claims, sensitive data, and
   enterprise pricing all force approval.

## Built-in agents

- `agents.founder_brief` — daily sovereign one-pager.
- `agents.opportunity_mapper` — signal → opportunity wrapper.
- `agents.trust_checker` — guardrail entrypoint.
- `agents.asset_builder` — outcome → asset promotion.

## Money engine

`dealix.hermes.money.*` wraps the Kernel with cash-first helpers:

- `pricing.LADDER` — the 5-rung Dealix ladder (Free Diagnostic → Custom AI).
- `revenue_hunter.draft_hunt` — fastest signal-to-draft, always manual send.
- `proposal_factory.build_proposal` — bilingual proposal draft.
- `followup.schedule_from` — recommended cadence (no autosend).
- `cashflow.snapshot` / `dashboard.render` — sovereign read-only view.
