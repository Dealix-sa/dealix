"""A checkout retry must return the same invoice, not mint a second one.

``POST /api/v1/checkout`` created a Moyasar invoice on every call. A retry is
ordinary — the customer double-clicks, or their connection drops after Moyasar
answered but before the response landed — and each attempt produced another
invoice against the same buyer and plan.

Refusing the retry with 409 would be worse than the bug: it stops someone
paying after a network blip, which costs more than a stray unpaid invoice that
expires. So the fix has to *answer* the duplicate with the original result,
which needs a store that returns a value.

``IdempotencyStore`` only had ``claim``/``seen``/``mark`` — flags. That is
enough to **drop** a duplicate, which is what the Moyasar webhook wants, and
not enough to **answer** one. ``remember``/``recall`` were added for this.
"""

from __future__ import annotations

import pytest

PATH = "/api/v1/checkout"
PLAN = "growth"
BUYER = "buyer@example.com"


@pytest.fixture(autouse=True)
def _clean_stores():
    from dealix.reliability import idempotency

    idempotency._LOCAL_STORE.clear()
    idempotency._LOCAL_VALUES.clear()
    yield
    idempotency._LOCAL_STORE.clear()
    idempotency._LOCAL_VALUES.clear()


@pytest.fixture
def approved_plans(monkeypatch):
    """Two sellable plans.

    `ALLOWED_PLANS` is **empty** on main: #996 made every offering quote-only
    (`commercial_status != "public_approved"`), so checkout sells nothing
    today by design. That gate has its own tests
    (`test_pricing_catalog_fail_closed.py`); what is under test here is what
    happens once a plan *is* approved, so the allowlist is widened rather
    than the gate bypassed.
    """
    from api.routers import pricing

    assert PLAN in pricing.PLANS, f"{PLAN} vanished from the catalogue"
    monkeypatch.setattr(pricing, "ALLOWED_PLANS", frozenset({PLAN, "scale"}))


@pytest.fixture
def client(monkeypatch, approved_plans):
    from fastapi.testclient import TestClient

    from api.main import app

    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "1")
    monkeypatch.setenv("APP_URL", "https://api.dealix.me")
    return TestClient(app)


@pytest.fixture
def moyasar(monkeypatch):
    """Counts invoice creations, so a duplicate is visible."""
    from api.routers import pricing

    calls: list[dict] = []

    class _Client:
        async def create_invoice(self, **kwargs):
            calls.append(kwargs)
            return {
                "id": f"inv_{len(calls)}",
                "status": "initiated",
                "url": f"https://moyasar.test/pay/{len(calls)}",
            }

    monkeypatch.setattr(pricing, "MoyasarClient", _Client)
    return calls


def _order(**overrides) -> dict:
    body = {"plan": PLAN, "email": BUYER}
    body.update(overrides)
    return body


# ── The defect ────────────────────────────────────────────────────────────


def test_a_retry_returns_the_first_invoice(client, moyasar):
    first = client.post(PATH, json=_order())
    second = client.post(PATH, json=_order())

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert len(moyasar) == 1, f"a retry minted a second invoice: {len(moyasar)} created"
    assert second.json()["invoice_id"] == first.json()["invoice_id"]
    assert second.json()["payment_url"] == first.json()["payment_url"]


def test_the_replay_is_labelled(client, moyasar):
    client.post(PATH, json=_order())
    replay = client.post(PATH, json=_order())

    assert replay.json()["idempotent_replay"] is True


def test_the_first_response_is_not_labelled_a_replay(client, moyasar):
    first = client.post(PATH, json=_order())

    assert "idempotent_replay" not in first.json()


def test_a_retry_is_not_refused(client, moyasar):
    """409 would stop a customer paying — worse than the duplicate it fixes."""
    client.post(PATH, json=_order())
    retry = client.post(PATH, json=_order())

    assert retry.status_code == 200, (
        f"the retry was refused instead of answered: {retry.status_code}"
    )


# ── Not over-deduplicating ────────────────────────────────────────────────


def test_a_different_buyer_gets_their_own_invoice(client, moyasar):
    client.post(PATH, json=_order())
    other = client.post(PATH, json=_order(email="someone.else@example.com"))

    assert len(moyasar) == 2, "a second buyer was answered with the first one's invoice"
    assert other.json()["invoice_id"] == "inv_2"


def test_a_different_plan_gets_its_own_invoice(client, moyasar):
    client.post(PATH, json=_order())
    other = client.post(PATH, json=_order(plan="scale"))

    assert len(moyasar) == 2
    assert other.json()["invoice_id"] == "inv_2"


def test_an_explicit_idempotency_key_scopes_the_window(client, moyasar):
    """A client that wants two genuine orders can say so."""
    first = client.post(PATH, json=_order(idempotency_key="order-1"))
    second = client.post(PATH, json=_order(idempotency_key="order-2"))
    repeat = client.post(PATH, json=_order(idempotency_key="order-1"))

    assert len(moyasar) == 2, "distinct keys were collapsed into one invoice"
    assert repeat.json()["invoice_id"] == first.json()["invoice_id"]
    assert second.json()["invoice_id"] != first.json()["invoice_id"]


def test_the_email_is_matched_case_insensitively(client, moyasar):
    """`Buyer@` and `buyer@` are the same person placing the same order."""
    client.post(PATH, json=_order())
    again = client.post(PATH, json=_order(email=BUYER.upper()))

    assert len(moyasar) == 1
    assert again.json()["idempotent_replay"] is True


@pytest.mark.parametrize(
    "changed",
    [
        {"email": "someone.else@example.com"},
        {"plan": "scale"},
    ],
)
def test_client_key_cannot_replay_another_order(client, moyasar, changed):
    """A reused caller key must never disclose another order's invoice."""
    first = client.post(PATH, json=_order(idempotency_key="shared-client-key"))
    other = client.post(
        PATH,
        json=_order(idempotency_key="shared-client-key", **changed),
    )

    assert first.status_code == 200, first.text
    assert other.status_code == 200, other.text
    assert len(moyasar) == 2
    assert other.json()["invoice_id"] != first.json()["invoice_id"]
    assert other.json()["payment_url"] != first.json()["payment_url"]


# ── The guards in front of it still fire ──────────────────────────────────


def test_nothing_is_remembered_when_checkout_is_not_approved(client, monkeypatch, moyasar):
    monkeypatch.delenv("DEALIX_CHECKOUT_ENABLED", raising=False)

    resp = client.post(PATH, json=_order())

    assert resp.status_code == 503
    assert resp.json()["detail"] == "checkout_not_founder_approved"
    assert not moyasar


def test_an_invalid_email_is_still_rejected(client, moyasar):
    resp = client.post(PATH, json=_order(email="not-an-email"))

    assert resp.status_code == 400
    assert not moyasar


def test_a_provider_failure_is_not_remembered_as_success(client, monkeypatch):
    """A failed attempt must not poison the key and block the real retry."""
    from api.routers import pricing

    calls: list[int] = []

    class _Flaky:
        async def create_invoice(self, **kwargs):
            calls.append(1)
            if len(calls) == 1:
                raise RuntimeError("moyasar down")
            return {
                "id": "inv_after_recovery",
                "status": "initiated",
                "url": "https://moyasar.test/pay/ok",
            }

    monkeypatch.setattr(pricing, "MoyasarClient", _Flaky)

    failed = client.post(PATH, json=_order())
    recovered = client.post(PATH, json=_order())

    assert failed.status_code == 502
    assert recovered.status_code == 200, (
        "the failed attempt was remembered, so the customer could never retry"
    )
    assert recovered.json()["invoice_id"] == "inv_after_recovery"


# ── The store primitive ───────────────────────────────────────────────────


def test_remember_and_recall_round_trip():
    from dealix.reliability.idempotency import IdempotencyStore

    store = IdempotencyStore(prefix="test:checkout:")
    assert store.recall("k") is None

    store.remember("k", {"invoice_id": "inv_1"}, ttl_seconds=60)

    assert store.recall("k") == {"invoice_id": "inv_1"}


def test_recall_of_an_unknown_key_is_none_not_an_error():
    from dealix.reliability.idempotency import IdempotencyStore

    assert IdempotencyStore(prefix="test:checkout:").recall("never-written") is None


def test_value_memory_is_separate_from_the_claim_flag():
    """`claim` must not start answering, and `remember` must not start dropping."""
    from dealix.reliability.idempotency import IdempotencyStore

    store = IdempotencyStore(prefix="test:checkout:")
    store.remember("shared", {"v": 1}, ttl_seconds=60)

    assert store.claim("shared", ttl_seconds=60) is True, (
        "remembering a value consumed the claim — the webhook dedupe would "
        "start dropping first-time events"
    )
    assert store.recall("shared") == {"v": 1}
