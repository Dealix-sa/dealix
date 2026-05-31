from __future__ import annotations

from dealix.hermes.partners.program import (
    CoMarketingProposal,
    PartnerTier,
    check_partner_claim,
    classify_partner_tier,
    compute_revenue_share,
    review_co_marketing,
    review_partner_performance,
    run_partner_compliance,
    score_enablement,
)


def test_approved_claim_blocks_guarantee():
    res = check_partner_claim(
        "Dealix guarantees sales and is 100% secure."
    )
    assert res.safe is False
    assert any("forbidden_claim" in f for f in res.findings)


def test_tier_classification_strategic():
    t = classify_partner_tier(
        enablement_score=90,
        verified_revenue_sar_last_12mo=600_000,
        customer_complaints=0,
        compliance_pass=True,
        has_signed_partner_agreement=True,
    )
    assert t.tier == PartnerTier.STRATEGIC


def test_tier_classification_applicant_when_no_agreement():
    t = classify_partner_tier(
        enablement_score=90,
        verified_revenue_sar_last_12mo=1_000_000,
        customer_complaints=0,
        compliance_pass=True,
        has_signed_partner_agreement=False,
    )
    assert t.tier == PartnerTier.APPLICANT


def test_revenue_share_capped_at_50pct():
    split = compute_revenue_share(
        partner_id="agency_xyz",
        tier=PartnerTier.STRATEGIC,
        deal_sar=10_000,
        sourced_by_partner=True,
        delivered_by_partner=True,
    )
    assert split.partner_share_sar <= 5000


def test_compliance_check_lists_missing():
    res = run_partner_compliance(
        "agency_xyz",
        {"signed_partner_agreement": True, "approved_claims_acknowledgement": True},
    )
    assert res.passed is False
    assert "data_processing_addendum_signed" in res.failing
    assert "no_open_compliance_incidents" in res.failing


def test_enablement_score():
    progress = score_enablement(
        "agency_xyz",
        ["positioning_training", "delivery_playbook_walkthrough"],
    )
    assert progress.score == 40.0
    assert "approved_claims_quiz" in progress.pending


def test_co_marketing_blocks_unsupported_channel():
    proposal = CoMarketingProposal(
        partner_id="agency_xyz",
        asset_title="Trust briefing",
        asset_body="Dealix helps prepare governance packs.",
        proposed_channels=["linkedin_dm_blast"],
    )
    review = review_co_marketing(proposal)
    assert review.approved is False
    assert any("unsupported_channel" in f for f in review.findings)


def test_performance_review_triggers_actions():
    rev = review_partner_performance(
        partner_id="agency_xyz",
        quarter="2026Q2",
        verified_revenue_sar=20_000,
        customer_satisfaction_avg=3.5,
        customer_complaints=4,
        enablement_score=50,
    )
    assert any("compliance review" in a for a in rev.actions)
    assert any("re-enroll" in a for a in rev.actions)
