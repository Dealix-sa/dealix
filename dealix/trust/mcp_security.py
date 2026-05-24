"""خادم الثقة — MCP server security registry (spec §34).

Five canonical MCP risks: tool_poisoning, shadowing, rug_pull,
exfiltration, excessive_scope. Each registered MCP server carries
metadata + vetting evidence; runtime enforcement returns Allow / Deny /
Escalate per tool call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any
from urllib.parse import urlparse

from dealix.hermes.core.schemas import utcnow
from dealix.trust.tool_registry import MCPRiskHints


class AllowlistStatus(StrEnum):
    UNREVIEWED = "unreviewed"
    PROVISIONAL = "provisional"
    APPROVED = "approved"
    BLOCKED = "blocked"


class EnforcementDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


@dataclass
class Risk:
    """A risk hint with severity (0..1) for surfacing in dashboards."""

    risk: MCPRiskHints
    severity: float = 0.5
    detail: str | None = None


@dataclass
class MCPServerEntry:
    server_id: str
    url: str
    vendor: str
    capabilities: list[str] = field(default_factory=list)
    semantic_vetting_passed: bool = False
    allowlist_status: AllowlistStatus = AllowlistStatus.UNREVIEWED
    last_review_at: datetime = field(default_factory=utcnow)
    review_evidence_ref: str | None = None
    block_reason: str | None = None
    risks: list[Risk] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Heuristic precheck
# ─────────────────────────────────────────────────────────────


_KNOWN_VENDORS: frozenset[str] = frozenset(
    {"anthropic", "openai", "dealix", "google", "microsoft", "stripe", "hyperpay"}
)
_REVIEW_STALE_AFTER = timedelta(days=180)


def precheck(server_url: str, vendor: str | None = None) -> list[Risk]:
    """Heuristic risk surface based on URL + vendor only."""
    risks: list[Risk] = []
    parsed = urlparse(server_url)
    if not parsed.scheme:
        risks.append(Risk(MCPRiskHints.EXFILTRATION, 0.5, "no scheme in URL"))
    if parsed.scheme == "http":
        risks.append(
            Risk(MCPRiskHints.EXFILTRATION, 0.7, "plaintext http transport"),
        )
    if not parsed.netloc:
        risks.append(Risk(MCPRiskHints.SHADOWING, 0.6, "missing host"))
    if parsed.netloc and parsed.netloc.replace(".", "").isdigit():
        risks.append(Risk(MCPRiskHints.SHADOWING, 0.6, "raw IP host"))
    if vendor is None or vendor.lower() not in _KNOWN_VENDORS:
        risks.append(
            Risk(MCPRiskHints.RUG_PULL, 0.5, f"unknown vendor: {vendor or 'unspecified'}")
        )
    if "*" in (server_url or ""):
        risks.append(Risk(MCPRiskHints.EXCESSIVE_SCOPE, 0.7, "wildcard in URL"))
    return risks


# ─────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────


class MCPSecurityRegistry:
    """Registry + runtime enforcement gate for MCP servers."""

    def __init__(self) -> None:
        self._servers: dict[str, MCPServerEntry] = {}

    def register_server(
        self,
        server_id: str,
        url: str,
        vendor: str,
        capabilities: list[str] | None = None,
    ) -> MCPServerEntry:
        if server_id in self._servers:
            raise ValueError(f"duplicate MCP server_id: {server_id}")
        entry = MCPServerEntry(
            server_id=server_id,
            url=url,
            vendor=vendor,
            capabilities=list(capabilities or []),
            risks=precheck(url, vendor),
        )
        self._servers[server_id] = entry
        return entry

    def get(self, server_id: str) -> MCPServerEntry:
        try:
            return self._servers[server_id]
        except KeyError as exc:
            raise KeyError(f"unknown MCP server: {server_id}") from exc

    def all(self) -> list[MCPServerEntry]:
        return list(self._servers.values())

    def vet_server(self, server_id: str, evidence: dict[str, Any]) -> bool:
        """Mark a server as vetted iff the evidence checklist passes."""
        entry = self.get(server_id)
        required_keys = {"reviewer", "checklist_passed", "evidence_ref"}
        missing = required_keys - set(evidence.keys())
        if missing:
            raise ValueError(f"vetting evidence missing keys: {sorted(missing)}")
        if not evidence.get("checklist_passed"):
            entry.semantic_vetting_passed = False
            entry.allowlist_status = AllowlistStatus.BLOCKED
            entry.block_reason = "checklist did not pass"
            return False
        entry.semantic_vetting_passed = True
        entry.allowlist_status = AllowlistStatus.APPROVED
        entry.last_review_at = utcnow()
        entry.review_evidence_ref = evidence["evidence_ref"]
        entry.block_reason = None
        return True

    def block(self, server_id: str, reason: str) -> MCPServerEntry:
        entry = self.get(server_id)
        entry.allowlist_status = AllowlistStatus.BLOCKED
        entry.block_reason = reason
        return entry

    def enforce_runtime(
        self,
        server_id: str,
        tool_call: dict[str, Any],
    ) -> EnforcementDecision:
        entry = self.get(server_id)
        if entry.allowlist_status == AllowlistStatus.BLOCKED:
            return EnforcementDecision.DENY
        if entry.allowlist_status == AllowlistStatus.UNREVIEWED:
            return EnforcementDecision.DENY
        if entry.allowlist_status == AllowlistStatus.PROVISIONAL:
            return EnforcementDecision.ESCALATE
        # Approved — but check freshness + scope drift
        if utcnow() - entry.last_review_at > _REVIEW_STALE_AFTER:
            return EnforcementDecision.ESCALATE
        capabilities = set(entry.capabilities)
        called_tool = str(tool_call.get("tool", "")).strip()
        if capabilities and called_tool and called_tool not in capabilities:
            return EnforcementDecision.ESCALATE
        # Any critical residual risk → escalate.
        if any(r.severity >= 0.7 for r in entry.risks):
            return EnforcementDecision.ESCALATE
        return EnforcementDecision.ALLOW


__all__ = [
    "AllowlistStatus",
    "EnforcementDecision",
    "MCPRiskHints",
    "MCPSecurityRegistry",
    "MCPServerEntry",
    "Risk",
    "precheck",
]
