from __future__ import annotations

from scripts.commercial.build_sale_ready_pack import build_sale_ready_pack, load_registry


def _qualified_account() -> dict:
    return {
        "company_name": "Synthetic Saudi Services Co",
        "sector": "B2B services",
        "country": "Saudi Arabia",
        "buyer_persona": "founder_ceo",
        "business_problem": "Qualified opportunities stall because ownership and next actions are unclear.",
        "impact_hypothesis": "Longer sales cycles and lower conversion confidence.",
        "owner": "Revenue Lead",
        "available_sources": ["CRM export", "proposal tracker"],
        "bounded_pilot_willingness": True,
        "baseline": "Median proposal-to-decision time is not yet verified.",
        "target_metric": "Verified reduction in proposal-to-decision time.",
        "current_loss_or_cost": "Customer input required",
        "frequency": "Weekly",
        "affected_volume": "Customer input required",
        "decision_value": "Faster commercial decisions",
        "time_to_value": "Within a bounded 30-day pilot",
        "pilot_scope": {
            "scope_in": ["one opportunity segment", "one proposal workflow"],
            "scope_out": ["mass outbound", "production CRM mutation"],
            "approval_boundaries": ["external_send", "commercial_terms", "scope_change"],
            "delivery_checkpoints": ["baseline", "week_1", "week_2", "final_proof_pack"],
            "acceptance_criteria": ["source-backed baseline", "approved workflow", "proof pack"],
            "proof_requirements": ["source_snapshot", "approval_record", "outcome_evidence"],
            "rollback_or_stop_rule": "Stop if access, consent, or evidence quality is insufficient.",
        },
    }


def test_registry_is_quote_only_and_proof_gated() -> None:
    registry = load_registry()
    doctrine = registry["commercial_doctrine"]

    assert doctrine["public_fixed_price_forbidden"] is True
    assert doctrine["checkout_before_discovery_forbidden"] is True
    assert doctrine["quote_requires_discovery"] is True
    assert doctrine["revenue_claim_requires_payment_proof"] is True
    assert doctrine["delivery_claim_requires_delivery_proof"] is True
    assert doctrine["value_claim_requires_baseline_and_value_evidence"] is True


def test_qualified_account_produces_internal_sale_ready_pack_only() -> None:
    pack = build_sale_ready_pack(_qualified_account())

    assert pack["qualification_result"]["decision"] == "qualified"
    assert pack["recommended_offer"]["id"] == "saudi_opportunity_snapshot"
    assert pack["pilot_scope"]["status"] == "ready_for_quote"
    assert pack["next_step"] == "prepare_internal_quote_and_approval_pack"
    assert pack["quote_generated"] is False
    assert pack["external_actions_executed"] == 0
    assert [item["type"] for item in pack["approval_items"]] == [
        "proposal_scope",
        "commercial_terms",
        "external_send",
    ]


def test_missing_discovery_data_routes_to_mini_diagnostic() -> None:
    account = {
        "company_name": "Synthetic Company",
        "business_problem": "Pipeline visibility is weak.",
        "impact_hypothesis": "Decisions are delayed.",
        "owner": "Founder",
    }
    pack = build_sale_ready_pack(account)

    assert pack["qualification_result"]["decision"] == "uncertain"
    assert pack["qualification_result"]["route"] == "mini_diagnostic_only"
    assert pack["recommended_offer"]["id"] == "saudi_opportunity_snapshot"
    assert pack["pilot_scope"]["status"] == "discovery_required"
    assert pack["approval_items"] == []
    assert pack["next_step"] == "complete_discovery_and_missing_pilot_fields"


def test_unsafe_or_guaranteed_outcome_request_is_rejected() -> None:
    account = _qualified_account()
    account["requested_capabilities"] = ["uncontrolled_mass_outbound"]
    account["requires_guaranteed_revenue"] = True

    pack = build_sale_ready_pack(account)

    assert pack["qualification_result"]["decision"] == "not_qualified"
    assert pack["recommended_offer"] is None
    assert pack["pilot_scope"] == {"status": "withheld", "reason": "account_not_qualified"}
    assert pack["approval_items"] == []
    assert pack["next_step"] == "decline_or_refer"


def test_value_case_never_claims_roi() -> None:
    pack = build_sale_ready_pack(_qualified_account())

    assert pack["value_case"]["status"] == "supported_hypothesis"
    assert pack["value_case"]["roi_claim_allowed"] is False
    assert "guaranteed_roi" in pack["risks_and_assumptions"]["unsupported_claims_withheld"]


def test_buyer_personas_cover_core_company_functions() -> None:
    registry = load_registry()
    personas = {persona["id"] for persona in registry["buyer_personas"]}

    assert personas == {
        "founder_ceo",
        "head_of_sales",
        "operations_leader",
        "customer_success_leader",
        "technology_or_data_leader",
        "market_access_or_partnerships_leader",
    }
