"""Approved partner claims are HMAC-signed and tamper-detectable."""

from __future__ import annotations

import pytest

from dealix.hermes.partners.program.approved_claims import approve, is_approved, reset


def test_approved_claim_roundtrip_and_tamper() -> None:
    reset()
    approve("claim_roi", "Customers see 3x faster onboarding (median).", evidence_pack_id="ep_1")
    assert is_approved("claim_roi", "Customers see 3x faster onboarding (median).") is True
    assert is_approved("claim_roi", "Customers see 10x faster onboarding.") is False
    with pytest.raises(ValueError):
        approve("claim_x", "text", evidence_pack_id="")
