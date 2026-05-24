"""Tests for InternalTokenMiddleware and /api/v1/internal/ceo/summary.

Validates the dual-token contract:

  - Dev mode without credentials: pass-through (allows local development).
  - Production with credentials: requires either X-Dealix-Internal-Token
    (matched against DEALIX_INTERNAL_TOKEN) or X-API-Key (matched against
    one of ADMIN_API_KEYS).
  - Unauthenticated requests in production return 403.
"""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from api.middleware.internal_token import InternalTokenMiddleware
from core.config.settings import get_settings


def _make_app() -> FastAPI:
    """Minimal FastAPI app mounting the middleware + one internal route."""
    app = FastAPI()
    app.add_middleware(InternalTokenMiddleware)

    @app.get("/api/v1/internal/ceo/summary")
    async def summary() -> JSONResponse:
        return JSONResponse({"ok": True})

    @app.get("/healthz")
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return app


def test_healthz_is_public(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok-123")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get("/healthz")
        assert r.status_code == 200
    finally:
        get_settings.cache_clear()


def test_internal_requires_token_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok-123")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get("/api/v1/internal/ceo/summary")
        assert r.status_code == 403
        assert "internal_token_required" in r.text
    finally:
        get_settings.cache_clear()


def test_internal_accepts_x_dealix_internal_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok-abc")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get(
            "/api/v1/internal/ceo/summary",
            headers={"X-Dealix-Internal-Token": "tok-abc"},
        )
        assert r.status_code == 200
        assert r.json() == {"ok": True}
    finally:
        get_settings.cache_clear()


def test_internal_accepts_admin_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "admin-k1,admin-k2")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get(
            "/api/v1/internal/ceo/summary",
            headers={"X-API-Key": "admin-k2"},
        )
        assert r.status_code == 200
    finally:
        get_settings.cache_clear()


def test_internal_rejects_wrong_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok-right")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get(
            "/api/v1/internal/ceo/summary",
            headers={"X-Dealix-Internal-Token": "tok-wrong"},
        )
        assert r.status_code == 403
    finally:
        get_settings.cache_clear()


def test_dev_mode_pass_through_when_no_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r = client.get("/api/v1/internal/ceo/summary")
        assert r.status_code == 200, "dev with no credentials must pass through"
    finally:
        get_settings.cache_clear()


def test_dev_mode_still_enforces_when_credentials_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok-dev")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    get_settings.cache_clear()
    try:
        client = TestClient(_make_app())
        r_bad = client.get("/api/v1/internal/ceo/summary")
        assert r_bad.status_code == 403
        r_ok = client.get(
            "/api/v1/internal/ceo/summary",
            headers={"X-Dealix-Internal-Token": "tok-dev"},
        )
        assert r_ok.status_code == 200
    finally:
        get_settings.cache_clear()
