"""Schema gate: every draft has the required fields and safety flags."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
QUEUE = REPO / "outputs" / "commercial_launch" / "latest" / "draft_queue.jsonl"

REQUIRED = {
    "id", "vertical", "company", "channel", "subject_en", "subject_ar",
    "body_en", "body_ar", "priority_score", "status",
    "send_allowed", "external_send_blocked", "no_auto_send", "created_at",
}


@pytest.fixture(scope="module", autouse=True)
def _gen():
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"),
                    "--target", "400"], check=True, cwd=REPO)


def test_each_draft_has_required_fields():
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        missing = REQUIRED - set(d.keys())
        assert not missing, f"{d.get('id')} missing {missing}"


def test_ids_unique():
    ids = [json.loads(l)["id"] for l in QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(ids) == len(set(ids))
