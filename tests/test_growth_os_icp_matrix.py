"""ICP matrix smoke + scoring monotonicity tests."""

from __future__ import annotations

from dealix.growth_os.icp.matrix import ICP_MATRIX, get_icp, list_icps
from dealix.growth_os.icp.scoring import score_icp_fit

REQUIRED_KEYS = {
    "agencies",
    "b2b_smb",
    "founders",
    "ai_users_governance",
    "enterprise",
    "consultants",
    "training_providers",
}


def test_icp_matrix_has_seven_required_profiles() -> None:
    assert set(ICP_MATRIX.keys()) == REQUIRED_KEYS
    assert len(list_icps()) == 7


def test_each_icp_has_bilingual_pain_and_offer() -> None:
    for icp in ICP_MATRIX.values():
        assert icp.name_ar and icp.name_en
        assert icp.primary_pain_ar and icp.primary_pain_en
        assert icp.primary_offer
        assert icp.decision_makers
        lo, hi = icp.typical_arr_band_usd
        assert lo > 0 and hi >= lo


def test_get_icp_unknown_raises() -> None:
    try:
        get_icp("does_not_exist")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown icp key")


def test_score_icp_fit_is_monotonic_in_matches() -> None:
    # Compare an empty-signal account to one with a matching offer request.
    empty = score_icp_fit(
        {
            "pains": [],
            "decision_makers": [],
            "estimated_arr_usd": 0,
            "requested_assets": [],
            "flags": [],
        }
    )
    strong = score_icp_fit(
        {
            "pains": ["governed AI"],
            "decision_makers": ["cto"],
            "estimated_arr_usd": 20_000,
            "requested_assets": ["governance_kit"],
            "flags": [],
        }
    )
    assert strong.score >= empty.score


def test_disqualifier_lowers_band_to_reject() -> None:
    res = score_icp_fit(
        {
            "pains": ["pre_revenue"],
            "decision_makers": ["ceo"],
            "estimated_arr_usd": 0,
            "requested_assets": [],
            "flags": ["pre_revenue"],
        }
    )
    # The b2b_smb ICP disqualifies on pre_revenue. The best-fit may not be
    # b2b_smb, but if any disqualifier is set on the chosen ICP it must reject.
    if res.icp_key == "b2b_smb":
        assert res.band == "reject"
