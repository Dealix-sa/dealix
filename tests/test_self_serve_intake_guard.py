"""SelfServeIntakeGuard — Phase 1 doctrine enforcement.

Verifies that the guard composes forbidden_actions + claim_safety +
lawful_basis primitives correctly and rejects every doctrine violation
with bilingual reasons.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.lawful_basis import LawfulBasis
from auto_client_acquisition.governance_os.self_serve_intake_guard import (
    ALLOWED_OFFER_IDS,
    AUTO_APPROVE_OFFERS,
    evaluate_intake,
    is_auto_approve_offer,
)


def test_allow_minimal_valid_intake():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="passport_abc",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
        free_text="",
    )
    assert v.allow is True
    assert v.violation_codes == ()


def test_reject_unknown_offer():
    v = evaluate_intake(
        offer_id="not_an_offer",
        source_passport_id="p",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert v.allow is False
    assert "offer_id_invalid" in v.violation_codes
    assert any("Offer" in r or "غير" in r for r in v.reasons_ar + v.reasons_en)


def test_reject_missing_source_passport():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
    )
    assert v.allow is False
    assert "source_passport_id_missing" in v.violation_codes


def test_reject_missing_lawful_basis():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis=None,
        consent_given=True,
    )
    assert v.allow is False
    assert "lawful_basis_missing" in v.violation_codes


def test_reject_consent_basis_without_consent():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=False,
    )
    assert v.allow is False
    assert "consent_not_given" in v.violation_codes


def test_contract_basis_does_not_require_consent_flag():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis=LawfulBasis.CONTRACT,
        consent_given=False,
    )
    assert v.allow is True


def test_reject_forbidden_channel_pattern():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis=LawfulBasis.CONSENT,
        consent_given=True,
        free_text="please run a cold whatsapp blast on this list",
    )
    assert v.allow is False
    assert "channel_pattern_forbidden" in v.violation_codes


def test_lawful_basis_string_accepted():
    """String form of LawfulBasis is normalized to the enum."""
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis="consent",
        consent_given=True,
    )
    assert v.allow is True


def test_lawful_basis_invalid_string_rejected():
    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="p",
        lawful_basis="space_aliens",
        consent_given=True,
    )
    assert v.allow is False
    assert "lawful_basis_missing" in v.violation_codes


def test_bilingual_reasons_present():
    v = evaluate_intake(
        offer_id="not_an_offer",
        source_passport_id="",
        lawful_basis=None,
        consent_given=False,
    )
    assert len(v.reasons_ar) == len(v.violation_codes)
    assert len(v.reasons_en) == len(v.violation_codes)
    # AR reasons must contain Arabic characters in at least one entry.
    assert any(any("؀" <= ch <= "ۿ" for ch in r) for r in v.reasons_ar)


def test_to_dict_is_serializable():
    """Verdict serializes to JSON-friendly dict for HTTP responses."""
    import json

    v = evaluate_intake(
        offer_id="sprint_499",
        source_passport_id="",
        lawful_basis=None,
        consent_given=False,
    )
    payload = v.to_dict()
    assert json.dumps(payload, ensure_ascii=False)  # roundtrip
    assert payload["allow"] is False
    assert "violation_codes" in payload
    assert "reasons" in payload and "ar" in payload["reasons"] and "en" in payload["reasons"]


@pytest.mark.parametrize("offer", AUTO_APPROVE_OFFERS)
def test_auto_approve_classification(offer: str):
    assert is_auto_approve_offer(offer) is True


def test_escalate_offers_not_auto_approve():
    assert is_auto_approve_offer("managed_ops_retainer") is False
    assert is_auto_approve_offer("custom_ai") is False
    assert is_auto_approve_offer("unknown") is False


def test_allowed_offers_match_catalog_size():
    """Sanity: 5 productized offers, no more, no fewer."""
    assert len(ALLOWED_OFFER_IDS) == 5
    assert len(set(ALLOWED_OFFER_IDS)) == 5
