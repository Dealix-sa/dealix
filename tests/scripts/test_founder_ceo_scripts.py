"""Smoke tests for the four founder-CEO report-generator scripts.

These tests exercise the scripts via subprocess so they stay isolated from
the heavier project-level conftest (which initializes LLM mocks). Each
script gets three checks:

  1. --help works (sanity)
  2. running with no inputs is graceful (templates seeded or message shown)
  3. for the decision-log writer: --dry-run does NOT write to disk
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"

LEVERAGE = SCRIPTS_DIR / "generate_founder_leverage_report.py"
CAPITAL = SCRIPTS_DIR / "generate_capital_allocation_report.py"
ASSUMPTIONS = SCRIPTS_DIR / "generate_strategic_assumptions_review.py"
DECISION_LOG = SCRIPTS_DIR / "generate_decision_log_entry.py"


def _run(args: list[str], cwd: Path | None = None, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# generate_founder_leverage_report.py
# ---------------------------------------------------------------------------


def test_leverage_help() -> None:
    result = _run([str(LEVERAGE), "--help"])
    assert result.returncode == 0
    assert "founder-leverage" in result.stdout.lower() or "leverage" in result.stdout.lower()


def test_leverage_no_input_seeds_template(tmp_path: Path) -> None:
    input_csv = tmp_path / "founder_time_audit.csv"
    out_path = tmp_path / "report.md"
    result = _run([
        str(LEVERAGE),
        "--input",
        str(input_csv),
        "--out",
        str(out_path),
    ])
    assert result.returncode == 0
    assert input_csv.exists()
    text = input_csv.read_text()
    assert "date,category,hours" in text.replace(" ", "")


# ---------------------------------------------------------------------------
# generate_capital_allocation_report.py
# ---------------------------------------------------------------------------


def test_capital_help() -> None:
    result = _run([str(CAPITAL), "--help"])
    assert result.returncode == 0
    assert "capital" in result.stdout.lower()


def test_capital_no_input_seeds_or_prints(tmp_path: Path) -> None:
    input_yaml = tmp_path / "capital_allocation.yaml"
    result = _run([
        str(CAPITAL),
        "--input",
        str(input_yaml),
    ])
    assert result.returncode == 0
    # Either the canonical modules produced a snapshot (markdown printed to
    # stdout) or the template was seeded. One of those two is true.
    seeded = input_yaml.exists()
    printed_report = "capital allocation snapshot" in result.stdout.lower()
    assert seeded or printed_report


# ---------------------------------------------------------------------------
# generate_strategic_assumptions_review.py
# ---------------------------------------------------------------------------


def test_assumptions_help() -> None:
    result = _run([str(ASSUMPTIONS), "--help"])
    assert result.returncode == 0
    assert "assumption" in result.stdout.lower()


def test_assumptions_missing_register_is_graceful(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.md"
    result = _run([
        str(ASSUMPTIONS),
        "--register",
        str(missing),
    ])
    assert result.returncode == 0
    assert "register not initialized" in result.stdout.lower()


def test_assumptions_parses_real_register(tmp_path: Path) -> None:
    register = REPO_ROOT / "docs" / "founder" / "STRATEGIC_ASSUMPTIONS_REGISTER.md"
    if not register.exists():
        # Skip silently if the content agent hasn't shipped the register.
        return
    out_path = tmp_path / "review.md"
    result = _run([
        str(ASSUMPTIONS),
        "--register",
        str(register),
        "--as-of",
        "2026-05-24",
        "--out",
        str(out_path),
    ])
    assert result.returncode == 0, result.stderr
    assert out_path.exists()
    report = out_path.read_text()
    assert "Strategic assumptions review" in report


# ---------------------------------------------------------------------------
# generate_decision_log_entry.py
# ---------------------------------------------------------------------------


def test_decision_log_help() -> None:
    result = _run([str(DECISION_LOG), "--help"])
    assert result.returncode == 0
    assert "decision" in result.stdout.lower()


def test_decision_log_requires_decision() -> None:
    result = _run([str(DECISION_LOG)])
    assert result.returncode != 0
    assert "decision" in result.stderr.lower()


def test_decision_log_dry_run_does_not_write(tmp_path: Path) -> None:
    log_path = tmp_path / "decision_log.jsonl"
    result = _run([
        str(DECISION_LOG),
        "--decision",
        "Adopt vertical playbook for clinics",
        "--context",
        "weekly review",
        "--owner",
        "<founder>",
        "--tags",
        "strategy,vertical",
        "--out",
        str(log_path),
        "--dry-run",
    ])
    assert result.returncode == 0, result.stderr
    assert not log_path.exists(), "dry-run must not write to disk"
    # stdout should be a single JSON line with the decision text.
    assert "Adopt vertical playbook for clinics" in result.stdout


def test_decision_log_writes_when_not_dry_run(tmp_path: Path) -> None:
    log_path = tmp_path / "decision_log.jsonl"
    result = _run([
        str(DECISION_LOG),
        "--decision",
        "Pause LinkedIn experiments",
        "--owner",
        "<founder>",
        "--out",
        str(log_path),
    ])
    assert result.returncode == 0, result.stderr
    assert log_path.exists()
    line = log_path.read_text().strip()
    assert "Pause LinkedIn experiments" in line


def test_decision_log_rejects_oversized_decision(tmp_path: Path) -> None:
    log_path = tmp_path / "decision_log.jsonl"
    oversized = "x" * 281
    result = _run([
        str(DECISION_LOG),
        "--decision",
        oversized,
        "--out",
        str(log_path),
    ])
    assert result.returncode != 0
    assert not log_path.exists()
