"""API static check: commercial surface has no external-send patterns."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "final_launch_control" / "api_commercial_static_check.json"


def test_api_commercial_static_check_passes():
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "api_commercial_static_check.py")], cwd=REPO)
    assert r.returncode == 0
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["pass"] is True
    assert data.get("send_pattern_violations", []) == []
