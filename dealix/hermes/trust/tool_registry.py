"""
Tool Registry — every tool must be registered with owner, risk level, and scope.

Hard rules:
  - Tool without owner = forbidden
  - Tool without risk_level = forbidden
  - External tool without approval = forbidden
  - MCP tool without review = forbidden
"""

from __future__ import annotations

from threading import RLock

from dealix.hermes.core.schemas import RiskLevel, ToolRecord


class ToolRegistryError(ValueError):
    """Raised when a tool registration violates a hard rule."""


class ToolRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ToolRecord] = {}
        self._lock = RLock()

    def register(
        self,
        *,
        id: str,
        name: str,
        tool_type: str,
        owner: str,
        risk_level: RiskLevel | str,
        requires_approval: bool = True,
        enabled: bool = False,
        data_scope: str = "tenant_only",
        allowed_agents: list[str] | None = None,
        audit_required: bool = True,
    ) -> ToolRecord:
        if not owner:
            raise ToolRegistryError("tool_owner_required")
        if risk_level is None:
            raise ToolRegistryError("tool_risk_level_required")
        if tool_type == "external" and not requires_approval:
            raise ToolRegistryError("external_tool_requires_approval")
        if tool_type == "mcp" and not requires_approval:
            raise ToolRegistryError("mcp_tool_requires_review_and_approval")
        record = ToolRecord(
            id=id,
            name=name,
            tool_type=tool_type,
            owner=owner,
            risk_level=RiskLevel(risk_level),
            requires_approval=requires_approval,
            enabled=enabled,
            data_scope=data_scope,
            allowed_agents=allowed_agents or [],
            audit_required=audit_required,
        )
        with self._lock:
            self._items[id] = record
        return record

    def get(self, tool_id: str) -> ToolRecord | None:
        with self._lock:
            return self._items.get(tool_id)

    def list(self) -> list[ToolRecord]:
        with self._lock:
            return sorted(self._items.values(), key=lambda t: t.id)

    def enable(self, tool_id: str) -> ToolRecord | None:
        with self._lock:
            tool = self._items.get(tool_id)
            if tool is None:
                return None
            updated = tool.model_copy(update={"enabled": True})
            self._items[tool_id] = updated
            return updated

    def disable(self, tool_id: str) -> ToolRecord | None:
        with self._lock:
            tool = self._items.get(tool_id)
            if tool is None:
                return None
            updated = tool.model_copy(update={"enabled": False})
            self._items[tool_id] = updated
            return updated

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


def _seed_default_tools(reg: ToolRegistry) -> None:
    reg.register(
        id="read_opportunities",
        name="Read Opportunities",
        tool_type="internal",
        owner="Sami",
        risk_level=RiskLevel.LOW,
        requires_approval=False,
        enabled=True,
        data_scope="tenant_only",
        audit_required=False,
    )
    reg.register(
        id="draft_message",
        name="Draft Internal Message",
        tool_type="internal",
        owner="Sami",
        risk_level=RiskLevel.LOW,
        requires_approval=False,
        enabled=True,
        data_scope="tenant_only",
    )
    reg.register(
        id="send_external",
        name="Send External Communication",
        tool_type="external",
        owner="Sami",
        risk_level=RiskLevel.HIGH,
        requires_approval=True,
        enabled=False,
    )
    reg.register(
        id="sign_contract",
        name="Sign Contract on Behalf",
        tool_type="external",
        owner="Sami",
        risk_level=RiskLevel.CRITICAL,
        requires_approval=True,
        enabled=False,
    )
    reg.register(
        id="export_data",
        name="Export Tenant Data",
        tool_type="external",
        owner="Sami",
        risk_level=RiskLevel.CRITICAL,
        requires_approval=True,
        enabled=False,
        data_scope="restricted",
    )


_default_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = ToolRegistry()
        _seed_default_tools(_default_registry)
    return _default_registry
