"""Tests for the strategic autonomy cycle."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os.agent_registry import (
    clear_for_test as clear_agents,
)
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    clear_for_test as clear_ledger,
)
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    query_decisions,
)
from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
    StrategicCycleReport,
    latest_strategic_report,
    run_strategic_cycle,
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


def test_run_cycle_returns_report() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000, "retainer_count": 4},
        delegate_full_ops=False,
    )
    assert isinstance(report, StrategicCycleReport)
    assert report.cycle_id.startswith("sac_")
    assert report.signal_snapshot["days_since_launch"] > 0
    assert report.gate_evaluations


def test_irreversible_decision_is_approval_gated_not_delegated() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 20000},
        delegate_full_ops=True,
    )
    # Set founder hours via pipeline summary to trigger HIRE.
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={
            "total_revenue_sar": 20000,
            "founder_hours_per_sprint": 9,
        },
        delegate_full_ops=True,
    )
    hire_decisions = [d for d in report.decisions if d["decision_type"] == "hire"]
    assert hire_decisions, "expected a HIRE decision"
    for d in hire_decisions:
        assert d["irreversible"] is True
        assert d["status"] == "pending_approval"
        assert d["status"] != "delegated"
    assert report.approvals_pending["count"] >= 1


def test_irreversible_routed_to_approval_queue() -> None:
    run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={
            "total_revenue_sar": 20000,
            "founder_hours_per_sprint": 9,
        },
        delegate_full_ops=False,
    )
    pending = get_default_approval_store().list_pending()
    strategic = [p for p in pending if p.object_type == "strategic_decision"]
    assert strategic


def test_decisions_recorded_to_ledger() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000, "retainer_count": 4},
        delegate_full_ops=False,
    )
    rows = query_decisions(cycle_id=report.cycle_id)
    assert len(rows) == len(report.decisions)


def test_reversible_delegates_to_full_ops() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 90000, "retainer_count": 6},
        delegate_full_ops=True,
    )
    reversible = [d for d in report.decisions if not d["irreversible"]]
    if reversible:
        assert report.delegated_cycles
        assert (
            report.delegated_cycles[0]["delegated_to"]
            == "fo_orchestrator_chief_of_staff"
        )


def test_no_delegation_when_disabled() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 90000, "retainer_count": 6},
        delegate_full_ops=False,
    )
    assert report.delegated_cycles == []


def test_report_persisted_and_latest_returns_it() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000},
        delegate_full_ops=False,
    )
    assert report.report_paths.get("json")
    latest = latest_strategic_report()
    assert latest is not None
    assert latest["cycle_id"] == report.cycle_id


def test_monthly_cadence_runs() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        cadence="monthly",
        pipeline_summary={"total_revenue_sar": 42000},
        delegate_full_ops=False,
    )
    assert report.cadence == "monthly"


def test_to_dict_shape() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000},
        delegate_full_ops=False,
    )
    data = report.to_dict()
    for key in (
        "cycle_id",
        "generated_at",
        "on_date",
        "cadence",
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
        assert key in data
