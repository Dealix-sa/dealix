"""Smoke tests for the Wave 6 Revenue Operating Rhythm scaffolding."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def test_verify_wave6_exits_zero() -> None:
    proc = _run("scripts/verify_wave6_revenue_rhythm.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WAVE6_READY=true" in proc.stdout


def test_founder_daily_command_on_empty_ledgers() -> None:
    proc = _run("scripts/founder_daily_command.py", "--out", "-")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Founder Daily Command" in proc.stdout


def test_founder_daily_command_json() -> None:
    proc = _run("scripts/founder_daily_command.py", "--format", "json", "--out", "-")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert '"top_actions"' in proc.stdout


def test_create_customer_workspace_dry_run() -> None:
    proc = _run("scripts/create_customer_workspace.py", "--name", "demo-co", "--dry-run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "00_intake.md" in proc.stdout


def test_create_customer_workspace_rejects_bad_name() -> None:
    proc = _run("scripts/create_customer_workspace.py", "--name", "!!!", "--dry-run")
    assert proc.returncode == 2
