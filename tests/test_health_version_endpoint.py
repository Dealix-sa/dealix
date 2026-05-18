"""Health router exposes /version for production smoke tests (isolated app)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.health import router


def test_version_endpoint_returns_deploy_identity():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "dealix-api"
    assert "version" in body
    assert body["health"] == "/healthz"
