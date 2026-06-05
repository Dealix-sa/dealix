#!/usr/bin/env python3
"""Generate the Dealix growth template library (free templates and paid kits)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    ensure_dirs,
    write_json,
)

_OUT = DATA_DIR / "templates.json"

_FREE_TEMPLATES: list[dict[str, Any]] = [
    {
        "name": "Revenue Map Worksheet",
        "purpose": "Map lead-to-payment stages and spot drop-offs.",
        "contents": ["stage_table", "owner_column", "evidence_column"],
        "feeds": "revenue_leakage_calculator",
        "tier": "free",
    },
    {
        "name": "Proof Register Starter",
        "purpose": "Record one piece of evidence per engagement.",
        "contents": ["engagement_row", "evidence_link", "client_confirmation"],
        "feeds": "proof_gap_audit",
        "tier": "free",
    },
    {
        "name": "Executive Command Brief Template",
        "purpose": "One-page weekly decision brief for owners.",
        "contents": ["signal", "decision", "next_action", "owner"],
        "feeds": "business_os_score",
        "tier": "free",
    },
    {
        "name": "Next Action Board",
        "purpose": "Visible single next action per client.",
        "contents": ["client", "next_action", "owner", "due"],
        "feeds": "delivery_visibility_score",
        "tier": "free",
    },
    {
        "name": "WhatsApp Follow-up Checklist",
        "purpose": "Compliant, opt-in, owned follow-up steps.",
        "contents": ["optin_check", "owner", "approval_step", "evidence_log"],
        "feeds": "whatsapp_follow_up_risk_score",
        "tier": "free",
    },
    {
        "name": "AI Governance Checklist Sheet",
        "purpose": "Approval-first, sourced, PDPL-aware AI usage.",
        "contents": ["source_passport", "approval_gate", "pii_rule"],
        "feeds": "ai_governance_checklist",
        "tier": "free",
    },
    {
        "name": "Client Memory Capture Sheet",
        "purpose": "Hold context between client interactions.",
        "contents": ["context_note", "shared_record_link", "handoff_note"],
        "feeds": "client_memory_score",
        "tier": "free",
    },
    {
        "name": "Sector Pain Self-Diagnosis",
        "purpose": "Spot the top operational pain by sector.",
        "contents": ["pain_list", "self_rating", "suggested_tool"],
        "feeds": "consulting",
        "tier": "free",
    },
]

_PAID_KITS: list[dict[str, Any]] = [
    {
        "name": "Command Sprint Delivery Kit",
        "purpose": "Run the 7-day Command Sprint end to end.",
        "contents": [
            "revenue_map",
            "proof_register",
            "executive_command_brief",
            "next_action_board",
        ],
        "feeds": "business_os_score",
        "tier": "paid",
    },
    {
        "name": "Proof Pack Builder Kit",
        "purpose": "Assemble a 14-section ProofPack with score and tier.",
        "contents": ["section_templates", "scoring_guide", "tier_rubric"],
        "feeds": "proof_gap_audit",
        "tier": "paid",
    },
    {
        "name": "Sector Command Pack Kit",
        "purpose": "Sector-specific operating pack and offers.",
        "contents": ["sector_command_pack", "recommended_os", "sprint_offer"],
        "feeds": "consulting",
        "tier": "paid",
    },
    {
        "name": "Governed Outreach Kit",
        "purpose": "Approval-first, opt-in outreach playbook.",
        "contents": ["approval_workflow", "optin_policy", "evidence_log"],
        "feeds": "whatsapp_follow_up_risk_score",
        "tier": "paid",
    },
    {
        "name": "Managed Operations Kit",
        "purpose": "Recurring managed cadence with retainer readiness.",
        "contents": ["adoption_scorecard", "retainer_readiness", "monthly_value_report"],
        "feeds": "delivery_visibility_score",
        "tier": "paid",
    },
]


def build_templates() -> list[dict[str, Any]]:
    """Return free and paid templates sorted by tier then name."""
    combined = _FREE_TEMPLATES + _PAID_KITS
    return sorted(combined, key=lambda t: (t["tier"], t["name"]))


def main() -> int:
    """Write the template library and print a summary line."""
    ensure_dirs()
    templates = build_templates()
    free = sum(1 for t in templates if t["tier"] == "free")
    paid = sum(1 for t in templates if t["tier"] == "paid")
    size = write_json(_OUT, templates)
    print(
        f"templates: wrote {free} free + {paid} paid to {_OUT} ({size} bytes)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
