"""Tests for the CEO Operating System CLIs and audits.

Each test is hermetic: it runs the CLI as a subprocess with a temporary
ROOT and verifies the contract documented in docs/founder/.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts" / "ceo"


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def staged_repo(tmp_path: Path) -> Path:
    """Clone the minimum subset of the repo into a tmp workspace and stage."""

    workspace = tmp_path / "dealix"
    workspace.mkdir()

    (workspace / "scripts" / "ceo").mkdir(parents=True)
    for src in SCRIPTS.glob("*.py"):
        shutil.copy(src, workspace / "scripts" / "ceo" / src.name)

    docs = workspace / "docs" / "founder"
    docs.mkdir(parents=True)
    shutil.copy(
        REPO_ROOT / "docs" / "founder" / "DAILY_COMMAND_BRIEF.md",
        docs / "DAILY_COMMAND_BRIEF.md",
    )
    shutil.copy(
        REPO_ROOT / "docs" / "founder" / "WEEKLY_CEO_REVIEW.md",
        docs / "WEEKLY_CEO_REVIEW.md",
    )

    result = _run(["scripts/ceo/stage_private_ops.py"], workspace)
    assert result.returncode == 0, result.stderr
    assert (workspace / "dealix-ops-private").is_dir()
    return workspace


def test_stage_is_idempotent(staged_repo: Path) -> None:
    """Running stage twice must not create new files on the second run."""
    second = _run(["scripts/ceo/stage_private_ops.py"], staged_repo)
    assert second.returncode == 0, second.stderr
    assert "created : 0" in second.stdout


def test_stage_creates_expected_structure(staged_repo: Path) -> None:
    private = staged_repo / "dealix-ops-private"
    expected_dirs = [
        "founder",
        "revenue/invoices",
        "sales/call_notes",
        "delivery/reports",
        "client_success/feedback",
        "trust/audits",
        "finance",
        "product",
        "engineering",
        "content/case_study_consents",
        "people/scorecards",
        "partners/scorecards",
    ]
    for rel in expected_dirs:
        assert (private / rel).is_dir(), f"missing dir {rel}"

    expected_csvs = [
        "revenue/cash_collected.csv",
        "revenue/mrr_tracker.csv",
        "sales/pipeline.csv",
        "sales/dms_sent.csv",
        "delivery/sprint_register.csv",
        "client_success/retainers.csv",
        "finance/expenses.csv",
        "engineering/dora.csv",
        "partners/referrals.csv",
    ]
    for rel in expected_csvs:
        path = private / rel
        assert path.is_file(), f"missing csv {rel}"
        assert path.read_text(encoding="utf-8").strip(), f"empty csv {rel}"


def test_daily_brief_creates_from_template(staged_repo: Path) -> None:
    target = staged_repo / "dealix-ops-private" / "founder" / "daily_brief.md"
    if target.exists():
        target.unlink()
    result = _run(["scripts/ceo/daily_brief.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    assert target.is_file()
    body = target.read_text(encoding="utf-8")
    assert "## Date:" in body
    assert "yyyy-mm-dd" not in body


def test_close_day_appends_time_log(staged_repo: Path) -> None:
    log = staged_repo / "dealix-ops-private" / "founder" / "founder_time_log.md"
    initial = log.read_text(encoding="utf-8") if log.exists() else ""
    result = _run(["scripts/ceo/close_day.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    final = log.read_text(encoding="utf-8")
    assert final != initial
    assert "total_hours:" in final


def test_dashboard_renders_with_empty_ledgers(staged_repo: Path) -> None:
    result = _run(["scripts/ceo/dashboard.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    target = staged_repo / "dealix-ops-private" / "founder" / "master_dashboard.md"
    assert target.is_file()
    body = target.read_text(encoding="utf-8")
    assert "Master CEO Dashboard" in body
    assert "Cash collected (MTD)" in body
    assert "Pipeline" in body


def test_dashboard_picks_up_paid_cash(staged_repo: Path) -> None:
    private = staged_repo / "dealix-ops-private"
    csv_path = private / "revenue" / "cash_collected.csv"
    today = "2026-05-23"
    csv_path.write_text(
        "date,invoice_no,customer,amount_sar,method,status,notes\n"
        f"{today},INV-0001,ACME,4500,bank,paid,Sprint #1\n",
        encoding="utf-8",
    )
    result = _run(["scripts/ceo/dashboard.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    body = (private / "founder" / "master_dashboard.md").read_text(encoding="utf-8")
    assert "4,500 SAR" in body


def test_advance_logs_marker(staged_repo: Path) -> None:
    result = _run(["scripts/ceo/advance.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    marker = staged_repo / "dealix-ops-private" / "founder" / "advance_log.md"
    assert marker.is_file()
    assert "advance check run" in marker.read_text(encoding="utf-8")


def test_kit_lists_all_sprint_files(staged_repo: Path) -> None:
    sprint_docs = REPO_ROOT / "docs" / "delivery" / "revenue_sprint"
    workspace_sprint = staged_repo / "docs" / "delivery" / "revenue_sprint"
    workspace_sprint.mkdir(parents=True, exist_ok=True)
    for md in sprint_docs.glob("*.md"):
        shutil.copy(md, workspace_sprint / md.name)
    result = _run(["scripts/ceo/kit.py"], staged_repo)
    assert result.returncode == 0, result.stderr
    assert "Revenue Sprint Kit" in result.stdout
    assert "REVENUE_SPRINT_FACTORY.md" in result.stdout
    assert "✗" not in result.stdout, "all kit files should exist (✓)"


def test_audit_passes_against_ceo_os_surface() -> None:
    """The new CEO OS surface must be clean of doctrine + PII violations."""

    result = subprocess.run(
        [sys.executable, "scripts/ceo/audit.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "CEO OS audit must be clean; got findings:\n" + result.stdout
    )
    assert "no doctrine or PII violations" in result.stdout


def test_audit_supports_all_flag() -> None:
    """--all must still be available (one-time cleanup pass)."""

    result = subprocess.run(
        [sys.executable, "scripts/ceo/audit.py", "--all"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # We do not assert a specific outcome (legacy may have findings);
    # we just confirm the flag is supported and the script ran.
    assert result.returncode in {0, 1}
    assert ("all of docs/" in result.stdout) or ("findings" in result.stdout.lower())
