"""Draft factory: generates >=400 review-only drafts with safe flags."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
QUEUE = REPO / "outputs" / "commercial_launch" / "latest" / "draft_queue.jsonl"


@pytest.fixture(scope="module", autouse=True)
def _generate():
    subprocess.run(
        [sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"), "--target", "400"],
        check=True, cwd=REPO,
    )


def _drafts():
    return [json.loads(l) for l in QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_at_least_400_drafts():
    assert len(_drafts()) >= 400


def test_every_draft_review_only():
    for d in _drafts():
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["no_auto_send"] is True
        assert d["status"] == "draft_for_review"


def test_target_floor_is_enforced():
    subprocess.run(
        [sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"), "--target", "10"],
        check=True, cwd=REPO,
    )
    assert len(_drafts()) >= 400
