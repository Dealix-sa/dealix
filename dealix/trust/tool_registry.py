"""خادم الثقة — tool registry.

Every tool (email_send, whatsapp_send, payment_charge, …) is registered
with vendor, risk level, allowlist status, MCP server reference and last
review evidence. `assert_callable` is the gate the orchestrator uses
before any tool runs.

Seeded with the canonical set: email_send, whatsapp_send, proposal_render,
landing_page_publish, crm_sync, payment_charge (blocked by default),
data_export.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from dealix.hermes.core.schemas import RiskLevel, utcnow


class MCPRiskHints(StrEnum):
    """Spec §34 — the five MCP-specific risk categories."""

    TOOL_POISONING = "tool_poisoning"
    SHADOWING = "shadowing"
    RUG_PULL = "rug_pull"
    EXFILTRATION = "exfiltration"
    EXCESSIVE_SCOPE = "excessive_scope"


@dataclass
class ToolEntry:
    tool_id: str
    name: str
    vendor: str
    risk_level: RiskLevel = RiskLevel.LOW
    requires_approval: bool = False
    data_scopes: set[str] = field(default_factory=set)
    mcp_server: str | None = None
    allowlisted: bool = True
    last_reviewed_at: datetime = field(default_factory=utcnow)
    review_evidence_ref: str | None = None
    block_reason: str | None = None
    mcp_risks: set[MCPRiskHints] = field(default_factory=set)


class ToolRegistry:
    """In-memory tool registry with assert_callable gating."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolEntry] = {}

    # ── CRUD ─────────────────────────────────────────────────
    def register(self, entry: ToolEntry) -> ToolEntry:
        if entry.tool_id in self._tools:
            raise ValueError(f"tool already registered: {entry.tool_id}")
        self._tools[entry.tool_id] = entry
        return entry

    def get(self, tool_id: str) -> ToolEntry:
        try:
            return self._tools[tool_id]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {tool_id}") from exc

    def all(self) -> list[ToolEntry]:
        return list(self._tools.values())

    # ── allow / block ────────────────────────────────────────
    def allowlist(self, tool_id: str, evidence_ref: str | None = None) -> ToolEntry:
        entry = self.get(tool_id)
        entry.allowlisted = True
        entry.block_reason = None
        entry.last_reviewed_at = utcnow()
        if evidence_ref:
            entry.review_evidence_ref = evidence_ref
        return entry

    def block(self, tool_id: str, reason: str) -> ToolEntry:
        entry = self.get(tool_id)
        entry.allowlisted = False
        entry.block_reason = reason
        return entry

    def mark_risk(self, tool_id: str, risk: MCPRiskHints) -> ToolEntry:
        entry = self.get(tool_id)
        entry.mcp_risks.add(risk)
        return entry

    # ── enforcement ─────────────────────────────────────────
    def assert_callable(
        self,
        tool_id: str,
        agent_id: str,
        data_scope: str | None = None,
    ) -> ToolEntry:
        entry = self.get(tool_id)
        if not entry.allowlisted:
            raise PermissionError(
                f"tool {tool_id} is BLOCKED: {entry.block_reason or 'no reason recorded'}"
            )
        if data_scope is not None and entry.data_scopes and data_scope not in entry.data_scopes:
            raise PermissionError(
                f"tool {tool_id} not approved for data_scope {data_scope}"
            )
        # agent_id is recorded but additional agent↔tool checks live in
        # AgentRegistry.assert_can_use_tool; we only validate the tool half.
        _ = agent_id
        return entry


# ─────────────────────────────────────────────────────────────
# Seed
# ─────────────────────────────────────────────────────────────


_DEFAULT_TOOLS: list[ToolEntry] = [
    ToolEntry(
        tool_id="email_send",
        name="Email Send",
        vendor="postmark",
        risk_level=RiskLevel.MEDIUM,
        requires_approval=True,
        data_scopes={"customer", "partner"},
    ),
    ToolEntry(
        tool_id="whatsapp_send",
        name="WhatsApp Send",
        vendor="twilio",
        risk_level=RiskLevel.HIGH,
        requires_approval=True,
        data_scopes={"customer"},
    ),
    ToolEntry(
        tool_id="proposal_render",
        name="Proposal Renderer",
        vendor="dealix",
        risk_level=RiskLevel.LOW,
        requires_approval=False,
        data_scopes={"internal", "customer"},
    ),
    ToolEntry(
        tool_id="landing_page_publish",
        name="Landing Page Publisher",
        vendor="dealix",
        risk_level=RiskLevel.MEDIUM,
        requires_approval=True,
        data_scopes={"internal"},
    ),
    ToolEntry(
        tool_id="crm_sync",
        name="CRM Sync",
        vendor="dealix",
        risk_level=RiskLevel.LOW,
        requires_approval=False,
        data_scopes={"internal", "customer", "partner"},
    ),
    ToolEntry(
        tool_id="payment_charge",
        name="Payment Charge",
        vendor="hyperpay",
        risk_level=RiskLevel.CRITICAL,
        requires_approval=True,
        data_scopes={"customer"},
        allowlisted=False,
        block_reason="financial transfer requires explicit allowlisting",
    ),
    ToolEntry(
        tool_id="data_export",
        name="Data Export",
        vendor="dealix",
        risk_level=RiskLevel.HIGH,
        requires_approval=True,
        data_scopes={"internal"},
    ),
]


def seed_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for entry in _DEFAULT_TOOLS:
        # Re-construct to avoid sharing mutable defaults between callers.
        registry.register(
            ToolEntry(
                tool_id=entry.tool_id,
                name=entry.name,
                vendor=entry.vendor,
                risk_level=entry.risk_level,
                requires_approval=entry.requires_approval,
                data_scopes=set(entry.data_scopes),
                allowlisted=entry.allowlisted,
                block_reason=entry.block_reason,
            )
        )
    return registry


__all__ = [
    "MCPRiskHints",
    "ToolEntry",
    "ToolRegistry",
    "seed_default_tool_registry",
]
