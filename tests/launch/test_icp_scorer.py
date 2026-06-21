"""Tests for dealix.launch_os.icp_scorer.

Covers tier classification, individual scoring dimensions, batch_score,
input validation, and boundary conditions.
"""

from __future__ import annotations

from typing import Any

import pytest

from dealix.launch_os.icp_scorer import (
    ICPScore,
    batch_score,
    score_account,
    tier_label,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scores(**overrides: int) -> dict[str, int]:
    """Return a complete scores dict with all dimensions set to zero except overrides."""
    base: dict[str, int] = {
        "urgency": 0,
        "lost_revenue_visibility": 0,
        "process_chaos": 0,
        "decision_maker_access": 0,
        "ability_to_start_small": 0,
        "proof_speed": 0,
        "budget_likelihood": 0,
        "repeatability": 0,
        "referral_potential": 0,
        "compliance_delivery_risk": 0,
    }
    base.update(overrides)
    return base


def _account(account_id: str = "test_001", **score_kwargs: int) -> dict[str, Any]:
    """Return an account dict with embedded scores sub-dict."""
    return {"account_id": account_id, "scores": _scores(**score_kwargs)}


def _max_scores() -> dict[str, int]:
    """Return scores at their documented maximums."""
    return {
        "urgency": 20,
        "lost_revenue_visibility": 15,
        "process_chaos": 15,
        "decision_maker_access": 10,
        "ability_to_start_small": 10,
        "proof_speed": 10,
        "budget_likelihood": 10,
        "repeatability": 5,
        "referral_potential": 5,
        "compliance_delivery_risk": 0,
    }


# ---------------------------------------------------------------------------
# tier_label — boundary classification
# ---------------------------------------------------------------------------

class TestTierLabel:
    def test_score_at_75_is_tier_a(self) -> None:
        assert tier_label(75) == "A"

    def test_score_above_75_is_tier_a(self) -> None:
        assert tier_label(90) == "A"
        assert tier_label(100) == "A"

    def test_score_at_55_is_tier_b(self) -> None:
        assert tier_label(55) == "B"

    def test_score_between_55_and_74_is_tier_b(self) -> None:
        assert tier_label(60) == "B"
        assert tier_label(74) == "B"

    def test_score_at_35_is_tier_c(self) -> None:
        assert tier_label(35) == "C"

    def test_score_between_35_and_54_is_tier_c(self) -> None:
        assert tier_label(40) == "C"
        assert tier_label(54) == "C"

    def test_score_below_35_is_dq(self) -> None:
        assert tier_label(34) == "DQ"
        assert tier_label(0) == "DQ"

    def test_negative_score_is_dq(self) -> None:
        assert tier_label(-10) == "DQ"
        assert tier_label(-20) == "DQ"

    def test_boundary_74_is_b_not_a(self) -> None:
        assert tier_label(74) == "B"

    def test_boundary_54_is_c_not_b(self) -> None:
        assert tier_label(54) == "C"


# ---------------------------------------------------------------------------
# score_account — dimension scoring
# ---------------------------------------------------------------------------

class TestScoreAccountDimensions:
    """Test each scoring dimension in isolation via the scores sub-dict path."""

    def test_urgency_dimension_contributes_to_total(self) -> None:
        result = score_account(_account(urgency=20))
        assert result.scores["urgency"] == 20
        assert result.total >= 20

    def test_lost_revenue_visibility_dimension(self) -> None:
        result = score_account(_account(lost_revenue_visibility=15))
        assert result.scores["lost_revenue_visibility"] == 15

    def test_process_chaos_dimension(self) -> None:
        result = score_account(_account(process_chaos=15))
        assert result.scores["process_chaos"] == 15

    def test_decision_maker_access_dimension(self) -> None:
        result = score_account(_account(decision_maker_access=10))
        assert result.scores["decision_maker_access"] == 10

    def test_ability_to_start_small_dimension(self) -> None:
        result = score_account(_account(ability_to_start_small=10))
        assert result.scores["ability_to_start_small"] == 10

    def test_proof_speed_dimension(self) -> None:
        result = score_account(_account(proof_speed=10))
        assert result.scores["proof_speed"] == 10

    def test_budget_likelihood_dimension(self) -> None:
        result = score_account(_account(budget_likelihood=10))
        assert result.scores["budget_likelihood"] == 10

    def test_repeatability_dimension(self) -> None:
        result = score_account(_account(repeatability=5))
        assert result.scores["repeatability"] == 5

    def test_referral_potential_dimension(self) -> None:
        result = score_account(_account(referral_potential=5))
        assert result.scores["referral_potential"] == 5

    def test_compliance_delivery_risk_penalty_reduces_total(self) -> None:
        clean = score_account(_account(urgency=20))
        penalised = score_account(
            {"account_id": "pen", "scores": {**_scores(urgency=20), "compliance_delivery_risk": -20}}
        )
        assert penalised.total < clean.total

    def test_all_dimensions_present_in_scores_dict(self) -> None:
        result = score_account(_account())
        expected_dims = {
            "urgency", "lost_revenue_visibility", "process_chaos",
            "decision_maker_access", "ability_to_start_small", "proof_speed",
            "budget_likelihood", "repeatability", "referral_potential",
            "compliance_delivery_risk",
        }
        assert set(result.scores.keys()) == expected_dims


# ---------------------------------------------------------------------------
# score_account — tier assignment
# ---------------------------------------------------------------------------

class TestScoreAccountTiers:
    def test_perfect_account_scores_tier_a(self) -> None:
        result = score_account({"account_id": "perfect", "scores": _max_scores()})
        assert result.tier == "A"
        assert result.total == 100

    def test_all_zero_scores_gives_dq(self) -> None:
        result = score_account(_account())
        assert result.tier == "DQ"
        assert result.total == 0

    def test_tier_a_has_pursue_today_action(self) -> None:
        account = {"account_id": "a_tier", "scores": _max_scores()}
        result = score_account(account)
        assert result.action == "pursue_today"

    def test_tier_dq_has_ignore_action(self) -> None:
        result = score_account(_account())
        assert result.action == "ignore"

    def test_score_account_returns_icp_score_instance(self) -> None:
        result = score_account(_account())
        assert isinstance(result, ICPScore)

    def test_account_id_preserved_in_result(self) -> None:
        result = score_account(_account(account_id="custom_id_999"))
        assert result.account_id == "custom_id_999"

    def test_missing_account_id_defaults_to_unknown(self) -> None:
        result = score_account({"scores": _scores()})
        assert result.account_id == "unknown"

    def test_total_clamped_at_100_even_if_dimensions_overflow(self) -> None:
        over_max = _max_scores()
        over_max["urgency"] = 999
        result = score_account({"account_id": "overflow", "scores": over_max})
        assert result.total <= 100

    def test_total_clamped_at_minus_20_floor(self) -> None:
        extreme_penalty = _scores(compliance_delivery_risk=-999)
        result = score_account({"account_id": "penalty", "scores": extreme_penalty})
        assert result.total >= -20


# ---------------------------------------------------------------------------
# score_account — heuristic path (no scores sub-dict)
# ---------------------------------------------------------------------------

class TestScoreAccountHeuristics:
    def test_heuristic_urgency_critical_scores_higher_than_low(self) -> None:
        high_urgency = score_account({
            "account_id": "h",
            "urgency": "critical",
            "revenue_leak_sar": 0,
            "process_chaos_score": 0,
        })
        low_urgency = score_account({
            "account_id": "l",
            "urgency": "low",
            "revenue_leak_sar": 0,
            "process_chaos_score": 0,
        })
        assert high_urgency.total > low_urgency.total

    def test_heuristic_high_revenue_leak_boosts_score(self) -> None:
        high = score_account({"account_id": "rich", "revenue_leak_sar": 750_000})
        low = score_account({"account_id": "poor", "revenue_leak_sar": 0})
        assert high.total >= low.total

    def test_heuristic_direct_decision_maker_access(self) -> None:
        direct = score_account({"account_id": "d", "decision_maker_access": "direct"})
        unknown = score_account({"account_id": "u", "decision_maker_access": "unknown"})
        assert direct.scores["decision_maker_access"] > unknown.scores["decision_maker_access"]

    def test_heuristic_confirmed_budget_signal(self) -> None:
        confirmed = score_account({"account_id": "c", "budget_signal": "confirmed"})
        unlikely = score_account({"account_id": "u", "budget_signal": "unlikely"})
        assert confirmed.scores["budget_likelihood"] > unlikely.scores["budget_likelihood"]


# ---------------------------------------------------------------------------
# batch_score
# ---------------------------------------------------------------------------

class TestBatchScore:
    def test_batch_score_returns_list_sorted_descending(self) -> None:
        accounts = [
            {"account_id": "low", "scores": _scores(urgency=5)},
            {"account_id": "high", "scores": _max_scores()},
            {"account_id": "mid", "scores": _scores(urgency=15, lost_revenue_visibility=10)},
        ]
        results = batch_score(accounts)
        totals = [r.total for r in results]
        assert totals == sorted(totals, reverse=True)

    def test_batch_score_first_result_is_highest(self) -> None:
        accounts = [
            {"account_id": "low", "scores": _scores()},
            {"account_id": "top", "scores": _max_scores()},
        ]
        results = batch_score(accounts)
        assert results[0].account_id == "top"

    def test_batch_score_returns_all_accounts(self) -> None:
        accounts = [_account(f"acc_{i}") for i in range(5)]
        results = batch_score(accounts)
        assert len(results) == 5

    def test_batch_score_empty_list_returns_empty(self) -> None:
        assert batch_score([]) == []

    def test_batch_score_single_account(self) -> None:
        accounts = [_account("solo")]
        results = batch_score(accounts)
        assert len(results) == 1
        assert results[0].account_id == "solo"

    def test_batch_score_mixed_tiers(self) -> None:
        accounts = [
            {"account_id": "tier_a", "scores": _max_scores()},
            {"account_id": "tier_b", "scores": _scores(urgency=15, lost_revenue_visibility=12, process_chaos=12, decision_maker_access=8, ability_to_start_small=8)},
            {"account_id": "tier_c", "scores": _scores(urgency=8, lost_revenue_visibility=5)},
            {"account_id": "tier_dq", "scores": _scores(urgency=2)},
        ]
        results = batch_score(accounts)
        tiers = [r.tier for r in results]
        assert "A" in tiers
        assert "DQ" in tiers

    def test_batch_score_all_icp_score_instances(self) -> None:
        accounts = [_account(f"x_{i}") for i in range(3)]
        for result in batch_score(accounts):
            assert isinstance(result, ICPScore)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_score_zero_is_dq(self) -> None:
        result = score_account(_account())
        assert result.total == 0
        assert result.tier == "DQ"

    def test_score_100_is_tier_a(self) -> None:
        result = score_account({"account_id": "max", "scores": _max_scores()})
        assert result.total == 100
        assert result.tier == "A"

    def test_notes_passed_through(self) -> None:
        result = score_account({**_account(), "notes": "Important client"})
        assert result.notes == "Important client"

    def test_notes_defaults_to_empty_string(self) -> None:
        result = score_account(_account())
        assert result.notes == ""

    @pytest.mark.parametrize("score,expected_tier", [
        (100, "A"),
        (75, "A"),
        (74, "B"),
        (55, "B"),
        (54, "C"),
        (35, "C"),
        (34, "DQ"),
        (0, "DQ"),
        (-20, "DQ"),
    ])
    def test_tier_label_parametrized_boundaries(self, score: int, expected_tier: str) -> None:
        assert tier_label(score) == expected_tier

    @pytest.mark.parametrize("tier,expected_action", [
        ("A", "pursue_today"),
        ("B", "warm_sequence"),
        ("C", "nurture"),
        ("DQ", "ignore"),
    ])
    def test_action_labels_parametrized(self, tier: str, expected_action: str) -> None:
        # Build an account that lands on the desired tier
        tier_to_score = {
            "A": _max_scores(),
            "B": _scores(urgency=20, lost_revenue_visibility=15, process_chaos=10, decision_maker_access=10),
            # C tier: total 35-54. urgency=20 + lost_revenue_visibility=15 + process_chaos=5 = 40 -> C
            "C": _scores(urgency=20, lost_revenue_visibility=15, process_chaos=5),
            "DQ": _scores(urgency=1),
        }
        result = score_account({"account_id": f"action_{tier}", "scores": tier_to_score[tier]})
        assert result.action == expected_action
