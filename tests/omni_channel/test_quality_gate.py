"""Tests for QualityGate — scoring, pass/fail thresholds, per-dimension logic."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.quality_gate import QualityGate
from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Company,
    GCCCountry,
    Language,
    RiskLevel,
    Sector,
)


@pytest.fixture
def gate() -> QualityGate:
    return QualityGate()


def _company(name: str = "Acme Legal Partners", sector: Sector = Sector.legal) -> Company:
    return Company(name=name, sector=sector, country=GCCCountry.KSA)


def _asset(
    body: str,
    cta: str = "Get your free diagnostic",
    asset_type: AssetType = AssetType.email_draft,
    language: Language = Language.english,
    **kwargs,
) -> ChannelAsset:
    return ChannelAsset(
        company_id="abc123",
        asset_type=asset_type,
        channel=ChannelType.email,
        language=language,
        body=body,
        cta=cta,
        **kwargs,
    )


_GOOD_BODY = (
    "Dear Acme Legal Partners team, we noticed that legal firms in KSA often struggle "
    "with manual document review and case file tracking. Our Legal Knowledge OS helps "
    "law firms automate these workflows without risking client confidentiality. "
    "We would love to offer you a free 30-minute diagnostic to show you how it works."
)

_SHORT_BODY = "Hi"

_FORBIDDEN_BODY = (
    "We guaranteed roi for your firm. Lorem ipsum dolor sit amet. "
    "This is a placeholder message with todo items fill in the details here."
)


class TestQualityGate:
    def test_no_auto_send_flag(self) -> None:
        assert QualityGate._NO_AUTO_SEND is True

    def test_score_returns_float_in_range(self, gate: QualityGate) -> None:
        asset = _asset(body=_GOOD_BODY)
        score = gate.score(asset, _company())
        assert 0.0 <= score <= 100.0

    def test_good_asset_scores_above_65(self, gate: QualityGate) -> None:
        asset = _asset(body=_GOOD_BODY)
        assert gate.score(asset, _company()) >= 65.0

    def test_short_body_scores_lower(self, gate: QualityGate) -> None:
        short_asset = _asset(body=_SHORT_BODY)
        good_asset = _asset(body=_GOOD_BODY)
        assert gate.score(short_asset, _company()) < gate.score(good_asset, _company())

    def test_forbidden_patterns_reduce_score(self, gate: QualityGate) -> None:
        forbidden_asset = _asset(body=_FORBIDDEN_BODY)
        clean_asset = _asset(body=_GOOD_BODY)
        assert gate.score(forbidden_asset, _company()) < gate.score(clean_asset, _company())

    def test_passes_returns_true_for_good_asset(self, gate: QualityGate) -> None:
        asset = _asset(body=_GOOD_BODY)
        assert gate.passes(asset, _company()) is True

    def test_passes_returns_false_for_short_body(self, gate: QualityGate) -> None:
        asset = _asset(body=_SHORT_BODY)
        assert gate.passes(asset, _company()) is False

    def test_passes_custom_threshold(self, gate: QualityGate) -> None:
        asset = _asset(body=_GOOD_BODY)
        assert gate.passes(asset, _company(), min_score=0.0) is True
        assert gate.passes(asset, _company(), min_score=100.0) is False

    def test_score_length_short_body(self, gate: QualityGate) -> None:
        asset = _asset(body="Too short")
        score = gate._score_length(asset)
        assert score < 70.0

    def test_score_length_sufficient_body(self, gate: QualityGate) -> None:
        body = " ".join(["word"] * 80)
        asset = _asset(body=body)
        score = gate._score_length(asset)
        assert score >= 70.0

    def test_score_personalization_with_company_name(self, gate: QualityGate) -> None:
        asset = _asset(body="Dear Acme Legal Partners, we have a solution for your legal firm.")
        company = _company("Acme Legal Partners")
        score = gate._score_personalization(asset, company)
        assert score > 40.0

    def test_score_personalization_penalizes_template_tokens(self, gate: QualityGate) -> None:
        asset = _asset(body="Dear {name}, we help {company} in {sector}.")
        company = _company()
        score = gate._score_personalization(asset, company)
        assert score < 40.0

    def test_score_cta_presence_with_cta_keyword(self, gate: QualityGate) -> None:
        asset = _asset(body="Click here to get started", cta="Get your free trial now")
        score = gate._score_cta_presence(asset)
        assert score > 20.0

    def test_score_cta_presence_no_cta_keyword(self, gate: QualityGate) -> None:
        asset = _asset(body="Just a plain message with no action words", cta="")
        score = gate._score_cta_presence(asset)
        assert score == 20.0

    def test_score_cta_arabic_language(self, gate: QualityGate) -> None:
        asset = _asset(
            body="احصل على تشخيص مجاني لعملياتكم اليوم",
            cta="ابدأ الآن",
            language=Language.arabic,
        )
        score = gate._score_cta_presence(asset)
        assert score > 20.0

    def test_score_forbidden_clean_body(self, gate: QualityGate) -> None:
        asset = _asset(body=_GOOD_BODY)
        assert gate._score_forbidden_patterns(asset) == 100.0

    def test_score_forbidden_with_guarantee_claim(self, gate: QualityGate) -> None:
        asset = _asset(body="We offer guaranteed roi for your company")
        score = gate._score_forbidden_patterns(asset)
        assert score < 100.0

    def test_min_word_count_dict_covers_key_types(self, gate: QualityGate) -> None:
        assert AssetType.email_draft in gate.MIN_WORD_COUNT
        assert AssetType.linkedin_connection_note in gate.MIN_WORD_COUNT
        assert AssetType.proposal_seed in gate.MIN_WORD_COUNT

    def test_min_word_count_proposal_seed_is_100(self, gate: QualityGate) -> None:
        assert gate.MIN_WORD_COUNT[AssetType.proposal_seed] == 100

    def test_min_word_count_email_draft_is_60(self, gate: QualityGate) -> None:
        assert gate.MIN_WORD_COUNT[AssetType.email_draft] == 60
