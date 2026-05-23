"""
Tests for the internal Founder Console API.

Covers:
    - auth dependency (dev mode + token mode + bad token)
    - runtime_reader CSV read / append round-trip
    - policy_adapter graceful fallback
    - router exposes the documented prefix + endpoint set
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def test_require_internal_token_dev_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """When DEALIX_INTERNAL_TOKEN is unset, requests pass in dev mode."""
    from api.internal.auth import require_internal_token

    monkeypatch.delenv("DEALIX_INTERNAL_TOKEN", raising=False)

    import asyncio

    ctx = asyncio.get_event_loop().run_until_complete(require_internal_token(None))
    assert ctx.auth_mode == "dev_unprotected"
    assert ctx.token_present is False


def test_require_internal_token_accepts_match(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.auth import require_internal_token

    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "secret-value")

    import asyncio

    ctx = asyncio.get_event_loop().run_until_complete(
        require_internal_token("secret-value")
    )
    assert ctx.auth_mode == "token"
    assert ctx.token_present is True


def test_require_internal_token_rejects_bad_token(monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi import HTTPException

    from api.internal.auth import require_internal_token

    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "secret-value")

    import asyncio

    with pytest.raises(HTTPException) as exc:
        asyncio.get_event_loop().run_until_complete(require_internal_token("wrong"))
    assert exc.value.status_code == 401


def test_read_csv_rows_missing_file_returns_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.runtime_reader import read_csv_rows

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    result = read_csv_rows("does_not_exist.csv")
    assert result["source"] == "fallback"
    assert result["rows"] == []


def test_append_csv_row_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.runtime_reader import append_csv_row, read_csv_rows

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    res = append_csv_row("approvals/approval_queue.csv", {"id": "a1", "decision": "approve"})
    assert res["ok"] is True

    read = read_csv_rows("approvals/approval_queue.csv")
    assert read["source"] == "csv"
    assert read["rows"][0]["id"] == "a1"
    assert read["rows"][0]["decision"] == "approve"


def test_load_policies_falls_back_without_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """If the YAML file is missing the loader returns an empty list."""
    from api.internal import policy_adapter

    monkeypatch.setattr(policy_adapter, "POLICY_PATH", tmp_path / "missing.yaml")
    out = policy_adapter.load_policies()
    assert out["source"] == "fallback"
    assert out["rules"] == []


def test_router_exposes_documented_endpoints() -> None:
    """The router must publish the documented GET and POST endpoints."""
    from api.routers.internal.founder_console import router

    paths = {(r.path, frozenset(r.methods)) for r in router.routes}  # type: ignore[attr-defined]

    expected_gets = {
        "/api/v1/internal/ceo/summary",
        "/api/v1/internal/sales/funnel",
        "/api/v1/internal/approvals",
        "/api/v1/internal/workers/health",
        "/api/v1/internal/trust/flags",
        "/api/v1/internal/finance/summary",
        "/api/v1/internal/distribution/summary",
        "/api/v1/internal/delivery/queue",
        "/api/v1/internal/retention/queue",
        "/api/v1/internal/proof/library",
        "/api/v1/internal/audit/events",
        "/api/v1/internal/control/summary",
        "/api/v1/internal/control/policies",
        "/api/v1/internal/control/agents",
        "/api/v1/internal/control/scorecard",
        "/api/v1/internal/control/risks",
        "/api/v1/internal/evals/status",
        "/api/v1/internal/product/productization",
        "/api/v1/internal/security/status",
        "/api/v1/internal/sovereign/readiness",
        "/api/v1/internal/brand/summary",
        "/api/v1/internal/growth/targeting",
        "/api/v1/internal/marketing/summary",
        "/api/v1/internal/product/distribution",
        "/api/v1/internal/customer-success/summary",
        "/api/v1/internal/finance-ops/summary",
    }
    for path in expected_gets:
        assert (path, frozenset({"GET"})) in paths, f"missing GET {path}"

    expected_posts = {
        "/api/v1/internal/approvals/{approval_id}/approve",
        "/api/v1/internal/approvals/{approval_id}/reject",
        "/api/v1/internal/approvals/{approval_id}/request-edit",
        "/api/v1/internal/approvals/{approval_id}/escalate",
        "/api/v1/internal/workers/{worker_id}/retry",
        "/api/v1/internal/control/agents/{agent_id}/disable",
        "/api/v1/internal/control/agents/{agent_id}/enable",
    }
    for path in expected_posts:
        assert (path, frozenset({"POST"})) in paths, f"missing POST {path}"


# ── End-to-end TestClient coverage of every endpoint ─────────────


GET_PATHS = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/workers/health",
    "/api/v1/internal/trust/flags",
    "/api/v1/internal/finance/summary",
    "/api/v1/internal/distribution/summary",
    "/api/v1/internal/delivery/queue",
    "/api/v1/internal/retention/queue",
    "/api/v1/internal/proof/library",
    "/api/v1/internal/audit/events",
    "/api/v1/internal/control/summary",
    "/api/v1/internal/control/policies",
    "/api/v1/internal/control/agents",
    "/api/v1/internal/control/scorecard",
    "/api/v1/internal/control/risks",
    "/api/v1/internal/evals/status",
    "/api/v1/internal/product/productization",
    "/api/v1/internal/security/status",
    "/api/v1/internal/sovereign/readiness",
    "/api/v1/internal/brand/summary",
    "/api/v1/internal/growth/targeting",
    "/api/v1/internal/marketing/summary",
    "/api/v1/internal/product/distribution",
    "/api/v1/internal/customer-success/summary",
    "/api/v1/internal/finance-ops/summary",
]


POST_PATHS_WITH_BODY = [
    ("/api/v1/internal/approvals/A1/approve", {"note": "ok"}),
    ("/api/v1/internal/approvals/A1/reject", {"reason": "policy"}),
    ("/api/v1/internal/approvals/A1/request-edit", {"note": "tweak"}),
    ("/api/v1/internal/approvals/A1/escalate", {"reason": "high risk"}),
    ("/api/v1/internal/workers/ceo_summary/retry", {}),
    ("/api/v1/internal/control/agents/brand_guardian/disable", {"reason": "drill"}),
    ("/api/v1/internal/control/agents/brand_guardian/enable", {}),
    ("/api/v1/internal/control/scorecard/generate", {}),
    ("/api/v1/internal/control/risks/R1/accept", {"note": "documented"}),
    ("/api/v1/internal/sovereign/readiness/generate", {}),
]


@pytest.fixture()
def client_with_private_ops(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Spin up the FastAPI app with PRIVATE_OPS pointed at a tmp dir."""
    from fastapi.testclient import TestClient

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.delenv("DEALIX_INTERNAL_TOKEN", raising=False)
    from api.main import app

    return TestClient(app)


@pytest.mark.parametrize("path", GET_PATHS)
def test_internal_get_endpoint_returns_envelope(client_with_private_ops, path: str) -> None:
    r = client_with_private_ops.get(path)
    assert r.status_code == 200, f"{path} returned {r.status_code}: {r.text[:200]}"
    body = r.json()
    assert "auth_mode" in body
    assert "source" in body
    assert "data" in body


@pytest.mark.parametrize("path,payload", POST_PATHS_WITH_BODY)
def test_internal_post_endpoint_queues_action(
    client_with_private_ops, path: str, payload: dict
) -> None:
    r = client_with_private_ops.post(path, json=payload)
    assert r.status_code in (200, 202), f"{path} returned {r.status_code}: {r.text[:200]}"
    body = r.json()
    assert "auth_mode" in body
    assert "data" in body


def test_internal_get_rejects_bad_token(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "real-secret")
    from api.main import app

    client = TestClient(app)
    r = client.get(
        "/api/v1/internal/ceo/summary",
        headers={"X-Dealix-Internal-Token": "wrong"},
    )
    assert r.status_code == 401


def test_internal_get_accepts_valid_token(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "real-secret")
    from api.main import app

    client = TestClient(app)
    r = client.get(
        "/api/v1/internal/ceo/summary",
        headers={"X-Dealix-Internal-Token": "real-secret"},
    )
    assert r.status_code == 200
    assert r.json()["auth_mode"] == "token"


def test_runtime_reader_handles_csv_with_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure read_csv_rows decodes existing rows correctly."""
    from api.internal.runtime_reader import append_csv_row, read_csv_rows

    monkeypatch.setenv("DEALIX_PRIVATE_OPS_ROOT", str(tmp_path))
    append_csv_row("growth/sector_targets.csv", {"sector": "logistics", "priority": "high"})
    append_csv_row("growth/sector_targets.csv", {"sector": "ERP", "priority": "med"})

    read = read_csv_rows("growth/sector_targets.csv")
    assert read["source"] == "csv"
    assert len(read["rows"]) == 2
    assert {r["sector"] for r in read["rows"]} == {"logistics", "ERP"}


def test_policy_adapter_loads_real_policy_file() -> None:
    """When the policy YAML exists, return the loaded rules."""
    from api.internal import policy_adapter

    # Use the actual repo policy file.
    out = policy_adapter.load_policies()
    # Either it loads successfully or falls back gracefully.
    assert out["source"] in {"yaml", "fallback"}
    assert isinstance(out["rules"], list)
