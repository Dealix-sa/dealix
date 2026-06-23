"""Test that run_brain_day generates the expected reports."""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

import pytest

# Ensure the repo root is importable when running from the repo root.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from scripts.brain.run_brain_day import run_brain_day


def test_run_brain_day_generates_reports(tmp_path):
    """run_brain_day should create summary, memo, and plan files."""
    result = run_brain_day(reports_dir=str(tmp_path))
    reports = result.get("reports", {})

    # All three report paths should be present.
    assert "summary" in reports
    assert "memo" in reports
    assert "plan" in reports

    # Each file should exist and be non-empty.
    for key, path in reports.items():
        assert os.path.exists(path), f"{key} report not found at {path}"
        assert os.path.getsize(path) > 0, f"{key} report is empty at {path}"

    # The summary report should mention the date.
    with open(reports["summary"], encoding="utf-8") as fh:
        summary_text = fh.read()
    today = datetime.now(timezone.utc).date().isoformat()
    assert today in summary_text, "Summary report should reference today's date"


def test_run_brain_day_returns_bottleneck_count(tmp_path):
    """run_brain_day should return a numeric bottleneck_count."""
    result = run_brain_day(reports_dir=str(tmp_path))
    assert isinstance(result.get("bottleneck_count"), int)