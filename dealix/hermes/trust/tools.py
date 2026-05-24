"""
Tool registry — every tool an agent can call must be declared here.

A tool record names the owner, the scope of side-effects, and whether the
tool needs explicit per-call approval.
"""

from __future__ import annotations

from pydantic import BaseModel


class ToolRecord(BaseModel):
    tool_id: str
    owner: str
    description: str
    side_effects: str  # "none" | "internal" | "external" | "financial"
    requires_per_call_approval: bool = False
    enabled: bool = True


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolRecord] = {}

    def register(self, tool: ToolRecord) -> None:
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> ToolRecord | None:
        return self._tools.get(tool_id)

    def list_all(self) -> list[ToolRecord]:
        return list(self._tools.values())

    def list_external(self) -> list[ToolRecord]:
        return [t for t in self._tools.values() if t.side_effects in {"external", "financial"}]


_default_registry = ToolRegistry()


def default_registry() -> ToolRegistry:
    return _default_registry
