"""Readiness aggregates drafts + safety into a report and metrics."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
METRICS = REPO / "outputs" / "commercial_launch" / "latest" / "daily_metrics.json"
REPORT = REPO / "docs" / "commercial-launch" / "99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md"


@pytest.fixture(scope="module", autouse=True)
def _run():
    for script in ("commercial_generate_400_drafts.py", "commercial_safety_audit.py",
                   "commercial_launch_readiness.py"):
        args = [sys.executable, str(REPO / "scripts" / script)]
        if script.endswith("400_drafts.py"):
            args += ["--target", "400"]
        subprocess.run(args, check=True, cwd=REPO)


def test_report_exists():
    assert REPORT.exists()
    assert "Commercial Launch Readiness" in REPORT.read_text(encoding="utf-8")


def test_metrics_ready():
    m = json.loads(METRICS.read_text(encoding="utf-8"))
    assert m["draft_count"] >= 400
    assert m["safety_pass"] is True
    assert m["commercially_ready"] is True
