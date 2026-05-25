from __future__ import annotations

"""Subprocess smoke tests for `python -m dealix_cli`."""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    # Ensure repo root is importable regardless of cwd.
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{REPO_ROOT}{os.pathsep}{existing}" if existing else str(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, "-m", "dealix_cli", *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(cwd or REPO_ROOT),
        env=env,
    )


def test_cli_stage_exits_zero_on_empty_private_ops(tmp_path: Path) -> None:
    result = _run(["stage", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert "Current stage:" in result.stdout


def test_cli_sprint_exits_zero(tmp_path: Path) -> None:
    result = _run(["sprint", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert "Revenue Sprint Kit" in result.stdout


def test_cli_kit_exits_zero(tmp_path: Path) -> None:
    result = _run(["kit", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert "Sprint Kit Checklist" in result.stdout


def test_cli_daily_writes_brief(tmp_path: Path) -> None:
    result = _run(["daily", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "founder" / "daily_brief.md").exists()


def test_cli_advance_blocks_with_empty_ops(tmp_path: Path) -> None:
    result = _run(["advance", "--private-ops", str(tmp_path)])
    # Empty ops can't advance: expect non-zero exit.
    assert result.returncode != 0
    assert "Blockers" in result.stdout or "Not eligible" in result.stdout


def test_cli_close_day_appends_log(tmp_path: Path) -> None:
    result = _run(["close-day", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "founder" / "founder_time_log.md").exists()


def test_cli_weekly_writes_files(tmp_path: Path) -> None:
    result = _run(["weekly", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "metrics_history" / "weekly_metrics.csv").exists()
    assert (tmp_path / "founder" / "ceo_dashboard.md").exists()


def test_cli_dashboard_writes_json(tmp_path: Path) -> None:
    result = _run(["dashboard", "--private-ops", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "dashboard_data" / "company_metrics.json").exists()


def test_cli_help_lists_subcommands() -> None:
    result = _run(["--help"])
    assert result.returncode == 0
    for cmd in ("sprint", "kit", "stage", "daily", "advance", "weekly", "dashboard", "verify"):
        assert cmd in result.stdout
