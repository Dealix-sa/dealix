from __future__ import annotations

from scripts.commercial.build_company_operating_blueprint import (
    build_operating_blueprint,
    load_registry,
)


def _company() -> dict:
    return {
        "company_name": "Synthetic Saudi Services Co",
        "sector": "B2B services",
        "country": "Saudi Arabia",
        "strategic_goals": ["improve revenue execution", "prove customer value"],
        "source_refs": ["synthetic://company/context"],
        "function_evidence": {
            "sales": {
                "maturity": 1,
                "business_impact": 5,
                "urgency": 5,
                "owner_readiness": 5,
                "data_readiness": 4,
                "risk": 2,
                "named_owner": "Head of Sales",
                "problem": "Pipeline actions and qualification are inconsistent.",
                "baseline": "Only 35% of qualified opportunities have a dated next action.",
                "target_metric": "At least 80% have a dated evidence-backed next action.",
                "source_refs": ["synthetic://crm/pipeline"],
            },
            "customer_success": {
                "maturity": 1,
                "business_impact": 5,
                "urgency": 4,
                "owner_readiness": 4,
                "data_readiness": 3,
                "risk": 2,
                "named_owner": "Customer Success Lead",
                "problem": "Renewal risk appears too late and value is not evidenced.",
                "baseline": "No agreed value baseline exists for active customers.",
                "target_metric": "Every pilot has baseline, adoption, risk, and value evidence.",
                "source_refs": ["synthetic://cs/accounts"],
            },
            "finance": {
                "maturity": 0,
                "business_impact": 4,
                "urgency": 3,
                "owner_readiness": 0,
                "data_readiness": 0,
                "risk": 4,
            },
        },
    }


def test_registry_covers_full_company_operating_scope() -> None:
    registry = load_registry()

    function_ids = {item["id"] for item in registry["functions"]}
    assert len(function_ids) == 14
    assert {
        "executive_strategy",
        "market_intelligence",
        "marketing",
        "sales",
        "customer_success",
        "operations",
        "support",
        "product",
        "engineering_data_ai",
        "finance",
        "procurement",
        "people",
        "partnerships",
        "risk_compliance_security",
    } == function_ids


def test_blueprint_selects_at_most_two_initial_functions() -> None:
    result = build_operating_blueprint(_company())

    assert result["decision"] == "pilot_design_ready"
    assert len(result["initial_scope"]) == 2
    assert [item["function_id"] for item in result["initial_scope"]] == [
        "sales",
        "customer_success",
    ]
    assert all(item["readiness"] == "pilot_ready" for item in result["initial_scope"])


def test_blueprint_fails_closed_for_unverified_functions() -> None:
    result = build_operating_blueprint(_company())
    finance = next(
        item
        for item in result["company_maturity_assessment"]
        if item["function_id"] == "finance"
    )

    assert finance["readiness"] == "unverified"
    assert finance["recommended_action"] == "complete_diagnostic"
    assert "finance" in result["unverified_functions"]
    assert result["readiness_claims_generated"] is False


def test_blueprint_never_enables_big_bang_enterprise_rollout() -> None:
    result = build_operating_blueprint(_company())

    assert result["enterprise_expansion_allowed"] is False
    assert "big_bang_enterprise_rollout" in result["forbidden_patterns"]
    assert "verified_delivery" in result["enterprise_expansion_gate"]
    assert "owner_adoption" in result["enterprise_expansion_gate"]
    assert "unit_economics_review" in result["enterprise_expansion_gate"]


def test_blueprint_is_draft_only_and_quote_safe() -> None:
    result = build_operating_blueprint(_company())

    assert result["mode"] == "draft_only"
    assert result["external_actions_executed"] == 0
    assert result["quote_generated"] is False
    assert result["next_step"] == "prepare_bounded_pilot_and_internal_quote"
    assert [item["type"] for item in result["approval_items"]] == [
        "diagnostic_scope",
        "data_and_source_access",
        "pilot_design",
        "commercial_terms",
        "external_send",
    ]


def test_blueprint_requires_named_company() -> None:
    company = _company()
    company["company_name"] = ""

    result = build_operating_blueprint(company)

    assert result["decision"] == "blocked"
    assert result["next_step"] == "provide_named_company"
    assert result["external_actions_executed"] == 0


def test_blueprint_builds_phased_non_big_bang_roadmap() -> None:
    result = build_operating_blueprint(_company())

    assert [phase["phase"] for phase in result["phased_roadmap"]] == [
        "diagnostic",
        "pilot",
        "implementation",
        "managed_service",
    ]
    assert len(result["phased_roadmap"][1]["functions"]) == 1
