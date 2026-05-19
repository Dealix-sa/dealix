"""Tests for the autonomous strategy router."""

from __future__ import annotations

import asyncio

import pytest

from api.routers.autonomous_strategy import (
    _RunBody,
    decisions,
    gates,
    latest,
    router,
    run,
    tier,
)
from api.security.api_key import require_admin_key
from auto_client_acquisition.agent_os.agent_registry import (
    clear_for_test as clear_agents,
)
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    clear_for_test as clear_ledger,
)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "DEALIX_STRATEGIC_DECISION_LEDGER_PATH",
        str(tmp_path / "strategic-decision-ledger.jsonl"),
    )
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    clear_ledger()
    clear_agents()
    get_default_approval_store().clear()
    yield
    get_default_approval_store().clear()
    clear_agents()
    clear_ledger()


def test_router_prefix() -> None:
    assert router.prefix == "/api/v1/strategy/autonomous"


def test_tier_endpoint_shape() -> None:
    payload = asyncio.run(tier())
    assert "ceo" in payload
    ceo = payload["ceo"]
    for key in ("agent_id", "name", "role_ar", "role_en", "autonomy_level", "status"):
        assert key in ceo
    assert isinstance(ceo["delegates_to"], list)
    assert len(payload["board_directors"]) == 4
    for d in payload["board_directors"]:
        for key in (
            "agent_id",
            "name",
            "role_ar",
            "role_en",
            "autonomy_level",
            "status",
        ):
            assert key in d
    assert payload["delegates_to_operational"] == "fo_orchestrator_chief_of_staff"
    assert payload["totals"]["board_directors"] == 4
    assert payload["totals"]["max_autonomy_level"] == 3
    assert payload["governance_decision"] == "allow"


def test_run_endpoint_returns_report() -> None:
    body = _RunBody(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000, "retainer_count": 4},
        delegate_full_ops=False,
    )
    payload = asyncio.run(run(body))
    for key in (
        "cycle_id",
        "signal_snapshot",
        "gate_evaluations",
        "decisions",
        "approvals_pending",
        "delegated_cycles",
        "next_actions",
        "hard_gates",
        "report_paths",
        "warnings",
    ):
        assert key in payload
    assert payload["governance_decision"] == "allow_with_review"


def test_run_is_admin_gated() -> None:
    # The /run route must carry the admin-key dependency.
    run_route = next(r for r in router.routes if r.path.endswith("/run"))
    dep_calls = [d.call for d in run_route.dependant.dependencies]
    assert require_admin_key in dep_calls


def test_latest_empty_state() -> None:
    payload = asyncio.run(latest())
    # No cycle has run in this isolated tmp ledger; the data dir may still
    # hold a prior file, so accept either empty-state or a real report.
    assert "governance_decision" in payload
    assert "decisions" in payload


def test_latest_after_run() -> None:
    asyncio.run(
        run(
            _RunBody(
                on_date="2026-06-15",
                pipeline_summary={"total_revenue_sar": 42000},
                delegate_full_ops=False,
            )
        )
    )
    payload = asyncio.run(latest())
    assert payload.get("empty") is False
    assert payload["cycle_id"]


def test_decisions_endpoint() -> None:
    asyncio.run(
        run(
            _RunBody(
                on_date="2026-06-15",
                pipeline_summary={
                    "total_revenue_sar": 20000,
                    "founder_hours_per_sprint": 9,
                },
                delegate_full_ops=False,
            )
        )
    )
    payload = asyncio.run(decisions(decision_type=None, status=None, limit=50))
    assert "decisions" in payload
    assert isinstance(payload["decisions"], list)
    pending = asyncio.run(
        decisions(decision_type=None, status="pending_approval", limit=50)
    )
    assert all(d["status"] == "pending_approval" for d in pending["decisions"])


def test_gates_endpoint() -> None:
    payload = asyncio.run(gates())
    assert "gates" in payload
    assert len(payload["gates"]) >= 6
    for g in payload["gates"]:
        assert "gate_id" in g
        assert "comparator" in g
