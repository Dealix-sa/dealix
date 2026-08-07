"""Tests for the normalize_pipeline_lead adapter.

Verifies that operational revenue pipeline Leads are correctly bridged to
CanonicalOpportunity without escalating authority.
"""
from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalOpportunity,
    OpportunityStage,
)
from dealix.company_intelligence.pipeline_adapter import normalize_pipeline_lead


def _lead(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed pipeline Lead-like object."""
    values: dict[str, object] = {
        "id": "lead_abc123",
        "slot_id": "slot-01",
        "sector": "B2B SaaS",
        "region": "Riyadh",
        "relationship_strength": "warm_intro",
        "consent_status": "not_yet_asked",
        "stage": "warm_intro_selected",
        "last_touch_at": None,
        "expected_amount_sar": 5000,
        "actual_amount_sar": None,
        "commitment_evidence": "",
        "payment_evidence": "",
        "notes_placeholder": "",
        "created_at": datetime(2026, 8, 1, 12, 0, 0, tzinfo=UTC),
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizePipelineLeadBasic:
    """Core normalization behavior."""

    def test_produces_canonical_opportunity(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(), tenant_id="tenant-a", company_id="co-1", offer_id="offer-1"
        )
        assert isinstance(opp, CanonicalOpportunity)
        assert opp.tenant_id == "tenant-a"
        assert opp.company_id == "co-1"
        assert opp.offer_id == "offer-1"
        assert opp.opportunity_id == "opp_lead_abc123"

    def test_external_action_always_false(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(), tenant_id="t", company_id="c", offer_id="o"
        )
        assert opp.external_action_allowed is False

    def test_approval_always_required(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(), tenant_id="t", company_id="c", offer_id="o"
        )
        assert opp.approval_required is True

    def test_frozen_immutability(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(), tenant_id="t", company_id="c", offer_id="o"
        )
        with pytest.raises(Exception):
            opp.stage = OpportunityStage.WON  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Stage mapping
# ---------------------------------------------------------------------------


class TestStageMapping:
    """Verify pipeline stage → canonical OpportunityStage mapping."""

    @pytest.mark.parametrize(
        ("raw_stage", "expected"),
        [
            ("warm_intro_selected", OpportunityStage.RESEARCH),
            ("message_drafted", OpportunityStage.RESEARCH),
            ("founder_sent_manually", OpportunityStage.QUALIFY),
            ("replied", OpportunityStage.QUALIFY),
            ("diagnostic_requested", OpportunityStage.APPROVAL),
            ("diagnostic_delivered", OpportunityStage.APPROVAL),
            ("pilot_offered", OpportunityStage.CONVERSATION),
            ("commitment_received", OpportunityStage.PILOT),
            ("payment_received", OpportunityStage.PROOF),
            ("delivery_started", OpportunityStage.COMMERCIAL),
            ("delivered", OpportunityStage.COMMERCIAL),
            ("proof_pack_delivered", OpportunityStage.COMMERCIAL),
            ("upsell_offered", OpportunityStage.WON),
            ("closed_won", OpportunityStage.WON),
            ("closed_lost", OpportunityStage.LOST),
        ],
    )
    def test_stage_mapping(
        self, raw_stage: str, expected: OpportunityStage
    ) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage=raw_stage),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.stage == expected

    def test_unknown_stage_fallback_to_research(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="unknown_future_stage"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.stage == OpportunityStage.RESEARCH


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


class TestScoring:
    """Verify score derivation from stage + evidence."""

    def test_early_stage_low_score(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="warm_intro_selected"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.score == 10

    def test_commitment_adds_bonus(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(
                stage="commitment_received",
                commitment_evidence="verbal-agreement-2026-08-01",
            ),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        # PILOT base (60) + commitment bonus (10) = 70
        assert opp.score == 70

    def test_payment_adds_bonus(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(
                stage="payment_received",
                payment_evidence="transfer-ref-12345",
            ),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        # PROOF base (75) + payment bonus (15) = 90
        assert opp.score == 90

    def test_both_evidences_capped_at_100(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(
                stage="closed_won",
                commitment_evidence="signed-contract",
                payment_evidence="wire-transfer",
            ),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.score == 100

    def test_lost_deal_score_zero(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="closed_lost"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.score == 0

    def test_score_reasons_contain_stage_info(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="pilot_offered"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.score_reasons["pipeline_stage"] == "pilot_offered"
        assert opp.score_reasons["canonical_stage"] == "conversation"


# ---------------------------------------------------------------------------
# Confidence band
# ---------------------------------------------------------------------------


class TestConfidenceBand:
    """Verify confidence band derivation."""

    def test_early_stage_low_confidence(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="warm_intro_selected"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.confidence_band == "low"

    def test_mid_stage_medium_confidence(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="pilot_offered"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.confidence_band == "medium"

    def test_commitment_medium_confidence(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(
                stage="commitment_received",
                commitment_evidence="signed",
            ),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.confidence_band == "medium"

    def test_payment_high_confidence(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(
                stage="payment_received",
                payment_evidence="wire-transfer",
            ),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.confidence_band == "high"


# ---------------------------------------------------------------------------
# Blockers
# ---------------------------------------------------------------------------


class TestBlockers:
    """Verify blocker derivation."""

    def test_lost_has_blocker(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="closed_lost"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert "deal_lost" in opp.blockers

    def test_active_no_blockers(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="pilot_offered"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.blockers == []


# ---------------------------------------------------------------------------
# Next action and proof target
# ---------------------------------------------------------------------------


class TestNextActionAndProof:
    """Verify derived next action and proof target."""

    def test_research_next_action(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="warm_intro_selected"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.next_action == "research_and_qualify"
        assert opp.proof_target == "icp_fit_assessment"

    def test_won_next_action(self) -> None:
        opp = normalize_pipeline_lead(
            _lead(stage="closed_won"),
            tenant_id="t",
            company_id="c",
            offer_id="o",
        )
        assert opp.next_action == "explore_upsell"
        assert opp.proof_target == "renewal_or_upsell"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Verify input validation."""

    def test_rejects_empty_lead_id(self) -> None:
        with pytest.raises(ValueError, match="id"):
            normalize_pipeline_lead(
                _lead(id=""),
                tenant_id="t",
                company_id="c",
                offer_id="o",
            )

    def test_rejects_none_lead_id(self) -> None:
        with pytest.raises(ValueError, match="id"):
            normalize_pipeline_lead(
                _lead(id=None),
                tenant_id="t",
                company_id="c",
                offer_id="o",
            )
