"""Tool Registry — every tool an agent can invoke is declared here.

A tool not in the registry cannot be called. Each tool carries a risk score,
a sovereignty floor (minimum level the gate enforces regardless of caller),
a network/data scope, and an explicit reversibility flag.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from dealix.hermes.sovereignty import SovereigntyLevel


class ToolScope(StrEnum):
    INTERNAL = "internal"  # touches only Dealix state
    READ_EXTERNAL = "read_external"  # fetches public/permissioned data
    WRITE_EXTERNAL = "write_external"  # publishes / sends
    FINANCIAL = "financial"  # touches money
    DATA_EXPORT = "data_export"  # exfiltrates customer data


class ToolCard(BaseModel):
    tool_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    description: str
    scope: ToolScope
    sovereignty_floor: SovereigntyLevel
    risk_score: float = Field(ge=0.0, le=1.0)
    reversible: bool
    mcp_origin: bool = False
    mcp_metadata_hash: str | None = None
    registered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolCard] = {}

    def register(self, tool: ToolCard) -> ToolCard:
        if tool.tool_id in self._tools:
            raise ValueError(f"tool already registered: {tool.tool_id}")
        self._tools[tool.tool_id] = tool
        return tool

    def upsert(self, tool: ToolCard) -> ToolCard:
        self._tools[tool.tool_id] = tool
        return tool

    def get(self, tool_id: str) -> ToolCard | None:
        return self._tools.get(tool_id)

    def require(self, tool_id: str) -> ToolCard:
        t = self._tools.get(tool_id)
        if t is None:
            raise KeyError(f"unregistered tool: {tool_id}")
        return t

    def all(self) -> list[ToolCard]:
        return list(self._tools.values())

    def by_scope(self, scope: ToolScope) -> list[ToolCard]:
        return [t for t in self._tools.values() if t.scope is scope]


DEFAULT_TOOL_CARDS: tuple[ToolCard, ...] = (
    ToolCard(
        tool_id="read_console",
        description="Read the Sovereign Console snapshot.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.0,
        reversible=True,
    ),
    ToolCard(
        tool_id="read_opportunity",
        description="Read an opportunity from the graph.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.0,
        reversible=True,
    ),
    ToolCard(
        tool_id="read_outcome",
        description="Read an outcome.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.0,
        reversible=True,
    ),
    ToolCard(
        tool_id="rank_money_actions",
        description="Compute the ordered list of fastest cash actions.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.1,
        reversible=True,
    ),
    ToolCard(
        tool_id="draft_proposal",
        description="Render a commercial proposal from an opportunity.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S1_INTERNAL,
        risk_score=0.2,
        reversible=True,
    ),
    ToolCard(
        tool_id="draft_message",
        description="Draft an external message; never sends.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S1_INTERNAL,
        risk_score=0.2,
        reversible=True,
    ),
    ToolCard(
        tool_id="send_external_message",
        description="Send a message outside Dealix (email/whatsapp/linkedin).",
        scope=ToolScope.WRITE_EXTERNAL,
        sovereignty_floor=SovereigntyLevel.S3_SOVEREIGN_MEMO,
        risk_score=0.85,
        reversible=False,
    ),
    ToolCard(
        tool_id="sign_contract",
        description="Sign a commercial agreement.",
        scope=ToolScope.WRITE_EXTERNAL,
        sovereignty_floor=SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        risk_score=0.95,
        reversible=False,
    ),
    ToolCard(
        tool_id="execute_payment",
        description="Move money.",
        scope=ToolScope.FINANCIAL,
        sovereignty_floor=SovereigntyLevel.S3_SOVEREIGN_MEMO,
        risk_score=0.95,
        reversible=False,
    ),
    ToolCard(
        tool_id="export_data",
        description="Export customer data outside Dealix.",
        scope=ToolScope.DATA_EXPORT,
        sovereignty_floor=SovereigntyLevel.S3_SOVEREIGN_MEMO,
        risk_score=0.9,
        reversible=False,
    ),
    ToolCard(
        tool_id="publish_public_api",
        description="Expose a public API surface.",
        scope=ToolScope.WRITE_EXTERNAL,
        sovereignty_floor=SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        risk_score=0.9,
        reversible=False,
    ),
    ToolCard(
        tool_id="publish_marketplace_listing",
        description="List a marketplace asset.",
        scope=ToolScope.WRITE_EXTERNAL,
        sovereignty_floor=SovereigntyLevel.S4_SOVEREIGN_RESERVED,
        risk_score=0.85,
        reversible=False,
    ),
    ToolCard(
        tool_id="register_signal",
        description="Add a signal to the intake.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.1,
        reversible=True,
    ),
    ToolCard(
        tool_id="build_evidence_pack",
        description="Assemble an evidence pack from outcomes.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S1_INTERNAL,
        risk_score=0.1,
        reversible=True,
    ),
    ToolCard(
        tool_id="append_audit",
        description="Append a record to the immutable audit log.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.0,
        reversible=False,
    ),
    ToolCard(
        tool_id="read_market_feeds",
        description="Read public market signals (news, open data).",
        scope=ToolScope.READ_EXTERNAL,
        sovereignty_floor=SovereigntyLevel.S0_AUTONOMOUS,
        risk_score=0.2,
        reversible=True,
    ),
    ToolCard(
        tool_id="score_partner_fit",
        description="Score a prospective partner.",
        scope=ToolScope.INTERNAL,
        sovereignty_floor=SovereigntyLevel.S1_INTERNAL,
        risk_score=0.1,
        reversible=True,
    ),
)


def install_defaults(registry: ToolRegistry) -> ToolRegistry:
    for tool in DEFAULT_TOOL_CARDS:
        registry.upsert(tool)
    return registry


__all__ = [
    "ToolCard",
    "ToolRegistry",
    "ToolScope",
    "DEFAULT_TOOL_CARDS",
    "install_defaults",
]
