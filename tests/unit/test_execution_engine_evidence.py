"""Locks the Execution Engine v2 evidence pipeline behavior.

Covers:
- Scanner reads pipeline + revenue + filesystem evidence into a status dict.
- Stage checklist auto-updates Done/Pending from scanner output.
- Evidence report generator renders PASS/PENDING table rows.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from execution_engine.evidence_report_generator import generate_evidence_report
from execution_engine.evidence_scanner import scan_stage_1_evidence
from execution_engine.stage_checklist_updater import update_stage_checklist


CHECKLIST_HEADER = "criterion,status,evidence,next_action\n"
CHECKLIST_ROWS = [
    "25 leads,Pending,,Add 25 qualified leads",
    "25 DMs sent,Pending,,Log 25 outbound contacts",
    "3 samples prepared,Pending,,Drop 3 sample artifacts",
    "1 proposal sent,Pending,,Send first proposal",
    "payment or PO pursued,Pending,,Pursue first paid PO",
    "weekly learning completed,Pending,,Write weekly review",
    "one system update committed,Pending,,Commit a system update",
]


def _scaffold(root: Path, contacted_count: int = 0) -> None:
    for sub in ("pipeline", "revenue", "stage", "delivery/samples", "learning"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    with (root / "pipeline/pipeline_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lead_id", "company", "stage"])
        for i in range(contacted_count):
            writer.writerow([f"L{i:03d}", f"Co{i}", "Contacted"])

    (root / "revenue/revenue_action_log.csv").write_text("ts,type,note\n", encoding="utf-8")
    (root / "stage/stage_exit_checklist.csv").write_text(
        CHECKLIST_HEADER + "\n".join(CHECKLIST_ROWS) + "\n",
        encoding="utf-8",
    )


def test_scanner_returns_known_criteria(tmp_path: Path) -> None:
    _scaffold(tmp_path)
    evidence = scan_stage_1_evidence(str(tmp_path))

    assert set(evidence.keys()) == {
        "25 leads",
        "25 DMs sent",
        "3 samples prepared",
        "1 proposal sent",
        "payment or PO pursued",
        "weekly learning completed",
        "one system update committed",
    }
    assert all(value is False for value in evidence.values())


def test_checklist_flips_to_done_when_evidence_present(tmp_path: Path) -> None:
    _scaffold(tmp_path, contacted_count=25)

    updated_path = update_stage_checklist(str(tmp_path))

    rows = list(csv.DictReader(updated_path.open(encoding="utf-8")))
    statuses = {row["criterion"]: row["status"] for row in rows}

    assert statuses["25 leads"] == "Done"
    assert statuses["25 DMs sent"] == "Done"
    assert statuses["3 samples prepared"] == "Pending"
    assert statuses["1 proposal sent"] == "Pending"


def test_checklist_updater_errors_when_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        update_stage_checklist(str(tmp_path))


def test_evidence_report_renders_pass_and_pending() -> None:
    report = generate_evidence_report({"25 leads": True, "3 samples prepared": False})
    assert "| 25 leads | PASS |" in report
    assert "| 3 samples prepared | PENDING |" in report
    assert "## Decision" in report
