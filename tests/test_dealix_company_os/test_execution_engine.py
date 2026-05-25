from __future__ import annotations

"""Smoke tests for execution_engine."""

import csv
from pathlib import Path

import pytest

from execution_engine.evidence_checker import check_evidence_for_stage
from execution_engine.evidence_report_generator import generate_evidence_report
from execution_engine.next_action_engine import compute_next_action
from execution_engine.stage_checklist_updater import update_checklist
from execution_engine.stage_decision import advance_if_eligible, can_advance
from execution_engine.stage_reader import read_current_stage, write_current_stage


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


def test_stage_reader_returns_default_when_missing(tmp_path: Path) -> None:
    stage = read_current_stage(tmp_path)
    assert stage["stage"] == 0
    assert stage["status"] == "not_started"


def test_stage_reader_roundtrip(tmp_path: Path) -> None:
    write_current_stage(
        tmp_path,
        {
            "stage": 1,
            "started_at": "2026-01-01",
            "target_exit_date": "2026-02-01",
            "status": "in_progress",
        },
    )
    stage = read_current_stage(tmp_path)
    assert stage["stage"] == 1
    assert stage["status"] == "in_progress"
    assert stage["started_at"] == "2026-01-01"


def test_evidence_checker_stage1_empty_ops(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 1)
    assert len(checks) == 7
    assert all(c.status == "fail" for c in checks)


def test_evidence_checker_stage0_missing_dirs(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 0)
    assert any(c.status == "fail" for c in checks)


def test_can_advance_blocks_when_failures(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 1)
    eligible, blockers = can_advance(checks)
    assert eligible is False
    assert len(blockers) > 0


def test_next_action_picks_highest_leverage(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 1)
    msg = compute_next_action(checks)
    # Payment pursuit has the highest priority among unfulfilled checks.
    assert "Payment" in msg or "Next" in msg


def test_advance_if_eligible_writes_report_and_blocks(tmp_path: Path) -> None:
    result = advance_if_eligible(tmp_path)
    assert result["advanced"] is False
    assert (tmp_path / "stage" / "stage_exit_checklist.csv").exists()
    assert (tmp_path / "stage" / "evidence_report.md").exists()


def test_evidence_report_renders_table(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 1)
    out = generate_evidence_report(tmp_path, checks)
    content = out.read_text(encoding="utf-8")
    assert "# Stage Evidence Report" in content
    assert "| Criterion |" in content


def test_stage_checklist_csv_has_header(tmp_path: Path) -> None:
    checks = check_evidence_for_stage(tmp_path, 1)
    out = update_checklist(tmp_path, checks)
    with out.open("r", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert header == ["criterion", "status", "evidence", "next_action"]


def test_evidence_checker_passes_when_data_present(tmp_path: Path) -> None:
    # 25 leads
    leads_rows = [
        [f"lead-{i}", "lead", "fintech", "10000", "high"] for i in range(25)
    ]
    _write_csv(
        tmp_path / "pipeline" / "pipeline_tracker.csv",
        ["id", "stage", "sector", "deal_value_sar", "priority"],
        leads_rows,
    )
    # 25 DMs + 1 payment
    actions = [["dm_sent", "0", f"note-{i}"] for i in range(25)]
    actions.append(["payment_pursued", "5000", "PO"])
    _write_csv(
        tmp_path / "revenue" / "revenue_action_log.csv",
        ["action_type", "amount_sar", "notes"],
        actions,
    )
    # 3 samples
    samples_dir = tmp_path / "samples"
    samples_dir.mkdir()
    for i in range(3):
        (samples_dir / f"sample-{i}.md").write_text("x", encoding="utf-8")
    # 1 proposal
    proposals_dir = tmp_path / "proposals"
    proposals_dir.mkdir()
    (proposals_dir / "proposal-1.md").write_text("x", encoding="utf-8")
    # learning
    learning_dir = tmp_path / "learning"
    learning_dir.mkdir()
    (learning_dir / "2026-05-23.md").write_text("notes", encoding="utf-8")

    checks = check_evidence_for_stage(tmp_path, 1)
    # The git commit check may fail in tmp_path; assert the data-driven ones pass.
    passing = [c.criterion for c in checks if c.status == "pass"]
    assert "25 qualified leads in pipeline" in passing
    assert "25 DMs sent" in passing
    assert "3 client samples prepared" in passing
    assert "1 proposal sent" in passing
    assert "Payment or PO pursued" in passing
    assert "Weekly learning completed" in passing


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
