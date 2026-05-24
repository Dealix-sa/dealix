"""Tap.company client + webhook verification tests (no live keys)."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dealix.payments.tap import TapClient, _hashstring_from_body, verify_webhook


# ─────────────────────────── TapClient.create_charge ──────────────────────────


@pytest.mark.asyncio
async def test_create_charge_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_SECRET_KEY", "sk_test_xyz")

    fake_response: dict[str, Any] = {
        "id": "chg_TS01A000001",
        "status": "INITIATED",
        "amount": 99.0,
        "currency": "SAR",
        "transaction": {"url": "https://checkout.tap.company/redirect/abc"},
    }
    mock_resp = MagicMock()
    mock_resp.json = MagicMock(return_value=fake_response)
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.post = AsyncMock(return_value=mock_resp)

    with patch("dealix.payments.tap.httpx.AsyncClient", return_value=mock_client):
        client = TapClient()
        result = await client.create_charge(
            amount=99.0,
            currency="SAR",
            description="Dealix — Starter",
            callback_url="https://dealix.sa/checkout/return",
            metadata={"plan": "starter", "lead_id": "L1"},
            customer={"email": "ops@example.com", "first_name": "Ops"},
        )

    assert result["id"] == "chg_TS01A000001"
    assert result["transaction"]["url"].startswith("https://checkout.tap.company/")

    # Confirm the correct endpoint, auth, and amount-as-major-units shape.
    call_kwargs = mock_client.post.call_args
    args, kwargs = call_kwargs
    assert args[0].endswith("/v2/charges")
    sent_headers = kwargs["headers"]
    assert sent_headers["Authorization"] == "Bearer sk_test_xyz"
    sent_json = kwargs["json"]
    assert sent_json["amount"] == 99.0  # major units, not halalas
    assert sent_json["currency"] == "SAR"
    assert sent_json["metadata"]["plan"] == "starter"


@pytest.mark.asyncio
async def test_create_charge_missing_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TAP_SECRET_KEY", raising=False)
    client = TapClient(secret_key="")
    with pytest.raises(RuntimeError, match="TAP_SECRET_KEY not set"):
        await client.create_charge(amount=10.0)


@pytest.mark.asyncio
async def test_create_charge_rejects_unsupported_currency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TAP_SECRET_KEY", "sk_test_xyz")
    client = TapClient()
    with pytest.raises(ValueError, match="unsupported_currency"):
        await client.create_charge(amount=10.0, currency="EUR")


@pytest.mark.asyncio
async def test_create_charge_rejects_non_positive_amount(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TAP_SECRET_KEY", "sk_test_xyz")
    client = TapClient()
    with pytest.raises(ValueError, match="amount must be > 0"):
        await client.create_charge(amount=0)


# ─────────────────────────── TapClient.fetch_charge ───────────────────────────


@pytest.mark.asyncio
async def test_fetch_charge_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_SECRET_KEY", "sk_test_xyz")
    fake = {"id": "chg_1", "status": "CAPTURED"}
    mock_resp = MagicMock()
    mock_resp.json = MagicMock(return_value=fake)
    mock_resp.raise_for_status = MagicMock()
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("dealix.payments.tap.httpx.AsyncClient", return_value=mock_client):
        client = TapClient()
        out = await client.fetch_charge("chg_1")
    assert out == fake
    args, _ = mock_client.get.call_args
    assert args[0].endswith("/v2/charges/chg_1")


@pytest.mark.asyncio
async def test_fetch_charge_missing_id_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_SECRET_KEY", "sk_test_xyz")
    client = TapClient()
    with pytest.raises(ValueError, match="charge_id required"):
        await client.fetch_charge("")


# ─────────────────────────── verify_webhook ───────────────────────────────────


def _signed(body: dict[str, Any], secret: str) -> str:
    hashstring = _hashstring_from_body(body)
    return hmac.new(secret.encode("utf-8"), hashstring.encode("utf-8"), hashlib.sha256).hexdigest()


def test_verify_webhook_accepts_matching_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_WEBHOOK_SECRET", "whsec_tap_xyz")
    body: dict[str, Any] = {
        "id": "chg_1",
        "amount": 99.0,
        "currency": "SAR",
        "status": "CAPTURED",
        "reference": {"gateway": "g1", "payment": "p1"},
        "transaction": {"created": 1700000000},
    }
    sig = _signed(body, "whsec_tap_xyz")
    assert verify_webhook(body, sig) is True


def test_verify_webhook_rejects_wrong_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_WEBHOOK_SECRET", "whsec_tap_xyz")
    body = {"id": "chg_1", "amount": 99.0, "currency": "SAR", "status": "CAPTURED"}
    assert verify_webhook(body, "deadbeef" * 8) is False


def test_verify_webhook_rejects_missing_header(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAP_WEBHOOK_SECRET", "whsec_tap_xyz")
    body = {"id": "chg_1", "amount": 99.0, "currency": "SAR", "status": "CAPTURED"}
    assert verify_webhook(body, None) is False


def test_verify_webhook_rejects_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TAP_WEBHOOK_SECRET", raising=False)
    body = {"id": "chg_1"}
    assert verify_webhook(body, "anything") is False


def test_verify_webhook_explicit_secret_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Caller-provided secret must take precedence over env."""
    monkeypatch.setenv("TAP_WEBHOOK_SECRET", "env-secret")
    body = {"id": "chg_2", "amount": 50.0, "currency": "SAR", "status": "CAPTURED"}
    sig = _signed(body, "explicit-secret")
    assert verify_webhook(body, sig, expected_secret="explicit-secret") is True
    assert verify_webhook(body, sig) is False  # env mismatch
