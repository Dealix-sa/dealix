"""Tests for the Dealix internal Founder-Console API + supporting helpers.

These cover api/internal/{auth, runtime_reader, policy_adapter} and the read-only
routes under api/routers/internal/founder_console. The tests run against an
isolated FastAPI mount so we don't have to boot the full api.main app graph.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest


# ── api.internal.auth ────────────────────────────────────────────


def _reload_auth_with_env(monkeypatch, token):
    if token is None:
        monkeypatch.delenv("INTERNAL_API_TOKEN", raising=False)
    else:
        monkeypatch.setenv("INTERNAL_API_TOKEN", token)

    from api.internal import auth as auth_module

    return importlib.reload(auth_module)


@pytest.mark.asyncio
async def test_internal_auth_dev_mode_allows_anonymous(monkeypatch) -> None:
    auth = _reload_auth_with_env(monkeypatch, None)
    assert auth._expected_token() is None
    result = await auth.require_internal_token(x_internal_token=None)
    assert result == "anonymous-dev"


@pytest.mark.asyncio
async def test_internal_auth_blank_token_treated_as_unset(monkeypatch) -> None:
    auth = _reload_auth_with_env(monkeypatch, "   ")
    assert auth._expected_token() is None
    result = await auth.require_internal_token(x_internal_token=None)
    assert result == "anonymous-dev"


@pytest.mark.asyncio
async def test_internal_auth_valid_token_accepted(monkeypatch) -> None:
    auth = _reload_auth_with_env(monkeypatch, "s3cr3t")
    result = await auth.require_internal_token(x_internal_token="s3cr3t")
    assert result == "internal"


@pytest.mark.asyncio
async def test_internal_auth_missing_token_rejected(monkeypatch) -> None:
    from fastapi import HTTPException

    auth = _reload_auth_with_env(monkeypatch, "s3cr3t")
    with pytest.raises(HTTPException) as exc:
        await auth.require_internal_token(x_internal_token=None)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_internal_auth_invalid_token_rejected(monkeypatch) -> None:
    from fastapi import HTTPException

    auth = _reload_auth_with_env(monkeypatch, "s3cr3t")
    with pytest.raises(HTTPException) as exc:
        await auth.require_internal_token(x_internal_token="wrong")
    assert exc.value.status_code == 403


# ── api.internal.runtime_reader ──────────────────────────────────


def test_runtime_reader_missing_files_returns_empty(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PRIVATE_OPS_ROOT", str(tmp_path))

    from api.internal import runtime_reader

    importlib.reload(runtime_reader)

    assert runtime_reader.read_csv("nope", "missing.csv") == []
    assert list(runtime_reader.iter_csv("nope", "missing.csv")) == []
    assert runtime_reader.count_csv("nope", "missing.csv") == 0
    assert runtime_reader.first_csv("nope", "missing.csv") is None
    assert runtime_reader.private_ops_root() == tmp_path


def test_runtime_reader_reads_csv(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PRIVATE_OPS_ROOT", str(tmp_path))

    from api.internal import runtime_reader

    importlib.reload(runtime_reader)

    target = tmp_path / "runtime" / "worker_state.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "worker,status\nceo_summary_worker,ok\nsales_funnel_worker,fail\n",
        encoding="utf-8",
    )

    rows = runtime_reader.read_csv("runtime", "worker_state.csv")
    assert [r["worker"] for r in rows] == [
        "ceo_summary_worker",
        "sales_funnel_worker",
    ]

    assert (
        runtime_reader.count_csv(
            "runtime",
            "worker_state.csv",
            where=lambda r: r.get("status") == "ok",
        )
        == 1
    )

    first = runtime_reader.first_csv("runtime", "worker_state.csv")
    assert first is not None
    assert first["worker"] == "ceo_summary_worker"


# ── api.internal.policy_adapter ──────────────────────────────────


def test_policy_adapter_allows_internal_action() -> None:
    from api.internal.policy_adapter import evaluate

    decision = evaluate(
        {"action_type": "summary", "external_action_requested": False}
    )
    assert decision.decision == "allow"


def test_policy_adapter_blocks_guaranteed_revenue_claim() -> None:
    from api.internal.policy_adapter import evaluate

    decision = evaluate({"content_contains_guarantee_claim": True})
    assert decision.decision == "block"
    assert decision.rule_id == "no_guaranteed_revenue_claims"


def test_policy_adapter_blocks_a3_auto() -> None:
    from api.internal.policy_adapter import evaluate

    decision = evaluate({"action_class": "A3", "auto_execute": True})
    assert decision.decision == "block"
    assert decision.rule_id == "no_a3_auto"


def test_policy_adapter_blocks_suppressed_outreach() -> None:
    from api.internal.policy_adapter import evaluate

    decision = evaluate(
        {"action_type": "outreach", "target_in_suppression_list": True}
    )
    assert decision.decision == "block"
    assert decision.rule_id == "no_suppressed_outreach"


def test_policy_adapter_escalates_external_no_match() -> None:
    from api.internal.policy_adapter import evaluate

    decision = evaluate({"external_action_requested": True})
    assert decision.decision == "escalate"
    assert decision.rule_id == "default_external_action"


# ── api.routers.internal.founder_console ────────────────────────


@pytest.fixture
def founder_client(tmp_path: Path, monkeypatch):
    """Mount the founder_console router on a tiny FastAPI app for isolated testing."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    monkeypatch.setenv("PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.delenv("INTERNAL_API_TOKEN", raising=False)

    from api.internal import auth, runtime_reader
    from api.routers.internal import founder_console

    importlib.reload(auth)
    importlib.reload(runtime_reader)
    importlib.reload(founder_console)

    app = FastAPI()
    app.include_router(founder_console.router, prefix="/api/v1/internal")
    return TestClient(app)


FOUNDER_ENDPOINTS = [
    "/api/v1/internal/founder/ceo",
    "/api/v1/internal/founder/sales",
    "/api/v1/internal/founder/approvals",
    "/api/v1/internal/founder/workers",
    "/api/v1/internal/founder/trust",
    "/api/v1/internal/founder/finance",
    "/api/v1/internal/founder/distribution",
    "/api/v1/internal/founder/delivery",
    "/api/v1/internal/founder/retention",
    "/api/v1/internal/founder/proof",
    "/api/v1/internal/founder/audit",
    "/api/v1/internal/founder/evals",
    "/api/v1/internal/founder/product",
    "/api/v1/internal/founder/security",
    "/api/v1/internal/founder/growth",
    "/api/v1/internal/founder/marketing",
    "/api/v1/internal/founder/sovereign",
]

CONTROL_ENDPOINTS = [
    "/api/v1/internal/control/summary",
    "/api/v1/internal/control/policies",
    "/api/v1/internal/control/agents",
    "/api/v1/internal/control/scorecard",
    "/api/v1/internal/control/risks",
]


@pytest.mark.parametrize("endpoint", FOUNDER_ENDPOINTS + CONTROL_ENDPOINTS)
def test_internal_endpoints_respond_200_in_dev_mode(founder_client, endpoint) -> None:
    resp = founder_client.get(endpoint)
    assert resp.status_code == 200, resp.text
    assert resp.headers.get("content-type", "").startswith("application/json")


def test_internal_endpoints_require_token_when_set(tmp_path: Path, monkeypatch) -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    monkeypatch.setenv("PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.setenv("INTERNAL_API_TOKEN", "tk-abc")

    from api.internal import auth as auth_module
    from api.routers.internal import founder_console

    importlib.reload(auth_module)
    importlib.reload(founder_console)

    app = FastAPI()
    app.include_router(founder_console.router, prefix="/api/v1/internal")
    client = TestClient(app)

    # Missing token → 401
    assert client.get("/api/v1/internal/founder/ceo").status_code == 401

    # Wrong token → 403
    assert (
        client.get(
            "/api/v1/internal/founder/ceo",
            headers={"X-Internal-Token": "wrong"},
        ).status_code
        == 403
    )

    # Correct token → 200
    assert (
        client.get(
            "/api/v1/internal/founder/ceo",
            headers={"X-Internal-Token": "tk-abc"},
        ).status_code
        == 200
    )


def test_internal_workers_reads_runtime_csv(tmp_path: Path, monkeypatch) -> None:
    """Verify the workers endpoint reflects rows from runtime/worker_state.csv."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    monkeypatch.setenv("PRIVATE_OPS_ROOT", str(tmp_path))
    monkeypatch.delenv("INTERNAL_API_TOKEN", raising=False)

    from api.internal import auth, runtime_reader
    from api.routers.internal import founder_console

    importlib.reload(auth)
    importlib.reload(runtime_reader)
    importlib.reload(founder_console)

    target = tmp_path / "runtime" / "worker_state.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "worker,last_run,status,failures_24h,next_run,notes\n"
        "ceo_summary_worker,2026-05-23T13:00:00+00:00,ok,0,,\n"
        "sales_funnel_worker,2026-05-23T13:01:00+00:00,fail,3,,broken\n",
        encoding="utf-8",
    )

    app = FastAPI()
    app.include_router(founder_console.router, prefix="/api/v1/internal")
    client = TestClient(app)

    resp = client.get("/api/v1/internal/founder/workers")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert {row["worker"] for row in data} == {
        "ceo_summary_worker",
        "sales_funnel_worker",
    }
    failing = [r for r in data if r["worker"] == "sales_funnel_worker"][0]
    assert failing["failures_24h"] == 3
    assert failing["status"] == "fail"
