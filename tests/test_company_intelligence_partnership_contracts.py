"""Tests for the canonical PartnershipOpportunity contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence and score bounds
  - Safety invariants (no external action, approval required)
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.partnership_contracts import (
    CanonicalPartnershipOpportunity,
    PartnershipStage,
    PartnershipType,
    build_partnership_opportunity,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _partnership(**overrides: object) -> CanonicalPartnershipOpportunity:
    """Build a minimal valid partnership, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        company_id="company-1",
        partnership_type=PartnershipType.CHANNEL_PARTNER,
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_partnership_opportunity(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _partnership()
        b = _partnership()
        assert a.partnership_id == b.partnership_id

    def test_different_company_produces_different_id(self) -> None:
        a = _partnership(company_id="company-1")
        b = _partnership(company_id="company-2")
        assert a.partnership_id != b.partnership_id

    def test_different_type_produces_different_id(self) -> None:
        a = _partnership(partnership_type=PartnershipType.CHANNEL_PARTNER)
        b = _partnership(partnership_type=PartnershipType.RESELLER)
        assert a.partnership_id != b.partnership_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _partnership(tenant_id="tenant-a")
        b = _partnership(tenant_id="tenant-b")
        assert a.partnership_id != b.partnership_id

    def test_different_source_produces_different_id(self) -> None:
        a = _partnership(source_id="source-1")
        b = _partnership(source_id="source-2")
        assert a.partnership_id != b.partnership_id

    def test_partnership_id_format(self) -> None:
        a = _partnership()
        assert a.partnership_id.startswith("partner_")
        assert len(a.partnership_id) == 8 + 16  # "partner_" + 16 hex chars

    def test_whitespace_in_company_id_is_stripped(self) -> None:
        a = _partnership(company_id="  company-1  ")
        b = _partnership(company_id="company-1")
        assert a.partnership_id == b.partnership_id


# ---------------------------------------------------------------------------
# Score bounds
# ---------------------------------------------------------------------------


class TestScoreBounds:
    def test_default_score(self) -> None:
        a = _partnership()
        assert a.score == 0

    def test_custom_score(self) -> None:
        a = _partnership(score=85)
        assert a.score == 85

    def test_score_above_100_rejected(self) -> None:
        with pytest.raises(ValueError):
            _partnership(score=101)

    def test_score_below_0_rejected(self) -> None:
        with pytest.raises(ValueError):
            _partnership(score=-1)

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _partnership(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _partnership(confidence=-0.1)


# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------


class TestSafetyInvariants:
    def test_external_action_always_forbidden(self) -> None:
        a = _partnership()
        data = a.model_dump()
        data["external_action_allowed"] = True
        with pytest.raises(ValueError, match="external execution"):
            CanonicalPartnershipOpportunity(**data)

    def test_approval_always_required(self) -> None:
        a = _partnership()
        data = a.model_dump()
        data["approval_required"] = False
        with pytest.raises(ValueError, match="require approval"):
            CanonicalPartnershipOpportunity(**data)


# ---------------------------------------------------------------------------
# Partnership types coverage
# ---------------------------------------------------------------------------


class TestPartnershipTypes:
    def test_all_types_are_valid(self) -> None:
        for ptype in PartnershipType:
            a = _partnership(partnership_type=ptype)
            assert a.partnership_type == ptype


# ---------------------------------------------------------------------------
# Partnership stages
# ---------------------------------------------------------------------------


class TestPartnershipStages:
    def test_default_stage_is_signal_detected(self) -> None:
        a = _partnership()
        assert a.stage == PartnershipStage.SIGNAL_DETECTED

    def test_all_stages_are_valid(self) -> None:
        for stage in PartnershipStage:
            a = _partnership(stage=stage)
            assert a.stage == stage


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _partnership()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalPartnershipOpportunity(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_stage_is_signal_detected(self) -> None:
        a = _partnership()
        assert a.stage == PartnershipStage.SIGNAL_DETECTED

    def test_default_signal_ids_empty(self) -> None:
        a = _partnership()
        assert a.signal_ids == ()

    def test_default_approval_required(self) -> None:
        a = _partnership()
        assert a.approval_required is True

    def test_default_external_action_forbidden(self) -> None:
        a = _partnership()
        assert a.external_action_allowed is False

    def test_builder_with_full_context(self) -> None:
        a = build_partnership_opportunity(
            tenant_id="tenant-a",
            company_id="company-1",
            partnership_type=PartnershipType.TECHNOLOGY_PARTNER,
            source_id="source-1",
            stage=PartnershipStage.QUALIFIED,
            score=75,
            score_reasons={"market_fit": 80, "capability_match": 70},
            confidence=0.8,
            signal_ids=("sig-1", "sig-2"),
            next_action="Schedule discovery call",
            proof_target="Partnership agreement signed",
            description="Technology integration partnership",
            expected_value="Joint product offering for Saudi market",
        )
        assert a.partnership_type == PartnershipType.TECHNOLOGY_PARTNER
        assert a.stage == PartnershipStage.QUALIFIED
        assert a.score == 75
        assert a.confidence == 0.8
        assert len(a.signal_ids) == 2


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_partnership_is_frozen(self) -> None:
        a = _partnership()
        with pytest.raises(Exception):
            a.stage = PartnershipStage.ACTIVE  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for PartnershipOpportunity."""

    def test_required_fields_present(self) -> None:
        a = _partnership()
        # Required: tenant_id, company_id, partnership_type, score, score_reasons, next_action
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "company_id") and a.company_id
        assert hasattr(a, "partnership_type") and a.partnership_type
        assert hasattr(a, "score") and isinstance(a.score, int)
        assert hasattr(a, "score_reasons") and isinstance(a.score_reasons, dict)
        assert hasattr(a, "next_action")

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_partnership_opportunity(
                tenant_id="",
                company_id="company-1",
                partnership_type=PartnershipType.CHANNEL_PARTNER,
                source_id="source-1",
            )

    def test_empty_company_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_partnership_opportunity(
                tenant_id="tenant-a",
                company_id="",
                partnership_type=PartnershipType.CHANNEL_PARTNER,
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_partnership_opportunity(
                tenant_id="tenant-a",
                company_id="company-1",
                partnership_type=PartnershipType.CHANNEL_PARTNER,
                source_id="",
            )
