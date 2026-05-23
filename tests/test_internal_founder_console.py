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
