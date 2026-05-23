# Dealix Autonomous Company Control Plane

> The previous phase built the **files** of the company. This phase
> builds the **mind** of the company.

The Control Plane sits **above** every Dealix OS (Revenue, Delivery,
Trust, Product, Finance, Client Success, Content, Learning, Founder)
and answers, every day:

- What is happening?            (`COMPANY_STATE_SCHEMA.md`)
- What needs a decision?        (`docs/founder/DECISION_QUEUE_TEMPLATE.md`)
- What is risky?                (`docs/ops/ESCALATION_MATRIX.md`)
- What is an opportunity?       (`docs/learning/EXPERIMENT_SYSTEM.md`)
- What should we stop?          (`docs/founder/KILL_LIST.md`)
- What should we double down on? (`docs/strategy/MOAT_SYSTEM.md`)
- What evidence backs each call? (`docs/learning/COMPANY_MEMORY.md`)
- What is the next decision?    (Decision Queue, again)

## Components

| Layer                  | Public doctrine                                            | Private artefact (founder repo)       |
|------------------------|------------------------------------------------------------|---------------------------------------|
| Company State          | `docs/control_plane/COMPANY_STATE_SCHEMA.md`               | live data                             |
| Action Router          | `docs/control_plane/ACTION_ROUTER.md`                      | `trust/approval_log.csv`              |
| Operating Loops        | `docs/ops/OPERATING_LOOPS.md`                              | per-OS runbooks                       |
| System Owners          | `docs/ops/SYSTEM_OWNERS.md`                                | per-owner cadence                     |
| Escalation Matrix      | `docs/ops/ESCALATION_MATRIX.md`                            | live alerts                           |
| Metrics Contract       | `docs/ops/OPERATING_METRICS_CONTRACT.md`                   | per-system metric dashboards          |
| Founder Leverage Index | `docs/founder/FOUNDER_LEVERAGE_INDEX.md`                   | weekly score                          |
| Board Pack             | `docs/founder/BOARD_PACK_TEMPLATE.md`                      | monthly pack                          |
| CEO Dashboard          | `docs/founder/CEO_DASHBOARD_SPEC.md`                       | live dashboard                        |
| Kill List              | `docs/founder/KILL_LIST.md`                                | private rolling kill list             |
| Decision Queue         | `docs/founder/DECISION_QUEUE_TEMPLATE.md`                  | `founder/decision_queue.md`           |
| Company Memory         | `docs/learning/COMPANY_MEMORY.md`                          | private memory stores                 |
| Experiment System      | `docs/learning/EXPERIMENT_SYSTEM.md`                       | `learning/experiment_log.md`          |
| Productization Engine  | `docs/product/PRODUCTIZATION_ENGINE.md`                    | per-workflow stage tracker            |
| Revenue Quality        | `docs/revenue/REVENUE_QUALITY.md`                          | proposal acceptance log               |
| Client Tiering         | `docs/client_success/CLIENT_TIERING.md`                    | per-client tier in CRM                |
| Capital Allocation     | `docs/finance/CAPITAL_ALLOCATION.md`                       | weekly capital review                 |
| Moat System            | `docs/strategy/MOAT_SYSTEM.md`                             | monthly moat health check             |

## Verification

The doctrine is executable:

```bash
python scripts/verify_company_os.py
```

CI runs the same script via
`.github/workflows/verify-company-os.yml` on every push, PR, and
weekly heartbeat, so the doctrine cannot silently rot.

## You have reached v1 when

- [PASS] Company State Schema exists
- [PASS] CEO Brief (Dashboard Spec) exists
- [PASS] Decision Queue template exists
- [PASS] Action Router exists (doc + code)
- [PASS] Approval rules exist (`ACTION_ROUTER.md` APPROVE path)
- [PASS] Risk signals exist (`company_state.red_signals/yellow_signals`)
- [PASS] System Scorecard exists (`OPERATING_METRICS_CONTRACT.md`)
- [PASS] Operating Loops exist
- [PASS] Escalation Matrix exists
- [PASS] Company Memory exists
- [PASS] Experiment System exists
- [PASS] Productization Engine exists
- [PASS] Kill List exists
- [PASS] GitHub Actions verifies these files
