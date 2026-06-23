"""Tests for dealix.launch_os.outreach_factory.

Actual interface:
    CHANNEL_TEMPLATES: dict[str, dict[str, str]] — email/linkedin_manual/phone/whatsapp_after_consent
    OutreachDraft: dataclass with id, channel, persona_id, subject_ar, subject_en,
                   body_ar, body_en, cta_ar, cta_en, requires_approval, trust_score,
                   offer_id, account_id, drafted_by, evidence_level, pricing_status, created_at_iso
    build_draft(account, offer_id, channel, *, drafted_by, evidence_level,
                pricing_status, consent_record_ref, persona_id) -> OutreachDraft
    TrustPreflightError: raised when a block-severity rule fires

Channels: email | linkedin_manual | phone | whatsapp_after_consent
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from dealix.launch_os.outreach_factory import (
    CHANNEL_TEMPLATES,
    OutreachDraft,
    TrustPreflightError,
    build_draft,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_OFFER = "REVENUE_LEAK_AUDIT"


def _account(**overrides: Any) -> dict[str, Any]:
    """Return a minimal valid account dict."""
    base: dict[str, Any] = {
        "account_id": "acc_001",
        "account_name": "شركة النخبة",
        "contact_name": "Ahmed",
        "sector": "automotive",
    }
    base.update(overrides)
    return base


def _build(
    channel: str = "email",
    offer_id: str = _VALID_OFFER,
    **account_overrides: Any,
) -> OutreachDraft:
    return build_draft(
        _account(**account_overrides),
        offer_id=offer_id,
        channel=channel,
    )


# ---------------------------------------------------------------------------
# CHANNEL_TEMPLATES catalogue
# ---------------------------------------------------------------------------

class TestChannelTemplates:
    def test_channel_templates_is_a_dict(self) -> None:
        assert isinstance(CHANNEL_TEMPLATES, dict)

    def test_email_channel_template_exists(self) -> None:
        assert "email" in CHANNEL_TEMPLATES

    def test_linkedin_manual_channel_template_exists(self) -> None:
        assert "linkedin_manual" in CHANNEL_TEMPLATES

    def test_phone_channel_template_exists(self) -> None:
        assert "phone" in CHANNEL_TEMPLATES

    def test_whatsapp_after_consent_channel_template_exists(self) -> None:
        assert "whatsapp_after_consent" in CHANNEL_TEMPLATES

    def test_each_template_has_body_ar_key(self) -> None:
        for channel, tmpl in CHANNEL_TEMPLATES.items():
            assert "body_ar" in tmpl, f"Channel {channel!r} missing body_ar"

    def test_each_template_has_body_en_key(self) -> None:
        for channel, tmpl in CHANNEL_TEMPLATES.items():
            assert "body_en" in tmpl, f"Channel {channel!r} missing body_en"


# ---------------------------------------------------------------------------
# build_draft — valid channels
# ---------------------------------------------------------------------------

class TestBuildDraftChannels:
    def test_build_draft_email_returns_outreach_draft(self) -> None:
        draft = _build(channel="email")
        assert isinstance(draft, OutreachDraft)

    def test_build_draft_linkedin_manual_returns_outreach_draft(self) -> None:
        draft = _build(channel="linkedin_manual")
        assert isinstance(draft, OutreachDraft)

    def test_build_draft_phone_returns_outreach_draft(self) -> None:
        draft = _build(channel="phone")
        assert isinstance(draft, OutreachDraft)

    def test_build_draft_whatsapp_with_consent_ref_returns_draft(self) -> None:
        draft = build_draft(
            _account(),
            offer_id=_VALID_OFFER,
            channel="whatsapp_after_consent",
            consent_record_ref="consent_001",
        )
        assert isinstance(draft, OutreachDraft)

    def test_email_draft_has_channel_field_set_to_email(self) -> None:
        draft = _build(channel="email")
        assert draft.channel == "email"

    def test_linkedin_draft_has_channel_set(self) -> None:
        draft = _build(channel="linkedin_manual")
        assert draft.channel == "linkedin_manual"

    def test_phone_draft_has_channel_set(self) -> None:
        draft = _build(channel="phone")
        assert draft.channel == "phone"


# ---------------------------------------------------------------------------
# build_draft — required output fields
# ---------------------------------------------------------------------------

class TestBuildDraftFields:
    def test_draft_has_id(self) -> None:
        draft = _build()
        assert draft.id and isinstance(draft.id, str)

    def test_draft_id_starts_with_draft(self) -> None:
        draft = _build()
        assert draft.id.startswith("draft_")

    def test_draft_has_account_id(self) -> None:
        draft = _build()
        assert draft.account_id == "acc_001"

    def test_draft_has_offer_id(self) -> None:
        draft = _build()
        assert draft.offer_id == _VALID_OFFER

    def test_draft_has_body_ar_non_empty(self) -> None:
        draft = _build()
        assert draft.body_ar.strip()

    def test_draft_has_body_en_non_empty(self) -> None:
        draft = _build()
        assert draft.body_en.strip()

    def test_draft_has_subject_ar(self) -> None:
        draft = _build()
        assert hasattr(draft, "subject_ar")
        assert isinstance(draft.subject_ar, str)

    def test_draft_has_subject_en(self) -> None:
        draft = _build()
        assert hasattr(draft, "subject_en")
        assert isinstance(draft.subject_en, str)

    def test_draft_has_cta_ar(self) -> None:
        draft = _build()
        assert hasattr(draft, "cta_ar") and isinstance(draft.cta_ar, str)

    def test_draft_has_cta_en(self) -> None:
        draft = _build()
        assert hasattr(draft, "cta_en") and isinstance(draft.cta_en, str)

    def test_draft_has_trust_score_int(self) -> None:
        draft = _build()
        assert isinstance(draft.trust_score, int)
        assert draft.trust_score >= 0

    def test_draft_requires_approval_is_bool(self) -> None:
        draft = _build()
        assert isinstance(draft.requires_approval, bool)

    def test_draft_has_created_at_iso(self) -> None:
        draft = _build()
        assert hasattr(draft, "created_at_iso")
        assert "T" in draft.created_at_iso  # ISO timestamp contains T

    def test_draft_drafted_by_defaults_to_founder(self) -> None:
        draft = _build()
        assert draft.drafted_by == "founder"

    def test_draft_evidence_level_defaults_to_l2(self) -> None:
        draft = _build()
        assert draft.evidence_level == "L2"


# ---------------------------------------------------------------------------
# build_draft — trust_preflight integration
# ---------------------------------------------------------------------------

class TestBuildDraftPreflightIntegration:
    def test_trust_preflight_is_called_during_build_draft(self) -> None:
        """run_preflight must be invoked inside build_draft for compliance."""
        with patch("dealix.launch_os.outreach_factory.run_preflight") as mock_pf:
            # Return a passing result so build_draft completes
            mock_pf.return_value = (True, [])
            _build()
            assert mock_pf.called

    def test_trust_preflight_error_raised_for_blocked_draft(self) -> None:
        """When run_preflight returns a block violation, TrustPreflightError must be raised."""
        from dealix.launch_os.trust_preflight import TrustViolation

        block_viol = TrustViolation(
            rule_id="R01",
            severity="block",
            message_ar="محظور",
            message_en="Blocked by R01",
        )
        with patch("dealix.launch_os.outreach_factory.run_preflight") as mock_pf:
            mock_pf.return_value = (False, [block_viol])
            with pytest.raises(TrustPreflightError):
                _build()


# ---------------------------------------------------------------------------
# build_draft — invalid inputs
# ---------------------------------------------------------------------------

class TestBuildDraftInvalidInputs:
    def test_invalid_channel_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            build_draft(_account(), offer_id=_VALID_OFFER, channel="carrier_pigeon")

    def test_empty_channel_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            build_draft(_account(), offer_id=_VALID_OFFER, channel="")

    def test_whatsapp_without_consent_ref_raises_trust_preflight_error(self) -> None:
        """WhatsApp channel without consent_record_ref triggers R05 block."""
        with pytest.raises(TrustPreflightError):
            build_draft(
                _account(),
                offer_id=_VALID_OFFER,
                channel="whatsapp_after_consent",
                consent_record_ref="",
            )


# ---------------------------------------------------------------------------
# build_draft — account context interpolation
# ---------------------------------------------------------------------------

class TestBuildDraftAccountInterpolation:
    def test_account_name_appears_in_email_subject(self) -> None:
        draft = build_draft(
            _account(account_name="Acme Motors"),
            offer_id=_VALID_OFFER,
            channel="email",
        )
        assert "Acme Motors" in draft.subject_ar or "Acme Motors" in draft.subject_en

    def test_sector_appears_in_body(self) -> None:
        draft = build_draft(
            _account(sector="automotive"),
            offer_id=_VALID_OFFER,
            channel="email",
        )
        combined = draft.body_ar + draft.body_en
        assert "automotive" in combined.lower()

    def test_custom_drafted_by_is_stored(self) -> None:
        draft = build_draft(
            _account(),
            offer_id=_VALID_OFFER,
            channel="email",
            drafted_by="ops_lead",
        )
        assert draft.drafted_by == "ops_lead"

    def test_unknown_offer_id_still_produces_draft(self) -> None:
        """Unknown offer IDs should fall back gracefully, not crash."""
        draft = build_draft(
            _account(),
            offer_id="UNKNOWN_OFFER_XYZ",
            channel="email",
        )
        assert isinstance(draft, OutreachDraft)
