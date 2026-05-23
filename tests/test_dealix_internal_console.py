"""Tests for the Dealix internal Founder Console surface.

These tests cover:
- api.internal.auth — token gate
- api.internal.runtime_reader — CSV reader with missing dir / missing file
- api.internal.policy_adapter — load policy YAML + evaluate_action
- api.routers.founder_console_internal — every GET endpoint + a sample of
  POST endpoints, exercised through the FastAPI TestClient

They do not require external services. The private ops runtime is
pointed at a tmp dir per test.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

import pytest


@pytest.fixture
def private_ops_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Provide a fake private ops runtime dir for the duration of the test."""
    base = tmp_path / "ops"
    (base / "runtime").mkdir(parents=True)
    (base / "trust").mkdir(parents=True)
    (base / "finance").mkdir(parents=True)
    (base / "approvals").mkdir(parents=True)
    # seed a worker_state row so workers endpoint returns content
    state = base / "runtime" / "worker_state.csv"
    with state.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "name", "status", "last_run", "failure_count", "owner"])
        w.writerow(["ceo_summary", "CEO Summary", "ok", "2026-05-23T12:00:00Z", "0", "founder"])
    # seed cash collected for finance / ceo summary
    cash = base / "finance" / "cash_collected.csv"
    with cash.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "client", "amount_sar", "collected_at", "method"])
        w.writerow(["pay_1", "ACME", "1500", "2026-05-20T10:00:00Z", "bank"])
    monkeypatch.setenv("PRIVATE_OPS", str(base))
    # auth.py reads env at request time; ensure token gate is in dev mode
    monkeypatch.delenv("DEALIX_INTERNAL_TOKEN", raising=False)
    yield base


def test_runtime_reader_no_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.runtime_reader import read_csv

    monkeypatch.delenv("PRIVATE_OPS", raising=False)
    monkeypatch.delenv("DEALIX_PRIVATE_OPS_DIR", raising=False)
    r = read_csv("nothing/missing.csv")
    assert r.source == "no-runtime"
    assert r.rows == []
    assert r.path is None


def test_runtime_reader_missing_file(private_ops_dir: Path) -> None:
    from api.internal.runtime_reader import read_csv

    r = read_csv("not_there.csv")
    assert r.source == "missing"
    assert r.rows == []
    assert r.path is not None


def test_runtime_reader_reads_csv(private_ops_dir: Path) -> None:
    from api.internal.runtime_reader import read_csv

    r = read_csv("runtime/worker_state.csv")
    assert r.source == "csv"
    assert len(r.rows) == 1
    assert r.rows[0]["id"] == "ceo_summary"


def test_auth_dev_mode_when_token_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.auth import auth_mode

    monkeypatch.delenv("DEALIX_INTERNAL_TOKEN", raising=False)
    assert auth_mode() == "dev_unprotected"


def test_auth_enforced_when_token_set(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.auth import auth_mode

    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok_test_xyz")
    assert auth_mode() == "enforced"


def test_policy_loads_rules() -> None:
    from api.internal.policy_adapter import _load, list_rules

    _load.cache_clear()  # type: ignore[attr-defined]
    rules = list_rules()
    ids = {r.get("id") for r in rules}
    # canonical rules must be present
    assert "no_a3_auto" in ids
    assert "no_guaranteed_revenue_claims" in ids
    assert "public_proof_requires_approval" in ids


def test_policy_evaluate_a3_denied() -> None:
    from api.internal.policy_adapter import evaluate_action

    d = evaluate_action("external_send", {"approval_class": "A3"})
    assert d.allowed is False
    assert d.rule == "no_a3_auto"


def test_policy_evaluate_proof_publish_draft_denied() -> None:
    from api.internal.policy_adapter import evaluate_action

    d = evaluate_action("proof_publish", {"approval_state": "draft"})
    assert d.allowed is False
    assert d.rule == "public_proof_requires_approval"


def test_policy_evaluate_unrelated_action_allowed() -> None:
    from api.internal.policy_adapter import evaluate_action

    d = evaluate_action("approval_approve", {"approval_id": "apr_001"})
    assert d.allowed is True


# ── HTTP surface ────────────────────────────────────────────────


@pytest.fixture
def test_client(private_ops_dir: Path):  # noqa: ARG001 — fixture activates private ops env
    from fastapi.testclient import TestClient

    from api.main import app

    return TestClient(app)


GET_ENDPOINTS = [
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
    "/api/v1/internal/data/summary",
    "/api/v1/internal/experiments/backlog",
]


@pytest.mark.parametrize("path", GET_ENDPOINTS)
def test_internal_get_endpoint_smoke(test_client, path: str) -> None:
    res = test_client.get(path)
    assert res.status_code == 200, (path, res.text[:300])
    body = res.json()
    assert "data" in body
    assert "auth_mode" in body
    assert body["auth_mode"] in {"dev_unprotected", "enforced"}


def test_ceo_summary_reflects_seeded_cash(test_client) -> None:
    res = test_client.get("/api/v1/internal/ceo/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["cash_collected_30d_sar"] == 1500.0


def test_workers_health_returns_seeded_worker(test_client) -> None:
    res = test_client.get("/api/v1/internal/workers/health")
    workers = res.json()["data"]["workers"]
    assert len(workers) == 1
    assert workers[0]["id"] == "ceo_summary"


def test_approval_approve_records_audit(test_client, private_ops_dir: Path) -> None:
    res = test_client.post(
        "/api/v1/internal/approvals/apr_001/approve",
        json={"note": "looks good"},
    )
    assert res.status_code == 200
    audit = private_ops_dir / "trust" / "approval_decisions.csv"
    assert audit.exists()
    lines = audit.read_text(encoding="utf-8").splitlines()
    # header + 1 row
    assert len(lines) == 2
    assert "approval_approve" in lines[1]


def test_agent_disable_recorded(test_client) -> None:
    res = test_client.post(
        "/api/v1/internal/control/agents/ceo_copilot/disable",
        json={"reason": "drill"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body.get("audit_id")
    assert body.get("message") == "agent_disable_recorded"


def test_auth_enforced_rejects_wrong_token(monkeypatch: pytest.MonkeyPatch, private_ops_dir: Path) -> None:
    from fastapi.testclient import TestClient

    from api.main import app

    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "tok_secret")
    client = TestClient(app)
    res = client.get("/api/v1/internal/ceo/summary")
    assert res.status_code == 401

    res2 = client.get(
        "/api/v1/internal/ceo/summary",
        headers={"x-dealix-internal-token": "tok_secret"},
    )
    assert res2.status_code == 200
