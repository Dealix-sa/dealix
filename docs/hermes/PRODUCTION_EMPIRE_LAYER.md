# Hermes — Production Empire Layer

> Dealix is not an AI agent tool.
> Dealix is a sovereign control plane for governed AI execution and verified revenue.

This document is the high-level map for the `dealix/hermes/` namespace
introduced in sections 101–130 of the product master plan. It tells you
where each capability lives in code, which sub-systems compose into
which surfaces, and the hard rules that hold the layer together.

## Why this layer exists

The market is full of "AI agent" tools that are really just chatbots or
workflows under a new label. Independent analysts have warned that a
large share of agentic AI projects will be cancelled because of poor
ROI and weak governance ("agent washing"). Dealix wins by treating
governance and verified revenue as the *product* — not as compliance
checkboxes.

| Risk Dealix counters | How |
| --- | --- |
| Agent washing | Lifecycle gates + outcome logging + verified revenue |
| Prompt injection (direct + indirect) | `agent_comms.message_sanitizer` + `security.indirect_injection_detector` |
| Second-order injection via cross-agent calls | `agent_comms.delegation_policy` |
| MCP tool poisoning / shadowing / rug pulls | `mcp.gateway` (allowlist + manifest + descriptor + semantic + runtime) |
| Hallucinated marketing claims | `security.claim_verifier` |
| Data exfiltration | `security.data_loss_prevention` |
| Untrusted instructions | `provenance.downstream_validation` |
| Pipeline theatre | `money.verified_revenue` |
| Bad founder-time allocation | `sovereignty.founder_time` + `money.founder_time_cost` |
| Marketing invisible to AI search | `growth.geo` |

## File tree

```
dealix/hermes/
  control_plane/                # composes all the primitives below
  agent_lifecycle/              # registry → risk → scope → eval → promote → restrict → retire
  identity/                     # scoped, revocable, capability-bound identities + sessions
  agent_comms/                  # sanitize, source-trust, delegation, cross-agent validator
  provenance/                   # ledger, source metadata, trust level, lineage, downstream validation
  mcp/                          # allowlist, manifest review, descriptor scan, semantic vetting,
                                # capability attestation, runtime guardrails, anomaly detection,
                                # kill switch, gateway
  security/                     # prompt-injection vectors, indirect-injection detector,
                                # output sanitizer, instruction/data separator, DLP,
                                # claim verifier, red-team playbooks
  growth/
    trust_signals.py
    review_engine.py
    entity_consistency.py
    public_methodology.py
    revenue_status.py
    geo/                        # ai_visibility, answer_engine_pages, citation_assets,
                                # faq_builder, comparison_builder, entity_consistency,
                                # ai_search_monitor
    attribution/                # channel, campaign, message, asset, agent, partner,
                                # geo, trust_signal + composite record
    entity_data/                # company_profile, product, offer, faq, review schemas
  money/                        # verified_revenue, revenue_quality, founder_time_cost,
                                # delivery_margin
  sovereignty/                  # founder_time
  products/                     # offer_market_fit, experiment_metrics, repositioning,
                                # readiness_gate, from_asset, packages
  assets/                       # asset_to_product, commercialization
  partners/program/             # tiers, approved_claims, enablement, co_marketing,
                                # revenue_share, compliance, performance_review
  delivery/                     # delivery_playbook + 5 offer-specific playbooks +
                                # quality_checklists
  board/                        # executive_metrics, investor_update, board_memo,
                                # traction_report
```

## Hard rules

1. **No outbound sends without approval.** External messages, contract
   signing, refunds, exports, and production-config changes go through
   `dealix.governance.approvals.ApprovalGate`.
2. **No untrusted source can issue instructions.** Anything tagged
   `TrustLevel.UNTRUSTED` or `QUARANTINED` is treated as data.
3. **No lower-privilege agent can delegate externally-visible actions
   to a higher-privilege agent.**
4. **No MCP server is enabled without S4 Sovereign Approval.**
5. **No marketing or proposal text ships with absolute or unsupported
   claims.**
6. **Revenue means cash.** `money.verified_revenue.is_verified` is the
   single source of truth.
7. **Founder time is finite.** `sovereignty.founder_time.unproductive_hours`
   is a first-class KPI.

## How to use the layer

The simplest entry point is `dealix.hermes.control_plane.ControlPlane`:

```python
from dealix.hermes.control_plane import ControlPlane
from dealix.hermes.identity import IdentityStatus, SessionPolicy, build_identity

plane = ControlPlane()
identity = build_identity(
    "proposal_factory",
    "Sami",
    capability_scope=["read_approved_opportunity", "draft_proposal", "flag_risk"],
    forbidden_capabilities=["send_external", "sign_contract"],
)
identity.status = IdentityStatus.ACTIVE
plane.register_identity(identity)
session = plane.open_session(
    "proposal_factory",
    SessionPolicy(ttl_seconds=900, idle_timeout_seconds=300, max_operations=50),
)
decision = plane.authorize_capability(session.session_id, "draft_proposal")
assert decision.allowed
```

Sub-systems are also usable directly without the plane (the package is
intentionally pure-Python and side-effect-free at import time), so a
worker can compose only what it needs.

## Tests

Run the layer's tests:

```bash
cd tests/hermes
python -m pytest . --noconftest --override-ini="addopts=" -q
```

The Hermes tests intentionally do not depend on the global FastAPI /
Postgres / Redis stack so they can run inside a pre-commit hook or a
narrow CI job. The wider test suite continues to live under `tests/`.
