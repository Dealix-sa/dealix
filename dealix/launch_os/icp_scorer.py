"""ICP scoring engine for the Dealix launch OS.

Rubric (100 points max, -20 penalty floor):
  urgency                    0-20
  lost_revenue_visibility    0-15
  process_chaos              0-15
  decision_maker_access      0-10
  ability_to_start_small     0-10
  proof_speed                0-10
  budget_likelihood          0-10
  repeatability              0-5
  referral_potential         0-5
  compliance_delivery_risk   -20-0 (penalty)

Tier labels:
  A  >= 75   pursue_today
  B  55-74   warm_sequence
  C  35-54   nurture
  DQ < 35    ignore / manual_review

Schema validation honours schemas/launch/icp_score.schema.json.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent.parent / "schemas" / "launch" / "icp_score.schema.json"
)

# Maximum points per dimension (penalty is handled separately).
_MAX_SCORES: dict[str, int] = {
    "urgency": 20,
    "lost_revenue_visibility": 15,
    "process_chaos": 15,
    "decision_maker_access": 10,
    "ability_to_start_small": 10,
    "proof_speed": 10,
    "budget_likelihood": 10,
    "repeatability": 5,
    "referral_potential": 5,
    "compliance_delivery_risk": 0,  # penalty dimension
}

_POSITIVE_DIMS = [k for k, v in _MAX_SCORES.items() if v > 0]
_PENALTY_DIMS = ["compliance_delivery_risk"]


@dataclass
class ICPScore:
    """Result of scoring one target account.

    Attributes:
        account_id:     Identifier passed in from the account dict.
        scores:         Raw dimension scores as provided or derived.
        total:          Sum of all dimension scores (capped to -20..100).
        tier:           Letter grade A/B/C/DQ.
        action:         Recommended next action string.
        notes:          Optional free-text rationale.

    Examples:
        >>> s = ICPScore(
        ...     account_id="acme",
        ...     scores={"urgency": 18, "lost_revenue_visibility": 12,
        ...             "process_chaos": 10, "decision_maker_access": 8,
        ...             "ability_to_start_small": 9, "proof_speed": 8,
        ...             "budget_likelihood": 9, "repeatability": 4,
        ...             "referral_potential": 4, "compliance_delivery_risk": 0},
        ...     total=82, tier="A", action="pursue_today", notes="")
        >>> s.tier
        'A'
    """

    account_id: str
    scores: dict[str, int]
    total: int
    tier: str
    action: str
    notes: str = ""


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _derive_scores(account: dict[str, Any]) -> dict[str, int]:
    """Derive dimension scores from a raw account dict.

    The caller may embed a ``"scores"`` sub-dict directly, or rely on the
    heuristic mapping below which inspects top-level account fields.
    """
    if "scores" in account and isinstance(account["scores"], dict):
        raw = account["scores"]
        return {
            dim: _clamp(int(raw.get(dim, 0)), -20 if dim in _PENALTY_DIMS else 0, _MAX_SCORES[dim] if dim not in _PENALTY_DIMS else 0)
            for dim in _MAX_SCORES
        }

    # Heuristic derivation from account metadata.
    urgency_map = {"critical": 20, "high": 15, "medium": 8, "low": 3, "unknown": 0}
    size_map = {"enterprise": 10, "mid_market": 8, "smb": 6, "micro": 4, "unknown": 0}
    dm_map = {"direct": 10, "champion": 7, "gatekeeper": 4, "unknown": 0}
    budget_map = {"confirmed": 10, "likely": 7, "possible": 4, "unlikely": 0, "unknown": 0}

    urgency = urgency_map.get(str(account.get("urgency", "unknown")).lower(), 0)
    revenue_vis = _clamp(int(account.get("revenue_leak_sar", 0)) // 50_000, 0, 15)
    chaos = _clamp(int(account.get("process_chaos_score", 0)), 0, 15)
    dm_access = dm_map.get(str(account.get("decision_maker_access", "unknown")).lower(), 0)
    start_small = _clamp(int(account.get("start_small_score", 5)), 0, 10)
    proof_speed = _clamp(int(account.get("proof_speed_score", 5)), 0, 10)
    budget = budget_map.get(str(account.get("budget_signal", "unknown")).lower(), 0)
    repeatability = size_map.get(str(account.get("size", "unknown")).lower(), 0) // 2
    referral = _clamp(int(account.get("referral_potential_score", 2)), 0, 5)
    compliance_risk = _clamp(int(account.get("compliance_risk_penalty", 0)), -20, 0)

    return {
        "urgency": urgency,
        "lost_revenue_visibility": revenue_vis,
        "process_chaos": chaos,
        "decision_maker_access": dm_access,
        "ability_to_start_small": start_small,
        "proof_speed": proof_speed,
        "budget_likelihood": budget,
        "repeatability": repeatability,
        "referral_potential": referral,
        "compliance_delivery_risk": compliance_risk,
    }


def _action_for_tier(tier: str) -> str:
    mapping = {
        "A": "pursue_today",
        "B": "warm_sequence",
        "C": "nurture",
        "DQ": "ignore",
    }
    return mapping.get(tier, "manual_review")


def tier_label(score: float) -> str:
    """Return letter tier for a numeric ICP score.

    Args:
        score: Numeric total between -20 and 100.

    Returns:
        One of ``"A"``, ``"B"``, ``"C"``, ``"DQ"``.

    Examples:
        >>> tier_label(80)
        'A'
        >>> tier_label(60)
        'B'
        >>> tier_label(40)
        'C'
        >>> tier_label(20)
        'DQ'
    """
    if score >= 75:
        return "A"
    if score >= 55:
        return "B"
    if score >= 35:
        return "C"
    return "DQ"


def score_account(account: dict[str, Any]) -> ICPScore:
    """Score a single target account dict and return an ICPScore.

    Args:
        account: Dict with ``account_id`` and either a ``"scores"`` sub-dict
                 or heuristic fields (urgency, revenue_leak_sar, etc.).

    Returns:
        Fully populated :class:`ICPScore`.

    Examples:
        >>> result = score_account({
        ...     "account_id": "acme_001",
        ...     "scores": {
        ...         "urgency": 15,
        ...         "lost_revenue_visibility": 10,
        ...         "process_chaos": 10,
        ...         "decision_maker_access": 8,
        ...         "ability_to_start_small": 8,
        ...         "proof_speed": 7,
        ...         "budget_likelihood": 7,
        ...         "repeatability": 4,
        ...         "referral_potential": 3,
        ...         "compliance_delivery_risk": 0,
        ...     },
        ... })
        >>> result.tier
        'B'
        >>> result.total
        72
    """
    account_id = str(account.get("account_id", "unknown"))
    scores = _derive_scores(account)
    total = _clamp(sum(scores.values()), -20, 100)
    tier = tier_label(total)
    action = _action_for_tier(tier)
    notes = str(account.get("notes", ""))
    return ICPScore(
        account_id=account_id,
        scores=scores,
        total=total,
        tier=tier,
        action=action,
        notes=notes,
    )


def batch_score(accounts: list[dict[str, Any]]) -> list[ICPScore]:
    """Score a list of account dicts, sorted descending by total.

    Args:
        accounts: List of account dicts accepted by :func:`score_account`.

    Returns:
        List of :class:`ICPScore` objects sorted highest-to-lowest.

    Examples:
        >>> results = batch_score([
        ...     {"account_id": "a", "scores": {"urgency": 20, "lost_revenue_visibility": 15,
        ...       "process_chaos": 15, "decision_maker_access": 10,
        ...       "ability_to_start_small": 10, "proof_speed": 10,
        ...       "budget_likelihood": 10, "repeatability": 5,
        ...       "referral_potential": 5, "compliance_delivery_risk": 0}},
        ...     {"account_id": "b", "scores": {"urgency": 5, "lost_revenue_visibility": 2,
        ...       "process_chaos": 3, "decision_maker_access": 2,
        ...       "ability_to_start_small": 2, "proof_speed": 2,
        ...       "budget_likelihood": 2, "repeatability": 1,
        ...       "referral_potential": 1, "compliance_delivery_risk": 0}},
        ... ])
        >>> results[0].account_id
        'a'
        >>> results[0].tier
        'A'
    """
    scored = [score_account(a) for a in accounts]
    return sorted(scored, key=lambda s: s.total, reverse=True)


def load_schema() -> dict[str, Any]:
    """Return the raw JSON Schema dict for ICP Score."""
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"ICP scorer doctests: {results.attempted} run, {results.failed} failed")

    sample = {
        "account_id": "smoke_test",
        "urgency": "high",
        "revenue_leak_sar": 300_000,
        "process_chaos_score": 10,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 7,
        "budget_signal": "likely",
        "repeatability": 3,
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    }
    s = score_account(sample)
    print(f"Smoke test account '{s.account_id}': total={s.total} tier={s.tier} action={s.action}")
