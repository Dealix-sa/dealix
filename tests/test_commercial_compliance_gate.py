"""Compliance gate: no forbidden/exaggerated claims; safety audit passes."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LATEST = REPO / "outputs" / "commercial_launch" / "latest"
FORBIDDEN = ["guaranteed roi", "100%", "replace your team", "automate everything", "no human needed"]


@pytest.fixture(scope="module", autouse=True)
def _run():
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"),
                    "--target", "400"], check=True, cwd=REPO)
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_safety_audit.py")],
                   check=True, cwd=REPO)


def test_no_forbidden_claims_in_bodies():
    drafts = [json.loads(l) for l in (LATEST / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    for d in drafts:
        text = " ".join(str(d.get(k, "")) for k in ("subject_en", "subject_ar", "body_en", "body_ar")).lower()
        for c in FORBIDDEN:
            assert c not in text


def test_safety_audit_pass():
    data = json.loads((LATEST / "safety_audit.json").read_text(encoding="utf-8"))
    assert data["pass"] is True
