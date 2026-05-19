"""Tests for the strategic automation layer (G6).

Covers:
  - auto_client_acquisition/agent_os/dealix_org.py — seed_dealix_org()
    (idempotent, 10 agents, no L4+ autonomy).
  - auto_client_acquisition/automation/strategic_runner.py — the runner
    core functions (role briefs, executive report, scorecard, bottleneck
    sweep, business metrics, strategy synthesis).
  - core/tasks/worker.py — the strategic crons are registered and the
    cron count is correct.

Doctrine: every strategic artifact is INTERNAL ONLY. ``external_send`` is
hard-coded ``False``; the runner performs no prospect contact. Persistence
and email degrade gracefully when the dependency is unreachable, so these
tests run without Postgres / a live email provider.
"""

from __future__ import annotations

import asyncio

from auto_client_acquisition.agent_os import dealix_org
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    list_agents,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.automation import strategic_runner
from core.tasks.worker import WorkerSettings


# ─── G6-a: agent org seed ────────────────────────────────────────


def test_seed_dealix_org_registers_ten_agents() -> None:
    clear_agent_registry_for_tests()
    summary = dealix_org.seed_dealix_org()
    assert summary["status"] == "ok"
    assert summary["total"] == 10
    assert len(summary["registered"]) == 10
    assert len(list_agents()) == 10
    clear_agent_registry_for_tests()


def test_seed_dealix_org_is_idempotent() -> None:
    clear_agent_registry_for_tests()
    first = dealix_org.seed_dealix_org()
    second = dealix_org.seed_dealix_org()
    assert len(first["registered"]) == 10
    assert len(second["registered"]) == 0
    assert len(second["skipped"]) == 10
    # Still exactly 10 cards — no duplication.
    assert len(list_agents()) == 10
    clear_agent_registry_for_tests()


def test_dealix_org_has_no_l4_plus_autonomy() -> None:
    """No agent in the org may exceed L3 (Recommend)."""
    for card in dealix_org.build_org_cards():
        assert card.autonomy_level <= int(AutonomyLevel.L3_RECOMMEND)
        assert card.autonomy_level >= int(AutonomyLevel.L1_ANALYZE)


def test_dealix_org_layers_and_kill_switch() -> None:
    cards = {c.agent_id: c for c in dealix_org.build_org_cards()}
    assert set(cards) == set(dealix_org.DEALIX_ORG_AGENT_IDS)
    assert len(dealix_org.EXECUTIVE_LAYER) == 6
    assert len(dealix_org.EXECUTION_LAYER) == 4
    assert "dealix-pm" in dealix_org.EXECUTIVE_LAYER
    assert "dealix-engineer" in dealix_org.EXECUTION_LAYER
    for card in cards.values():
        assert card.owner
        assert card.purpose
        assert card.kill_switch_owner


# ─── G6-b: strategic runner cores ────────────────────────────────


def test_run_role_briefs_core() -> None:
    result = asyncio.run(strategic_runner.run_role_briefs_core())
    assert result["status"] == "ok"
    assert result["artifact_type"] == "role_briefs"
    assert result["roles_briefed"] >= 1
    assert result["external_send"] is False


def test_run_executive_report_core() -> None:
    result = asyncio.run(strategic_runner.run_executive_report_core())
    assert result["status"] == "ok"
    assert result["artifact_type"] == "executive_report"
    assert result["external_send"] is False


def test_run_scorecard_core() -> None:
    result = asyncio.run(strategic_runner.run_scorecard_core())
    assert result["status"] == "ok"
    assert result["artifact_type"] == "growth_scorecard"
    assert result["external_send"] is False


def test_run_bottleneck_sweep_core() -> None:
    result = asyncio.run(
        strategic_runner.run_bottleneck_sweep_core(
            blocking_approvals_count=2,
            overdue_followups=1,
        )
    )
    assert result["status"] == "ok"
    assert result["artifact_type"] == "bottleneck_sweep"
    assert result["external_send"] is False


def test_run_business_metrics_core() -> None:
    result = asyncio.run(strategic_runner.run_business_metrics_core())
    assert result["status"] == "ok"
    assert result["artifact_type"] == "business_metrics"
    assert result["external_send"] is False


# ─── G6-c: strategy synthesis ────────────────────────────────────


def test_run_strategy_synthesis_core() -> None:
    result = asyncio.run(strategic_runner.run_strategy_synthesis_core())
    assert result["status"] == "ok"
    assert result["artifact_type"] == "strategy_synthesis"
    assert isinstance(result["top_3_recommendations"], list)
    assert len(result["top_3_recommendations"]) <= 3
    assert isinstance(result["decision_forks_for_founder"], list)
    assert result["external_send"] is False


# ─── G6-d: doctrine — no external send ───────────────────────────


def test_strategic_runner_never_sends_externally() -> None:
    """The strategic layer is internal only — every artifact records
    external_send=False and the module-level flag is False."""
    assert strategic_runner.STRATEGIC_EXTERNAL_SEND is False
    assert strategic_runner.STRATEGIC_AUTONOMY_LEVEL == 3
    cores = [
        strategic_runner.run_role_briefs_core(),
        strategic_runner.run_executive_report_core(),
        strategic_runner.run_scorecard_core(),
        strategic_runner.run_bottleneck_sweep_core(),
        strategic_runner.run_business_metrics_core(),
        strategic_runner.run_strategy_synthesis_core(),
    ]

    async def _run_all() -> list[dict]:
        return [await c for c in cores]

    for result in asyncio.run(_run_all()):
        assert result["external_send"] is False


def test_strategic_crons_registered() -> None:
    """The 6 strategic crons (1 daily + 5 weekly) are registered, bringing
    the worker total to 13 cron jobs."""
    assert len(WorkerSettings.cron_jobs) == 13
    fn_names = {
        getattr(c, "coroutine", None).__name__
        for c in WorkerSettings.cron_jobs
        if getattr(c, "coroutine", None) is not None
    }
    expected = {
        "cron_business_metrics_snapshot",
        "cron_weekly_role_briefs",
        "cron_weekly_executive_report",
        "cron_weekly_scorecard",
        "cron_weekly_bottleneck_sweep",
        "cron_weekly_strategy_synthesis",
    }
    assert expected.issubset(fn_names)


def test_persist_strategic_brief_degrades_gracefully() -> None:
    """With Postgres unreachable, persist returns None — never crashes."""
    row_id = asyncio.run(
        strategic_runner.persist_strategic_brief(
            artifact_type="role_briefs",
            period_label="2026-W21",
            title="test",
            payload={"k": "v"},
        )
    )
    assert row_id is None or isinstance(row_id, str)
