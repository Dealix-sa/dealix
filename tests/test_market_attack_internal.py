"""Tests for the Market Attack & Scaling internal endpoints.

Covers all five admin-gated read-only endpoints exposed by
`api/routers/market_attack_internal.py`. The router reads from the
in-repo bootstrap CSVs as a fallback when `$PRIVATE_OPS` is not set,
so these tests run deterministically in CI without any external state.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


ADMIN_KEY = "test_admin_market_attack"

ENDPOINTS = (
    "/api/v1/internal/market-attack/summary",
    "/api/v1/internal/campaigns/summary",
    "/api/v1/internal/partners/pipeline",
    "/api/v1/internal/sales-assets/summary",
    "/api/v1/internal/authority/queue",
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture(autouse=True)
def _set_admin_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    # Force the router to use the bootstrap fallback (no live private ops).
    monkeypatch.delenv("PRIVATE_OPS", raising=False)


def _auth_headers() -> dict[str, str]:
    return {"X-Admin-API-Key": ADMIN_KEY}


@pytest.mark.parametrize("path", ENDPOINTS)
def test_endpoints_require_admin_key(client: TestClient, path: str) -> None:
    resp = client.get(path)
    # Without ADMIN_API_KEYS configured this would 200; with a key set it
    # must reject anonymous callers.
    assert resp.status_code in (401, 403)


def test_market_attack_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/market-attack/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "beachhead",
        "p0Count",
        "p1Count",
        "openObjections",
        "highFrequencyObjections",
        "activeT0AndT1Accounts",
    ):
        assert key in body, f"missing key: {key}"
    assert body["source"] in ("api", "fallback")
    # The seeded fallback has at least one P0 sector (construction, score 38).
    assert body["p0Count"] >= 1
    assert body["beachhead"] is not None
    assert body["beachhead"]["priority"] == "P0"


def test_campaigns_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/campaigns/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "campaignsByStatus",
        "queueByStatus",
        "assetsPendingApproval",
        "results",
    ):
        assert key in body, f"missing key: {key}"
    assert isinstance(body["campaignsByStatus"], dict)
    assert isinstance(body["queueByStatus"], dict)
    for k in (
        "impressions",
        "clicks",
        "replies",
        "positiveReplies",
        "samples",
        "proposals",
        "payments",
    ):
        assert k in body["results"]
        assert isinstance(body["results"][k], int)


def test_partners_pipeline_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/partners/pipeline", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "byType",
        "byStatus",
        "highReferralPartners",
        "whiteLabelCandidates",
    ):
        assert key in body
    # Bootstrap seed contains agency / erp_crm / cybersecurity_grc.
    assert "agency" in body["byType"]
    assert "erp_crm" in body["byType"]


def test_sales_assets_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/sales-assets/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "total",
        "byType",
        "byApprovalStatus",
        "championAssets",
    ):
        assert key in body
    assert body["total"] >= 1
    assert body["championAssets"] >= 0
    # Bootstrap seed has at least the one_pager + proposal types.
    assert "one_pager" in body["byType"]


def test_authority_queue_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/authority/queue", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "postsPending",
        "postsApproved",
        "insightsValidated",
        "reportIdeas",
    ):
        assert key in body
    assert body["postsPending"] + body["postsApproved"] >= 0
    assert body["reportIdeas"] >= 0


def test_no_endpoint_returns_5xx(client: TestClient) -> None:
    """The router must never crash on missing inputs; the fallback path
    is the contract."""
    for path in ENDPOINTS:
        resp = client.get(path, headers=_auth_headers())
        assert resp.status_code < 500, (
            f"{path} returned {resp.status_code}: {resp.text[:200]}"
        )
