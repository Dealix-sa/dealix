#!/usr/bin/env python3
"""Generate specs for the seven free Dealix diagnostic tools."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    assert_single_cta,
    ensure_dirs,
    write_json,
)

_OUT = DATA_DIR / "free_tools.json"

# Each tool: a single CTA, a top-3-result -> recommended Dealix OS mapping.
_TOOLS: list[dict[str, Any]] = [
    {
        "id": "business_os_score",
        "name_ar": "مؤشر نظام تشغيل الأعمال",
        "name_en": "Business OS Score",
        "core_question": "How operationally ready is your business to run on an AI operating system?",
        "inputs": [
            "team_size",
            "has_documented_processes",
            "crm_in_use",
            "decision_logging",
            "proof_register_exists",
        ],
        "scoring_model": "weighted_sum_0_100",
        "sample_output": {
            "score": 58,
            "band": "Developing",
            "top_gaps": ["decision_logging", "proof_register_exists"],
        },
        "recommended_os_by_result": {
            "high": ["governance_os", "value_os"],
            "medium": ["proof_os", "adoption_os"],
            "low": ["data_os", "governance_os"],
        },
        "cta": "Command Sprint",
    },
    {
        "id": "revenue_leakage_calculator",
        "name_ar": "حاسبة تسرب الإيراد",
        "name_en": "Revenue Leakage Calculator",
        "core_question": "Where is revenue leaking between lead and confirmed payment?",
        "inputs": [
            "monthly_leads",
            "reply_rate",
            "qualified_rate",
            "proposal_rate",
            "close_rate",
        ],
        "scoring_model": "funnel_dropoff_estimate",
        "sample_output": {
            "estimated_monthly_leak_band": "operational_estimate",
            "biggest_dropoff_stage": "qualified_to_proposal",
        },
        "recommended_os_by_result": {
            "high": ["value_os", "sales_os"],
            "medium": ["proof_os", "value_os"],
            "low": ["data_os", "sales_os"],
        },
        "cta": "Free Diagnostic",
    },
    {
        "id": "proof_gap_audit",
        "name_ar": "تدقيق فجوة الإثبات",
        "name_en": "Proof Gap Audit",
        "core_question": "Can you prove the value you delivered to each client?",
        "inputs": [
            "delivers_reports",
            "evidence_per_engagement",
            "client_confirmed_outcomes",
            "proof_pack_exists",
        ],
        "scoring_model": "coverage_ratio_0_100",
        "sample_output": {
            "coverage": 40,
            "band": "Thin",
            "missing_sections": ["client_confirmed_outcomes"],
        },
        "recommended_os_by_result": {
            "high": ["proof_os", "value_os"],
            "medium": ["proof_os", "adoption_os"],
            "low": ["proof_os", "data_os"],
        },
        "cta": "Command Sprint",
    },
    {
        "id": "whatsapp_follow_up_risk_score",
        "name_ar": "مؤشر مخاطر متابعة واتساب",
        "name_en": "WhatsApp Follow-up Risk Score",
        "core_question": "Is your WhatsApp follow-up compliant, owned, and evidenced?",
        "inputs": [
            "uses_optin_lists",
            "owner_assigned",
            "approval_before_send",
            "logs_evidence",
        ],
        "scoring_model": "compliance_checklist_0_100",
        "sample_output": {
            "risk_band": "Elevated",
            "flags": ["approval_before_send"],
        },
        "recommended_os_by_result": {
            "high": ["governance_os", "value_os"],
            "medium": ["governance_os", "proof_os"],
            "low": ["governance_os", "data_os"],
        },
        "cta": "Free Diagnostic",
    },
    {
        "id": "ai_governance_checklist",
        "name_ar": "قائمة حوكمة الذكاء الاصطناعي",
        "name_en": "AI Governance Checklist",
        "core_question": "Is every external AI touch approved, sourced, and PDPL-aware?",
        "inputs": [
            "source_passport_required",
            "approval_first_external",
            "pii_handling_documented",
            "no_unsafe_claims_policy",
        ],
        "scoring_model": "checklist_pass_ratio_0_100",
        "sample_output": {
            "pass_ratio": 75,
            "open_items": ["pii_handling_documented"],
        },
        "recommended_os_by_result": {
            "high": ["governance_os", "data_os"],
            "medium": ["governance_os", "proof_os"],
            "low": ["governance_os", "data_os"],
        },
        "cta": "Command Sprint",
    },
    {
        "id": "delivery_visibility_score",
        "name_ar": "مؤشر وضوح التسليم",
        "name_en": "Delivery Visibility Score",
        "core_question": "Can a client see where their engagement stands at any moment?",
        "inputs": [
            "status_badges_in_use",
            "next_action_visible",
            "owner_per_action",
            "weekly_cadence",
        ],
        "scoring_model": "weighted_sum_0_100",
        "sample_output": {
            "score": 62,
            "band": "Partial",
            "top_gaps": ["next_action_visible"],
        },
        "recommended_os_by_result": {
            "high": ["adoption_os", "value_os"],
            "medium": ["adoption_os", "proof_os"],
            "low": ["data_os", "adoption_os"],
        },
        "cta": "Free Diagnostic",
    },
    {
        "id": "client_memory_score",
        "name_ar": "مؤشر ذاكرة العميل",
        "name_en": "Client Memory Score",
        "core_question": "How much context survives between client interactions?",
        "inputs": [
            "context_captured",
            "shared_record",
            "retrieval_speed",
            "handoff_safe",
        ],
        "scoring_model": "weighted_sum_0_100",
        "sample_output": {
            "score": 51,
            "band": "Fragmented",
            "top_gaps": ["shared_record", "handoff_safe"],
        },
        "recommended_os_by_result": {
            "high": ["capital_os", "value_os"],
            "medium": ["data_os", "adoption_os"],
            "low": ["data_os", "capital_os"],
        },
        "cta": "Business OS Score",
    },
]


def build_tools() -> list[dict[str, Any]]:
    """Return validated free-tool spec records sorted by id."""
    for tool in _TOOLS:
        assert_single_cta(tool["cta"])
    return sorted(_TOOLS, key=lambda t: t["id"])


def main() -> int:
    """Write the free tool specs and print a summary line."""
    ensure_dirs()
    tools = build_tools()
    size = write_json(_OUT, tools)
    print(f"free_tools: wrote {len(tools)} tools to {_OUT} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
