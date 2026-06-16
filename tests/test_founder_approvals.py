"""Tests for the founder approval API (/api/v1/founder/approvals*).

Exercises the routes against the durable draft queue so the daily-draft loop
and the founder dashboard share one queue. Covers list, approve, reject,
status filtering, and the 404 path.
"""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture()
def client_and_queue(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_DRAFT_QUEUE_PATH", str(tmp_path / "q.jsonl"))
    from auto_client_acquisition.commercial_orchestrator import draft_queue
    from api.routers import founder

    app = FastAPI()
    app.include_router(founder.router)
    return TestClient(app), draft_queue


def _seed(draft_queue, n: int = 2) -> list[str]:
    ids = []
    for i in range(n):
        rec = draft_queue.enqueue({
            "kind": "outreach",
            "company_name": f"Acme {i}",
            "sector": "logistics",
            "city": "Riyadh",
            "subject_en": "hi",
            "subject_ar": "مرحبا",
            "body_md": "draft body",
            "consent_status": "required_before_contact",
        })
        ids.append(rec["id"])
    return ids


def test_get_approvals_empty(client_and_queue):
    client, _ = client_and_queue
    r = client.get("/api/v1/founder/approvals")
    assert r.status_code == 200
    data = r.json()
    assert data["pending"] == 0
    assert data["drafts"] == []
    assert data["hard_gates"]["no_live_send"] is True


def test_list_pending_drafts(client_and_queue):
    client, dq = client_and_queue
    _seed(dq, 3)
    r = client.get("/api/v1/founder/approvals")
    data = r.json()
    assert data["pending"] == 3
    assert len(data["drafts"]) == 3
    assert all(d["approval_required"] for d in data["drafts"])


def test_approve_draft(client_and_queue):
    client, dq = client_and_queue
    ids = _seed(dq, 2)
    r = client.post(f"/api/v1/founder/approvals/{ids[0]}/approve",
                    json={"who": "founder", "note": "ship it"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["change"]["status"] == "approved"
    assert body["no_live_send"] is True
    # one approved, one still pending
    listing = client.get("/api/v1/founder/approvals").json()
    assert listing["pending"] == 1


def test_reject_draft(client_and_queue):
    client, dq = client_and_queue
    ids = _seed(dq, 1)
    r = client.post(f"/api/v1/founder/approvals/{ids[0]}/reject",
                    json={"reason": "wrong segment"})
    assert r.status_code == 200
    assert r.json()["change"]["status"] == "rejected"


def test_status_filter(client_and_queue):
    client, dq = client_and_queue
    ids = _seed(dq, 2)
    client.post(f"/api/v1/founder/approvals/{ids[0]}/approve", json={})
    approved = client.get("/api/v1/founder/approvals?status=approved").json()
    assert len(approved["drafts"]) == 1
    assert approved["drafts"][0]["status"] == "approved"


def test_approve_unknown_returns_404(client_and_queue):
    client, _ = client_and_queue
    r = client.post("/api/v1/founder/approvals/does-not-exist/approve", json={})
    assert r.status_code == 404
    assert r.json()["detail"] == "draft_not_found"


def test_reject_unknown_returns_404(client_and_queue):
    client, _ = client_and_queue
    r = client.post("/api/v1/founder/approvals/nope/reject", json={})
    assert r.status_code == 404
