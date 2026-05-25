"""Default tool cards Hermes installs at boot."""

from __future__ import annotations

from dealix.hermes.trust.tool_registry import ToolCard, ToolRegistry, ToolRisk


DEFAULT_TOOL_CARDS: list[ToolCard] = [
    # ── Read-only utility ──────────────────────────────────────
    ToolCard(
        tool_id="read_signals",
        description="Read inbound signals.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
        data_scope="internal_only",
        audit_required=True,
    ),
    ToolCard(
        tool_id="read_opportunities",
        description="Read opportunities.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="read_decisions",
        description="Read decisions.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="read_outcomes",
        description="Read outcomes.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="read_offers",
        description="Read the offer library.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="read_revenue",
        description="Read revenue events.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),

    # ── Drafting tools (internal write) ────────────────────────
    ToolCard(
        tool_id="draft_proposal",
        description="Draft a commercial proposal.",
        risk_level=ToolRisk.medium,
        enabled=True,
        requires_approval=False,
        data_scope="customer_workspace",
        audit_required=True,
    ),
    ToolCard(
        tool_id="draft_followup",
        description="Draft a follow-up message.",
        risk_level=ToolRisk.low,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="draft_pitch",
        description="Draft a partner pitch.",
        risk_level=ToolRisk.medium,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="draft_case_study",
        description="Draft a customer case study.",
        risk_level=ToolRisk.medium,
        enabled=True,
        requires_approval=False,
    ),
    ToolCard(
        tool_id="draft_landing",
        description="Draft a landing page (never publish).",
        risk_level=ToolRisk.medium,
        enabled=True,
        requires_approval=False,
    ),

    # ── External / dangerous tools (default DISABLED) ──────────
    ToolCard(
        tool_id="send_external",
        description="Send any externally-visible message.",
        risk_level=ToolRisk.high,
        enabled=False,
        requires_approval=True,
        data_scope="explicit_recipient_only",
        audit_required=True,
        pdpl_relevant=True,
    ),
    ToolCard(
        tool_id="publish_landing",
        description="Publish a landing page live.",
        risk_level=ToolRisk.high,
        enabled=False,
        requires_approval=True,
    ),
    ToolCard(
        tool_id="publish_pricing",
        description="Change publicly visible pricing.",
        risk_level=ToolRisk.critical,
        enabled=False,
        requires_approval=True,
    ),
    ToolCard(
        tool_id="sign_contract",
        description="Sign a contract on behalf of Dealix.",
        risk_level=ToolRisk.critical,
        enabled=False,
        requires_approval=True,
    ),
    ToolCard(
        tool_id="transfer_money",
        description="Move money out of any Dealix account.",
        risk_level=ToolRisk.critical,
        enabled=False,
        requires_approval=True,
    ),
    ToolCard(
        tool_id="export_data",
        description="Export raw customer data outside Dealix.",
        risk_level=ToolRisk.critical,
        enabled=False,
        requires_approval=True,
        pdpl_relevant=True,
    ),
]


def seed_tools(registry: ToolRegistry) -> list[str]:
    """Register the default tool catalogue."""
    return [registry.register(card).tool_id for card in DEFAULT_TOOL_CARDS]
