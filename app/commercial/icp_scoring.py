"""ICP (Ideal Customer Profile) scoring for commercial accounts.

Scoring is deterministic and explainable: every account receives a 0–100
score built from weighted signals plus a short rationale. We never invent
data — an account with no source is penalised, never rewarded.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import COMMERCIAL_MOTIONS, CommercialAccount

# Default ICP rule set. Overridable via data/commercial/icp_rules.sample.json.
DEFAULT_ICP_RULES: dict[str, Any] = {
    "target_sectors": [
        "retail",
        "ecommerce",
        "healthcare",
        "real_estate",
        "logistics",
        "professional_services",
        "education",
        "hospitality",
    ],
    "target_cities": ["riyadh", "jeddah", "dammam", "khobar", "mecca", "medina"],
    "weights": {
        "sector_fit": 22,
        "location_fit": 12,
        "pain_signal": 20,
        "contactability": 16,
        "source_present": 14,
        "motion_fit": 10,
        "urgency_signal": 6,
    },
    "risk_penalty": {"high": 18, "medium": 6, "low": 0},
}


def _g(account: Any, key: str, default: Any = "") -> Any:
    if isinstance(account, Mapping):
        return account.get(key, default)
    return getattr(account, key, default)


def score_account(
    account: Any,
    icp_rules: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return ``{"score": float, "breakdown": {...}, "rationale": [...]}``.

    The score is clamped to ``[0, 100]``. The breakdown documents how each
    signal contributed so the result is auditable in the command room.
    """
    rules = {**DEFAULT_ICP_RULES, **(icp_rules or {})}
    weights = {**DEFAULT_ICP_RULES["weights"], **rules.get("weights", {})}
    sectors = [s.lower() for s in rules.get("target_sectors", [])]
    cities = [c.lower() for c in rules.get("target_cities", [])]

    breakdown: dict[str, float] = {}
    rationale: list[str] = []

    # Sector fit.
    sector = str(_g(account, "sector")).lower()
    if sector and sector in sectors:
        breakdown["sector_fit"] = weights["sector_fit"]
        rationale.append(f"sector '{sector}' is in ICP")
    else:
        breakdown["sector_fit"] = 0.0
        rationale.append(f"sector '{sector or 'unknown'}' outside core ICP")

    # Location fit.
    city = str(_g(account, "city")).lower()
    if city and city in cities:
        breakdown["location_fit"] = weights["location_fit"]
        rationale.append(f"city '{city}' is a target market")
    else:
        breakdown["location_fit"] = weights["location_fit"] * 0.4 if city else 0.0

    # Pain signal — a stated hypothesis is evidence of relevance.
    pain = str(_g(account, "pain_hypothesis")).strip()
    breakdown["pain_signal"] = weights["pain_signal"] if pain else 0.0
    if pain:
        rationale.append("documented pain hypothesis present")

    # Contactability — at least one usable, non-opted-out channel.
    has_channel = any(_g(account, k) for k in ("public_email", "whatsapp", "phone", "linkedin_url"))
    opted_out = str(_g(account, "contactability_status")).lower() in ("opted_out", "blocked")
    if has_channel and not opted_out:
        breakdown["contactability"] = weights["contactability"]
        rationale.append("reachable on at least one channel")
    else:
        breakdown["contactability"] = 0.0
        if opted_out:
            rationale.append("contact opted out — not eligible for outreach")

    # Source present — never reward fabricated leads.
    source = str(_g(account, "source_url")).strip()
    breakdown["source_present"] = weights["source_present"] if source else 0.0
    if not source:
        rationale.append("no source_url — flagged unverified, send blocked")

    # Motion fit.
    motion = str(_g(account, "recommended_motion")).strip()
    breakdown["motion_fit"] = weights["motion_fit"] if motion in COMMERCIAL_MOTIONS else 0.0

    # Urgency signal keyword sweep over the pain hypothesis.
    urgency_terms = ("urgent", "asap", "deadline", "عاجل", "بسرعة", "now", "this quarter")
    if any(t in pain.lower() for t in urgency_terms):
        breakdown["urgency_signal"] = weights["urgency_signal"]
        rationale.append("urgency signal detected")
    else:
        breakdown["urgency_signal"] = 0.0

    raw = sum(breakdown.values())

    # Risk penalty.
    risk = str(_g(account, "risk_level", "medium")).lower()
    penalty = rules.get("risk_penalty", {}).get(risk, 6)
    breakdown["risk_penalty"] = -float(penalty)
    if penalty:
        rationale.append(f"risk '{risk}' penalty -{penalty}")

    score = max(0.0, min(100.0, raw - penalty))
    return {
        "score": round(score, 1),
        "breakdown": breakdown,
        "rationale": rationale,
        "tier": _tier(score),
    }


def _tier(score: float) -> str:
    if score >= 70:
        return "A"
    if score >= 50:
        return "B"
    if score >= 30:
        return "C"
    return "D"


def apply_score(account: CommercialAccount, icp_rules: Mapping[str, Any] | None = None) -> CommercialAccount:
    """Mutate-and-return: write the computed ICP score onto the account."""
    result = score_account(account, icp_rules)
    account.icp_score = result["score"]
    return account
