"""Tests for the content_os daily operating engine."""
from __future__ import annotations

import datetime as dt

from auto_client_acquisition.content_os import daily_engine

_TEST_DATE = dt.date(2026, 5, 17)

_EXPECTED_STAGES = {
    "revenue_machine",
    "social_content",
    "partner_intros",
    "approval_expire_sweep",
    "action_list",
}


async def test_daily_engine_runs_all_stages(tmp_path, monkeypatch):
    monkeypatch.setattr(daily_engine, "_MARKER_DIR", tmp_path)
    result = await daily_engine.run_daily_engine(date=_TEST_DATE)

    assert result["status"] == "ok"
    assert result["date"] == _TEST_DATE.isoformat()
    assert set(result["stages"].keys()) == _EXPECTED_STAGES
    assert result["action_list"].strip()
    # The marker file was written.
    assert (tmp_path / f"{_TEST_DATE.isoformat()}.json").exists()


async def test_daily_engine_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(daily_engine, "_MARKER_DIR", tmp_path)
    first = await daily_engine.run_daily_engine(date=_TEST_DATE)
    assert first["status"] == "ok"

    second = await daily_engine.run_daily_engine(date=_TEST_DATE)
    assert second["status"] == "already_ran"
    assert second["date"] == _TEST_DATE.isoformat()


async def test_daily_engine_force_reruns(tmp_path, monkeypatch):
    monkeypatch.setattr(daily_engine, "_MARKER_DIR", tmp_path)
    await daily_engine.run_daily_engine(date=_TEST_DATE)
    forced = await daily_engine.run_daily_engine(date=_TEST_DATE, force=True)
    assert forced["status"] == "ok"
    assert forced["force"] is True


async def test_daily_engine_survives_revenue_machine_failure(tmp_path, monkeypatch):
    """A revenue-machine / DB failure must not abort the loop — the
    other stages still run and the engine completes."""
    monkeypatch.setattr(daily_engine, "_MARKER_DIR", tmp_path)

    async def _boom(_body):
        raise RuntimeError("db unreachable")

    monkeypatch.setattr("api.routers.drafts.revenue_machine_run", _boom)
    result = await daily_engine.run_daily_engine(date=_TEST_DATE)
    # The orchestrator catches the failure and still completes.
    assert result["status"] == "ok"
    assert result["stages"]["revenue_machine"]["status"] == "error"
    assert "social_content" in result["stages"]
    assert "action_list" in result["stages"]
