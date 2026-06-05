"""Dealix Targeting OS — draft lab generates clean, gated, founder-review drafts."""

from __future__ import annotations

from scripts.targeting_draft_lab import (
    BANNED_PHRASES,
    build_draft,
    eligible_for_draft,
    render_drafts_markdown,
    validate_draft,
)

ELIGIBLE = {
    "company_name": "Acme Consulting",
    "sector": "b2b_consulting",
    "grade": "A",
    "targeting_score": 84,
    "evidence_count": 2,
    "source_urls": ["https://acme.example/services", "https://acme.example/case-studies"],
    "pain_signals": ["no_case_studies"],
    "recommended_offer": "Command Sprint",
    "draft_status": "needs_approval",
}


def test_validate_draft_flags_banned_phrase():
    bad = "نضمن لكم مبيعات خلال أسبوع"
    hits = validate_draft(bad)
    assert hits  # at least one banned phrase detected


def test_validate_draft_clean_text():
    assert validate_draft("نبدأ بتشخيص مختصر قابل للمراجعة") == []


def test_generated_draft_has_no_banned_phrases():
    draft = build_draft(ELIGIBLE)
    assert draft["violations"] == []
    low = draft["body"].lower()
    for phrase in BANNED_PHRASES:
        assert phrase.lower() not in low


def test_draft_status_is_needs_approval():
    draft = build_draft(ELIGIBLE)
    assert draft["draft_status"] == "needs_approval"


def test_draft_cites_evidence():
    draft = build_draft(ELIGIBLE)
    assert draft["evidence_cited"]
    assert len(draft["evidence_cited"]) <= 2
    assert all(u.startswith("http") for u in draft["evidence_cited"])


def test_draft_has_single_cta():
    draft = build_draft(ELIGIBLE)
    assert draft["cta"]
    # exactly one question mark / call to action in the body
    assert draft["body"].count("؟") == 1


def test_eligibility_requires_a_grade():
    company = dict(ELIGIBLE, grade="B")
    ok, reason = eligible_for_draft(company)
    assert ok is False
    assert reason == "grade_below_A"


def test_eligibility_requires_two_evidence():
    company = dict(ELIGIBLE, evidence_count=1, source_urls=["https://acme.example/services"])
    ok, reason = eligible_for_draft(company)
    assert ok is False
    assert "evidence_below" in reason


def test_eligibility_requires_min_score():
    company = dict(ELIGIBLE, targeting_score=70)
    ok, reason = eligible_for_draft(company)
    assert ok is False
    assert "score_below" in reason


def test_eligible_company_passes():
    ok, reason = eligible_for_draft(ELIGIBLE)
    assert ok is True
    assert reason == "ok"


def test_render_markdown_contains_company_and_status():
    md = render_drafts_markdown([build_draft(ELIGIBLE)])
    assert "Acme Consulting" in md
    assert "needs_approval" in md
    assert "لا يُرسل أي شيء تلقائيًا" in md
