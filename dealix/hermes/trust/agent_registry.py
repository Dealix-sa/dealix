"""Agent Registry — every agent in Dealix has an Agent Card.

An agent without an Agent Card cannot execute through the sovereignty gate.
The card declares mission, owner, allowed/forbidden tools, the maximum
sovereignty level the agent may *propose*, and the KPIs it is judged on.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel, Field, field_validator

from dealix.hermes.sovereignty import SovereigntyLevel


class AgentCard(BaseModel):
    agent_id: str = Field(min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    name: str
    family: str  # sovereign | money | trust | product | network | venture | ...
    mission: str = Field(min_length=10)
    owner: str = "sami"
    allowed_tools: list[str] = Field(default_factory=list)
    forbidden_tools: list[str] = Field(default_factory=list)
    max_sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    kpis: list[str] = Field(min_length=1)
    enabled: bool = True
    registered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("forbidden_tools")
    @classmethod
    def _no_overlap(cls, v: list[str], info) -> list[str]:  # type: ignore[no-untyped-def]
        allowed: list[str] = info.data.get("allowed_tools") or []
        overlap = set(v) & set(allowed)
        if overlap:
            raise ValueError(f"tools cannot be both allowed and forbidden: {overlap}")
        return v


class AgentRegistry:
    def __init__(self) -> None:
        self._cards: dict[str, AgentCard] = {}

    def register(self, card: AgentCard) -> AgentCard:
        if card.agent_id in self._cards:
            raise ValueError(f"agent already registered: {card.agent_id}")
        self._cards[card.agent_id] = card
        return card

    def upsert(self, card: AgentCard) -> AgentCard:
        self._cards[card.agent_id] = card
        return card

    def get(self, agent_id: str) -> AgentCard | None:
        return self._cards.get(agent_id)

    def require(self, agent_id: str) -> AgentCard:
        c = self._cards.get(agent_id)
        if c is None:
            raise KeyError(f"unregistered agent: {agent_id}")
        if not c.enabled:
            raise PermissionError(f"agent disabled: {agent_id}")
        return c

    def disable(self, agent_id: str) -> AgentCard:
        c = self.require(agent_id)
        c = c.model_copy(update={"enabled": False})
        self._cards[agent_id] = c
        return c

    def all(self) -> list[AgentCard]:
        return list(self._cards.values())

    def by_family(self, family: str) -> list[AgentCard]:
        return [c for c in self._cards.values() if c.family == family]


# ─── Default Agent Workforce ────────────────────────────────────────────

DEFAULT_AGENT_CARDS: tuple[AgentCard, ...] = (
    # Sovereign — Sami-only
    AgentCard(
        agent_id="sami_chief_of_staff",
        name="Sami Chief-of-Staff",
        family="sovereign",
        mission="Surface today's most valuable move; one decision, one action.",
        allowed_tools=["read_console", "draft_memo"],
        forbidden_tools=["send_external_message", "execute_payment"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["console_open_rate", "decision_latency_minutes"],
    ),
    AgentCard(
        agent_id="sami_money_command",
        name="Sami Money Command",
        family="sovereign",
        mission="Rank cash actions by realisable value and surface the next move.",
        allowed_tools=["read_money_dashboard", "rank_money_actions"],
        forbidden_tools=["execute_payment", "issue_refund"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["cash_collected_sar", "pipeline_to_paid_ratio"],
    ),
    # Money
    AgentCard(
        agent_id="cash_scout",
        name="Cash Scout",
        family="money",
        mission="Find the fastest path to cash this week.",
        allowed_tools=["read_opportunity", "rank_money_actions"],
        forbidden_tools=["send_external_message"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["cash_actions_proposed", "cash_actions_won"],
    ),
    AgentCard(
        agent_id="revenue_hunter",
        name="Revenue Hunter",
        family="money",
        mission="Match opportunities to offers and queue the deal-room work.",
        allowed_tools=["read_opportunity", "match_offer", "draft_proposal"],
        forbidden_tools=["send_external_message", "sign_contract"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["deals_matched", "proposal_to_close_rate"],
    ),
    AgentCard(
        agent_id="proposal_agent",
        name="Proposal Agent",
        family="money",
        mission="Generate commercial proposals from approved opportunities.",
        allowed_tools=["read_opportunity", "draft_proposal"],
        forbidden_tools=["send_external_message", "sign_contract", "export_data"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["proposals_drafted", "proposal_to_close_rate"],
    ),
    AgentCard(
        agent_id="followup_agent",
        name="Follow-up Agent",
        family="money",
        mission="Draft follow-ups; never send them.",
        allowed_tools=["read_opportunity", "draft_message"],
        forbidden_tools=["send_external_message"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["followups_drafted", "reply_rate"],
    ),
    # Trust
    AgentCard(
        agent_id="policy_agent",
        name="Policy Agent",
        family="trust",
        mission="Draft AI use policies and permission matrices.",
        allowed_tools=["draft_policy", "read_agent_registry", "read_tool_registry"],
        forbidden_tools=["send_external_message", "export_data"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["policies_drafted", "policies_adopted"],
    ),
    AgentCard(
        agent_id="approval_agent",
        name="Approval Agent",
        family="trust",
        mission="Route approval requests to humans; never decide unilaterally.",
        allowed_tools=["read_approval_queue", "notify_approver"],
        forbidden_tools=["grant_approval", "execute_action"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["approval_median_latency_minutes", "approvals_expired"],
    ),
    AgentCard(
        agent_id="evidence_agent",
        name="Evidence Agent",
        family="trust",
        mission="Assemble evidence packs from outcomes.",
        allowed_tools=["read_outcome", "build_evidence_pack"],
        forbidden_tools=["send_external_message"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["evidence_packs_built", "evidence_completeness"],
    ),
    AgentCard(
        agent_id="audit_agent",
        name="Audit Agent",
        family="trust",
        mission="Append-only audit log; never modifies past entries.",
        allowed_tools=["append_audit"],
        forbidden_tools=["delete_audit", "modify_audit"],
        max_sovereignty_level=SovereigntyLevel.S0_AUTONOMOUS,
        kpis=["audit_coverage_percent"],
    ),
    AgentCard(
        agent_id="mcp_risk_agent",
        name="MCP Risk Agent",
        family="trust",
        mission="Screen MCP tool metadata for poisoning before registration.",
        allowed_tools=["read_tool_metadata", "score_mcp_risk"],
        forbidden_tools=["register_tool", "send_external_message"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["tools_screened", "tools_blocked"],
    ),
    AgentCard(
        agent_id="no_overclaim_agent",
        name="No-Overclaim Guardrail",
        family="trust",
        mission="Block messages that claim unproven results.",
        allowed_tools=["read_message_draft", "flag_message"],
        forbidden_tools=["send_external_message", "rewrite_message"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["overclaims_blocked"],
    ),
    # Product
    AgentCard(
        agent_id="offer_builder",
        name="Offer Builder",
        family="product",
        mission="Convert validated pains into offer cards.",
        allowed_tools=["read_opportunity", "draft_offer"],
        forbidden_tools=["publish_offer", "send_external_message"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["offers_drafted", "offers_to_pilot"],
    ),
    AgentCard(
        agent_id="scale_kill_agent",
        name="Scale/Kill Agent",
        family="product",
        mission="Compute scale/kill verdicts on offers and verticals.",
        allowed_tools=["read_outcomes", "compute_scale_verdict"],
        forbidden_tools=["kill_offer", "scale_offer"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["verdicts_proposed", "verdicts_acted_on"],
    ),
    # Network
    AgentCard(
        agent_id="partner_scout",
        name="Partner Scout",
        family="network",
        mission="Find prospective partners; never sign agreements.",
        allowed_tools=["read_partner_pipeline", "score_partner_fit"],
        forbidden_tools=["sign_partnership_agreement", "claim_partnership"],
        max_sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        kpis=["partners_proposed", "partners_signed"],
    ),
    # Intelligence
    AgentCard(
        agent_id="market_radar",
        name="Market Radar",
        family="intelligence",
        mission="Convert market signals into ranked opportunities.",
        allowed_tools=["read_market_feeds", "register_signal", "score_opportunity"],
        forbidden_tools=["send_external_message", "publish_report"],
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        kpis=["signals_ingested", "signals_to_opportunity_rate"],
    ),
)


def install_defaults(registry: AgentRegistry) -> AgentRegistry:
    for card in DEFAULT_AGENT_CARDS:
        registry.upsert(card)
    return registry


__all__ = [
    "AgentCard",
    "AgentRegistry",
    "DEFAULT_AGENT_CARDS",
    "install_defaults",
]
