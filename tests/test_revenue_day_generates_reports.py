"""Test that run_revenue_day.py generates latest.md and latest.json reports.

Uses a temp directory to avoid polluting the real repo ledgers.
Usage:
    python -m pytest tests/test_revenue_day_generates_reports.py -q
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def temp_revenue_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary repo root with ledgers, reports, outbox dirs."""
    # Copy essential structure to temp
    (tmp_path / "ledgers").mkdir()
    (tmp_path / "outbox").mkdir()
    (tmp_path / "reports" / "revenue").mkdir(parents=True)
    (tmp_path / "data" / "outreach").mkdir(parents=True)

    # Write empty ledger CSVs
    from scripts.revenue._lib import LEDGER_SCHEMAS
    import csv

    for name, fields in LEDGER_SCHEMAS.items():
        with (tmp_path / "ledgers" / f"{name}.csv").open("w", encoding="utf-8-sig", newline="") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()

    # Point REPO_ROOT to temp via env
    monkeypatch.setenv("DEALIX_REPO_ROOT", str(tmp_path))
    # Reimport _lib so REPO_ROOT picks up the env var
    for mod_name in list(sys.modules):
        if mod_name.startswith("scripts.revenue"):
            del sys.modules[mod_name]
    # Re-add the repo root to path
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    return tmp_path


def test_run_revenue_day_generates_latest_md_and_json(temp_revenue_workspace: Path) -> None:
    from scripts.revenue._lib import ensure_ledgers, REPO_ROOT
    ensure_ledgers()

    # Seed demo data so there are prospects to process
    from scripts.revenue import seed_demo_revenue_data
    seed_demo_revenue_data.main()

    # Run the revenue day
    from scripts.revenue import run_revenue_day
    rc = run_revenue_day.main()
    assert rc == 0, "run_revenue_day.py should exit 0"

    # Check latest.md and latest.json exist in reports/revenue/
    latest_md = REPO_ROOT / "reports" / "revenue" / "latest.md"
    latest_json = REPO_ROOT / "reports" / "revenue" / "latest.json"

    assert latest_md.exists(), f"Missing {latest_md}"
    assert latest_json.exists(), f"Missing {latest_json}"

    # Validate JSON is parseable and has expected keys
    report = json.loads(latest_json.read_text(encoding="utf-8"))
    assert "date" in report
    assert "prospects" in report
    assert "next_actions_today" in report
    assert isinstance(report["prospects"], dict)
    assert "total" in report["prospects"]


def test_run_revenue_day_generates_dated_folder(temp_revenue_workspace: Path) -> None:
    from scripts.revenue._lib import REPO_ROOT, ensure_ledgers, today_str
    ensure_ledgers()

    from scripts.revenue import seed_demo_revenue_data, run_revenue_day
    seed_demo_revenue_data.main()
    run_revenue_day.main()

    dated_dir = REPO_ROOT / "reports" / "revenue" / today_str()
    assert dated_dir.exists(), f"Missing dated report folder {dated_dir}"