"""Unit tests for strategic_targeting_engine."""

import pytest

from auto_client_acquisition.revenue_os.strategic_targeting_engine import (
    MotionType,
    TargetingDimensions,
    TargetTier,
    prioritize_accounts,
    score_target,
)


def _dims(**kwargs) -> TargetingDimensions:
    defaults = dict(
        icp_fit=50,
        pain_urgency=50,
        timing_score=50,
        access_score=50,
        budget_readiness=50,
        sector_fit=50,
        proof_path_potential=50,
        competitive_displacement=50,
    )
    defaults.update(kwargs)
    return TargetingDimensions(**defaults)


class TestWeightedScore:
    def test_all_zero_gives_no_fit(self):
        result = score_target(_dims(**{k: 0 for k in TargetingDimensions.__dataclass_fields__}))
        assert result.tier == TargetTier.NO_FIT

    def test_all_100_gives_p0(self):
        result = score_target(_dims(**{k: 100 for k in TargetingDimensions.__dataclass_fields__}))
        assert result.tier == TargetTier.P0
        assert result.total_score == 100

    def test_score_is_bounded_0_to_100(self):
        result = score_target(_dims())
        assert 0 <= result.total_score <= 100

    def test_high_pain_and_icp_yields_high_score(self):
        result = score_target(_dims(icp_fit=95, pain_urgency=95, timing_score=80, access_score=80))
        assert result.tier in (TargetTier.P0, TargetTier.P1)


class TestTierAssignment:
    def test_p0_threshold(self):
        result = score_target(_dims(**{k: 90 for k in TargetingDimensions.__dataclass_fields__}))
        assert result.tier == TargetTier.P0

    def test_nurture_low_scores(self):
        result = score_target(_dims(**{k: 28 for k in TargetingDimensions.__dataclass_fields__}))
        assert result.tier in (TargetTier.NURTURE, TargetTier.P2)

    def test_no_fit_near_zero(self):
        result = score_target(_dims(**{k: 3 for k in TargetingDimensions.__dataclass_fields__}))
        assert result.tier == TargetTier.NO_FIT


class TestMotionAssignment:
    def test_agency_sector_gets_motion_a(self):
        result = score_target(_dims(), sector="marketing_agency")
        assert result.recommended_motion == MotionType.A

    def test_executive_sector_gets_motion_d(self):
        result = score_target(_dims(), sector="enterprise_government")
        assert result.recommended_motion == MotionType.D

    def test_partner_sector_gets_motion_e(self):
        result = score_target(_dims(), sector="crm_partner")
        assert result.recommended_motion == MotionType.E

    def test_high_access_defaults_to_motion_b(self):
        result = score_target(_dims(access_score=80), sector="")
        assert result.recommended_motion == MotionType.B

    def test_low_access_defaults_to_motion_c(self):
        result = score_target(_dims(access_score=10), sector="")
        assert result.recommended_motion == MotionType.C


class TestBlockingSignals:
    def test_low_budget_flagged(self):
        result = score_target(_dims(budget_readiness=5))
        assert "budget_too_low_or_unclear" in result.blocking_signals

    def test_no_access_flagged(self):
        result = score_target(_dims(access_score=5))
        assert "no_decision_maker_access" in result.blocking_signals

    def test_no_proof_path_flagged(self):
        result = score_target(_dims(proof_path_potential=5))
        assert "no_viable_proof_path" in result.blocking_signals

    def test_good_dims_no_blocks(self):
        result = score_target(_dims())
        assert len(result.blocking_signals) == 0


class TestReasoningStrings:
    def test_reasoning_ar_nonempty(self):
        result = score_target(_dims())
        assert len(result.reasoning_ar) > 0

    def test_reasoning_en_nonempty(self):
        result = score_target(_dims())
        assert len(result.reasoning_en) > 0

    def test_next_action_ar_nonempty(self):
        result = score_target(_dims())
        assert len(result.next_action_ar) > 0


class TestPrioritizeAccounts:
    def test_returns_sorted_descending(self):
        accounts = [
            ("low", _dims(**{k: 20 for k in TargetingDimensions.__dataclass_fields__}), ""),
            ("high", _dims(**{k: 90 for k in TargetingDimensions.__dataclass_fields__}), ""),
            ("mid", _dims(**{k: 55 for k in TargetingDimensions.__dataclass_fields__}), ""),
        ]
        ranked = prioritize_accounts(accounts)
        scores = [r.total_score for _, r in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_returns_all_accounts(self):
        accounts = [
            (f"acct_{i}", _dims(**{k: i * 10 for k in TargetingDimensions.__dataclass_fields__}), "")
            for i in range(1, 6)
        ]
        ranked = prioritize_accounts(accounts)
        assert len(ranked) == 5

    def test_empty_list(self):
        assert prioritize_accounts([]) == []
