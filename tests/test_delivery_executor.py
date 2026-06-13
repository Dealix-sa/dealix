"""Tests for the stateful 7-day sprint executor + delivery API.

Covers the core doctrine behaviour: the sprint advances day-by-day, PAUSES at
the Day-5 governance gate (no founder approval → no further days), and resumes
only after explicit approval.
"""
from __future__ import annotations

import pytest

SAMPLE = {
    "sources": [{"source_type": "crm", "row_count": 120, "consent": "granted",
                 "has_source_passport": True}],
    "rows": [{"company": "A", "email": "a@x.com", "phone": "+966500000001", "amount": 1000},
             {"company": "B", "email": "b@x.com", "phone": "+966500000002", "amount": 2000}],
    "pain_summary": "scattered follow-up",
}


def _make_ctx(eid: str):
    from dealix.commercial.sprint_orchestrator import SprintContext
    return SprintContext(
        engagement_id=eid, customer_id="acme", customer_name="Acme",
        sector="logistics", city="Riyadh",
        sources=SAMPLE["sources"], rows=SAMPLE["rows"],
        pain_summary=SAMPLE["pain_summary"], founder_approved=False,
    )


@pytest.fixture()
def executor(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_SPRINT_STORE_PATH", str(tmp_path / "s.jsonl"))
    from auto_client_acquisition.delivery_factory import sprint_executor
    return sprint_executor


def test_sprint_pauses_at_day5_then_completes(executor):
    eid = "eng_1"
    st = executor.start_sprint(_make_ctx(eid))
    assert st["current_day"] == 0 and st["status"] == "running"

    for expected_day in (1, 2, 3, 4):
        st = executor.advance(eid)
        assert st["current_day"] == expected_day
        assert st["status"] == "running"

    # Day 5 — the governance gate pauses the sprint.
    st = executor.advance(eid)
    assert st["status"] == "awaiting_approval"
    assert st["awaiting_approval"] is True
    assert st["current_day"] == 4  # not advanced past the gate

    # Advancing while paused is a no-op until approval.
    assert executor.advance(eid)["status"] == "awaiting_approval"

    # Founder approves → resume.
    st = executor.approve_day5(eid, who="founder")
    assert st["status"] == "running" and st["awaiting_approval"] is False
    assert st.get("day5_approved_by") == "founder"

    st = executor.advance(eid)   # re-runs day 5, now complete
    assert st["current_day"] == 5
    st = executor.advance(eid)   # day 6
    assert st["current_day"] == 6
    st = executor.advance(eid)   # day 7
    assert st["current_day"] == 7 and st["status"] == "complete"

    days = sorted(r["day"] for r in st["day_results"])
    assert days == [1, 2, 3, 4, 5, 6, 7]


def test_get_unknown_returns_none(executor):
    assert executor.get("does-not-exist") is None
    assert executor.advance("does-not-exist") is None
    assert executor.approve_day5("does-not-exist") is None


def test_run_to_completion_auto_approve(executor):
    eid = "eng_auto"
    executor.start_sprint(_make_ctx(eid))
    st = executor.run_to_completion(eid, auto_approve=True)
    assert st["status"] == "complete"
    assert st["current_day"] == 7


def test_run_to_completion_pauses_without_auto_approve(executor):
    eid = "eng_pause"
    executor.start_sprint(_make_ctx(eid))
    st = executor.run_to_completion(eid, auto_approve=False)
    assert st["status"] == "awaiting_approval"


# ── Delivery API ────────────────────────────────────────────────────────────

@pytest.fixture()
def api_client(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_SPRINT_STORE_PATH", str(tmp_path / "api.jsonl"))
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.routers import delivery
    app = FastAPI()
    app.include_router(delivery.router)
    return TestClient(app)


_H = {"X-Admin-API-Key": "test-key"}


def test_delivery_api_full_flow(api_client):
    start = api_client.post("/api/v1/delivery/sprint/start", headers=_H,
                            json={"engagement_id": "e1", "customer_id": "acme", **SAMPLE})
    assert start.status_code == 200
    assert start.json()["status"] == "running"

    for _ in range(4):
        api_client.post("/api/v1/delivery/sprint/e1/advance", headers=_H)
    day5 = api_client.post("/api/v1/delivery/sprint/e1/advance", headers=_H)
    assert day5.json()["status"] == "awaiting_approval"

    appr = api_client.post("/api/v1/delivery/sprint/e1/approve-day5", headers=_H,
                           json={"who": "founder"})
    assert appr.json()["status"] == "running"

    got = api_client.get("/api/v1/delivery/sprint/e1", headers=_H)
    assert got.status_code == 200
    assert got.json()["engagement_id"] == "e1"


def test_delivery_api_auth_and_validation(api_client):
    # missing admin header → 401
    assert api_client.post("/api/v1/delivery/sprint/start",
                           json={"engagement_id": "x", "customer_id": "y"}).status_code == 401
    # missing required fields → 422
    assert api_client.post("/api/v1/delivery/sprint/start", headers=_H, json={}).status_code == 422
    # unknown sprint → 404
    assert api_client.get("/api/v1/delivery/sprint/nope", headers=_H).status_code == 404
