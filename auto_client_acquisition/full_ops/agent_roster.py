"""V12 Full-Ops — the 3-tier agent pyramid built on ``agent_os`` cards.

This module defines the autonomous workforce as ``agent_os`` agent
cards. It introduces NO new agent framework — every agent is an
``AgentCard`` produced by ``agent_os.new_card`` and registered through
``agent_os.register_agent``.

Pyramid:
  - Tier 1 — Chief agents (strategic, decide what to work on).
  - Tier 2 — Operator agents (tactical, produce draft artifacts).
  - Tier 3 — Tool agents (atomic, no decisions: render / score / write).

Hard rule: autonomy is capped at L4. L5 (fully autonomous) is forbidden
and is never used by any card here.
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
from auto_client_acquisition.full_ops.work_item import OSType

# Internal-only tools — no send/charge/scrape tool is ever granted.
_OPERATOR_TOOLS: list[str] = ["read", "analyze", "draft", "queue_for_approval"]
_CHIEF_TOOLS: list[str] = ["read", "analyze", "recommend", "queue_for_approval"]
_TOOL_AGENT_TOOLS: list[str] = ["read", "draft"]

_KILL_SWITCH_OWNER = "founder"


@dataclass(frozen=True, slots=True)
class RosterEntry:
    """A single agent definition before it becomes an ``AgentCard``."""

    agent_id: str
    name: str
    purpose: str
    tier: int
    autonomy_level: AutonomyLevel
    capability_tags: tuple[str, ...]
    allowed_tools: tuple[str, ...]


# ── Tier 1 — Chief agents ────────────────────────────────────────
_TIER1: tuple[RosterEntry, ...] = (
    RosterEntry(
        agent_id="fo-chief-revenue",
        name="Chief Revenue",
        purpose="Decide revenue priorities across Growth and Sales OS each tick.",
        tier=1,
        autonomy_level=AutonomyLevel.L3_RECOMMEND,
        capability_tags=("growth", "sales"),
        allowed_tools=tuple(_CHIEF_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-chief-delivery",
        name="Chief Delivery",
        purpose="Decide delivery and retention priorities across Delivery and "
        "Customer Success OS.",
        tier=1,
        autonomy_level=AutonomyLevel.L3_RECOMMEND,
        capability_tags=("delivery", "customer_success"),
        allowed_tools=tuple(_CHIEF_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-chief-intelligence",
        name="Chief Intelligence",
        purpose="Decide what sector and account intelligence to surface each tick.",
        tier=1,
        autonomy_level=AutonomyLevel.L3_RECOMMEND,
        capability_tags=("self_improvement", "executive"),
        allowed_tools=tuple(_CHIEF_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-chief-governance",
        name="Chief Governance",
        purpose="Enforce doctrine across the loop and own escalation of "
        "blocked actions.",
        tier=1,
        autonomy_level=AutonomyLevel.L3_RECOMMEND,
        capability_tags=("compliance",),
        allowed_tools=tuple(_CHIEF_TOOLS),
    ),
)


# ── Tier 2 — Operator agents ─────────────────────────────────────
_TIER2: tuple[RosterEntry, ...] = (
    RosterEntry(
        agent_id="fo-lead-scout",
        name="Lead Scout",
        purpose="Triage inbound growth signals into qualified WorkItems.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("growth",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-qualifier",
        name="Qualifier",
        purpose="Qualify sales WorkItems against the ICP and draft next steps.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("sales",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-account-scorer",
        name="Account Scorer",
        purpose="Score accounts and rank executive WorkItems by opportunity.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("executive",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-proposal-drafter",
        name="Proposal Drafter",
        purpose="Draft proposals and outreach artifacts (draft-only, never sent).",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("support",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-sprint-runner",
        name="Sprint Runner",
        purpose="Drive delivery WorkItems through their sprint steps.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("delivery",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-proof-assembler",
        name="Proof Assembler",
        purpose="Assemble proof artifacts for customer success WorkItems.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("customer_success",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-friction-watcher",
        name="Friction Watcher",
        purpose="Watch compliance WorkItems and draft governance escalations.",
        tier=2,
        autonomy_level=AutonomyLevel.L2_DRAFT,
        capability_tags=("compliance",),
        allowed_tools=tuple(_OPERATOR_TOOLS),
    ),
)


# ── Tier 3 — Tool agents ─────────────────────────────────────────
_TIER3: tuple[RosterEntry, ...] = (
    RosterEntry(
        agent_id="fo-tool-renderer",
        name="Artifact Renderer",
        purpose="Render bilingual draft artifacts from structured input.",
        tier=3,
        autonomy_level=AutonomyLevel.L1_ANALYZE,
        capability_tags=(),
        allowed_tools=tuple(_TOOL_AGENT_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-tool-scorer",
        name="Score Calculator",
        purpose="Compute deterministic scores for prioritization.",
        tier=3,
        autonomy_level=AutonomyLevel.L1_ANALYZE,
        capability_tags=(),
        allowed_tools=tuple(_TOOL_AGENT_TOOLS),
    ),
    RosterEntry(
        agent_id="fo-tool-ledger-writer",
        name="Ledger Writer",
        purpose="Append tick records to the operating-loop ledger.",
        tier=3,
        autonomy_level=AutonomyLevel.L1_ANALYZE,
        capability_tags=(),
        allowed_tools=tuple(_TOOL_AGENT_TOOLS),
    ),
)


ROSTER: tuple[RosterEntry, ...] = _TIER1 + _TIER2 + _TIER3


# WorkItem ``os_type`` → operator agent_id that handles it.
_CAPABILITY_MAP: dict[OSType, str] = {
    "growth": "fo-lead-scout",
    "sales": "fo-qualifier",
    "executive": "fo-account-scorer",
    "support": "fo-proposal-drafter",
    "delivery": "fo-sprint-runner",
    "customer_success": "fo-proof-assembler",
    "compliance": "fo-friction-watcher",
    "partnership": "fo-qualifier",
    "self_improvement": "fo-account-scorer",
}

# Default operator when no specific mapping applies.
_DEFAULT_OPERATOR = "fo-qualifier"


def build_roster_cards() -> list[AgentCard]:
    """Build (but do not register) every agent card in the pyramid.

    Pure function — useful for tests that need the cards without
    touching the process-global registry.
    """
    cards: list[AgentCard] = []
    for entry in ROSTER:
        level = int(entry.autonomy_level)
        kill_switch = (
            _KILL_SWITCH_OWNER if level >= int(AutonomyLevel.L4_AUTO_WITH_AUDIT) else ""
        )
        cards.append(
            new_card(
                agent_id=entry.agent_id,
                name=entry.name,
                owner="founder",
                purpose=entry.purpose,
                autonomy_level=level,
                allowed_tools=list(entry.allowed_tools),
                kill_switch_owner=kill_switch,
                notes=f"full_ops tier {entry.tier}",
            )
        )
    return cards


def register_full_ops_agents() -> list[AgentCard]:
    """Register every pyramid agent in the ``agent_os`` registry.

    Idempotent: an agent already present in the registry is returned
    as-is rather than re-registered (the registry rejects duplicates).
    """
    registered: list[AgentCard] = []
    for card in build_roster_cards():
        existing = get_agent(card.agent_id)
        if existing is not None:
            registered.append(existing)
            continue
        registered.append(register_agent(card))
    return registered


def capability_map() -> dict[OSType, str]:
    """Return a copy of the WorkItem ``os_type`` → operator agent map."""
    return dict(_CAPABILITY_MAP)


def agent_for_os(os_type: OSType) -> str:
    """Return the operator agent_id responsible for ``os_type``."""
    return _CAPABILITY_MAP.get(os_type, _DEFAULT_OPERATOR)


def roster_summary() -> dict[str, object]:
    """Bilingual structural summary of the pyramid (no registry access)."""
    by_tier: dict[int, list[dict[str, object]]] = {1: [], 2: [], 3: []}
    for entry in ROSTER:
        by_tier[entry.tier].append(
            {
                "agent_id": entry.agent_id,
                "name": entry.name,
                "autonomy_level": int(entry.autonomy_level),
                "capability_tags": list(entry.capability_tags),
            }
        )
    return {
        "title_ar": "هرم وكلاء Full-Ops",
        "title_en": "Full-Ops Agent Pyramid",
        "tier_1_chief": by_tier[1],
        "tier_2_operator": by_tier[2],
        "tier_3_tool": by_tier[3],
        "total_agents": len(ROSTER),
        "max_autonomy_level": max(int(e.autonomy_level) for e in ROSTER),
    }


def pyramid_status() -> dict[str, object]:
    """Live pyramid status — the structural summary plus registry state.

    Reads the ``agent_os`` registry so each agent reports whether it is
    registered and its current lifecycle status. Always reaffirms the
    autonomy cap: L4 is the ceiling, L5 is forbidden.
    """
    summary = roster_summary()
    tier_keys = ("tier_1_chief", "tier_2_operator", "tier_3_tool")
    for key in tier_keys:
        rows = summary.get(key, [])
        if not isinstance(rows, list):
            continue
        for row in rows:
            card = get_agent(str(row["agent_id"]))
            row["registered"] = card is not None
            row["status"] = card.status if card is not None else "unregistered"
    summary["max_autonomy_level"] = int(AutonomyLevel.L4_AUTO_WITH_AUDIT)
    summary["l5_forbidden"] = True
    summary["capability_map"] = capability_map()
    return summary


__all__ = [
    "ROSTER",
    "RosterEntry",
    "agent_for_os",
    "build_roster_cards",
    "capability_map",
    "pyramid_status",
    "register_full_ops_agents",
    "roster_summary",
]
