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

from api.main import app  # noqa: E402

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