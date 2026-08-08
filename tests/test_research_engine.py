"""Tests for the Research & Discovery Engine.

Covers ICP scoring, prospect ranking, research brief generation,
batch research, safety invariants, and bilingual output.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.research_engine import (
    CompanyProfile,
    CompanySize,
    DataQuality,
    DecisionMaker,
    DecisionMakerRole,
    ICPScore,
    PainSignal,
    ProspectPriority,
    ResearchBrief,
    ResearchDepth,
    SectorFit,
    batch_research,
    generate_research_brief,
    rank_prospects,
    score_access,
    score_company_size,
    score_data_quality,
    score_pain_signals,
    score_prospect,
    score_sector_fit,
)

TENANT = "tenant_test_research"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Sector scoring
# -----------------------------------------------------------------------


class TestSectorScoring:
    def test_ideal_sector(self):
        fit, score = score_sector_fit("saas")
        assert fit == SectorFit.IDEAL
        assert score == 25.0

    def test_excluded_sector(self):
        fit, score = score_sector_fit("banking")
        assert fit == SectorFit.EXCLUDED
        assert score == 0.0

    def test_partial_match(self):
        fit, score = score_sector_fit("saas_platform")
        assert fit == SectorFit.GOOD
        assert score == 18.0

    def test_unknown_sector(self):
        fit, score = score_sector_fit("agriculture")
        assert fit == SectorFit.POSSIBLE
        assert score == 10.0

    def test_case_insensitive(self):
        fit, _ = score_sector_fit("SAAS")
        assert fit == SectorFit.IDEAL


# -----------------------------------------------------------------------
# Company size scoring
# -----------------------------------------------------------------------


class TestCompanySizeScoring:
    def test_sweet_spot(self):
        size, score = score_company_size(100)
        assert size == CompanySize.MEDIUM
        assert score == 20.0

    def test_too_small(self):
        size, score = score_company_size(5)
        assert size == CompanySize.MICRO
        assert score < 20.0

    def test_too_large(self):
        size, score = score_company_size(500)
        assert size == CompanySize.LARGE
        assert score < 20.0

    def test_enterprise(self):
        size, score = score_company_size(2000)
        assert size == CompanySize.ENTERPRISE
        assert score == 5.0

    def test_zero_employees(self):
        size, score = score_company_size(0)
        assert size == CompanySize.MICRO


# -----------------------------------------------------------------------
# Access scoring
# -----------------------------------------------------------------------


class TestAccessScoring:
    def test_founder_access(self):
        dms = (
            DecisionMaker(
                name="Test", role=DecisionMakerRole.FOUNDER_CEO,
                email="ceo@test.com", is_primary=True,
            ),
        )
        score = score_access(dms)
        assert score >= 10.0

    def test_no_decision_makers(self):
        assert score_access(()) == 0.0

    def test_max_capped_at_20(self):
        dms = tuple(
            DecisionMaker(
                name=f"DM{i}", role=DecisionMakerRole.FOUNDER_CEO,
                email=f"dm{i}@test.com", is_primary=True,
            )
            for i in range(10)
        )
        assert score_access(dms) == 20.0


# -----------------------------------------------------------------------
# Pain signal scoring
# -----------------------------------------------------------------------


class TestPainSignalScoring:
    def test_high_value_signals(self):
        signals = (PainSignal.REVENUE_LEAKAGE, PainSignal.FOLLOW_UP_GAPS)
        score = score_pain_signals(signals)
        assert score >= 12.0

    def test_no_signals(self):
        assert score_pain_signals(()) == 0.0

    def test_max_capped_at_20(self):
        signals = tuple(PainSignal)
        assert score_pain_signals(signals) == 20.0


# -----------------------------------------------------------------------
# ICP prospect scoring
# -----------------------------------------------------------------------


class TestProspectScoring:
    def _make_profile(self, **overrides):
        defaults = dict(
            tenant_id=TENANT,
            company_name="TestCo",
            sector="saas",
            employee_count=100,
            city="Riyadh",
            country="SA",
            website="https://testco.sa",
            source_id=SOURCE,
            pain_signals=(PainSignal.REVENUE_LEAKAGE, PainSignal.FOLLOW_UP_GAPS),
            decision_makers=(
                DecisionMaker(
                    name="Ahmad", role=DecisionMakerRole.FOUNDER_CEO,
                    email="ahmad@testco.sa", is_primary=True,
                ),
            ),
        )
        defaults.update(overrides)
        return CompanyProfile(**defaults)

    def test_hot_prospect(self):
        profile = self._make_profile()
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        assert score.priority == ProspectPriority.HOT
        assert score.qualified is True
        assert score.total_score >= 70

    def test_excluded_sector_disqualifies(self):
        profile = self._make_profile(sector="banking")
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        assert score.priority == ProspectPriority.DISQUALIFIED
        assert score.qualified is False

    def test_non_saudi_disqualifies(self):
        profile = self._make_profile(country="US")
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        assert score.priority == ProspectPriority.DISQUALIFIED

    def test_deterministic_id(self):
        profile = self._make_profile()
        s1 = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        s2 = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        assert s1.score_id == s2.score_id
        assert s1.score_id.startswith("icpscore_")

    def test_cold_prospect(self):
        profile = self._make_profile(
            sector="agriculture",
            employee_count=5,
            pain_signals=(),
            decision_makers=(),
            website="",
        )
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        assert score.priority in (ProspectPriority.COLD, ProspectPriority.COOL)
        assert score.qualified is False


# -----------------------------------------------------------------------
# Prospect ranking
# -----------------------------------------------------------------------


class TestProspectRanking:
    def test_sorts_by_priority_then_score(self):
        high = ICPScore(
            tenant_id=TENANT, score_id="s1", total_score=80,
            priority=ProspectPriority.HOT, qualified=True, source_id=SOURCE,
        )
        low = ICPScore(
            tenant_id=TENANT, score_id="s2", total_score=20,
            priority=ProspectPriority.COLD, qualified=False, source_id=SOURCE,
        )
        ranked = rank_prospects([low, high])
        assert ranked[0].priority == ProspectPriority.HOT
        assert ranked[-1].priority == ProspectPriority.COLD

    def test_empty_list(self):
        assert rank_prospects([]) == []


# -----------------------------------------------------------------------
# Research brief generation
# -----------------------------------------------------------------------


class TestResearchBrief:
    def _make_hot_profile(self):
        return CompanyProfile(
            tenant_id=TENANT,
            company_name="CloudSoft",
            company_name_ar="كلاود سوفت",
            sector="saas",
            employee_count=80,
            city="Riyadh",
            country="SA",
            website="https://cloudsoft.sa",
            source_id=SOURCE,
            pain_signals=(PainSignal.REVENUE_LEAKAGE, PainSignal.DATA_SCATTERED),
            decision_makers=(
                DecisionMaker(
                    name="Faisal", role=DecisionMakerRole.FOUNDER_CEO,
                    email="faisal@cloudsoft.sa", whatsapp="+966500000000",
                    is_primary=True,
                ),
            ),
        )

    def test_generates_brief(self):
        profile = self._make_hot_profile()
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        brief = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        assert isinstance(brief, ResearchBrief)
        assert brief.approval_required is True
        assert brief.auto_contact_allowed is False
        assert len(brief.talking_points) > 0
        assert brief.summary_ar
        assert brief.summary_en

    def test_deterministic_id(self):
        profile = self._make_hot_profile()
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        b1 = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        b2 = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        assert b1.brief_id == b2.brief_id
        assert b1.brief_id.startswith("research_")

    def test_hot_recommends_contact(self):
        profile = self._make_hot_profile()
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        brief = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        assert "فوري" in brief.recommended_approach or "contact" in brief.recommended_approach.lower()

    def test_disqualified_recommends_no_contact(self):
        profile = CompanyProfile(
            tenant_id=TENANT, company_name="BankCo", sector="banking",
            employee_count=5000, country="SA", source_id=SOURCE,
        )
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        brief = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        assert brief.recommended_channel == "none"

    def test_bilingual_summaries(self):
        profile = self._make_hot_profile()
        score = score_prospect(tenant_id=TENANT, profile=profile, source_id=SOURCE)
        brief = generate_research_brief(
            tenant_id=TENANT, profile=profile, icp_score=score, source_id=SOURCE,
        )
        # Arabic summary should contain Arabic text
        assert any(ord(c) > 0x600 for c in brief.summary_ar)
        # English summary should contain company name
        assert "CloudSoft" in brief.summary_en


# -----------------------------------------------------------------------
# Batch research
# -----------------------------------------------------------------------


class TestBatchResearch:
    def test_batch_returns_sorted(self):
        profiles = [
            CompanyProfile(
                tenant_id=TENANT, company_name=f"Co{i}",
                sector="saas" if i < 2 else "agriculture",
                employee_count=100 if i < 2 else 5,
                country="SA", source_id=SOURCE,
            )
            for i in range(3)
        ]
        briefs = batch_research(
            tenant_id=TENANT, profiles=profiles, source_id=SOURCE,
        )
        assert len(briefs) == 3
        # First brief should have the highest score
        assert briefs[0].icp_score.total_score >= briefs[-1].icp_score.total_score

    def test_empty_batch(self):
        briefs = batch_research(
            tenant_id=TENANT, profiles=[], source_id=SOURCE,
        )
        assert briefs == []


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestResearchEngineSafety:
    def test_icp_score_never_auto_contact(self):
        with pytest.raises(ValueError, match="auto_contact_allowed must be False"):
            ICPScore(
                tenant_id=TENANT, score_id="fake",
                auto_contact_allowed=True, source_id=SOURCE,
            )

    def test_research_brief_never_auto_contact(self):
        profile = CompanyProfile(
            tenant_id=TENANT, company_name="Test",
            source_id=SOURCE,
        )
        score = ICPScore(
            tenant_id=TENANT, score_id="s1",
            auto_contact_allowed=False, source_id=SOURCE,
        )
        with pytest.raises(ValueError, match="auto_contact_allowed must be False"):
            ResearchBrief(
                tenant_id=TENANT, profile=profile, icp_score=score,
                auto_contact_allowed=True, approval_required=True,
                source_id=SOURCE,
            )

    def test_research_brief_requires_approval(self):
        profile = CompanyProfile(
            tenant_id=TENANT, company_name="Test",
            source_id=SOURCE,
        )
        score = ICPScore(
            tenant_id=TENANT, score_id="s1",
            auto_contact_allowed=False, source_id=SOURCE,
        )
        with pytest.raises(ValueError, match="approval_required must be True"):
            ResearchBrief(
                tenant_id=TENANT, profile=profile, icp_score=score,
                auto_contact_allowed=False, approval_required=False,
                source_id=SOURCE,
            )
