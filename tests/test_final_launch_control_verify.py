"""Master verification gate passes after the full pipeline runs."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RESULT = REPO / "outputs" / "final_launch_control" / "final_verification.json"

PIPELINE = [
    ("commercial_generate_400_drafts.py", ["--target", "400"]),
    ("commercial_safety_audit.py", []),
    ("commercial_launch_readiness.py", []),
    ("media_social_calendar_generate.py", []),
    ("final_launch_control_verify.py", []),
]


@pytest.fixture(scope="module", autouse=True)
def _run():
    for script, extra in PIPELINE:
        subprocess.run([sys.executable, str(REPO / "scripts" / script), *extra],
                       check=True, cwd=REPO)


def test_overall_pass():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["overall_pass"] is True, f"critical: {data['critical_failures']}"
    assert data["draft_count"] >= 400


def test_no_critical_failures():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["critical_failures"] == []
