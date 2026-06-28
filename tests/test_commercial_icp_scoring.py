"""ICP scoring is deterministic, bounded and penalises missing data."""

from __future__ import annotations

from app.commercial import icp_scoring
from app.commercial.schemas import CommercialAccount


def _account(**kw):
    base = dict(
        account_id="a1",
        company_name="Co",
        sector="retail",
        city="riyadh",
        source_url="https://example.com",
        public_email="x@y.com",
        pain_hypothesis="leads go unanswered",
        recommended_motion="sales_prospecting",
        verification_status="verified",
        contactability_status="contactable",
        risk_level="low",
    )
    base.update(kw)
    return CommercialAccount(**base)


def test_score_is_bounded_0_100():
    res = icp_scoring.score_account(_account())
    assert 0.0 <= res["score"] <= 100.0


def test_strong_fit_scores_high():
    res = icp_scoring.score_account(_account())
    assert res["score"] >= 70
    assert res["tier"] == "A"


def test_missing_source_lowers_score_and_is_flagged():
    res = icp_scoring.score_account(_account(source_url=""))
    assert any("source" in r.lower() for r in res["rationale"])
    assert res["breakdown"]["source_present"] == 0.0


def test_off_icp_sector_scores_lower_than_on_icp():
    on = icp_scoring.score_account(_account(sector="retail"))
    off = icp_scoring.score_account(_account(sector="mining"))
    assert off["score"] < on["score"]


def test_high_risk_penalty_applied():
    low = icp_scoring.score_account(_account(risk_level="low"))
    high = icp_scoring.score_account(_account(risk_level="high"))
    assert high["score"] < low["score"]


def test_apply_score_writes_back():
    acc = _account()
    icp_scoring.apply_score(acc)
    assert acc.icp_score > 0
