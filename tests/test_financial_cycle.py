"""Tests for the weekly financial autonomy cycle."""
from __future__ import annotations

import json
import os

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.financial_autonomy.financial_cycle import (
    FinancialCycleReport,
    latest_financial_report,
    run_financial_cycle,
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


def test_run_financial_cycle_returns_report() -> None:
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    assert isinstance(report, FinancialCycleReport)
    assert report.cycle_id.startswith("fc_")
    assert report.period_end == "2026-05-22"
    assert report.cadence == "weekly"
    # bilingual titles
    assert report.title_ar
    assert report.title_en


def test_run_financial_cycle_hard_gates_present() -> None:
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    for gate in (
        "no_live_send",
        "no_live_charge",
        "no_auto_refund",
        "approval_required_for_financial_decisions",
        "no_fake_revenue",
    ):
        assert gate in report.hard_gates


def test_run_financial_cycle_creates_pending_approval_for_margin_floor() -> None:
    """The zero-state aggregator produces a margin-floor violation that
    must become a pending founder approval."""
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    assert report.approvals_pending["count"] >= 1
    store = get_default_approval_store()
    pending = store.list_pending()
    object_ids = {p.object_id for p in pending}
    # Approval object_id pattern: cycle_id:rule_id (or :anomaly_kind)
    assert any(":gross_margin_floor" in oid for oid in object_ids)


def test_run_financial_cycle_persists_files(tmp_path) -> None:
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    paths = report.report_paths
    assert "json" in paths and "md" in paths
    json_data = json.loads(open(paths["json"], encoding="utf-8").read())
    assert json_data["cycle_id"] == report.cycle_id
    md_text = open(paths["md"], encoding="utf-8").read()
    assert "Financial autonomy cycle" in md_text
    assert "دورة الاستقلالية المالية" in md_text


def test_run_financial_cycle_appends_event_jsonl() -> None:
    run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    cycles_dir = os.environ["DEALIX_FINANCIAL_CYCLES_PATH"]
    events_path = os.path.join(cycles_dir, "events.jsonl")
    assert os.path.exists(events_path)
    lines = [l for l in open(events_path, encoding="utf-8").read().splitlines() if l]
    assert lines
    last = json.loads(lines[-1])
    assert last["event_type"] == "financial_cycle_run"
    assert last["period_end"] == "2026-05-22"


def test_latest_financial_report_returns_newest() -> None:
    assert latest_financial_report() is None
    run_financial_cycle(period_end="2026-05-20", cadence="weekly")
    run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    latest = latest_financial_report()
    assert latest is not None
    assert latest["period_end"] == "2026-05-22"


def test_run_financial_cycle_detects_anomaly_against_previous() -> None:
    """Forced anomaly: persist a fake "previous" snapshot then re-run."""
    cycles_dir = os.environ["DEALIX_FINANCIAL_CYCLES_PATH"]
    os.makedirs(cycles_dir, exist_ok=True)
    prev_payload = {
        "cycle_id": "fc_prev0000",
        "period_end": "2026-05-01",
        "metrics": {
            "mrr_sar": 100_000.0,
            "churn_pct_monthly": 1.0,
            "runway_months": 24.0,
            "gross_margin_pct": 60.0,
        },
    }
    with open(os.path.join(cycles_dir, "2026-05-01.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(prev_payload))

    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    # The zero-state aggregator records MRR=0; vs previous MRR=100k that is
    # a revenue regression and a runway drop.
    kinds = {a["kind"] for a in report.anomalies}
    assert "revenue_regression" in kinds


def test_report_to_dict_shape() -> None:
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    payload = report.to_dict()
    for key in (
        "cycle_id",
        "generated_at",
        "period_end",
        "cadence",
        "title_ar",
        "title_en",
        "metrics",
        "unit_economics",
        "anomalies",
        "threshold_violations",
        "approvals_pending",
        "hard_gates",
        "warnings",
        "report_paths",
    ):
        assert key in payload
