"""Tests for ``scripts/full_ops_tick.py`` and the ``recent_ticks`` shape
added to ``GET /api/v1/full-ops/daily-command-center``.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.agent_os import clear_for_test
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.full_ops.work_queue import _reset


# ── Helpers ────────────────────────────────────────────────────────


def _load_tick_script() -> ModuleType:
    """Import scripts/full_ops_tick.py as a module (path-based)."""
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "full_ops_tick.py"
    spec = importlib.util.spec_from_file_location("full_ops_tick_script", script_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


# ── Script tests ───────────────────────────────────────────────────


@pytest.fixture()
def _isolated(tmp_path, monkeypatch):
    """Fresh registry, store, queue and ledger per test."""
    ledger = tmp_path / "ticks.jsonl"
    monkeypatch.setenv("DEALIX_FULL_OPS_LEDGER_PATH", str(ledger))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    clear_for_test()
    get_default_approval_store().clear()
    _reset()
    yield ledger
    clear_for_test()
    get_default_approval_store().clear()
    _reset()


def test_script_main_exits_zero(_isolated: Path) -> None:
    """``main()`` must return 0 on a clean run."""
    mod = _load_tick_script()
    exit_code = mod.main()
    assert exit_code == 0


def test_script_writes_tick_to_ledger(_isolated: Path) -> None:
    """After ``main()``, the ledger file must contain at least one JSON line."""
    mod = _load_tick_script()
    mod.main()
    ledger: Path = _isolated
    assert ledger.exists(), "ledger file was not created"
    lines = [ln.strip() for ln in ledger.read_text().splitlines() if ln.strip()]
    assert len(lines) >= 1
    row = json.loads(lines[0])
    assert "tick_id" in row
    assert row["tick_id"].startswith("tick_")


def test_script_records_zero_sends_and_charges(_isolated: Path) -> None:
    """The tick script must never produce a live send or charge."""
    mod = _load_tick_script()
    mod.main()
    ledger: Path = _isolated
    row = json.loads(ledger.read_text().strip().splitlines()[-1])
    assert row.get("sends", 0) == 0
    assert row.get("charges", 0) == 0


def test_script_prints_summary_line(_isolated: Path, capsys) -> None:
    """``main()`` must print a non-empty one-line summary to stdout."""
    mod = _load_tick_script()
    mod.main()
    out = capsys.readouterr().out
    assert "tick_id=" in out
    assert "sensed=" in out
    assert "approvals_required=" in out
    assert "approvals_blocked=" in out
    assert "ledger=" in out


# ── daily-command-center recent_ticks field tests ──────────────────


@pytest.fixture()
def _dcc_isolated(tmp_path, monkeypatch):
    """Isolated env for command-center endpoint tests."""
    ledger = tmp_path / "ticks.jsonl"
    monkeypatch.setenv("DEALIX_FULL_OPS_LEDGER_PATH", str(ledger))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    clear_for_test()
    get_default_approval_store().clear()
    _reset()
    yield ledger
    clear_for_test()
    get_default_approval_store().clear()
    _reset()


@pytest.mark.asyncio
async def test_daily_command_center_returns_recent_ticks_field(
    _dcc_isolated: Path,
) -> None:
    """``/daily-command-center`` must include ``recent_ticks`` key."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    assert "recent_ticks" in body
    assert isinstance(body["recent_ticks"], list)


@pytest.mark.asyncio
async def test_daily_command_center_recent_ticks_reflects_recorded_tick(
    _dcc_isolated: Path,
) -> None:
    """After a tick is recorded, ``recent_ticks`` must surface it with the
    expected compact shape."""
    from auto_client_acquisition.full_ops.operating_loop import run_tick

    # Write one tick to the ledger
    run_tick(record_ledger=True)

    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    recent = body["recent_ticks"]
    assert isinstance(recent, list)
    assert len(recent) >= 1

    entry = recent[0]
    for field in (
        "tick_id",
        "generated_at",
        "work_items_sensed",
        "approvals_created",
        "internal_only_count",
        "sends",
        "charges",
    ):
        assert field in entry, f"compact tick entry missing field: {field}"

    assert entry["sends"] == 0
    assert entry["charges"] == 0


@pytest.mark.asyncio
async def test_daily_command_center_recent_ticks_capped_at_10(
    _dcc_isolated: Path,
) -> None:
    """``recent_ticks`` must return at most 10 entries."""
    from auto_client_acquisition.full_ops.operating_loop import run_tick

    for _ in range(15):
        run_tick(record_ledger=True)

    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    assert len(body["recent_ticks"]) <= 10


@pytest.mark.asyncio
async def test_daily_command_center_existing_keys_unchanged(
    _dcc_isolated: Path,
) -> None:
    """Adding ``recent_ticks`` must not remove any previously existing keys."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    for key in (
        "schema_version",
        "generated_at",
        "today_top_3_decisions",
        "growth_queue",
        "sales_queue",
        "support_queue",
        "cs_queue",
        "delivery_queue",
        "compliance_alerts",
        "executive_summary",
        "blocked_actions",
        "revenue_truth",
        "revenue_execution_next_step",
        "hard_gates",
        "degraded",
        "degraded_sections",
        "recent_ticks",
    ):
        assert key in body, f"expected key missing from daily-command-center: {key}"
