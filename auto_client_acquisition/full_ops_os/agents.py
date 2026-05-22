"""Runtime agent pyramid for the Full Ops Sales System.

Eighteen governed agents — one conductor, four directors, thirteen
specialist workers — each carrying an ``AgentCard`` (non-negotiable #9:
no agent without identity). External-facing workers cap at ``L2_DRAFT``;
only the conductor reaches ``L4_AUTO_WITH_AUDIT``.

See ``docs/full_ops_sales_os/RUNTIME_AGENT_HIERARCHY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.agent_os import (
    AgentCard,
    AutonomyLevel,
    get_agent,
    new_card,
    register_agent,
)

OWNER = "founder"
KILL_SWITCH_OWNER = "founder"
CONDUCTOR_ID = "revenue-conductor"

# Tool grants by autonomy level, drawn only from ALLOWED_TOOLS_MVP.
_L4_TOOLS = ["read", "analyze", "recommend", "queue_for_approval"]
_L3_TOOLS = ["read", "analyze", "recommend"]
_L2_TOOLS = ["read", "analyze", "draft"]
_L1_TOOLS = ["read", "analyze"]


@dataclass(frozen=True, slots=True)
class FullOpsAgentSpec:
    """Static description of one runtime agent."""

    agent_id: str
    name: str
    tier: int  # 0 conductor | 1 director | 2 worker
    autonomy_level: AutonomyLevel
    allowed_tools: tuple[str, ...]
    purpose: str


FULL_OPS_AGENT_SPECS: tuple[FullOpsAgentSpec, ...] = (
    # ── Tier 0 — conductor ───────────────────────────────────────
    FullOpsAgentSpec(
        CONDUCTOR_ID, "Revenue Conductor", 0,
        AutonomyLevel.L4_AUTO_WITH_AUDIT, tuple(_L4_TOOLS),
        "Owns the workflow run; sequences the 12 stages; routes external actions to approval.",
    ),
    # ── Tier 1 — domain directors ────────────────────────────────
    FullOpsAgentSpec(
        "sales-director", "Sales Director", 1,
        AutonomyLevel.L3_RECOMMEND, tuple(_L3_TOOLS),
        "Owns stages 1-8: signal intake through the approval gate.",
    ),
    FullOpsAgentSpec(
        "delivery-director", "Delivery Director", 1,
        AutonomyLevel.L3_RECOMMEND, tuple(_L3_TOOLS),
        "Owns stages 9-10: delivery and Proof Pack closure.",
    ),
    FullOpsAgentSpec(
        "growth-director", "Growth Director", 1,
        AutonomyLevel.L3_RECOMMEND, tuple(_L3_TOOLS),
        "Owns stages 11-12: expansion, learning, authority content.",
    ),
    FullOpsAgentSpec(
        "governance-warden", "Governance Warden", 1,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Evaluates every action against the auto-exec boundary before it runs.",
    ),
    # ── Tier 2 — specialist workers ──────────────────────────────
    FullOpsAgentSpec(
        "lead-intake-agent", "Lead Intake Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Stage 1: intake + Source Passport validation.",
    ),
    FullOpsAgentSpec(
        "enrichment-agent", "Enrichment Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 2: enrichment waterfall over declared sources.",
    ),
    FullOpsAgentSpec(
        "scoring-agent", "Scoring Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 3: ICP, account, and risk scoring.",
    ),
    FullOpsAgentSpec(
        "pain-extraction-agent", "Pain Extraction Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 4: extract pain signals from the request.",
    ),
    FullOpsAgentSpec(
        "qualification-agent", "Qualification Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Stage 5: the 8-question qualification.",
    ),
    FullOpsAgentSpec(
        "prioritization-agent", "Prioritization Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 6: pipeline prioritization.",
    ),
    FullOpsAgentSpec(
        "draft-agent", "Draft Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Stage 7: proposal and outreach drafts — draft only, never sends.",
    ),
    FullOpsAgentSpec(
        "followup-agent", "Follow-up Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Stage 8: prepares the gated follow-up/outreach for approval.",
    ),
    FullOpsAgentSpec(
        "proof-agent", "Proof Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Stages 9-10: delivery assembly and Proof Pack.",
    ),
    FullOpsAgentSpec(
        "value-agent", "Value Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Support: records value-ledger events during delivery and proof.",
    ),
    FullOpsAgentSpec(
        "expansion-agent", "Expansion Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 11: adoption and retainer-readiness assessment.",
    ),
    FullOpsAgentSpec(
        "content-agent", "Content Agent", 2,
        AutonomyLevel.L2_DRAFT, tuple(_L2_TOOLS),
        "Support: drafts anonymized authority content from proof.",
    ),
    FullOpsAgentSpec(
        "friction-agent", "Friction Agent", 2,
        AutonomyLevel.L1_ANALYZE, tuple(_L1_TOOLS),
        "Stage 12: aggregates operational friction for learning.",
    ),
)

# Highest autonomy any external-facing worker may hold.
EXTERNAL_FACING_MAX_LEVEL: AutonomyLevel = AutonomyLevel.L2_DRAFT

_SPEC_BY_ID: dict[str, FullOpsAgentSpec] = {s.agent_id: s for s in FULL_OPS_AGENT_SPECS}


def build_card(spec: FullOpsAgentSpec) -> AgentCard:
    """Construct a validated AgentCard from a spec."""
    kill_switch = (
        KILL_SWITCH_OWNER
        if spec.autonomy_level >= AutonomyLevel.L4_AUTO_WITH_AUDIT
        else ""
    )
    return new_card(
        agent_id=spec.agent_id,
        name=spec.name,
        owner=OWNER,
        purpose=spec.purpose,
        autonomy_level=spec.autonomy_level,
        allowed_tools=list(spec.allowed_tools),
        kill_switch_owner=kill_switch,
        notes=f"full_ops_os tier {spec.tier}",
    )


def register_full_ops_agents() -> list[AgentCard]:
    """Register every Full Ops agent. Idempotent — skips already-registered IDs."""
    cards: list[AgentCard] = []
    for spec in FULL_OPS_AGENT_SPECS:
        existing = get_agent(spec.agent_id)
        if existing is not None:
            cards.append(existing)
            continue
        cards.append(register_agent(build_card(spec)))
    return cards


def spec_for(agent_id: str) -> FullOpsAgentSpec | None:
    """Return the spec for an agent id, or None."""
    return _SPEC_BY_ID.get(agent_id)


__all__ = [
    "CONDUCTOR_ID",
    "EXTERNAL_FACING_MAX_LEVEL",
    "FULL_OPS_AGENT_SPECS",
    "FullOpsAgentSpec",
    "build_card",
    "register_full_ops_agents",
    "spec_for",
]
