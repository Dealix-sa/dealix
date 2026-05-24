"""
Agent Registry — every agent must be registered with owner, KPIs, and max sovereignty.

Hard rules:
  - Agent without owner = forbidden
  - Agent without KPI = forbidden
  - Agent without max_sovereignty_level = forbidden
  - Agent using an unregistered tool = forbidden
"""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import AgentRecord, SovereigntyLevel


class AgentRegistryError(ValueError):
    """Raised when an agent registration violates a hard rule."""


class AgentRegistry:
    def __init__(self) -> None:
        self._items: dict[str, AgentRecord] = {}
        self._lock = RLock()

    def register(
        self,
        *,
        id: str,
        name: str,
        mission: str,
        domain: str,
        owner: str,
        max_sovereignty_level: SovereigntyLevel | str,
        allowed_tools: list[str] | None = None,
        forbidden_tools: list[str] | None = None,
        kpis: list[str] | None = None,
        status: str = "active",
    ) -> AgentRecord:
        if not owner:
            raise AgentRegistryError("agent_owner_required")
        if not kpis:
            raise AgentRegistryError("agent_kpis_required")
        if not max_sovereignty_level:
            raise AgentRegistryError("agent_max_sovereignty_required")
        record = AgentRecord(
            id=id,
            name=name,
            mission=mission,
            domain=domain,
            owner=owner,
            max_sovereignty_level=SovereigntyLevel(max_sovereignty_level),
            allowed_tools=allowed_tools or [],
            forbidden_tools=forbidden_tools or [],
            kpis=list(kpis),
            status=status,
        )
        with self._lock:
            self._items[id] = record
        return record

    def get(self, agent_id: str) -> AgentRecord | None:
        with self._lock:
            return self._items.get(agent_id)

    def list(self) -> list[AgentRecord]:
        with self._lock:
            return sorted(self._items.values(), key=lambda a: a.id)

    def can_use_tool(self, agent_id: str, tool_id: str) -> bool:
        with self._lock:
            agent = self._items.get(agent_id)
        if agent is None:
            return False
        if tool_id in agent.forbidden_tools:
            return False
        if agent.allowed_tools and tool_id not in agent.allowed_tools:
            return False
        return True

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


def _seed_default_agents(reg: AgentRegistry) -> None:
    """Seed the canonical agent roster from the spec."""
    reg.register(
        id="revenue_hunter",
        name="Revenue Hunter",
        mission="Find monetizable opportunities",
        domain="money",
        owner="Sami",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        allowed_tools=["read_opportunities", "draft_message"],
        forbidden_tools=["send_external", "sign_contract", "export_data"],
        kpis=["qualified_opportunities", "messages_drafted", "meetings_booked"],
    )
    reg.register(
        id="partner_scout",
        name="Partner Scout",
        mission="Identify and qualify partners",
        domain="partners",
        owner="Sami",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        allowed_tools=["read_opportunities", "draft_message"],
        forbidden_tools=["sign_contract", "send_external"],
        kpis=["partners_qualified", "partner_pitches_drafted"],
    )
    reg.register(
        id="market_radar",
        name="Market Radar",
        mission="Convert market signals into offers",
        domain="intelligence",
        owner="Sami",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        allowed_tools=["read_opportunities"],
        forbidden_tools=["send_external"],
        kpis=["signals_processed", "reports_generated"],
    )


_default_registry: AgentRegistry | None = None


def get_agent_registry() -> AgentRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = AgentRegistry()
        _seed_default_agents(_default_registry)
    return _default_registry
