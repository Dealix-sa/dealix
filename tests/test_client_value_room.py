from __future__ import annotations

from scripts.commercial.build_client_value_room import build_client_value_room, load_registry


def _engagement() -> dict:
    return {
        "client_name": "Synthetic Client",
        "engagement_id": "eng-1",
        "pilot_id": "pilot-1",
        "sector": "services",
        "current_phase": "pilot",
        "overall_status": "on_track",
        "scope_in": ["lead qualification", "daily command"],
        "scope_out": ["live outbound", "payment capture"],
        "owner_matrix": {"client": "client-owner", "dealix": "dealix-owner"},
        "baseline": {"qualified_opportunities_per_week": 2},
        "target_metrics": ["qualified_opportunities_per_week"],
        "acceptance_criteria": ["daily command generated", "proof reviewed"],
        "stop_rule": "stop if source access or approval boundary is unavailable",
        "work_items": [
            {"id": "w1", "status": "in_progress", "owner": "dealix-owner"},
            {"id": "w2", "status": "blocked", "owner": "client-owner"},
        ],
        "decisions": [
            {"id": "d1", "status": "pending", "decision": "approve source access"}
        ],
        "risks": [
            {"risk_id": "r1", "severity": "high", "business_impact": "measurement delay"}
        ],
        "deliverables": [
            {
                "deliverable": "weekly command pack",
                "completion_status": "completed",
                "completion_evidence": ["artifact://weekly-command-1"],
                "acceptance_status": "not_requested",
                "acceptance_evidence": [],
            }
        ],
        "value_metrics": [
            {
                "metric": "qualified_opportunities_per_week",
                "baseline": 2,
                "target": 5,
                "current": 4,
                "unit": "count",
                "measurement_window": "2026-08-01/2026-08-07",
                "source": "crm://report-1",
                "confidence": 0.8,
                "verified": False,
                "customer_accepted": False,
                "evidence_refs": ["artifact://metric-1"],
            }
        ],
        "timeline": [{"event_id": "evt-1", "event_type": "pilot_started"}],
        "next_checkpoint": "2026-08-10",
        "source_last_updated_at": "2026-08-03T06:00:00Z",
    }


def test_registry_requires_complete_client_visibility() -> None:
    registry = load_registry()
    assert registry["client_promise"]["know_what_is_happening"] is True
    assert registry["client_promise"]["know_what_value_is_proven"] is True
    assert registry["client_promise"]["know_what_is_not_yet_proven"] is True
    assert registry["proof_rules"]["activity_is_not_delivery"] is True
    assert registry["proof_rules"]["delivery_is_not_acceptance"] is True
    assert registry["proof_rules"]["acceptance_is_not_value"] is True


def test_client_value_room_surfaces_status_risk_and_decisions() -> None:
    result = build_client_value_room(_engagement())

    assert result["mode"] == "draft_only"
    assert result["external_actions_executed"] == 0
    assert result["executive_summary"]["overall_status"] == "at_risk"
    assert len(result["executive_summary"]["top_risks"]) == 1
    assert len(result["executive_summary"]["decisions_needed"]) == 1


def test_directional_metric_is_visible_but_not_claimable() -> None:
    result = build_client_value_room(_engagement())
    metric = result["value_realization"][0]

    assert metric["value_status"] == "directional_signal"
    assert metric["claim_allowed"] is False
    assert result["executive_summary"]["value_status"] == "directional_signal"


def test_verified_customer_accepted_metric_is_claimable() -> None:
    engagement = _engagement()
    engagement["value_metrics"][0]["verified"] = True
    engagement["value_metrics"][0]["customer_accepted"] = True

    result = build_client_value_room(engagement)
    metric = result["value_realization"][0]

    assert metric["value_status"] == "customer_accepted"
    assert metric["claim_allowed"] is True
    assert result["executive_summary"]["value_status"] == "customer_accepted"


def test_missing_baseline_is_disclosed_and_not_claimable() -> None:
    engagement = _engagement()
    engagement["value_metrics"][0]["baseline"] = None

    result = build_client_value_room(engagement)
    metric = result["value_realization"][0]

    assert metric["value_status"] == "baseline_missing"
    assert metric["claim_allowed"] is False
    assert "baseline" in result["disclosures"]["missing_data"]["value_metrics"][0]["missing"]


def test_delivery_and_acceptance_remain_separate() -> None:
    result = build_client_value_room(_engagement())
    deliverable = result["delivery_and_acceptance"][0]

    assert deliverable["delivery_claim_allowed"] is True
    assert deliverable["acceptance_claim_allowed"] is False


def test_renewal_never_sends_from_draft_room() -> None:
    engagement = _engagement()
    engagement["renewal_recommendation"] = "extend"
    engagement["renewal_evidence"] = ["artifact://value-review"]

    result = build_client_value_room(engagement)

    assert result["renewal_and_expansion"]["recommendation"] == "extend"
    assert result["renewal_and_expansion"]["external_send_allowed"] is False


def test_open_standards_are_alignment_only_without_new_dependency() -> None:
    registry = load_registry()
    standards = registry["open_standards_alignment"]

    assert set(standards) == {"cloudevents", "opentelemetry", "openlineage", "openfeature"}
    assert all(item["dependency_required_now"] is False for item in standards.values())
