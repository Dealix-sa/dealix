from __future__ import annotations

import json

from api.routers.client_value_room import compose_client_value_room
from api.routers.domains.customers import get_routers


def test_value_room_route_is_mounted_in_customers_domain() -> None:
    paths = {
        route.path
        for router in get_routers()
        for route in router.routes
        if hasattr(route, "path")
    }

    assert "/api/v1/customer-portal/{customer_handle}/value-room" in paths


def test_empty_customer_value_room_fails_closed_without_invented_value() -> None:
    room = compose_client_value_room("synthetic-client")

    assert room["mode"] == "draft_only"
    assert room["client_context"]["customer_handle"] == "synthetic-client"
    assert room["external_actions_executed"] == 0
    assert room["executive_summary"]["value_status"] == "baseline_missing"
    assert room["renewal_and_expansion"]["external_send_allowed"] is False
    assert room["renewal_and_expansion"]["recommendation"] == "withheld_pending_evidence"
    assert room["disclosures"]["customer_safe_adapter"] is True
    assert room["disclosures"]["no_duplicate_storage"] is True
    assert room["source_summary"]["proof_events"] == 0
    assert room["source_summary"]["value_events"] == 0


def test_value_room_contract_exposes_all_customer_decision_sections() -> None:
    room = compose_client_value_room("synthetic-client")

    required = {
        "client_context",
        "executive_summary",
        "scope_and_success",
        "work_items",
        "decisions_and_approvals",
        "risks_and_exceptions",
        "delivery_and_acceptance",
        "value_realization",
        "timeline",
        "renewal_and_expansion",
        "data_freshness",
        "disclosures",
    }
    assert required.issubset(room)


def test_value_room_never_serializes_secret_shaped_fields() -> None:
    rendered = json.dumps(compose_client_value_room("synthetic-client")).lower()

    forbidden = [
        "api_key",
        "secret_key",
        "access_token",
        "refresh_token",
        "password",
        "chain_of_thought",
    ]
    assert all(name not in rendered for name in forbidden)


def test_missing_sources_are_disclosed_instead_of_replaced_with_demo_metrics() -> None:
    room = compose_client_value_room("synthetic-client")

    missing = room["disclosures"]["missing_data"]
    assert "baseline" in missing["scope_and_success"]
    assert room["value_realization"] == []
    assert room["disclosures"]["negative_and_inconclusive_results_visible"] is True
