"""Tests for AssetFactory."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.asset_factory import AssetFactory, OfferData
from auto_client_acquisition.omni_channel_os.buyer_mapper import BuyerMapper
from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    Company,
    CompanySize,
    GCCCountry,
    Language,
    Sector,
)


@pytest.fixture()
def factory() -> AssetFactory:
    return AssetFactory()


@pytest.fixture()
def legal_company() -> Company:
    return Company(
        name="Al Nasser Law",
        sector=Sector.legal,
        country=GCCCountry.KSA,
        language=Language.arabic,
        company_size=CompanySize.sme,
    )


@pytest.fixture()
def offer() -> OfferData:
    return OfferData(
        offer_name="Legal Knowledge OS",
        angle_ar="ذكاء اصطناعي لمستندات المكتب",
        angle_en="AI document intelligence for law offices",
        lead_magnet_ar="قائمة فحص AI للمحامين",
        lead_magnet_en="Legal AI Checklist",
        cta_ar="احصل على تشخيص مجاني",
        cta_en="Get your free diagnostic",
        tier="sprint_499",
    )


class TestAssetFactory:
    def test_generates_non_empty_body_for_email(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        assert AssetType.email_draft.value in assets
        assert len(assets[AssetType.email_draft.value].body) > 0

    def test_all_drafts_have_approval_required(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        for key, asset in assets.items():
            assert asset.approval_status == "approval_required", (
                f"Asset {key} has approval_status={asset.approval_status}"
            )

    def test_linkedin_assets_are_not_auto_sendable(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        from auto_client_acquisition.omni_channel_os.schemas import ChannelType

        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        linkedin_assets = [
            (k, v) for k, v in assets.items()
            if v.channel == ChannelType.linkedin
        ]
        assert len(linkedin_assets) > 0, "Expected at least one LinkedIn asset"
        for key, asset in linkedin_assets:
            assert asset.is_auto_sendable is False, (
                f"LinkedIn asset {key} should not be auto-sendable"
            )

    def test_whatsapp_optin_is_auto_sendable(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        wa_key = AssetType.whatsapp_optin_reply.value
        if wa_key in assets:
            assert assets[wa_key].is_auto_sendable is True

    def test_quality_score_greater_than_zero(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        from auto_client_acquisition.omni_channel_os.quality_gate import QualityGate

        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        gate = QualityGate()
        for key, asset in assets.items():
            score = gate.score(asset, legal_company)
            assert score > 0, f"Asset {key} got quality_score=0"

    def test_word_count_greater_than_zero(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        for key, asset in assets.items():
            assert asset.word_count > 0, f"Asset {key} has word_count=0"

    def test_generates_assets_for_multiple_sectors(self, factory: AssetFactory) -> None:
        mapper = BuyerMapper()
        for sector in [Sector.consulting, Sector.facilities_management, Sector.real_estate]:
            company = Company(
                name="Multi Sector Co",
                sector=sector,
                country=GCCCountry.KSA,
                language=Language.arabic,
                company_size=CompanySize.sme,
            )
            persona = mapper.map(company)
            offer_data = OfferData(
                offer_name="Test Offer",
                angle_ar="اختبار",
                angle_en="test angle",
                lead_magnet_ar="مغناطيس الرصاص",
                lead_magnet_en="lead magnet",
                cta_ar="ابدأ",
                cta_en="Start",
                tier="sprint_499",
            )
            assets = factory.generate_full_package(company, persona, offer_data)
            assert len(assets) > 0, f"No assets generated for sector {sector}"

    def test_email_asset_company_name_in_body(
        self, factory: AssetFactory, legal_company: Company, offer: OfferData
    ) -> None:
        mapper = BuyerMapper()
        persona = mapper.map(legal_company)
        assets = factory.generate_full_package(legal_company, persona, offer)
        if AssetType.email_draft.value in assets:
            body = assets[AssetType.email_draft.value].body
            assert legal_company.name in body
