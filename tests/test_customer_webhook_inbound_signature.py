"""Inbound customer-webhook HMAC-SHA256 signature verification.

Asserts constant-time signature checking on the inbound endpoint:
  - valid signature passes,
  - invalid signature is rejected with 401 in strict (production) env,
  - missing signature is rejected with 401 in strict env,
  - unconfigured secret stays permissive (no hard-fail).

The secret and signature values are never asserted via logs.
"""
from __future__ import annotations

import hashlib
import hmac

import pytest
from httpx import ASGITransport, AsyncClient

from api.routers.customer_webhooks import (
    SIGNATURE_HEADER,
    verify_inbound_signature,
)
from core.config.settings import get_settings

SECRET = "unit-test-inbound-secret"
INBOUND_URL = "/api/v1/customer-webhooks/inbound"


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def _sign(body: bytes, secret: str = SECRET) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


# ── Pure helper ─────────────────────────────────────────────────────

def test_verify_inbound_signature_accepts_valid() -> None:
    body = b'{"event":"lead.created"}'
    assert verify_inbound_signature(secret=SECRET, body=body, signature=_sign(body)) is True


def test_verify_inbound_signature_accepts_sha256_prefix() -> None:
    body = b'{"event":"lead.created"}'
    assert verify_inbound_signature(
        secret=SECRET, body=body, signature="sha256=" + _sign(body)
    ) is True


def test_verify_inbound_signature_rejects_tampered_body() -> None:
    sig = _sign(b"original")
    assert verify_inbound_signature(secret=SECRET, body=b"tampered", signature=sig) is False


def test_verify_inbound_signature_rejects_missing_inputs() -> None:
    assert verify_inbound_signature(secret="", body=b"x", signature=_sign(b"x")) is False
    assert verify_inbound_signature(secret=SECRET, body=b"x", signature=None) is False


# ── Endpoint behaviour ──────────────────────────────────────────────

async def _post(app, body: bytes, headers: dict[str, str] | None = None):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.post(INBOUND_URL, content=body, headers=headers or {})


@pytest.mark.asyncio
async def test_inbound_accepts_valid_signature_in_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CUSTOMER_WEBHOOK_SECRET", SECRET)
    get_settings.cache_clear()
    from api.main import create_app

    app = create_app()
    body = b'{"event":"payment.received","amount":100}'
    res = await _post(app, body, {SIGNATURE_HEADER: _sign(body)})
    assert res.status_code == 200
    payload = res.json()
    assert payload["status"] == "accepted"
    assert payload["signature_verified"] is True


@pytest.mark.asyncio
async def test_inbound_rejects_invalid_signature_in_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CUSTOMER_WEBHOOK_SECRET", SECRET)
    get_settings.cache_clear()
    from api.main import create_app

    app = create_app()
    body = b'{"event":"payment.received"}'
    res = await _post(app, body, {SIGNATURE_HEADER: "sha256=deadbeef"})
    assert res.status_code == 401
    assert res.json()["detail"] == "missing_or_invalid_signature"


@pytest.mark.asyncio
async def test_inbound_rejects_missing_signature_in_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CUSTOMER_WEBHOOK_SECRET", SECRET)
    get_settings.cache_clear()
    from api.main import create_app

    app = create_app()
    res = await _post(app, b'{"event":"x"}', {})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_inbound_permissive_when_secret_unconfigured(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("CUSTOMER_WEBHOOK_SECRET", raising=False)
    get_settings.cache_clear()
    from api.main import create_app

    app = create_app()
    # No secret configured -> do not hard-fail (warn-only), even in prod.
    res = await _post(app, b'{"event":"x"}', {})
    assert res.status_code == 200
    assert res.json()["signature_verified"] is False
