# Hermes — Dealix Production Empire Layer

> Dealix is not an AI agent tool.
> Dealix is a sovereign control plane for governed AI execution and verified revenue.

Hermes is the layer that operationalizes that positioning. It is intentionally
**pure-Python** and **side-effect-free at import time**: every module exposes
dataclasses, scoring functions, and policy gates that can be composed into the
existing FastAPI / Postgres stack without leaking infrastructure dependencies.

## Sub-packages

| Package | Responsibility |
| --- | --- |
| `control_plane` | Central composition entrypoint that ties identity → comms → MCP → audit together |
| `agent_lifecycle` | Registry, risk scoring, capability scoping, evaluation, promotion, restriction, retirement |
| `identity` | Scoped, revocable, capability-bound agent identities (richer than OAuth/OIDC) |
| `agent_comms` | Sanitization, delegation policy, source-trust gating for agent-to-agent messages |
| `provenance` | Source / lineage ledger for prompts and outputs |
| `mcp` | Manifest review, descriptor scan, semantic vetting, kill switch for MCP servers |
| `security` | Defense-in-depth against prompt injection, data leakage, hallucinated claims |
| `growth` | Generative Engine Optimization, multi-layer attribution, entity-data consistency |
| `money` | Verified revenue, revenue quality, delivery margin, founder time cost |
| `sovereignty` | Founder time accounting |
| `products` | Offer-market-fit metrics, experimentation, readiness gates |
| `assets` | Asset → product commercialization |
| `partners` | Tiered partner program with approved-claims policy |
| `delivery` | Per-offer delivery playbooks and quality gates |
| `board` | Board-level metrics, investor updates, traction reports |

## Design rules

1. **No external sends.** Hermes never calls outbound APIs. It produces
   structured decisions and drafts that the existing approval gate
   ([`dealix.governance.approvals`](../governance/approvals.py)) renders to
   humans.
2. **Provenance everywhere.** Every cross-agent message, MCP call, and
   marketing claim carries source metadata and a trust level.
3. **Capability scope, not God-mode.** Agents declare positive capability
   scopes and a `forbidden_capabilities` list. Any action outside the scope
   is denied at the comms gate, not at runtime.
4. **Revenue means cash.** `money.verified_revenue` only counts cash that
   matches one of `payment_received`, `signed_agreement`, `retainer_active`,
   `partner_paid_customer`.
5. **Founder time is finite.** `sovereignty.founder_time` is a first-class
   cost. Anything that consumes founder time without producing an asset or a
   retainer is flagged for repositioning.

See [`docs/enterprise/`](../../docs/enterprise/) for the customer-facing
governance documents that this layer produces.
