"""Verify tool name + version is on the approved registry."""

from __future__ import annotations

from dataclasses import dataclass

_APPROVED_TOOLS: dict[str, set[str]] = {}


@dataclass(frozen=True)
class ToolAttestation:
    tool_name: str
    tool_version: str
    approved: bool


def register_tool(tool_name: str, version: str) -> None:
    """Add a (tool, version) pair to the approved registry."""
    _APPROVED_TOOLS.setdefault(tool_name, set()).add(version)


def attest_tool(tool_name: str, tool_version: str) -> ToolAttestation:
    """Return ToolAttestation indicating if the tool+version is approved."""
    versions = _APPROVED_TOOLS.get(tool_name, set())
    return ToolAttestation(tool_name=tool_name, tool_version=tool_version, approved=tool_version in versions)


def clear_registry() -> None:
    """Reset the in-memory tool registry (test helper)."""
    _APPROVED_TOOLS.clear()
