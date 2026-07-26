"""GTM public surfaces registry tests."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import health, platform_meta
from dealix.commercial_ops.gtm_public_surfaces import (
    build_gtm_public_surfaces_snapshot,
    verify_gtm_public_surfaces_repo,
)


def test_gtm_public_surfaces_repo_ok() -> None:
    repo = verify_gtm_public_surfaces_repo()
    assert repo["ok"], repo["issues"]


def test_gtm_public_surfaces_snapshot_has_routes() -> None:
    snap = build_gtm_public_surfaces_snapshot()
    assert len(snap["frontend_public_routes"]) >= 5
    assert len(snap["api_trust_endpoints"]) >= 4


def _trust_layer_app() -> FastAPI:
    """Minimal app — avoids full api.main optional-router import chain."""
    mini = FastAPI()
    mini.include_router(health.router)
    mini.include_router(platform_meta.router)
    return mini


def test_version_and_meta_public() -> None:
    client = TestClient(_trust_layer_app())
    ver = client.get("/version")
    assert ver.status_code == 200
    body = ver.json()
    assert body["status"] == "ok"
    assert "version" in body

    meta = client.get("/api/v1/meta")
    assert meta.status_code == 200
    assert "surfaces" in meta.json()


def test_healthz_is_a_minimal_liveness_payload() -> None:
    """/healthz answers liveness only; identity lives at /version.

    This previously asserted that /healthz returns a "version" field, which
    production never did. ``_trust_layer_app`` above includes health.router
    before platform_meta.router — the reverse of api/main.py — so the test app
    resolved /healthz to a richer implementation that the real app always
    shadowed. It also contradicted
    ``test_health_deep::test_healthz_default_is_simple``, which pins the
    minimal shape; both passed only because they built different apps.

    The duplicate definition has since been removed, so this now asserts the
    contract Railway's healthcheck actually receives.
    """
    client = TestClient(_trust_layer_app())

    hz = client.get("/healthz")

    assert hz.status_code == 200
    body = hz.json()
    assert body["status"] == "ok"
    assert body["service"] == "dealix"
    assert "version" not in body, (
        "/healthz must stay a low-latency liveness probe — version and build "
        "identity belong to /version (see test_version_and_meta_public)."
    )
