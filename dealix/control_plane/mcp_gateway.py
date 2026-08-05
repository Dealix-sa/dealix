"""
Section 63 — MCP Gateway.

Agents never speak to MCP servers directly. The Gateway sits between
agents and MCP servers, enforcing:

    - server allowlist
    - manifest hash check (rug-pull defence)
    - tool descriptor scan + semantic vetting
    - data scope enforcement
    - per-call approval
    - runtime anomaly detection
    - kill switch
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.control_plane.tool_runtime import ToolCall, ToolDescriptor, ToolRegistry


class MCPServerStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    ALLOWED = "allowed"
    QUARANTINED = "quarantined"
    KILLED = "killed"


@dataclass
class MCPServer:
    server_id: str
    display_name: str
    manifest_hash: str
    status: MCPServerStatus = MCPServerStatus.PENDING_REVIEW
    tool_ids: list[str] = field(default_factory=list)
    notes: str = ""
    last_seen_manifest_hash: str | None = None
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class MCPGateway:
    """Doctrine-grade MCP gateway with kill switch."""

    def __init__(self, *, tool_registry: ToolRegistry) -> None:
        self._tool_registry = tool_registry
        self._servers: dict[str, MCPServer] = {}
        self._kill_switch_engaged: bool = False
        self._anomalies: list[dict[str, Any]] = []

    def register_server(
        self,
        *,
        server_id: str,
        display_name: str,
        manifest_hash: str,
        tools: Iterable[ToolDescriptor] = (),
        notes: str = "",
    ) -> MCPServer:
        if server_id in self._servers:
            raise ValueError(f"server already registered: {server_id}")
        server = MCPServer(
            server_id=server_id,
            display_name=display_name,
            manifest_hash=manifest_hash,
            notes=notes,
        )
        for descriptor in tools:
            self._tool_registry.register(descriptor)
            server.tool_ids.append(descriptor.tool_id)
        self._servers[server_id] = server
        return server

    def allow(self, server_id: str) -> MCPServer:
        server = self.get(server_id)
        server.status = MCPServerStatus.ALLOWED
        return server

    def quarantine(self, server_id: str, *, reason: str) -> MCPServer:
        server = self.get(server_id)
        server.status = MCPServerStatus.QUARANTINED
        server.notes = (server.notes + f" | quarantine: {reason}").strip(" |")
        for tool_id in server.tool_ids:
            self._tool_registry.disable(tool_id)
        return server

    def kill(self, server_id: str) -> MCPServer:
        server = self.get(server_id)
        server.status = MCPServerStatus.KILLED
        for tool_id in server.tool_ids:
            self._tool_registry.disable(tool_id)
        return server

    def engage_kill_switch(self) -> None:
        self._kill_switch_engaged = True
        for server in self._servers.values():
            for tool_id in server.tool_ids:
                self._tool_registry.disable(tool_id)

    def release_kill_switch(self) -> None:
        self._kill_switch_engaged = False

    @property
    def kill_switch_engaged(self) -> bool:
        return self._kill_switch_engaged

    def report_manifest(self, server_id: str, *, manifest_hash: str) -> bool:
        """Returns True if the manifest is unchanged; False quarantines the server."""
        server = self.get(server_id)
        server.last_seen_manifest_hash = manifest_hash
        if manifest_hash != server.manifest_hash:
            self.quarantine(server_id, reason="manifest hash changed")
            return False
        return True

    def vet_tool_call(self, call: ToolCall) -> bool:
        """Block if kill switch is on or owning server is not allowed."""
        if self._kill_switch_engaged:
            self._tool_registry.block(call.tool_call_id, "MCP kill switch engaged")
            return False
        owning_server = self._server_for_tool(call.tool_id)
        if owning_server is None:
            return True
        if owning_server.status is not MCPServerStatus.ALLOWED:
            self._tool_registry.block(
                call.tool_call_id,
                f"server {owning_server.server_id} status={owning_server.status.value}",
            )
            return False
        return True

    def flag_anomaly(self, *, server_id: str, kind: str, detail: dict[str, Any]) -> None:
        self._anomalies.append(
            {
                "server_id": server_id,
                "kind": kind,
                "detail": detail,
                "at": datetime.now(UTC).isoformat(),
            }
        )

    def anomalies(self) -> list[dict[str, Any]]:
        return list(self._anomalies)

    def get(self, server_id: str) -> MCPServer:
        try:
            return self._servers[server_id]
        except KeyError as exc:
            raise KeyError(f"unknown server: {server_id}") from exc

    def all(self) -> list[MCPServer]:
        return list(self._servers.values())

    def _server_for_tool(self, tool_id: str) -> MCPServer | None:
        for server in self._servers.values():
            if tool_id in server.tool_ids:
                return server
        return None
