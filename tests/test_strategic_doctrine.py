"""Doctrine guardrails for the strategic autonomy layer."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os.agent_registry import (
    clear_for_test as clear_agents,
)
from auto_client_acquisition.agent_os.agent_registry import list_agents
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    clear_for_test as clear_ledger,
)
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    query_decisions,
    record_decision,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    IRREVERSIBLE,
    is_irreversible,
)
from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
    run_strategic_cycle,
)
from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
    all_strategic_nodes,
    seed_strategic_tier,
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


def test_no_strategic_agent_above_l3() -> None:
    seed_strategic_tier()
    for node in all_strategic_nodes():
        assert node.autonomy_level <= 3
    for card in list_agents(owner="founder"):
        if card.agent_id.startswith("sa_"):
            assert card.autonomy_level <= 3


def test_no_irreversible_decision_auto_delegated() -> None:
    # A cycle that produces an irreversible HIRE decision must never mark
    # it delegated — it stays pending_approval until an APPROVED approval.
    run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={
            "total_revenue_sar": 20000,
            "founder_hours_per_sprint": 9,
        },
        delegate_full_ops=True,
    )
    delegated = query_decisions(status="delegated")
    for d in delegated:
        assert not is_irreversible(d.decision_type), (
            "irreversible decision must never be auto-delegated"
        )


def test_irreversible_decisions_require_approval_flag() -> None:
    for decision_type in IRREVERSIBLE:
        decision = record_decision(
            cycle_id="cyc_doctrine",
            decision_type=decision_type,
            target="t",
            rationale_ar="a",
            rationale_en="a",
            score=10.0,
            decision_band="hold",
            evidence=["grounded"],
            status="pending_approval",
        )
        assert decision.requires_approval is True
        assert decision.irreversible is True


def test_irreversible_without_evidence_is_refused() -> None:
    for decision_type in IRREVERSIBLE:
        with pytest.raises(ValueError):
            record_decision(
                cycle_id="cyc_doctrine",
                decision_type=decision_type,
                target="t",
                rationale_ar="a",
                rationale_en="a",
                score=10.0,
                decision_band="hold",
                evidence=[],
            )


def test_cycle_hard_gates_present() -> None:
    report = run_strategic_cycle(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 42000},
        delegate_full_ops=False,
    )
    assert "no_autonomous_irreversible_execution" in report.hard_gates
    assert "no_agent_above_l3" in report.hard_gates
    assert "doctrine_non_negotiables_enforced" in report.hard_gates
