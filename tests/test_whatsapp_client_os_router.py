"""WhatsApp Client OS — router HTTP smoke (isolated FastAPI app).

Mounts ONLY the Client OS router on a fresh FastAPI app (no heavy ``api.main``
import) so the HTTP contract is tested in isolation. Skipped when fastapi /
the test client transport are unavailable.
"""

from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
pytest.importorskip("httpx")  # fastapi TestClient transport

from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_WHATSAPP_OS_DIR", str(tmp_path))
    from auto_client_acquisition.whatsapp_client_os import client_profile_store as store

    store.clear_for_test()
    from api.routers import whatsapp_client_os as router_mod

    app = FastAPI()
    app.include_router(router_mod.router)
    return TestClient(app)


def test_message_welcome_returns_menu(client) -> None:
    res = client.post(
        "/api/v1/whatsapp-client-os/message",
        json={"client_handle": "966500000000", "text": "مرحبا"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["intent"] == "welcome"
    assert body["cards"][0]["kind"] == "menu"
    assert len(body["whatsapp_payloads"]) == 1
    assert body["safety_summary"] == "no_live_send_no_secrets_in_chat"


def test_secrets_message_is_blocked(client) -> None:
    res = client.post(
        "/api/v1/whatsapp-client-os/message",
        json={"client_handle": "966500000001", "text": "api_key=sk-abcdefghijklmnopqrstuvwxyz1234"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["blocked"] is True
    assert body["handoff"] is not None
    assert body["handoff"]["reason"] == "secrets_attempt"


def test_permissions_levels_endpoint(client) -> None:
    res = client.get("/api/v1/whatsapp-client-os/permissions/levels")
    assert res.status_code == 200
    levels = res.json()["levels"]
    assert [lv["level"] for lv in levels] == ["L0", "L1", "L2", "L3", "L4", "L5"]
    assert any(lv["whatsapp_only_allowed"] is False for lv in levels)  # L5


def test_templates_endpoint(client) -> None:
    res = client.get("/api/v1/whatsapp-client-os/templates")
    assert res.status_code == 200
    assert "welcome" in res.json()["canonical"]


def test_full_assessment_via_api(client) -> None:
    from auto_client_acquisition.whatsapp_client_os.assessment import AXIS_ORDER, axis_spec

    start = client.post(
        "/api/v1/whatsapp-client-os/assessment/start",
        json={"client_handle": "966500000002", "company_name": "شركة"},
    ).json()
    session_id = start["session"]["session_id"]
    last = start
    for ax in AXIS_ORDER:
        opt = axis_spec(ax)["options"][0]["id"]
        last = client.post(
            "/api/v1/whatsapp-client-os/assessment/answer",
            json={
                "session_id": session_id,
                "client_handle": "966500000002",
                "axis": ax,
                "option_id": opt,
            },
        ).json()
    assert last["assessment"] is not None
    assert last["assessment"]["completed"] is True
    aid = last["assessment"]["assessment_id"]
    report = client.get(f"/api/v1/whatsapp-client-os/assessment/{aid}/report")
    assert report.status_code == 200
    assert "report_markdown" in report.json()


def test_metrics_endpoint(client) -> None:
    client.post(
        "/api/v1/whatsapp-client-os/message",
        json={"client_handle": "966500000003", "text": "مرحبا"},
    )
    res = client.get("/api/v1/whatsapp-client-os/metrics")
    assert res.status_code == 200
    assert res.json()["new_sessions"] >= 1
