"""Hermes agent registry seeds (Section 57).

Eight founder-owned agents that compose the Hermes commercial loop.
"""

from __future__ import annotations

from typing import Any

AGENTS: list[dict[str, Any]] = [
    {
        "id": "signal_classifier_agent",
        "role": "SignalClassifierAgent",
        "owner": "founder",
        "purpose": (
            "Classify inbound signals from intake, market data, and "
            "control events into typed opportunity candidates."
        ),
        "allowed_tools": [
            "market_signal_pull",
            "lead_lookup",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "opportunity_mapper_agent",
        "role": "OpportunityMapperAgent",
        "owner": "founder",
        "purpose": (
            "Map classified signals to ICPs, offers, and a scored "
            "opportunity record."
        ),
        "allowed_tools": [
            "lead_lookup",
            "partner_lookup",
            "pricing_lookup",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "revenue_hunter_agent",
        "role": "RevenueHunterAgent",
        "owner": "founder",
        "purpose": (
            "Draft outbound sequences and call plans for qualified "
            "opportunities — drafts only, never auto-send."
        ),
        "allowed_tools": [
            "email_draft_only",
            "whatsapp_draft_only",
            "calendar_read",
            "crm_write_draft",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "proposal_factory_agent",
        "role": "ProposalFactoryAgent",
        "owner": "founder",
        "purpose": (
            "Assemble proposal drafts from offer registry, ICP context, "
            "and outcome ledger inputs."
        ),
        "allowed_tools": [
            "pricing_lookup",
            "evidence_pack_read",
            "crm_write_draft",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "trust_checker_agent",
        "role": "TrustCheckerAgent",
        "owner": "founder",
        "purpose": (
            "Evaluate proposed external actions against the control "
            "library and surface required approvals."
        ),
        "allowed_tools": [
            "evidence_pack_read",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "outcome_logger_agent",
        "role": "OutcomeLoggerAgent",
        "owner": "founder",
        "purpose": (
            "Record execution outcomes (estimated, observed, verified, "
            "client_confirmed) into the value ledger."
        ),
        "allowed_tools": [
            "invoice_lookup_readonly",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "asset_builder_agent",
        "role": "AssetBuilderAgent",
        "owner": "founder",
        "purpose": (
            "Compose reusable assets (case studies, proof packs, "
            "playbooks) from verified executions and outcomes."
        ),
        "allowed_tools": [
            "evidence_pack_read",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
    {
        "id": "growth_attribution_agent",
        "role": "GrowthAttributionAgent",
        "owner": "founder",
        "purpose": (
            "Attribute revenue events back to leads, campaigns, and "
            "touches using the configured attribution model."
        ),
        "allowed_tools": [
            "invoice_lookup_readonly",
            "lead_lookup",
        ],
        "required_output_fields": ["text"],
        "locale": "ar",
    },
]


__all__ = ["AGENTS"]
