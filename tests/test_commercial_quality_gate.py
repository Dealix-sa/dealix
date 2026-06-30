"""Quality gate: drafts are bilingual, scored, and prioritized."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LATEST = REPO / "outputs" / "commercial_launch" / "latest"


@pytest.fixture(scope="module", autouse=True)
def _gen():
    subprocess.run([sys.executable, str(REPO / "scripts" / "commercial_generate_400_drafts.py"),
                    "--target", "400"], check=True, cwd=REPO)


def _drafts():
    return [json.loads(l) for l in (LATEST / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def test_bilingual_and_scored():
    for d in _drafts():
        assert d["body_en"].strip()
        assert d["body_ar"].strip()
        assert 0 <= d["priority_score"] <= 100


def test_top_50_present():
    top = (LATEST / "top_50_priority.md").read_text(encoding="utf-8")
    assert "Top 50" in top
    assert top.count("DRAFT-") >= 50


def test_founder_review_present():
    rev = (LATEST / "founder_review.md").read_text(encoding="utf-8")
    assert "Founder Review Queue" in rev
