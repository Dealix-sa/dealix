"""
Unit tests for APIKeyMiddleware path policy.

Verifies:
  * /api/v1/pricing/plans is PUBLIC (prospects must see pricing without a key).
  * /api/v1/checkout still requires an API key.
  * Webhooks prefix stays public (signature-verified separately).
"""

from __future__ import annotations

import os

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient

from api.security.api_key import PUBLIC_PATHS, APIKeyMiddleware, verify_api_key


@pytest.fixture()
def app_with_keys(monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    monkeypatch.setenv("API_KEYS", "test-secret-key")
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware)

    @app.get("/api/v1/pricing/plans")
    def plans() -> JSONResponse:
        return JSONResponse({"plans": []})

    @app.post("/api/v1/checkout")
    def checkout() -> JSONResponse:
        return JSONResponse({"ok": True})

    @app.post("/api/v1/webhooks/moyasar")
    def moyasar() -> JSONResponse:
        return JSONResponse({"ok": True})

    return app


@pytest.mark.parametrize(
    ("raw", "valid_key"),
    [
        ("alpha,beta", "beta"),
        ("alpha\nbeta", "beta"),
        ("alpha;beta", "beta"),
        ('["alpha", "beta"]', "beta"),
        ('{"API_KEYS": ["alpha", "beta"]}', "beta"),
        ('{"value": "alpha,beta"}', "beta"),
    ],
)
def test_verify_api_key_accepts_production_secret_shapes(
    monkeypatch: pytest.MonkeyPatch,
    raw: str,
    valid_key: str,
) -> None:
    monkeypatch.setenv("API_KEYS", raw)
    assert verify_api_key(valid_key)


def test_verify_api_key_accepts_dealix_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_KEYS", raising=False)
    monkeypatch.setenv("DEALIX_API_KEY", "alias-secret-key")
    assert verify_api_key("alias-secret-key")


def test_pricing_plans_is_public(app_with_keys: FastAPI) -> None:
    client = TestClient(app_with_keys)
    r = client.get("/api/v1/pricing/plans")
    assert r.status_code == 200, r.text


def test_pricing_plans_in_public_paths_constant() -> None:
    # Regression guard: ensure nobody removes this entry without updating tests.
    assert "/api/v1/pricing/plans" in PUBLIC_PATHS


def test_checkout_requires_api_key(app_with_keys: FastAPI) -> None:
    client = TestClient(app_with_keys)
    r = client.post("/api/v1/checkout", json={})
    assert r.status_code == 401


def test_checkout_accepts_valid_key(app_with_keys: FastAPI) -> None:
    client = TestClient(app_with_keys)
    r = client.post("/api/v1/checkout", json={}, headers={"X-API-Key": "test-secret-key"})
    assert r.status_code == 200


def test_webhook_path_is_public(app_with_keys: FastAPI) -> None:
    client = TestClient(app_with_keys)
    r = client.post("/api/v1/webhooks/moyasar", json={})
    assert r.status_code == 200
