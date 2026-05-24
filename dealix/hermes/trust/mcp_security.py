"""MCP Gateway.

Implements the MCP-specific defences from section 115:

* Server allowlist — refuses servers not on the explicit list.
* Manifest pinning — hash mismatch trips the gateway.
* Tool-descriptor scan — checks for prompt-injection-style descriptors.
* Per-call data scope — restricts tool args to a declared scope.
* Lookalike / shadowing detection — refuses two tools whose names differ
  only by Unicode confusables (very basic check).
* Anomaly / abuse heuristic — refuses unusually large/odd payloads.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field

from dealix.hermes.trust.guardrails import Guardrails


@dataclass
class MCPServerCard:
    server_id: str
    name: str
    url: str
    owner: str
    risk_level: str = "medium"
    enabled: bool = True
    manifest_hash: str = ""        # sha256 of the pinned manifest
    allowed_tools: list[str] = field(default_factory=list)
    data_scope: str = ""


class MCPViolation(ValueError):
    """Raised when the MCP gateway refuses a call."""


@dataclass
class MCPGateway:
    _servers: dict[str, MCPServerCard] = field(default_factory=dict)
    _tool_names_seen: dict[str, str] = field(default_factory=dict)
    _guardrails: Guardrails = field(default_factory=Guardrails)
    max_arg_bytes: int = 64 * 1024

    def register_server(self, card: MCPServerCard, *, manifest: dict | None = None) -> MCPServerCard:
        if manifest is not None:
            expected = card.manifest_hash
            actual = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest()
            if expected and expected != actual:
                raise MCPViolation(f"Manifest hash mismatch for server {card.server_id}.")
            card.manifest_hash = actual
        for tool in card.allowed_tools:
            normalized = self._normalize(tool)
            existing = self._tool_names_seen.get(normalized)
            if existing and existing != card.server_id:
                raise MCPViolation(
                    f"Lookalike/shadow tool '{tool}' on server '{card.server_id}'"
                    f" conflicts with server '{existing}'."
                )
            self._tool_names_seen[normalized] = card.server_id
        self._servers[card.server_id] = card
        return card

    def vet_descriptor(self, descriptor: str) -> None:
        # Tool poisoning often hides instructions inside descriptions.
        report = self._guardrails.scan_input(descriptor)
        if not report.ok:
            raise MCPViolation(f"Tool descriptor failed guardrails: {report.violations[0].detail}")

    def call(
        self,
        *,
        server_id: str,
        tool_name: str,
        args: dict,
        data_scope: str = "",
    ) -> dict:
        if server_id not in self._servers:
            raise MCPViolation(f"Server '{server_id}' is not allowlisted.")
        card = self._servers[server_id]
        if not card.enabled:
            raise MCPViolation(f"Server '{server_id}' is disabled.")
        if tool_name not in card.allowed_tools:
            raise MCPViolation(f"Tool '{tool_name}' not allowed on server '{server_id}'.")

        # Per-call scope check.
        scope = data_scope or card.data_scope
        if scope and not self._scope_matches(scope, args):
            raise MCPViolation(f"Args violate data scope '{scope}'.")

        # Crude abuse heuristic.
        payload = json.dumps(args, default=str).encode("utf-8")
        if len(payload) > self.max_arg_bytes:
            raise MCPViolation(
                f"Arg payload {len(payload)}B exceeds max_arg_bytes={self.max_arg_bytes}."
            )
        return {"server": server_id, "tool": tool_name, "ok": True}

    def kill(self, server_id: str) -> None:
        if server_id in self._servers:
            self._servers[server_id].enabled = False

    @staticmethod
    def _normalize(name: str) -> str:
        nfkd = unicodedata.normalize("NFKD", name)
        only_ascii = nfkd.encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[\W_]+", "", only_ascii).lower()

    @staticmethod
    def _scope_matches(scope: str, args: dict) -> bool:
        """Cheap rule language. Scope like 'tenant=dealix' or 'repo=dealix_repo_only'."""
        if "=" not in scope:
            return True
        key, _, value = scope.partition("=")
        return str(args.get(key.strip(), "")).strip() == value.strip()


__all__ = ["MCPGateway", "MCPServerCard", "MCPViolation"]
