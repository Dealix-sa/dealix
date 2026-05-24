"""
MCP Gateway — §90.

Vets external Model Context Protocol servers before agents talk to
them. Enforces manifest verification, semantic vetting of tool names,
runtime anomaly checks, and an emergency kill switch.
"""

from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass, field
from typing import Any

from dealix.sovereign_control_plane.context_feed import ContextPacket
from dealix.sovereign_control_plane.tool_gateway import ToolDescriptor
from dealix.sovereign_control_plane.types import RiskLevel


_SUSPICIOUS_TOKENS = (
    "exfiltrate", "send_all", "dump", "wire_transfer", "ssh_exec",
    "delete_all", "drop_table", "rm_rf", "leak", "scrape_all",
)


@dataclass
class MCPServerDescriptor:
    server_id: str
    name: str
    manifest_hash: str
    allowed_tools: list[str] = field(default_factory=list)
    vetted: bool = False
    kill_switch_enabled: bool = False
    last_anomaly_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "server_id": self.server_id,
            "name": self.name,
            "manifest_hash": self.manifest_hash,
            "allowed_tools": list(self.allowed_tools),
            "vetted": self.vetted,
            "kill_switch_enabled": self.kill_switch_enabled,
            "last_anomaly_score": self.last_anomaly_score,
            "metadata": dict(self.metadata),
        }


def manifest_hash_of(manifest: dict[str, Any]) -> str:
    import json
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class MCPGateway:
    def __init__(self) -> None:
        self._servers: dict[str, MCPServerDescriptor] = {}
        self._lock = threading.Lock()

    def register_server(self, descriptor: MCPServerDescriptor) -> MCPServerDescriptor:
        with self._lock:
            self._servers[descriptor.server_id] = descriptor
            return descriptor

    def get(self, server_id: str) -> MCPServerDescriptor | None:
        return self._servers.get(server_id)

    def verify_descriptor(
        self, server_id: str, manifest: dict[str, Any]
    ) -> bool:
        srv = self._servers.get(server_id)
        if srv is None:
            return False
        return manifest_hash_of(manifest) == srv.manifest_hash

    def semantic_vet(self, tool: ToolDescriptor) -> bool:
        """Return False if the tool name contains a suspicious token."""
        name = tool.name.lower()
        return not any(tok in name for tok in _SUSPICIOUS_TOKENS)

    def runtime_anomaly_check(self, call: dict[str, Any]) -> RiskLevel:
        size = len(str(call.get("args", "")))
        if size > 50_000:
            return RiskLevel.CRITICAL
        if size > 5_000:
            return RiskLevel.HIGH
        if size > 500:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def kill(self, server_id: str) -> bool:
        with self._lock:
            srv = self._servers.get(server_id)
            if srv is None:
                return False
            srv.kill_switch_enabled = True
            return True

    def call(
        self,
        server_id: str,
        tool_name: str,
        args: dict[str, Any],
        context_packet: ContextPacket | None = None,
    ) -> dict[str, Any]:
        srv = self._servers.get(server_id)
        if srv is None:
            return {"ok": False, "reason": "server_not_registered"}
        if srv.kill_switch_enabled:
            return {"ok": False, "reason": "kill_switch_enabled"}
        if not srv.vetted:
            return {"ok": False, "reason": "not_vetted"}
        if tool_name not in srv.allowed_tools:
            return {"ok": False, "reason": "tool_not_allowed"}
        risk = self.runtime_anomaly_check({"args": args})
        srv.last_anomaly_score = {
            RiskLevel.NONE: 0.0, RiskLevel.LOW: 0.1, RiskLevel.MEDIUM: 0.4,
            RiskLevel.HIGH: 0.7, RiskLevel.CRITICAL: 0.95,
        }[risk]
        if risk in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            return {"ok": False, "reason": "anomaly_blocked", "risk": risk.value}
        return {"ok": True, "tool": tool_name, "risk": risk.value, "args": dict(args)}
