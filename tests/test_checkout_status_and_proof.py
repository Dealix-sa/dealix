"""Paid-launch money-path coverage.

B1 — GET /api/v1/checkout/status (post-payment return page source).
B3 — L5 revenue proof event recorded on a real `paid` Moyasar webhook.

Both paths are non-fatal by design; these tests pin the happy + degraded
behaviour so a paying customer's journey can be trusted.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app

# ─── B1: checkout status endpoint ────────────────────────────────────


def test_status_requires_a_reference() -> None:
    resp = TestClient(create_app()).get("/api/v1/checkout/status")
    assert resp.status_code == 400


def test_status_rejects_malformed_reference() -> None:
    # Path-traversal / SSRF-shaped ids must never reach the provider URL.
    client = TestClient(create_app())
    for bad in ["../../admin", "pay id", "x", "a" * 65]:
        resp = client.get("/api/v1/checkout/status", params={"payment_id": bad})
        assert resp.status_code == 400, bad


def test_status_degrades_to_pending_without_provider_or_db(monkeypatch) -> None:
    # No MOYASAR_SECRET_KEY and no DB row → safe "pending" so the page polls.
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)

    async def _no_row(_pid: str):
        return None

    monkeypatch.setattr("api.routers.pricing._lookup_payment_from_db", _no_row)
    resp = TestClient(create_app()).get(
        "/api/v1/checkout/status", params={"payment_id": "pay_unknown"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["state"] == "pending"
    assert body["paid"] is False
    assert body["reference"] == "pay_unknown"


def test_status_paid_via_provider(monkeypatch) -> None:
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_xxx")

    async def _fake_fetch(self, payment_id: str):
        return {"status": "paid", "amount": 49900, "metadata": {"plan": "sprint_499"}}

    monkeypatch.setattr("api.routers.pricing.MoyasarClient.fetch_payment", _fake_fetch)
    resp = TestClient(create_app()).get(
        "/api/v1/checkout/status", params={"payment_id": "pay_live_1"}
    )
    body = resp.json()
    assert body["state"] == "paid"
    assert body["paid"] is True
    assert body["amount_sar"] == 499.0
    assert body["plan"] == "sprint_499"
    # No PII leaked to the browser.
    assert "email" not in body


def test_status_falls_back_to_db_when_no_provider_key(monkeypatch) -> None:
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)

    async def _paid_row(_pid: str):
        return {"status": "paid", "amount_halalas": 150000, "plan": "data_1500"}

    monkeypatch.setattr("api.routers.pricing._lookup_payment_from_db", _paid_row)
    resp = TestClient(create_app()).get(
        "/api/v1/checkout/status", params={"payment_id": "pay_db_1"}
    )
    body = resp.json()
    assert body["state"] == "paid"
    assert body["amount_sar"] == 1500.0
    assert body["plan"] == "data_1500"


# ─── B3: revenue proof event on paid webhook ─────────────────────────


def _webhook_body(status: str) -> dict:
    return {
        "id": f"evt_{status}_1",
        "type": f"payment_{status}",
        "secret_token": "whsec_test",
        "data": {
            "object": "payment",
            "id": "pay_proof_1",
            "status": status,
            "amount": 49900,
            "currency": "SAR",
            "source": {"company": "Test Agency Co"},
            "metadata": {"plan": "sprint_499"},
        },
    }


@pytest.fixture()
def _isolated_ledger(tmp_path, monkeypatch):
    """Point the proof ledger + evidence CSV at tmp so tests don't touch the repo."""
    from auto_client_acquisition.proof_ledger import FileProofLedger

    ledger = FileProofLedger(base_dir=tmp_path / "proof")
    monkeypatch.setattr(
        "auto_client_acquisition.proof_ledger.get_default_ledger", lambda: ledger
    )

    import dealix.commercial_ops.evidence_append as ea

    csv_path = tmp_path / "evidence.csv"
    csv_path.write_text(
        "event_id,event_date,event_type,company,contact,motion,offer_id,owner,"
        "source_channel,notes,next_action,next_action_date,war_room_status\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ea, "EVIDENCE_TRACKER_CSV", csv_path)

    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", "whsec_test")
    monkeypatch.delenv("REDIS_URL", raising=False)  # in-memory idempotency
    return ledger


def test_paid_webhook_records_l5_proof_event(_isolated_ledger, monkeypatch) -> None:
    resp = TestClient(create_app()).post(
        "/api/v1/webhooks/moyasar", json=_webhook_body("paid")
    )
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"

    events = _isolated_ledger.list_events()
    paid_events = [e for e in events if e.event_type == "payment_confirmed"]
    assert len(paid_events) == 1, events
    ev = paid_events[0]
    assert ev.evidence_source == "moyasar://payment/pay_proof_1"
    assert ev.payload.get("evidence_level") == "L5"
    assert ev.payload.get("amount_sar") == 499.0
    # Proof-first doctrine: never auto-published.
    assert ev.consent_for_publication is False


def test_nonpaid_webhook_records_no_proof_event(_isolated_ledger) -> None:
    resp = TestClient(create_app()).post(
        "/api/v1/webhooks/moyasar", json=_webhook_body("failed")
    )
    assert resp.status_code == 200
    events = _isolated_ledger.list_events()
    assert [e for e in events if e.event_type == "payment_confirmed"] == []
