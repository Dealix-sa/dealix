# Hermes Universal Kernel

Hermes is the Sovereign Value Control Plane for Dealix. Every input the
business receives — a customer message, a tender notice, a partner reply,
a github webhook, a market signal — becomes a **Signal**, and every Signal
moves through a deterministic seven-phase lifecycle:

```
Signal → Opportunity → Decision → Execution → Outcome → Asset → Scale / Kill
```

The kernel itself is in `dealix/hermes/kernel/`. It is dependency-light
(Pydantic only), holds no I/O, and is therefore safe to depend on from
any router, agent, or test.

## Phases

| Phase | Module | Output |
|---|---|---|
| 1 Signal | `kernel/signals.py` | `Signal` rows + `signal.captured` / `signal.classified` events |
| 2 Opportunity | `kernel/opportunities.py` | scored `Opportunity` + `opportunity.created` / `opportunity.scored` |
| 3 Decision | `kernel/decisions.py` | `Decision` memo with approval gate |
| 4 Execution | `kernel/executions.py` | policy-checked, optionally approval-held plan |
| 5 Outcome | `kernel/outcomes.py` | one Outcome per Execution — no skipping |
| 6 Asset | `kernel/assets.py` | reusable IP harvested from successful Outcomes |
| 7 Scale/Kill | `kernel/scale_kill.py` | thresholds applied to every Asset on schedule |

## Schemas

The seven kernel contracts live in `kernel/schemas.py`:

- `Signal`
- `Opportunity` — six 0..5 scores + composite + sovereignty level
- `Decision`
- `Execution`
- `Outcome`
- `Asset`
- `LifecycleEvent` — emitted at every phase transition

Every entity uses prefixed IDs (`sig_`, `opp_`, `dec_`, `exe_`, `out_`,
`ast_`) so they read clearly in logs.

## The 14 Non-Negotiables

| # | Rule | Enforced by |
|---|---|---|
| 1 | No Signal is lost | `SignalStore.capture()` is the only entry point; archive is timestamped, never deleted |
| 2 | No Opportunity without a score | `OpportunityStore.create_from_signal` always calls `score_opportunity` |
| 3 | No Execution without a Trust Check | `Execution.dispatch` raises until `trust_check_passed` is true |
| 4 | No external action without approval | `Execution.dispatch` raises if `approval_required` and not approved |
| 5 | No Tool without Registry | `PermissionMatrix.can_invoke` rejects unknown tools |
| 6 | No Agent without Owner + KPI | `AgentCard` requires `owner`; revenue/customer/growth/venture cards require `kpis` (tested) |
| 7 | No MCP without Gateway + Review | All MCP calls flow through `MCPGateway.invoke` |
| 8 | No Outcome without Asset Review | `AssetStore.review_outcome` flags every profitable outcome |
| 9 | No Revenue without Verification | `RevenueAssurance.verify` requires payment + invoice |
| 10 | No Campaign without Attribution | `CampaignStore.create` requires `offer_id`; `RevenueAttribution` links revenue to campaigns |
| 11 | No Partner without Performance Review | `PartnerPolicyRule` blocks partner-visible actions without a review record |
| 12 | No Customer without Value Report | `ValueReport.is_complete` enforced; no paid customer without one |
| 13 | No Scale without Data | `evaluate(asset)` thresholds in `kernel/scale_kill.py` |
| 14 | No Sovereign Decision without Sami | `ApprovalCenter.open` raises requirement; `S4`/`S5` paths block dispatch |

Each is covered by tests in `tests/hermes/`.

## Orchestrator

`dealix/hermes/orchestrator.py` exposes `HermesOrchestrator` — a single
object bundling the kernel, sovereignty primitives, trust plane, and MCP
gateway. Bootstrap once at process start; tests build their own.

```python
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.config import seed_tools

orch = HermesOrchestrator().bootstrap()
seed_tools(orch.tool_registry)
```

51 default agent cards register on bootstrap. The orchestrator also
exposes the MCP gateway, kill switch, approval center, audit log, risk
register, and incident register.

## API Surface

All Hermes endpoints live under `/api/v1/hermes/*`. Mount via
`api.routers.hermes.composite.build_hermes_router()` — already wired in
`api/main.py`.

Core endpoints:
- `POST /signals/capture`
- `POST /opportunities/score`
- `POST /decisions/create`
- `POST /executions/plan`
- `POST /outcomes/log`
- `POST /assets/build`
- `GET  /events`

Sovereign endpoints (`/sovereign/*`), trust endpoints (`/trust/*`), money
(`/money/*`), growth (`/growth/*`), products (`/products/*`), partners
(`/partners/*`), customers (`/customers/*`), intelligence
(`/intelligence/*`), training (`/training/*`), ventures (`/ventures/*`),
assets (`/assets/*`), observability (`/observability/*`).
