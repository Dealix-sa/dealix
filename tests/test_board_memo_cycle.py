"""Tests for the monthly board-memo cycle."""
from __future__ import annotations

import json

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.board_ready_os.board_memo import BOARD_MEMO_SECTIONS
from auto_client_acquisition.financial_autonomy.board_memo_cycle import (
    BoardMemoReport,
    latest_board_memo,
    run_board_memo_cycle,
)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "DEALIX_FINANCIAL_CYCLES_PATH",
        str(tmp_path / "financial_cycles"),
    )
    monkeypatch.setenv(
        "DEALIX_BOARD_MEMOS_PATH",
        str(tmp_path / "board_memos"),
    )
    monkeypatch.setenv(
        "DEALIX_CAPITAL_LEDGER_PATH",
        str(tmp_path / "capital-ledger.jsonl"),
    )
    monkeypatch.setenv(
        "DEALIX_FRICTION_LOG_PATH",
        str(tmp_path / "friction.jsonl"),
    )
    get_default_approval_store().clear()
    yield
    get_default_approval_store().clear()


def test_run_board_memo_cycle_basic_shape() -> None:
    report = run_board_memo_cycle(month="2026-05")
    assert isinstance(report, BoardMemoReport)
    assert report.month == "2026-05"
    # Every documented section slug is present
    for slug in BOARD_MEMO_SECTIONS:
        assert slug in report.sections


def test_run_board_memo_cycle_creates_approval() -> None:
    report = run_board_memo_cycle(month="2026-05")
    assert report.approval_id.startswith("apr_")
    store = get_default_approval_store()
    pending = store.list_pending()
    assert any(p.approval_id == report.approval_id for p in pending)
    target = next(p for p in pending if p.approval_id == report.approval_id)
    assert target.object_type == "board_memo"
    assert target.object_id == "board_memo:2026-05"
    assert target.action_mode == "approval_required"


def test_run_board_memo_cycle_persists_files() -> None:
    report = run_board_memo_cycle(month="2026-05")
    paths = report.report_paths
    assert "json" in paths and "md" in paths
    md_text = open(paths["md"], encoding="utf-8").read()
    assert "Dealix Board Memo" in md_text
    assert "مذكّرة مجلس Dealix" in md_text
    # the markdown contains the executive summary headers
    assert "Executive Summary" in md_text
    assert "الملخّص التنفيذي" in md_text


def test_run_board_memo_cycle_sections_have_titles_and_bodies() -> None:
    report = run_board_memo_cycle(month="2026-05")
    for slug, block in report.sections.items():
        assert "title_ar" in block
        assert "title_en" in block
        assert "body_ar" in block
        assert "body_en" in block


def test_run_board_memo_cycle_invalid_month_raises() -> None:
    with pytest.raises(ValueError):
        run_board_memo_cycle(month="not-a-month")


def test_latest_board_memo_returns_persisted_memo() -> None:
    assert latest_board_memo("2026-05") is None
    report = run_board_memo_cycle(month="2026-05")
    fetched = latest_board_memo("2026-05")
    assert fetched is not None
    assert fetched["month"] == "2026-05"
    assert fetched["approval_id"] == report.approval_id


def test_latest_board_memo_without_month_returns_newest() -> None:
    run_board_memo_cycle(month="2026-04")
    run_board_memo_cycle(month="2026-05")
    fetched = latest_board_memo()
    assert fetched is not None
    assert fetched["month"] == "2026-05"


def test_to_dict_round_trip() -> None:
    report = run_board_memo_cycle(month="2026-05")
    payload = report.to_dict()
    for key in (
        "month",
        "generated_at",
        "sections",
        "section_order",
        "sections_complete",
        "missing_sections",
        "approval_id",
        "warnings",
        "report_paths",
        "financial_cycle",
    ):
        assert key in payload
    # JSON-serializable
    json.dumps(payload, ensure_ascii=False)


def test_section_order_preserved() -> None:
    report = run_board_memo_cycle(month="2026-05")
    assert report.section_order == list(BOARD_MEMO_SECTIONS)
