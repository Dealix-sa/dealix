"""Quality gate: drafts are bilingual, scored, and well-formed."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT  # noqa: F401

from launch_os.drafts import generate_drafts
from launch_os.leads import VERTICALS


def test_bilingual_and_nonempty():
    for d in generate_drafts(target=400):
        for f in ("subject_en", "subject_ar", "body_en", "body_ar"):
            assert d[f] and isinstance(d[f], str) and len(d[f].strip()) > 10


def test_priority_in_range():
    for d in generate_drafts(target=400):
        assert 0 <= d["priority_score"] <= 100
        assert 40 <= d["icp_score"] <= 95


def test_all_five_verticals_present():
    verticals = {d["vertical"] for d in generate_drafts(target=400)}
    assert {v["key"] for v in VERTICALS}.issubset(verticals)


def test_arabic_body_contains_arabic():
    sample = generate_drafts(target=10)
    for d in sample:
        assert any("؀" <= ch <= "ۿ" for ch in d["body_ar"])
