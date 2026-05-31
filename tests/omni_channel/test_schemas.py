"""Tests for omni_channel_os schemas — model construction and computed fields."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    AutomationLevel,
    ChannelAsset,
    ChannelDecision,
    ChannelType,
    Company,
    CompanySize,
    DailyQuota,
    FounderReviewItem,
    GCCCountry,
    InboundLead,
    Language,
    LeadCapture,
    LearningSignal,
    OmniChannelBrief,
    PlaybookUpdate,
    ReviewAction,
    RiskLevel,
    Sector,
)
from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper


def _make_company(**kwargs) -> Company:
    defaults = dict(name="Test Co", sector=Sector.legal, country=GCCCountry.KSA)
    defaults.update(kwargs)
    return Company(**defaults)


def _make_asset(body: str = "Hello world test body for asset content", **kwargs) -> ChannelAsset:
    defaults = dict(
        company_id="abc123",
        asset_type=AssetType.email_draft,
        channel=ChannelType.email,
        language=Language.arabic,
        body=body,
        cta="احصل على تشخيص مجاني",
    )
    defaults.update(kwargs)
    return ChannelAsset(**defaults)


class TestCompany:
    def test_default_id_generated(self) -> None:
        c = _make_company()
        assert len(c.id) == 12

    def test_default_sector_other(self) -> None:
        c = Company(name="X")
        assert c.sector == Sector.other

    def test_all_gcc_countries(self) -> None:
        for country in GCCCountry:
            c = _make_company(country=country)
            assert c.country == country

    def test_enrichment_score_bounds(self) -> None:
        with pytest.raises(Exception):
            _make_company(enrichment_score=101)
        with pytest.raises(Exception):
            _make_company(enrichment_score=-1)


class TestChannelAsset:
    def test_word_count_computed(self) -> None:
        asset = _make_asset(body="one two three four five")
        assert asset.word_count == 5

    def test_requires_founder_approval_default(self) -> None:
        asset = _make_asset()
        assert asset.requires_founder_approval is True

    def test_is_auto_sendable_default_false(self) -> None:
        asset = _make_asset()
        assert asset.is_auto_sendable is False

    def test_quality_score_bounds(self) -> None:
        with pytest.raises(Exception):
            _make_asset(quality_score=101.0)
        with pytest.raises(Exception):
            _make_asset(quality_score=-1.0)

    def test_approval_status_default(self) -> None:
        asset = _make_asset()
        assert asset.approval_status == "pending"


class TestDailyQuota:
    def test_total_assets_done(self) -> None:
        q = DailyQuota(date="2026-05-31", email_drafts_done=10, linkedin_drafts_done=5)
        assert q.total_assets_done == 15

    def test_completion_pct_zero_when_target_zero(self) -> None:
        q = DailyQuota(
            date="2026-05-31",
            email_drafts_target=0,
            linkedin_drafts_target=0,
            website_form_drafts_target=0,
            whatsapp_drafts_target=0,
        )
        assert q.completion_pct == 0.0

    def test_completion_pct_calculation(self) -> None:
        q = DailyQuota(
            date="2026-05-31",
            email_drafts_target=100,
            linkedin_drafts_target=100,
            website_form_drafts_target=100,
            whatsapp_drafts_target=100,
            email_drafts_done=100,
            linkedin_drafts_done=100,
            website_form_drafts_done=100,
            whatsapp_drafts_done=100,
        )
        assert q.completion_pct == 100.0


class TestLeadCapture:
    def test_lead_id_generated(self) -> None:
        lc = LeadCapture(source="google_lead_form", name="Ahmed")
        assert len(lc.lead_id) == 16

    def test_default_country_ksa(self) -> None:
        lc = LeadCapture(source="website_intake", name="Fatima")
        assert lc.country == "KSA"


class TestChannelDecision:
    def test_construction(self) -> None:
        cd = ChannelDecision(
            company_id="abc",
            segment="legal_local_arabic",
            primary_channels=[ChannelType.email],
            secondary_channels=[ChannelType.linkedin],
            avoid_channels=[],
            automation_levels={"email": AutomationLevel.partial},
            rationale="test",
        )
        assert cd.segment == "legal_local_arabic"


class TestEnums:
    def test_all_channel_types_exist(self) -> None:
        expected = {
            "email", "linkedin", "whatsapp_optin", "website_form",
            "google_lead_form", "linkedin_lead_gen", "meta_lead_ads",
            "seo_content", "webinar", "phone_call", "partnership",
            "procurement_portal", "community", "retargeting", "founder_brand",
        }
        actual = {c.value for c in ChannelType}
        assert actual == expected

    def test_all_asset_types_exist(self) -> None:
        assert len(list(AssetType)) == 18

    def test_all_sectors_exist(self) -> None:
        assert len(list(Sector)) == 14  # 13 + other

    def test_risk_levels(self) -> None:
        assert {r.value for r in RiskLevel} == {"low", "medium", "high"}
