"""Tests for API health endpoints: /healthz, /readyz, /livez, /api/status."""

import os

import pytest
from fastapi.testclient import TestClient

# Set safe env before importing app
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dealix_test_health.db")
os.environ.setdefault("APP_SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("API_KEYS", "test")
os.environ.setdefault("ADMIN_API_KEYS", "admin")
os.environ.setdefault("EXTERNAL_SEND_ENABLED", "false")
os.environ.setdefault("OUTBOUND_MODE", "draft_only")

from api.main import app

client = TestClient(app, raise_server_exceptions=False)


class TestHealthEndpoints:
    def test_healthz_returns_ok(self):
        response = client.get("/healthz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "dealix"

    def test_readyz_returns_ready(self):
        response = client.get("/readyz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_livez_returns_alive(self):
        response = client.get("/livez")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_ready_returns_ready(self):
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_live_returns_alive(self):
        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_api_status_returns_operational(self):
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert "external_send_enabled" in data
        assert "outbound_mode" in data

    def test_openapi_health_routes_match_what_actually_runs(self):
        """api/routers/health.py's /health, /ready, /live are shadowed at
        runtime by platform_meta.router (registered first in api.main). They
        must stay include_in_schema=False so /openapi.json never documents a
        response shape (e.g. HealthResponse with `providers`) that the live
        endpoint doesn't actually return — see api/routers/health.py comments.
        """
        schema = app.openapi()
        for path in ("/health", "/ready", "/live"):
            assert path not in schema["paths"], (
                f"{path} reappeared in the OpenAPI schema — if health.py's handler "
                "is now reachable, drop include_in_schema=False; otherwise this is "
                "a docs/reality mismatch regression"
            )
        # Confirm the schema omission isn't hiding a live behavior change.
        live = client.get("/health").json()
        assert "providers" not in live
