"""Safety audit passes on a freshly generated draft queue."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "outputs" / "commercial_launch" / "latest" / "safety_audit.json"


@pytest.fixture(scope="module", autouse=True)
def _run():
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"),
                    "--target", "400"], check=True, cwd=REPO)
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_safety_audit.py")], cwd=REPO)
    assert r.returncode == 0


def test_audit_passes():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["pass"] is True
    assert data["checks"]["send_allowed_true_count"] == 0
    assert data["checks"]["external_send_blocked_false_count"] == 0
    assert data["checks"]["no_auto_send_false_count"] == 0
    assert data["checks"]["no_forbidden_claims"] is True
