"""
End-to-end tests for `api/routers/hermes.py` via `fastapi.testclient.TestClient`.

The router isn't wired into `api/main.py` yet (that's a separate review), so this
suite mounts it on a minimal `FastAPI()` to give it exhaustive coverage while
keeping the router's contract honest.
"""

from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from api.routers.hermes import _state, router  # noqa: E402
from dealix.hermes.control_plane import HermesRuntime  # noqa: E402
from dealix.hermes.products import default_registry as default_offer_registry  # noqa: E402


@pytest.fixture()
def client() -> TestClient:
    """Fresh runtime + offer registry per test so state never leaks."""
    _state.runtime = HermesRuntime()
    _state.offers = default_offer_registry()
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def _founder_run(client: TestClient, intent: str, **extra) -> dict:
    body = {
        "actor": {"actor_id": "founder.sami", "kind": "founder"},
        "intent": intent,
        **extra,
    }
    r = client.post("/api/v1/hermes/run", json=body)
    assert r.status_code == 200, r.text
    return r.json()


def test_run_internal_intent_passes_with_s1(client: TestClient) -> None:
    body = _founder_run(client, "internal.signal.capture", payload={"note": "hi"})
    assert body["success"] is True
    assert body["risk"]["sovereignty_level"] == "S1_INTERNAL_AUTO"
    assert body["risk"]["approval_required"] is False


def test_run_public_external_is_denied_by_authorization(client: TestClient) -> None:
    r = client.post(
        "/api/v1/hermes/run",
        json={
            "actor": {"actor_id": "anon", "kind": "public"},
            "intent": "external.send.email",
            "declared_output_kind": "message",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is False
    assert body["error"]["code"] == "denied"


def test_run_external_send_opens_approval_ticket(client: TestClient) -> None:
    body = _founder_run(
        client,
        "external.send.email",
        declared_output_kind="message",
        draft={"text": "مرحبا، هذه مسودة نظيفة بدون ادعاءات."},
    )
    assert body["success"] is True
    assert body["risk"]["approval_required"] is True
    ticket_id = body["next_actions"][0]["ticket_id"]
    assert ticket_id.startswith("apr_")

    # /approvals lists the pending ticket
    listed = client.get("/api/v1/hermes/approvals").json()
    assert listed["count"] >= 1
    assert any(t["ticket_id"] == ticket_id for t in listed["tickets"])

    # /approvals/{id}/decide approves it
    r = client.post(
        f"/api/v1/hermes/approvals/{ticket_id}/decide",
        json={"decided_by": "sami", "approve": True, "note": "ok"},
    )
    assert r.status_code == 200
    ticket = r.json()["ticket"]
    assert ticket["status"] == "approved"
    assert ticket["decided_by"] == "sami"


def test_run_overclaim_draft_fails_trust_gate(client: TestClient) -> None:
    body = _founder_run(
        client,
        "external.send.email",
        declared_output_kind="message",
        draft={"text": "نضمن لك 100% من النتائج الفورية"},
    )
    assert body["success"] is False
    assert body["error"]["code"] == "denied"


def test_decide_unknown_ticket_returns_404(client: TestClient) -> None:
    r = client.post(
        "/api/v1/hermes/approvals/apr_does_not_exist/decide",
        json={"decided_by": "sami", "approve": True},
    )
    assert r.status_code == 404


def test_trace_endpoint_returns_audit_events_for_request(client: TestClient) -> None:
    body = _founder_run(client, "internal.signal.capture", payload={"x": 1})
    request_id = body["request_id"]
    r = client.get(f"/api/v1/hermes/trace/{request_id}")
    assert r.status_code == 200
    trace = r.json()["events"]
    assert isinstance(trace, list)
    assert any(e["stage"] == "gate.authorization" for e in trace)
    assert all(e["request_id"] == request_id for e in trace)


def test_offers_list_and_readiness(client: TestClient) -> None:
    listed = client.get("/api/v1/hermes/offers").json()
    assert listed["count"] == 10
    sample_id = listed["offers"][0]["offer_id"]

    r = client.get(f"/api/v1/hermes/offers/{sample_id}/readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["offer_id"] == sample_id
    assert isinstance(body["ready"], bool)
    assert 0 <= body["score"] <= 100


def test_offer_readiness_unknown_returns_404(client: TestClient) -> None:
    r = client.get("/api/v1/hermes/offers/does_not_exist/readiness")
    assert r.status_code == 404


def test_controls_evaluate_endpoint(client: TestClient) -> None:
    r = client.get(
        "/api/v1/hermes/controls/evaluate",
        params={
            "agent_owner": "founder",
            "tool_owner": "founder",
            "is_external_action": "true",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "verdicts" in body
    assert isinstance(body["verdicts"], list)
    codes = {v["control_id"] for v in body["verdicts"]}
    # the full library must be evaluated
    assert "CTRL-GOV-001" in codes
    assert "CTRL-GOV-003" in codes


def test_kill_switch_trip_restore_and_listing(client: TestClient) -> None:
    trip = client.post(
        "/api/v1/hermes/kill-switch/agent/agent_x/trip",
        json={"tripped_by": "sami", "reason": "test"},
    )
    assert trip.status_code == 200
    assert trip.json()["record"]["state"] == "tripped"

    active = client.get("/api/v1/hermes/kill-switch/active").json()
    assert any(
        r["kind"] == "agent" and r["target_id"] == "agent_x"
        for r in active["records"]
    )

    restore = client.post(
        "/api/v1/hermes/kill-switch/agent/agent_x/restore",
        json={"restored_by": "sami", "reason": "test"},
    )
    assert restore.status_code == 200
    assert restore.json()["record"]["state"] == "active"


def test_kill_switch_invalid_kind_is_rejected(client: TestClient) -> None:
    r = client.post(
        "/api/v1/hermes/kill-switch/nonsense/x/trip",
        json={"tripped_by": "sami", "reason": "test"},
    )
    assert r.status_code in (400, 422)
