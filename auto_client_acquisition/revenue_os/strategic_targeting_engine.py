"""Strategic Targeting Engine — autonomous multi-dimensional account prioritization.

Scores prospects across 8 dimensions and outputs prioritized targeting results
with Saudi-market-aware motions and recommended offers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TargetTier(StrEnum):
    P0 = "P0"           # Act now — highest priority
    P1 = "P1"           # This week
    P2 = "P2"           # This month
    NURTURE = "nurture" # 90+ days
    NO_FIT = "no_fit"   # Do not engage


class MotionType(StrEnum):
    A = "A"  # Agency wedge — proof pack
    B = "B"  # Direct B2B — governed diagnostic
    C = "C"  # Diagnostic layer — capability diagnostic
    D = "D"  # Executive governance — board-level
    E = "E"  # CRM partner / referral


@dataclass(frozen=True, slots=True)
class TargetingDimensions:
    """8-dimensional prospect scoring for strategic account prioritization."""

    icp_fit: int                # 0-100: Firmographic match to ICP profile
    pain_urgency: int           # 0-100: How acute is the pain right now
    timing_score: int           # 0-100: Budget cycle, trigger events alignment
    access_score: int           # 0-100: Decision-maker proximity
    budget_readiness: int       # 0-100: Budget signals (5k+ SAR threshold)
    sector_fit: int             # 0-100: Saudi sector opportunity size
    proof_path_potential: int   # 0-100: Can we generate compelling proof
    competitive_displacement: int  # 0-100: Competitor vulnerability


@dataclass(frozen=True, slots=True)
class TargetingResult:
    """Output of strategic targeting engine."""

    total_score: int
    tier: TargetTier
    recommended_motion: MotionType
    recommended_offer_id: str
    priority_rank_percentile: int   # 0-100, 100 = top priority
    reasoning_ar: str
    reasoning_en: str
    next_action_ar: str
    next_action_en: str
    blocking_signals: tuple[str, ...]


# Dimension weights — must sum to 100
_WEIGHTS: dict[str, int] = {
    "icp_fit": 20,
    "pain_urgency": 20,
    "timing_score": 15,
    "access_score": 15,
    "budget_readiness": 10,
    "sector_fit": 8,
    "proof_path_potential": 7,
    "competitive_displacement": 5,
}

assert sum(_WEIGHTS.values()) == 100, "Weights must sum to 100"

# Tier score thresholds
_TIER_THRESHOLDS: list[tuple[int, TargetTier]] = [
    (78, TargetTier.P0),
    (62, TargetTier.P1),
    (45, TargetTier.P2),
    (25, TargetTier.NURTURE),
]

# Motion assignment: sector keyword fragments → motion
_MOTION_MAP: list[tuple[tuple[str, ...], MotionType]] = [
    (("marketing_agency", "digital_agency", "creative_agency", "agency"), MotionType.A),
    (("enterprise", "government", "semi_government", "soe"), MotionType.D),
    (("crm_partner", "si_partner", "reseller", "partner"), MotionType.E),
]

# Offer assignment by (tier, motion)
_OFFER_MAP: dict[tuple[TargetTier, MotionType], str] = {
    (TargetTier.P0, MotionType.A): "agency_proof_pack",
    (TargetTier.P0, MotionType.B): "revenue_intelligence_sprint",
    (TargetTier.P0, MotionType.C): "governed_diagnostic",
    (TargetTier.P0, MotionType.D): "executive_governance_diagnostic",
    (TargetTier.P0, MotionType.E): "partner_sprint",
    (TargetTier.P1, MotionType.A): "ten_lead_audit",
    (TargetTier.P1, MotionType.B): "governed_diagnostic",
    (TargetTier.P1, MotionType.C): "capability_diagnostic",
    (TargetTier.P1, MotionType.D): "executive_governance_diagnostic",
    (TargetTier.P1, MotionType.E): "partner_sprint",
    (TargetTier.P2, MotionType.A): "ten_lead_audit",
    (TargetTier.P2, MotionType.B): "capability_diagnostic",
    (TargetTier.P2, MotionType.C): "capability_diagnostic",
    (TargetTier.P2, MotionType.D): "governed_diagnostic",
    (TargetTier.P2, MotionType.E): "partner_sprint",
    (TargetTier.NURTURE, MotionType.A): "ten_lead_audit",
    (TargetTier.NURTURE, MotionType.B): "ten_lead_audit",
    (TargetTier.NURTURE, MotionType.C): "free_diagnostic",
    (TargetTier.NURTURE, MotionType.D): "free_diagnostic",
    (TargetTier.NURTURE, MotionType.E): "free_diagnostic",
}


def _weighted_score(dims: TargetingDimensions) -> int:
    raw = {
        "icp_fit": dims.icp_fit,
        "pain_urgency": dims.pain_urgency,
        "timing_score": dims.timing_score,
        "access_score": dims.access_score,
        "budget_readiness": dims.budget_readiness,
        "sector_fit": dims.sector_fit,
        "proof_path_potential": dims.proof_path_potential,
        "competitive_displacement": dims.competitive_displacement,
    }
    weighted = sum(min(100, max(0, raw[k])) * _WEIGHTS[k] for k in _WEIGHTS)
    return min(100, weighted // 100)


def _assign_tier(score: int) -> TargetTier:
    for threshold, tier in _TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    if score >= 5:
        return TargetTier.NURTURE
    return TargetTier.NO_FIT


def _assign_motion(dims: TargetingDimensions, sector: str) -> MotionType:
    s = sector.lower()
    for sectors, motion in _MOTION_MAP:
        if any(k in s for k in sectors):
            return motion
    if dims.access_score >= 60:
        return MotionType.B
    return MotionType.C


def _detect_blocking_signals(dims: TargetingDimensions) -> tuple[str, ...]:
    blocks: list[str] = []
    if dims.budget_readiness < 20:
        blocks.append("budget_too_low_or_unclear")
    if dims.access_score < 15:
        blocks.append("no_decision_maker_access")
    if dims.proof_path_potential < 10:
        blocks.append("no_viable_proof_path")
    return tuple(blocks)


def _build_reasoning(
    score: int, tier: TargetTier, dims: TargetingDimensions
) -> tuple[str, str]:
    signals_ar: list[str] = []
    signals_en: list[str] = []
    if dims.pain_urgency >= 70:
        signals_ar.append("ألم عاجل")
        signals_en.append("urgent pain")
    if dims.icp_fit >= 70:
        signals_ar.append("تطابق ICP عالٍ")
        signals_en.append("strong ICP fit")
    if dims.timing_score >= 70:
        signals_ar.append("توقيت مثالي")
        signals_en.append("ideal timing")
    if dims.access_score >= 70:
        signals_ar.append("وصول مباشر للقرار")
        signals_en.append("direct decision access")
    if dims.competitive_displacement >= 70:
        signals_ar.append("فرصة إزاحة منافس")
        signals_en.append("competitive displacement opportunity")
    if not signals_ar:
        signals_ar = ["ملاءمة جزئية"]
        signals_en = ["partial fit"]

    tier_labels_ar: dict[TargetTier, str] = {
        TargetTier.P0: "أولوية قصوى",
        TargetTier.P1: "أولوية هذا الأسبوع",
        TargetTier.P2: "أولوية هذا الشهر",
        TargetTier.NURTURE: "حضانة",
        TargetTier.NO_FIT: "غير مناسب",
    }
    ar = f"{tier_labels_ar[tier]} (درجة {score}/100): {', '.join(signals_ar)}"
    en = f"{tier.value} (score {score}/100): {', '.join(signals_en)}"
    return ar, en


def _build_next_action(tier: TargetTier, offer_id: str) -> tuple[str, str]:
    action_ar: dict[TargetTier, str] = {
        TargetTier.P0: f"صِغ رسالة مُخصَّصة الآن وأرسلها بموافقة المؤسس — عرض: {offer_id}",
        TargetTier.P1: f"ضع في جدول هذا الأسبوع — حرك بعرض: {offer_id}",
        TargetTier.P2: f"أضف لقائمة الشهر — ابدأ بتشخيص: {offer_id}",
        TargetTier.NURTURE: "أضف لقائمة المتابعة — أرسل محتوى ذو قيمة شهرياً",
        TargetTier.NO_FIT: "لا إجراء — دوّن السبب في سجل الاحتكاك",
    }
    action_en: dict[TargetTier, str] = {
        TargetTier.P0: f"Draft personalized message now, send with founder approval — offer: {offer_id}",
        TargetTier.P1: f"Schedule for this week — move with offer: {offer_id}",
        TargetTier.P2: f"Add to monthly list — start with diagnostic: {offer_id}",
        TargetTier.NURTURE: "Add to nurture list — send value content monthly",
        TargetTier.NO_FIT: "No action — log reason in friction log",
    }
    return action_ar[tier], action_en[tier]


def score_target(
    dims: TargetingDimensions,
    *,
    sector: str = "",
) -> TargetingResult:
    """Score a single prospect and return a full targeting result."""
    score = _weighted_score(dims)
    tier = _assign_tier(score)
    motion = _assign_motion(dims, sector)
    offer_id = _OFFER_MAP.get((tier, motion), "capability_diagnostic")
    blocking = _detect_blocking_signals(dims)
    reasoning_ar, reasoning_en = _build_reasoning(score, tier, dims)
    action_ar, action_en = _build_next_action(tier, offer_id)

    return TargetingResult(
        total_score=score,
        tier=tier,
        recommended_motion=motion,
        recommended_offer_id=offer_id,
        priority_rank_percentile=min(100, max(0, score)),
        reasoning_ar=reasoning_ar,
        reasoning_en=reasoning_en,
        next_action_ar=action_ar,
        next_action_en=action_en,
        blocking_signals=blocking,
    )


def prioritize_accounts(
    accounts: list[tuple[str, TargetingDimensions, str]],
) -> list[tuple[str, TargetingResult]]:
    """Score and rank a list of (account_id, dimensions, sector) tuples.

    Returns sorted list (highest score first) of (account_id, result).
    """
    scored = [
        (acct_id, score_target(dims, sector=sector))
        for acct_id, dims, sector in accounts
    ]
    return sorted(scored, key=lambda x: x[1].total_score, reverse=True)


__all__ = [
    "MotionType",
    "TargetingDimensions",
    "TargetingResult",
    "TargetTier",
    "prioritize_accounts",
    "score_target",
]
