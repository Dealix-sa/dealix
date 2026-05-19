"""Strategic agent tier — the CEO/board pyramid above Full Ops.

A separate hierarchy that sits ABOVE the Full Ops Chief of Staff. It is
never merged with ``full_ops.agent_hierarchy`` (whose tests pin its exact
shape). Every node is registered through the existing ``agent_registry``
at autonomy L3 (recommend) — nothing in this tier ever runs above L3, and
nothing auto-executes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, new_card
from auto_client_acquisition.agent_os.agent_registry import (
    get_agent,
    list_agents,
    register_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel

# Hard ceiling for every node in the strategic tier (never exceed L3).
STRATEGIC_MAX_AUTONOMY_LEVEL: int = int(AutonomyLevel.L3_RECOMMEND)

_OWNER = "founder"
_KILL_SWITCH_OWNER = "founder"
_L3 = int(AutonomyLevel.L3_RECOMMEND)

# The operational orchestrator the CEO tier delegates execution to.
OPERATIONAL_ORCHESTRATOR_ID: str = "fo_orchestrator_chief_of_staff"


@dataclass(frozen=True, slots=True)
class StrategicHierarchyNode:
    """One node in the strategic (CEO/board) agent pyramid."""

    tier: str  # "ceo" | "director"
    agent_id: str
    name: str
    role_ar: str
    role_en: str
    parent_id: str | None
    autonomy_level: int
    delegates_to: tuple[str, ...] = field(default_factory=tuple)
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tier": self.tier,
            "agent_id": self.agent_id,
            "name": self.name,
            "role_ar": self.role_ar,
            "role_en": self.role_en,
            "parent_id": self.parent_id,
            "autonomy_level": self.autonomy_level,
            "delegates_to": list(self.delegates_to),
            "capabilities": list(self.capabilities),
            "allowed_tools": list(self.allowed_tools),
        }


# ── CEO orchestrator ──────────────────────────────────────────────────

_CEO = StrategicHierarchyNode(
    tier="ceo",
    agent_id="sa_ceo_strategic_orchestrator",
    name="Strategic Orchestrator (CEO)",
    role_ar="المنسّق الاستراتيجي — يقود الحلقة الاستراتيجية ويفوّض التنفيذ",
    role_en="Strategic Orchestrator — runs the strategic loop, delegates execution",
    parent_id=None,
    autonomy_level=_L3,
    delegates_to=(OPERATIONAL_ORCHESTRATOR_ID,),
    capabilities=("aggregate_signals", "evaluate_gates", "decide", "delegate"),
    allowed_tools=("read", "analyze", "recommend"),
)


# ── Board directors ───────────────────────────────────────────────────

_DIRECTORS: tuple[StrategicHierarchyNode, ...] = (
    StrategicHierarchyNode(
        tier="director",
        agent_id="sa_director_strategy",
        name="Strategy Director",
        role_ar="مدير الاستراتيجية — يقيّم بوابات التوسّع والبناء",
        role_en="Strategy Director — evaluates scale and build gates",
        parent_id=_CEO.agent_id,
        autonomy_level=_L3,
        delegates_to=(),
        capabilities=("evaluate_strategy_gates", "recommend_scale"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    StrategicHierarchyNode(
        tier="director",
        agent_id="sa_director_capital",
        name="Capital Director",
        role_ar="مدير رأس المال — يقيّم تخصيص رأس المال والتسعير",
        role_en="Capital Director — evaluates capital allocation and pricing",
        parent_id=_CEO.agent_id,
        autonomy_level=_L3,
        delegates_to=(),
        capabilities=("evaluate_capital", "recommend_price"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    StrategicHierarchyNode(
        tier="director",
        agent_id="sa_director_risk_governance",
        name="Risk and Governance Director",
        role_ar="مدير المخاطر والحوكمة — يحرس الخطوط الحمراء الاستراتيجية",
        role_en="Risk and Governance Director — guards strategic non-negotiables",
        parent_id=_CEO.agent_id,
        autonomy_level=_L3,
        delegates_to=(),
        capabilities=("enforce_doctrine", "block_unsafe", "require_approval"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    StrategicHierarchyNode(
        tier="director",
        agent_id="sa_director_ventures",
        name="Ventures Director",
        role_ar="مدير المشاريع الجديدة — يقيّم وحدات الأعمال ومرشّحي venture",
        role_en="Ventures Director — evaluates business units and venture candidates",
        parent_id=_CEO.agent_id,
        autonomy_level=_L3,
        delegates_to=(),
        capabilities=("evaluate_ventures", "recommend_business_unit"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
)


def all_strategic_nodes() -> tuple[StrategicHierarchyNode, ...]:
    """Return every node in the strategic tier (CEO + directors)."""
    return (_CEO, *_DIRECTORS)


def _purpose(node: StrategicHierarchyNode) -> str:
    return f"Strategic tier {node.tier}: {node.role_en}"


def _node_to_card(node: StrategicHierarchyNode) -> AgentCard:
    """Build a validated :class:`AgentCard` for a strategic node.

    Asserts the L3 ceiling defensively before delegating to ``new_card``.
    """
    if node.autonomy_level > STRATEGIC_MAX_AUTONOMY_LEVEL:
        raise ValueError(
            f"node {node.agent_id} autonomy_level {node.autonomy_level} "
            f"exceeds the L3 ceiling"
        )
    return new_card(
        agent_id=node.agent_id,
        name=node.name,
        owner=_OWNER,
        purpose=_purpose(node),
        autonomy_level=node.autonomy_level,
        allowed_tools=list(node.allowed_tools),
        kill_switch_owner=_KILL_SWITCH_OWNER,
        notes=f"parent={node.parent_id or 'none'}; tier={node.tier}",
    )


def seed_strategic_tier() -> list[AgentCard]:
    """Register every strategic-tier node as an :class:`AgentCard`.

    Idempotent: an already-registered node is returned as-is rather than
    re-registered. Returns the full set of cards.
    """
    cards: list[AgentCard] = []
    for node in all_strategic_nodes():
        existing = get_agent(node.agent_id)
        if existing is not None:
            cards.append(existing)
            continue
        card = _node_to_card(node)
        try:
            cards.append(register_agent(card))
        except ValueError:
            again = get_agent(node.agent_id)
            cards.append(again if again is not None else card)
    return cards


def get_strategic_tier() -> dict[str, Any]:
    """Return the strategic tier as a CEO node plus board directors."""
    return {
        "ceo": _CEO.to_dict(),
        "board_directors": [d.to_dict() for d in _DIRECTORS],
        "delegates_to_operational": OPERATIONAL_ORCHESTRATOR_ID,
        "totals": {
            "board_directors": len(_DIRECTORS),
            "max_autonomy_level": STRATEGIC_MAX_AUTONOMY_LEVEL,
        },
    }


def strategic_tier_status() -> dict[str, Any]:
    """Return the strategic tier annotated with live registry status."""
    registered = {c.agent_id: c for c in list_agents()}

    def _status(agent_id: str) -> str:
        card = registered.get(agent_id)
        return card.status if card is not None else "unregistered"

    tree = get_strategic_tier()
    tree["ceo"]["status"] = _status(tree["ceo"]["agent_id"])
    for director in tree["board_directors"]:
        director["status"] = _status(director["agent_id"])
    return tree


__all__ = [
    "OPERATIONAL_ORCHESTRATOR_ID",
    "STRATEGIC_MAX_AUTONOMY_LEVEL",
    "StrategicHierarchyNode",
    "all_strategic_nodes",
    "get_strategic_tier",
    "seed_strategic_tier",
    "strategic_tier_status",
]
