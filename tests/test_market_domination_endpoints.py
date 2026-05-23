"""Tests for the Dealix Market Domination internal endpoints.

Verifies the four read-only summary endpoints exist, return well-shaped
payloads, and explicitly carry ``source=fallback`` until the runtime
ledgers are wired. Also confirms the router mounts under the expected
``/api/v1/internal`` prefix so downstream gating layers can locate it.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _client() -> TestClient:
    from api.main import app

    return TestClient(app)


def test_market_domination_router_is_registered() -> None:
    from api.main import app

    paths = {route.path for route in app.routes}
    assert "/api/v1/internal/brand/summary" in paths
    assert "/api/v1/internal/growth/targeting" in paths
    assert "/api/v1/internal/marketing/summary" in paths
    assert "/api/v1/internal/product/distribution" in paths


def test_brand_summary_payload_shape() -> None:
    resp = _client().get("/api/v1/internal/brand/summary")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source"] == "fallback"
    brand = body["brand"]
    assert brand["wordmark"] == "DEALIX"
    assert brand["tagline_en"] == "Intelligent Deals. Real Growth."
    assert brand["colors"]["deep_navy"] == "#0B1220"
    assert brand["colors"]["emerald_teal"] == "#00D1A1"
    assert {"Built on Trust", "Driven by Growth"}.issubset(set(brand["pillars"]))
    assert body["assets"]["favicon_svg"].endswith("favicon.svg")


def test_growth_targeting_payload_shape() -> None:
    resp = _client().get("/api/v1/internal/growth/targeting")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source"] == "fallback"
    sectors = body["sectors"]
    assert len(sectors) == 8
    assert sectors[0]["rank"] == 1
    assert set(body["tier_distribution"].keys()) == {"A", "B", "C", "D"}


def test_marketing_summary_payload_shape() -> None:
    resp = _client().get("/api/v1/internal/marketing/summary")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source"] == "fallback"
    assert "slots_next_7d" in body["calendar"]
    surfaces = {s["surface"] for s in body["surfaces"]}
    assert {"linkedin", "sector_pulse", "case_study", "landing"}.issubset(surfaces)


def test_product_distribution_payload_shape() -> None:
    resp = _client().get("/api/v1/internal/product/distribution")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source"] == "fallback"
    rungs = [r["rung"] for r in body["ladder"]]
    assert rungs == [1, 2, 3, 4, 5, 6, 7]
    guardrails = body["guardrails"]
    assert guardrails["no_guaranteed_claims"] is True
    assert guardrails["trust_gated_external_actions"] is True


def test_endpoints_are_read_only_and_do_not_mutate_state() -> None:
    client = _client()
    for path in (
        "/api/v1/internal/brand/summary",
        "/api/v1/internal/growth/targeting",
        "/api/v1/internal/marketing/summary",
        "/api/v1/internal/product/distribution",
    ):
        post_status = client.post(path).status_code
        put_status = client.put(path).status_code
        delete_status = client.delete(path).status_code
        assert post_status in (404, 405, 422)
        assert put_status in (404, 405, 422)
        assert delete_status in (404, 405, 422)
