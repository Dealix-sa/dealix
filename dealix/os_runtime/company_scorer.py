"""
Company Scorer
==============
Scores a company's fit for Dealix based on operational signals.
Returns a tier (A/B/C/D) and recommended action.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CompanySignal:
    """Operational signals observed for a prospect company."""

    company: str
    country: str = ""
    sector: str = ""

    # Primary fit signals (weighted)
    operations_heavy: bool = False
    maintenance_or_field_work: bool = False
    repeated_reporting: bool = False
    multi_branch_or_multi_site: bool = False
    clear_buyer_title: bool = False
    public_growth_signal: bool = False
    likely_data_or_api: bool = False
    founder_domain_fit: bool = False

    # Enrichment (unweighted, stored for context)
    extras: dict = field(default_factory=dict)
    notes: str = ""
    source_ref: Optional[str] = None


# Factor weights — must sum to 100 for a perfect score
WEIGHTS: dict[str, int] = {
    "operations_heavy": 20,
    "maintenance_or_field_work": 20,
    "repeated_reporting": 15,
    "multi_branch_or_multi_site": 10,
    "clear_buyer_title": 10,
    "public_growth_signal": 10,
    "likely_data_or_api": 10,
    "founder_domain_fit": 5,
}

# Tier thresholds
TIER_THRESHOLDS = [
    (85, "A", "deep_research_custom_pack"),
    (70, "B", "sector_personalized_pack"),
    (55, "C", "nurture_or_light_touch"),
    (0, "D", "archive_or_research_later"),
]


def score_company(signal: CompanySignal) -> dict:
    """
    Score a company and return tier + recommended action.

    Returns:
        dict with keys: company, country, sector, fit_score, tier,
                        recommended_action, reasons
    """
    score = 0
    reasons = []

    for key, weight in WEIGHTS.items():
        if getattr(signal, key, False):
            score += weight
            reasons.append({"factor": key, "points": weight})

    # Determine tier
    tier = "D"
    action = "archive_or_research_later"
    for threshold, t, a in TIER_THRESHOLDS:
        if score >= threshold:
            tier = t
            action = a
            break

    return {
        "company": signal.company,
        "country": signal.country,
        "sector": signal.sector,
        "fit_score": score,
        "tier": tier,
        "recommended_action": action,
        "reasons": reasons,
        "source_ref": signal.source_ref,
        "governance_decision": {
            "module": "company_scorer",
            "version": "1.0",
            "score": score,
            "tier": tier,
            "action": action,
        },
    }


def score_from_dict(data: dict) -> dict:
    """
    Convenience: build a CompanySignal from a plain dict and score it.
    Used by __main__ and tests.
    """
    signal = CompanySignal(
        company=data.get("company") or data.get("name") or "",
        country=data.get("country", ""),
        sector=data.get("sector", ""),
        operations_heavy=bool(data.get("operations_heavy", False)),
        maintenance_or_field_work=bool(data.get("maintenance_or_field_work", False)),
        repeated_reporting=bool(data.get("repeated_reporting", False)),
        multi_branch_or_multi_site=bool(data.get("multi_branch_or_multi_site", False)),
        clear_buyer_title=bool(data.get("clear_buyer_title", False)),
        public_growth_signal=bool(data.get("public_growth_signal", False)),
        likely_data_or_api=bool(data.get("likely_data_or_api", False)),
        founder_domain_fit=bool(data.get("founder_domain_fit", False)),
        extras=data.get("extras", {}),
        notes=data.get("notes", ""),
        source_ref=data.get("source_ref"),
    )
    return score_company(signal)
