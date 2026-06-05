#!/usr/bin/env python3
"""Verification specs for Dealix V10 OS layers.

Single source of truth for which docs each V10 OS must contain, plus key
content markers. Consumed by the per-OS verify scripts and the master verifier.
"""

from __future__ import annotations

_MARKER = "## القاعدة غير القابلة للكسر"


def _files(dir_: str, names: list[str]) -> list[str]:
    return [f"docs/{dir_}/{n}" for n in names]


SPECS: dict[str, dict] = {
    "institutional_scale": {
        "label": "INSTITUTIONAL_SCALE_OS",
        "json": "outputs/v10_verification/institutional_scale_verification.json",
        "files": _files(
            "institutional-scale-os",
            [
                "00_INSTITUTIONAL_SCALE_OS.md",
                "01_SCALE_THESIS.md",
                "02_STAGE_BASED_OPERATING_MODEL.md",
                "03_0_TO_10_CLIENTS_PLAYBOOK.md",
                "04_10_TO_50_CLIENTS_PLAYBOOK.md",
                "05_50_PLUS_CLIENTS_OPERATING_MODEL.md",
                "06_FOUNDER_TO_TEAM_TRANSITION.md",
                "07_PROCESS_TO_PLATFORM_TRANSITION.md",
                "08_SCALE_RISK_REGISTER.md",
                "99_INSTITUTIONAL_SCALE_REPORT.md",
            ],
        ),
        "marker_file": "docs/institutional-scale-os/00_INSTITUTIONAL_SCALE_OS.md",
    },
    "board_governance": {
        "label": "BOARD_GOVERNANCE_OS",
        "json": "outputs/v10_verification/board_governance_verification.json",
        "files": [
            *_files(
                "board-governance-os",
                [
                    "00_BOARD_GOVERNANCE_OS.md",
                    "01_BOARD_PACKET_TEMPLATE.md",
                    "02_MONTHLY_BOARD_REVIEW.md",
                    "03_DECISION_MEMO_TEMPLATE.md",
                    "04_RISK_REVIEW_TEMPLATE.md",
                    "05_METRIC_INTEGRITY_POLICY.md",
                    "06_FOUNDER_ACCOUNTABILITY_SYSTEM.md",
                    "99_BOARD_GOVERNANCE_REPORT.md",
                ],
            ),
            "scripts/board_packet_generate.py",
        ],
        "marker_file": "docs/board-governance-os/01_BOARD_PACKET_TEMPLATE.md",
    },
    "market_domination": {
        "label": "MARKET_DOMINATION_OS",
        "json": "outputs/v10_verification/market_domination_verification.json",
        "files": _files(
            "market-domination-os",
            [
                "00_MARKET_DOMINATION_OS.md",
                "01_BEACHHEAD_STRATEGY.md",
                "02_VERTICAL_DOMINATION_PLAN.md",
                "03_THOUGHT_LEADERSHIP_MOAT.md",
                "04_PROOF_ASSET_DISTRIBUTION.md",
                "05_REFERRAL_AND_PARTNER_LOOP.md",
                "06_LOCAL_MARKET_CREDIBILITY.md",
                "07_CATEGORY_EDUCATION_PLAN.md",
                "99_MARKET_DOMINATION_REPORT.md",
            ],
        ),
        "marker_file": "docs/market-domination-os/00_MARKET_DOMINATION_OS.md",
    },
    "enterprise_sales_room": {
        "label": "ENTERPRISE_SALES_ROOM_OS",
        "json": "outputs/v10_verification/enterprise_sales_room_verification.json",
        "files": [
            *_files(
                "enterprise-sales-room-os",
                [
                    "00_ENTERPRISE_SALES_ROOM_OS.md",
                    "01_ENTERPRISE_SALES_PROCESS.md",
                    "02_STAKEHOLDER_MAP.md",
                    "03_BUSINESS_CASE_TEMPLATE.md",
                    "04_SECURITY_AND_LEGAL_PACK.md",
                    "05_PROCUREMENT_PACK.md",
                    "06_EXECUTIVE_PROPOSAL_TEMPLATE.md",
                    "07_PILOT_GOVERNANCE_MODEL.md",
                    "08_ENTERPRISE_CLOSE_PLAN.md",
                    "99_ENTERPRISE_SALES_ROOM_REPORT.md",
                ],
            ),
            "scripts/enterprise_sales_room_generate.py",
        ],
        "marker_file": "docs/enterprise-sales-room-os/04_SECURITY_AND_LEGAL_PACK.md",
    },
    "profitability": {
        "label": "PROFITABILITY_OS",
        "json": "outputs/v10_verification/profitability_verification.json",
        "files": [
            *_files(
                "profitability-os",
                [
                    "00_PROFITABILITY_OS.md",
                    "01_SERVICE_MARGIN_MODEL.md",
                    "02_DELIVERY_COST_MODEL.md",
                    "03_GROSS_MARGIN_GUARDRAILS.md",
                    "04_PRICING_FLOOR_POLICY.md",
                    "05_DISCOUNT_APPROVAL_RULES.md",
                    "06_SCOPE_CREEP_COST_CONTROL.md",
                    "07_MONTHLY_PROFIT_REVIEW.md",
                    "99_PROFITABILITY_REPORT.md",
                ],
            ),
            "config/profitability_model_schema.json",
            "data/profitability_inputs.example.jsonl",
            "scripts/profitability_summary.py",
        ],
        "marker_file": "docs/profitability-os/04_PRICING_FLOOR_POLICY.md",
    },
    "scope_control": {
        "label": "SCOPE_CONTROL_OS",
        "json": "outputs/v10_verification/scope_control_verification.json",
        "files": _files(
            "scope-control-os",
            [
                "00_SCOPE_CONTROL_OS.md",
                "01_SCOPE_BOUNDARY_POLICY.md",
                "02_CHANGE_REQUEST_PROCESS.md",
                "03_OUT_OF_SCOPE_LIBRARY.md",
                "04_CLIENT_REQUEST_TRIAGE.md",
                "05_DELIVERY_ACCEPTANCE_GATES.md",
                "99_SCOPE_CONTROL_REPORT.md",
            ],
        ),
        "marker_file": "docs/scope-control-os/00_SCOPE_CONTROL_OS.md",
    },
    "localization": {
        "label": "SAUDI_GCC_LOCALIZATION_OS",
        "json": "outputs/v10_verification/localization_verification.json",
        "files": _files(
            "localization-os",
            [
                "00_SAUDI_GCC_LOCALIZATION_OS.md",
                "01_ARABIC_BUSINESS_LANGUAGE_GUIDE.md",
                "02_SAUDI_BUYER_CONTEXT.md",
                "03_GCC_EXPANSION_NOTES.md",
                "04_SECTOR_LANGUAGE_GUIDE.md",
                "05_LOCAL_TRUST_SIGNALS.md",
                "06_CULTURAL_TONE_RULES.md",
                "99_LOCALIZATION_REPORT.md",
            ],
        ),
        "marker_file": "docs/localization-os/01_ARABIC_BUSINESS_LANGUAGE_GUIDE.md",
    },
    "productization": {
        "label": "PRODUCTIZATION_OS",
        "json": "outputs/v10_verification/productization_verification.json",
        "files": _files(
            "productization-os",
            [
                "00_PRODUCTIZATION_OS.md",
                "01_FROM_SERVICE_TO_PRODUCT.md",
                "02_REPEATABLE_MODULES.md",
                "03_TEMPLATE_LIBRARY.md",
                "04_CLIENT_PORTAL_ROADMAP.md",
                "05_INTERNAL_TOOLING_ROADMAP.md",
                "06_PRODUCTIZED_DELIVERY_CHECKLIST.md",
                "99_PRODUCTIZATION_REPORT.md",
            ],
        ),
        "marker_file": "docs/productization-os/00_PRODUCTIZATION_OS.md",
    },
    "operating_leverage": {
        "label": "OPERATING_LEVERAGE_OS",
        "json": "outputs/v10_verification/operating_leverage_verification.json",
        "files": _files(
            "operating-leverage-os",
            [
                "00_OPERATING_LEVERAGE_OS.md",
                "01_LEVERAGE_MAP.md",
                "02_AUTOMATION_WITH_BOUNDARIES.md",
                "03_TEMPLATE_REUSE_SYSTEM.md",
                "04_AGENT_ASSISTED_WORKFLOWS.md",
                "05_FOUNDER_TIME_MULTIPLIER.md",
                "99_OPERATING_LEVERAGE_REPORT.md",
            ],
        ),
        "marker_file": "docs/operating-leverage-os/02_AUTOMATION_WITH_BOUNDARIES.md",
    },
    "moat_metrics": {
        "label": "MOAT_METRICS_OS",
        "json": "outputs/v10_verification/moat_metrics_verification.json",
        "files": [
            *_files(
                "moat-metrics-os",
                [
                    "00_MOAT_METRICS_OS.md",
                    "01_LEARNING_ASSET_COUNT.md",
                    "02_REUSABLE_TEMPLATE_COUNT.md",
                    "03_SECTOR_DEPTH_SCORE.md",
                    "04_DELIVERY_REUSE_RATE.md",
                    "05_TRUST_ASSET_SCORE.md",
                    "06_CATEGORY_AUTHORITY_SCORE.md",
                    "99_MOAT_METRICS_REPORT.md",
                ],
            ),
            "scripts/moat_metrics_summary.py",
            "data/moat_metrics_inputs.example.jsonl",
        ],
        "marker_file": "docs/moat-metrics-os/00_MOAT_METRICS_OS.md",
    },
    "ceo_cockpit": {
        "label": "CEO_COCKPIT_OS",
        "json": "outputs/v10_verification/ceo_cockpit_verification.json",
        "files": [
            *_files(
                "ceo-cockpit-os",
                [
                    "00_CEO_COCKPIT_OS.md",
                    "01_CEO_DAILY_VIEW.md",
                    "02_CEO_WEEKLY_VIEW.md",
                    "03_CEO_MONTHLY_VIEW.md",
                    "04_DECISION_QUEUE.md",
                    "05_RISK_QUEUE.md",
                    "06_OPPORTUNITY_QUEUE.md",
                    "99_CEO_COCKPIT_REPORT.md",
                ],
            ),
            "scripts/ceo_cockpit_generate.py",
        ],
        "marker_file": "docs/ceo-cockpit-os/00_CEO_COCKPIT_OS.md",
    },
}


def markers_for(key: str) -> dict[str, list[str]]:
    spec = SPECS[key]
    return {spec["marker_file"]: [_MARKER]}


def verify(key: str):
    """Run the check for an OS key, returning a v10_common.CheckResult."""
    import importlib.util
    from pathlib import Path

    _spec = importlib.util.spec_from_file_location(
        "v10_common", Path(__file__).resolve().parent / "v10_common.py"
    )
    _mod = importlib.util.module_from_spec(_spec)
    assert _spec and _spec.loader
    _spec.loader.exec_module(_mod)
    s = SPECS[key]
    return _mod.run_check(s["label"], s["files"], markers_for(key)), s["json"]


def verify_all():
    """Run every V10 OS check. Returns list of (key, CheckResult, json_out)."""
    results = []
    for key in SPECS:
        result, json_out = verify(key)
        results.append((key, result, json_out))
    return results
