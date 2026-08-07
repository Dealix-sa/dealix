"""Media/social verification: planning-only, no auto-post code."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "media_social" / "final_media_social_verification.json"


def test_media_social_verify_passes():
    subprocess.run([sys.executable, str(REPO / "scripts" / "media_social_calendar_generate.py")],
                   check=True, cwd=REPO)
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "media_social_verify.py")], cwd=REPO)
    assert r.returncode == 0
    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["pass"] is True
    assert data["auto_post_disabled"] is True
    assert data["auto_post_code_violations"] == []
