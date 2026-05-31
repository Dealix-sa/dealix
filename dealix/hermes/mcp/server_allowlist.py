"""
MCP server allowlist — only servers explicitly approved by S4 Sovereign
Approval can be enabled.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class AllowedServer:
    server_id: str
    canonical_url: str
    manifest_sha256: str
    approved_by: str
    approved_at: float
    notes: str = ""
    enabled: bool = True


@dataclass
class ServerAllowlist:
    _servers: dict[str, AllowedServer] = field(default_factory=dict)

    def approve(
        self,
        server_id: str,
        canonical_url: str,
        manifest_sha256: str,
        approved_by: str,
        notes: str = "",
    ) -> AllowedServer:
        if not approved_by:
            raise ValueError("S4 sovereign approval required (approved_by)")
        if not manifest_sha256 or len(manifest_sha256) < 32:
            raise ValueError("manifest_sha256 looks invalid")
        entry = AllowedServer(
            server_id=server_id,
            canonical_url=canonical_url,
            manifest_sha256=manifest_sha256,
            approved_by=approved_by,
            approved_at=time.time(),
            notes=notes,
        )
        self._servers[server_id] = entry
        return entry

    def is_allowed(self, server_id: str, manifest_sha256: str) -> bool:
        entry = self._servers.get(server_id)
        if entry is None or not entry.enabled:
            return False
        return entry.manifest_sha256 == manifest_sha256

    def disable(self, server_id: str, reason: str, disabled_by: str) -> None:
        if not reason or not disabled_by:
            raise ValueError("disable requires reason and disabled_by")
        entry = self._servers.get(server_id)
        if entry is None:
            raise KeyError(f"unknown server '{server_id}'")
        entry.enabled = False
        entry.notes = f"{entry.notes} | DISABLED by {disabled_by}: {reason}".strip(" |")

    def get(self, server_id: str) -> AllowedServer | None:
        return self._servers.get(server_id)

    def __len__(self) -> int:
        return len(self._servers)
