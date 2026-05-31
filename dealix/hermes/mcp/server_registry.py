"""MCP server registry — only approved servers may be called."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ServerState(StrEnum):
    pending = "pending"
    approved = "approved"
    blocked = "blocked"
    deprecated = "deprecated"


class MCPServerCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    server_id: str
    name: str
    owner: str = "Sami"
    endpoint: str
    state: ServerState = ServerState.pending
    manifest_hash: str | None = None
    manifest_signed: bool = False
    data_scope: str = "internal_only"
    external_execution_enabled: bool = False
    audit_required: bool = True
    last_reviewed_at: str | None = None
    notes: str = ""


@dataclass
class MCPServerRegistry:
    _servers: dict[str, MCPServerCard] = field(default_factory=dict)

    def register(self, card: MCPServerCard) -> MCPServerCard:
        self._servers[card.server_id] = card
        return card

    def approve(self, server_id: str, *, manifest_hash: str, signed: bool) -> MCPServerCard:
        c = self._servers[server_id]
        updated = c.model_copy(update={
            "state": ServerState.approved,
            "manifest_hash": manifest_hash,
            "manifest_signed": signed,
            "last_reviewed_at": datetime.now(UTC).isoformat(),
        })
        self._servers[server_id] = updated
        return updated

    def block(self, server_id: str, reason: str = "") -> MCPServerCard:
        c = self._servers[server_id]
        updated = c.model_copy(update={"state": ServerState.blocked, "notes": reason})
        self._servers[server_id] = updated
        return updated

    def get(self, server_id: str) -> MCPServerCard:
        return self._servers[server_id]

    def is_approved(self, server_id: str) -> bool:
        return server_id in self._servers and self._servers[server_id].state == ServerState.approved

    def list(self) -> list[MCPServerCard]:
        return list(self._servers.values())
