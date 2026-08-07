"""Site static check runs and reports no forbidden claims."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "final_launch_control" / "site_static_check.json"


def test_site_static_check_passes():
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "site_launch_static_check.py")], cwd=REPO)
    assert r.returncode == 0
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["pass"] is True
    if data.get("web_present"):
        assert data["checks"]["no_forbidden_claims"] is True
