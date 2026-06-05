# Dealix Business OS — Architecture

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> How the 14 operating systems fit together, and how they map to the existing
> code planes in this repository.

---

## 1. Mental model

Dealix is **one** operating system made of fourteen modules. Each module answers
one operating question for a Saudi B2B company. They share a common spine:
**Data → Decision → Approval → Action → Proof.**

```
            ┌─────────────────────────────────────────────┐
            │                 COMMAND OS                   │
            │   what happened · what to decide · who owns  │
            └───────────────▲───────────────▲─────────────┘
                            │               │
        ┌───────────────────┴───┐   ┌───────┴───────────────────┐
        │      REVENUE OS        │   │       CLIENT OS           │
        │  leads · pipeline ·    │   │  account memory ·         │
        │  follow-up · proposals │   │  promises · renewals      │
        └───────────┬───────────┘   └───────────┬───────────────┘
                    │                            │
        ┌───────────┴───────────┐   ┌────────────┴──────────────┐
        │     DELIVERY OS        │   │       SUPPORT OS          │
        │  plans · SLA · blockers│   │  tickets · escalation     │
        └───────────┬───────────┘   └────────────┬──────────────┘
                    │                            │
        ┌───────────┴────────────────────────────┴──────────────┐
        │     FINANCE OS   ·   KNOWLEDGE OS   ·   ACADEMY OS      │
        └───────────┬────────────────────────────┬──────────────┘
                    │                            │
   ┌────────────────┴──────────┐    ┌────────────┴──────────────┐
   │         DATA OS            │    │       AGENT OS            │
   │  intake · consent ·        │    │  registry · contracts ·   │
   │  retention · quality       │    │  permissions · logs       │
   └────────────────┬──────────┘    └────────────┬──────────────┘
                    │                            │
            ┌───────┴────────────────────────────┴───────┐
            │   GOVERNANCE OS  +  PROOF OS  (trust spine) │
            │  approval · audit · evidence · claims       │
            └─────────────────────────────────────────────┘

   Ecosystem layer (future): PARTNER OS · VENTURE OS
```

---

## 2. The trust spine

Every action in any module passes through the trust spine before it touches the
outside world:

1. **Data OS** — is the data consented, minimal, and retained correctly?
2. **Governance OS** — does this action need human approval? Which class?
3. **Agent OS** — does the acting agent have a contract permitting this?
4. **Proof OS** — is there evidence for any claim being made?

**Operating rule:** AI explores, analyzes, and recommends. Deterministic
workflows execute. Humans approve critical external commitments.

---

## 3. Module → code plane mapping

The repository is already organized into five planes (see
`docs/blueprint/master-architecture.md`). The 14 OS modules map onto them:

| OS module | Primary plane | Example code locations |
|---|---|---|
| Command OS | Decision | `core/agents/`, `docs/19_command_os/` |
| Revenue OS | Decision + Execution | `auto_client_acquisition/`, `autonomous_growth/`, `docs/17_revenue_os/` |
| Client OS | Data + Decision | `db/`, `clients/`, `docs/05_client_os/`, `docs/11_client_os/` |
| Delivery OS | Execution | `dealix/execution/`, `auto_client_acquisition/pipeline.py` |
| Support OS | Execution + Decision | `api/` routers (support), roadmap |
| Finance OS | Data + Execution | `integrations/`, pricing config, `docs/21_operating_finance/` |
| Data OS | Data | `db/`, `integrations/`, `docs/04_data_os/`, `docs/06_data_os/` |
| Governance OS | Trust | `dealix/trust/`, `dealix/registers/`, `docs/07_governance/` |
| Proof OS | Trust | `dealix/registers/`, `docs/07_proof_os/`, `docs/14_proof/` |
| Knowledge OS | Data | `docs/`, `prompts/` |
| Agent OS | Decision + Trust | `core/agents/`, `AGENTS.md`, `docs/10_agents/`, `docs/16_agents/` |
| Partner OS | Operating | roadmap |
| Academy OS | Operating | `docs/12_adoption_os/`, `docs/20_adoption/` |
| Venture OS | Operating | roadmap |

> Note: the repository contains historical numbered doc folders (e.g.
> `docs/17_revenue_os/`). Those remain valid deep references. The canonical
> human-readable specs now live under `docs/02_operating_systems/`.

---

## 4. Five-plane reminder

| Plane | Responsibility |
|---|---|
| Decision | Agents, reasoning, synthesis, recommendation, evidence assembly |
| Execution | Deterministic workflows, retries, compensation, external commitments |
| Trust | Policy, approval, audit, verification, evidence packs |
| Data | Operational source of truth, lineage, metrics, integrations |
| Operating | CI/CD, Docker, release discipline, repo governance, runbooks |

Features cross planes through **explicit contracts**, not hidden shared state.

---

## 5. The AI model layer (LLM Gateway)

Dealix is provider-agnostic. Every AI task is routed by a task router and logged.

```
Task Router
├─ Fast classification → small/fast model
├─ Arabic writing      → best Arabic-capable model
├─ Deep reasoning      → premium model (Claude / equivalent)
├─ Coding              → coding-optimized model
├─ Cheap drafts        → local/low-cost model
└─ Fallback            → gateway/router provider
```

Every AI call records: `task_type`, `model`, `cost_estimate`, `latency_ms`,
`input_class`, `approval_required`, `output_hash`. See
`docs/02_operating_systems/AGENT_OS.md` and `docs/06_llm_gateway/` /
`docs/09_llm_gateway/`.

---

## 6. Expansion sequence (do not skip)

1. Sell Command Sprint → deliver Proof Pack.
2. Convert to Managed Business OS.
3. Expand inside the customer: Client → Delivery → Support.
4. Add enterprise depth: Finance → Governance → Data.
5. Open ecosystem: Partner → Academy → Venture.

Each step requires the previous step's gates to pass. See
[`MODULE_STATUS_MAP.md`](MODULE_STATUS_MAP.md) for what is allowed to ship.
