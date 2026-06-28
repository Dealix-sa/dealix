"""Tests for outbound safety status endpoint."""

import os

from fastapi.testclient import TestClient

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dealix_test_safety.db")
os.environ.setdefault("APP_SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("API_KEYS", "test")
os.environ.setdefault("ADMIN_API_KEYS", "admin")
os.environ.setdefault("EXTERNAL_SEND_ENABLED", "false")
os.environ.setdefault("OUTBOUND_MODE", "draft_only")

from api.main import app

client = TestClient(app, raise_server_exceptions=False)


class TestOutboundSafetyStatus:
    def test_safety_endpoint_exists(self):
        response = client.get("/api/outbound/safety")
        assert response.status_code == 200

    def test_safety_defaults_to_false(self):
        response = client.get("/api/outbound/safety")
        data = response.json()
        assert data["external_send_enabled"] is False
        assert data["outbound_mode"] == "draft_only"
        assert data["safe_to_send"] is False

    def test_safety_has_all_channels(self):
        response = client.get("/api/outbound/safety")
        data = response.json()
        assert "email_send_enabled" in data
        assert "whatsapp_send_enabled" in data
        assert "whatsapp_allow_live_send" in data
        assert "sms_send_enabled" in data

    def test_api_status_shows_safety(self):
        response = client.get("/api/status")
        data = response.json()
        assert data["external_send_enabled"] is False
        assert data["outbound_mode"] == "draft_only"
