"""The Moyasar webhook must never process the same event twice.

The dedupe was conditional on the event carrying a top-level ``id``::

    event_id = str(body.get("id") or "")
    if event_id and not idem.claim(event_id, ttl_seconds=7 * 86400):
        return {"status": "duplicate", ...}

An event without one skipped the claim entirely, so every provider retry
re-ran the whole success path: a second receipt email to the customer, a
second founder alert, and a second ZATCA e-invoice issued against a single
payment. Moyasar retries whenever it does not receive a 2xx, so a slow
response was enough — this did not need a malformed event, only a late one.

``_dedupe_key`` now always produces a key. These tests pin that, and pin the
part that is easy to get wrong in the other direction: successive status
transitions on one payment are distinct events and must still each be
processed.
"""

from __future__ import annotations

import pytest

WEBHOOK_SECRET = "webhook-secret-under-test"
PATH = "/api/v1/webhooks/moyasar"


@pytest.fixture
def client(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", WEBHOOK_SECRET)
    return TestClient(app)


@pytest.fixture(autouse=True)
def _clean_idempotency_store():
    """The process-local store outlives a test, so clear it around each one."""
    from dealix.reliability import idempotency

    idempotency._LOCAL_STORE.clear()
    yield
    idempotency._LOCAL_STORE.clear()


def _event(**overrides):
    body = {
        "secret_token": WEBHOOK_SECRET,
        "type": "payment_paid",
        "data": {"id": "pay_abc123", "status": "paid", "amount": 49900},
    }
    body.update(overrides)
    return body


# ── The defect ────────────────────────────────────────────────────────────


def test_event_without_top_level_id_is_deduped(client):
    """The regression: no ``id`` used to mean no dedupe at all."""
    body = _event()
    assert "id" not in body

    first = client.post(PATH, json=body)
    second = client.post(PATH, json=body)

    assert first.status_code == 200, first.text
    assert first.json()["status"] != "duplicate"
    assert second.json()["status"] == "duplicate", (
        "a provider retry of an id-less event was processed a second time"
    )


def test_event_with_neither_id_nor_payment_id_is_deduped(client):
    """Weakest case — falls back to hashing the body, still never skips."""
    body = {"secret_token": WEBHOOK_SECRET, "type": "payment_paid"}

    first = client.post(PATH, json=body)
    second = client.post(PATH, json=body)

    assert first.json()["status"] != "duplicate"
    assert second.json()["status"] == "duplicate"


def test_event_with_top_level_id_is_still_deduped(client):
    """The path that already worked must keep working."""
    body = _event(id="evt_00001")

    first = client.post(PATH, json=body)
    second = client.post(PATH, json=body)

    assert first.json()["status"] != "duplicate"
    assert second.json()["status"] == "duplicate"


# ── Not over-deduping ─────────────────────────────────────────────────────


def test_distinct_events_are_not_collapsed(client):
    a = client.post(PATH, json=_event(id="evt_00001"))
    b = client.post(PATH, json=_event(id="evt_00002"))

    assert a.json()["status"] != "duplicate"
    assert b.json()["status"] != "duplicate", "two distinct events were collapsed"


def test_status_transitions_on_one_payment_are_distinct_events(client):
    """A payment moves initiated → paid; swallowing the second loses the sale.

    Both events name the same payment and neither carries a top-level ``id``,
    so the fallback key has to include the status.
    """
    initiated = client.post(
        PATH,
        json=_event(
            type="payment_initiated",
            data={"id": "pay_abc123", "status": "initiated", "amount": 49900},
        ),
    )
    paid = client.post(
        PATH,
        json=_event(
            type="payment_paid",
            data={"id": "pay_abc123", "status": "paid", "amount": 49900},
        ),
    )

    assert initiated.json()["status"] != "duplicate"
    assert paid.json()["status"] != "duplicate", (
        "the paid event was swallowed as a duplicate of the initiated one"
    )


def test_two_payments_sharing_a_status_are_distinct(client):
    a = client.post(PATH, json=_event(data={"id": "pay_aaa", "status": "paid"}))
    b = client.post(PATH, json=_event(data={"id": "pay_bbb", "status": "paid"}))

    assert a.json()["status"] != "duplicate"
    assert b.json()["status"] != "duplicate"


# ── Key construction, without the HTTP stack ──────────────────────────────


def test_dedupe_key_prefers_the_event_id():
    from api.routers.pricing import _dedupe_key

    key = _dedupe_key({"id": "evt_1", "data": {"id": "pay_1", "status": "paid"}})
    assert key == "evt_1"


def test_dedupe_key_falls_back_to_payment_and_status():
    from api.routers.pricing import _dedupe_key

    key = _dedupe_key({"data": {"id": "pay_1", "status": "paid"}})
    assert "pay_1" in key
    assert "paid" in key


def test_dedupe_key_is_never_empty():
    from api.routers.pricing import _dedupe_key

    for body in ({}, {"id": ""}, {"data": {}}, {"data": None}, {"data": "not-a-dict"}):
        assert _dedupe_key(body), f"empty key for {body!r} — dedupe would be skipped"


# ── Signature verification ────────────────────────────────────────────────


def test_wrong_secret_is_rejected(client):
    resp = client.post(PATH, json=_event(secret_token="wrong-secret"))
    assert resp.status_code == 401


def test_unconfigured_secret_rejects_every_event(client, monkeypatch):
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", "")
    resp = client.post(PATH, json=_event())
    assert resp.status_code == 401


def test_non_ascii_secret_token_is_rejected_not_a_server_error(client):
    """``hmac.compare_digest`` raises TypeError on non-ASCII ``str`` inputs.

    ``verify_webhook`` runs before the handler's try block, so the TypeError
    escaped as an unhandled 500 instead of the 401 a bad token deserves.
    """
    resp = client.post(PATH, json=_event(secret_token="رمز-غير-صحيح"))
    assert resp.status_code == 401, resp.text
