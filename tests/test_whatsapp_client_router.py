"""WhatsApp Client OS router — endpoint tests on an isolated app.

Mounts only the router on a fresh FastAPI app (no DB / full-app boot needed)
and redirects the JSONL stores to a tmp path.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import whatsapp_client
from auto_client_acquisition.whatsapp_client_os import session_store as store
from auto_client_acquisition.whatsapp_client_os.readiness_scan import READINESS_AXES


@pytest.fixture()
def client(tmp_path, monkeypatch):
    for name in ("SESSIONS", "MESSAGES", "CARDS", "ASSESSMENTS", "PERMISSIONS"):
        monkeypatch.setenv(f"DEALIX_WHATSAPP_{name}_PATH", str(tmp_path / f"{name}.jsonl"))
    store.clear_for_test()
    app = FastAPI()
    app.include_router(whatsapp_client.router)
    with TestClient(app) as c:
        yield c
    store.clear_for_test()


def test_message_endpoint_welcome(client) -> None:
    r = client.post("/api/v1/whatsapp-client/message", json={"wa_id": "+966500000001", "text": ""})
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "welcome"
    assert body["governance_decision"] == "ALLOW"
    # The raw WhatsApp id must never be echoed back.
    assert "966500000001" not in r.text


def test_message_endpoint_blocks_unsafe(client) -> None:
    r = client.post(
        "/api/v1/whatsapp-client/message",
        json={"wa_id": "+966500000002", "text": "ارسل واتساب لكل الارقام المشتراة"},
    )
    assert r.json()["governance_decision"] == "BLOCK"


def test_scan_endpoint(client) -> None:
    answers = {a.id: a.options[-1].value for a in READINESS_AXES}
    r = client.post(
        "/api/v1/whatsapp-client/scan",
        json={"answers": answers, "company": "Acme", "session_id": "s1"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["assessment"]["revenue_readiness"] >= 80
    assert body["recommendation_card"]["kind"] == "recommendation"


def test_triage_endpoint(client) -> None:
    r = client.post(
        "/api/v1/whatsapp-client/triage",
        json={"answers": {"has_leads": "نعم", "biggest_problem": "المتابعة"}},
    )
    assert r.json()["assessment"]["recommended_offer_id"]


def test_scan_questions_endpoint(client) -> None:
    r = client.get("/api/v1/whatsapp-client/scan/questions")
    body = r.json()
    assert len(body["axes"]) == 10
    assert len(body["quick_triage"]) == 4


def test_flows_endpoint(client) -> None:
    r = client.get("/api/v1/whatsapp-client/flows")
    assert len(r.json()["flows"]) == 12


def test_metrics_endpoint(client) -> None:
    client.post("/api/v1/whatsapp-client/message", json={"wa_id": "+966500000009", "text": ""})
    r = client.get("/api/v1/whatsapp-client/metrics")
    assert r.json()["new_sessions"] >= 1


def test_webhook_verify_requires_token(client) -> None:
    r = client.get(
        "/api/v1/whatsapp-client/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": "wrong", "hub.challenge": "123"},
    )
    assert r.status_code == 403
