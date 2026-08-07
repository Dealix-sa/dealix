"""CRM schema verification: required fields, valid stages, no send fields."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "final_launch_control" / "crm_schema_verification.json"


def test_crm_schema_verify_passes():
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_crm_schema_verify.py")], cwd=REPO)
    assert r.returncode == 0
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["pass"] is True
    assert data["errors"] == []
    assert data["lead_count"] >= 5
