"""No external-send capability anywhere in the commercial launch surface."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
QUEUE = REPO / "outputs" / "commercial_launch" / "latest" / "draft_queue.jsonl"

CONTENT_SCRIPTS = [
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "scripts/commercial_launch_readiness.py",
    "scripts/media_social_calendar_generate.py",
]
FORBIDDEN_TERMS = ["smtp", "whatsapp", "linkedin"]


@pytest.fixture(scope="module", autouse=True)
def _gen():
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"),
                    "--target", "400"], check=True, cwd=REPO)


def test_no_draft_is_sendable():
    drafts = [json.loads(l) for l in QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert sum(1 for d in drafts if d.get("send_allowed")) == 0


def test_content_scripts_have_no_forbidden_terms():
    for rel in CONTENT_SCRIPTS:
        low = (REPO / rel).read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_TERMS:
            assert term not in low, f"{term} found in {rel}"
