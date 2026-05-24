"""Tests for `dealix.partners.onboarding.PartnerOnboarding`."""

from __future__ import annotations

import pytest

from dealix.partners.onboarding import (
    PartnerOnboarding,
    PartnerOnboardingError,
    PartnerStage,
)


def test_prospect_to_qualified_transition() -> None:
    machine = PartnerOnboarding()
    record = machine.register("Acme Studios")
    advanced = machine.advance(record.partner_id, PartnerStage.QUALIFIED)
    assert advanced.stage == PartnerStage.QUALIFIED
    assert advanced.history[-1]["from"] == "prospect"
    assert advanced.history[-1]["to"] == "qualified"


def test_mou_drafted_requires_evidence_ref() -> None:
    machine = PartnerOnboarding()
    record = machine.register("Acme Studios")
    machine.advance(record.partner_id, PartnerStage.QUALIFIED)
    with pytest.raises(PartnerOnboardingError):
        machine.advance(record.partner_id, PartnerStage.MOU_DRAFTED)
    advanced = machine.advance(
        record.partner_id,
        PartnerStage.MOU_DRAFTED,
        evidence_ref="epk_test",
    )
    assert advanced.stage == PartnerStage.MOU_DRAFTED
    assert "epk_test" in advanced.evidence_refs


def test_invalid_transition_is_rejected() -> None:
    machine = PartnerOnboarding()
    record = machine.register("Acme Studios")
    # Cannot jump straight from PROSPECT to LIVE.
    with pytest.raises(PartnerOnboardingError):
        machine.advance(record.partner_id, PartnerStage.LIVE, evidence_ref="ok")


def test_pause_and_resume_round_trip() -> None:
    machine = PartnerOnboarding()
    record = machine.register("Acme Studios")
    machine.advance(record.partner_id, PartnerStage.QUALIFIED)
    paused = machine.advance(
        record.partner_id,
        PartnerStage.PAUSED,
        evidence_ref="hold",
    )
    assert paused.stage == PartnerStage.PAUSED
    resumed = machine.advance(record.partner_id, PartnerStage.QUALIFIED)
    assert resumed.stage == PartnerStage.QUALIFIED
