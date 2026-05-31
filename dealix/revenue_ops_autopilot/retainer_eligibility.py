"""Retainer Eligibility Engine — determines whether a sprint client qualifies
for a Managed Ops retainer after completing the Revenue Intelligence Sprint.

Eligibility rules:
  - proof_level >= L1
  - satisfaction_score >= 7
  - measurable_result_achieved is True

Recommended tier is determined by proof level and satisfaction:
  - L3-L4 + satisfaction >= 9  → scale_4999
  - L2-L3 + satisfaction >= 8  → growth_3999
  - Otherwise eligible         → starter_2999

Governance doctrine:
  - RetainerPitch always requires_founder_review = True
  - No revenue guarantees in pitch copy (claim_safety enforced)
  - ROI framing uses time/effort comparisons, never revenue promises
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

ProofLevel = Literal["L0", "L1", "L2", "L3", "L4"]
RetainerTier = Literal["starter_2999", "growth_3999", "scale_4999"]

_PROOF_LEVEL_RANK: dict[ProofLevel, int] = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
    "L4": 4,
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class RetainerEligibilityCheck(BaseModel):
    """Result of the retainer eligibility evaluation for one sprint."""

    model_config = ConfigDict(extra="forbid")

    sprint_id: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    proof_level: ProofLevel = Field(..., description="Highest proof level achieved in the sprint.")
    satisfaction_score: float = Field(
        ..., ge=0.0, le=10.0, description="Founder/client satisfaction 0-10."
    )
    measurable_result_achieved: bool = Field(
        ..., description="At least one measurable, documented outcome reached."
    )
    is_eligible: bool = Field(
        default=False, description="True when all eligibility criteria are met."
    )
    recommended_tier: RetainerTier | None = Field(
        default=None, description="Tier to propose when eligible."
    )
    ineligibility_reasons: list[str] = Field(
        default_factory=list,
        description="Reasons for ineligibility (empty when eligible).",
    )
    upsell_pitch_ar: str = Field(default="", description="Arabic upsell pitch text.")
    upsell_pitch_en: str = Field(default="", description="English upsell pitch text.")


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

_MIN_PROOF_LEVEL: ProofLevel = "L1"
_MIN_SATISFACTION: float = 7.0

_TIER_PITCHES: dict[RetainerTier, tuple[str, str]] = {
    "starter_2999": (
        "انضم إلى باقة Starter بـ 2,999 ريال/شهر واحصل على دعم عمليات منتظم، "
        "ومراجعة شهرية للعملاء المحتملين، وتقارير أداء موثَّقة.",
        "Join the Starter plan at 2,999 SAR/month for regular operations support, "
        "monthly pipeline reviews, and documented performance reports.",
    ),
    "growth_3999": (
        "ارتقِ إلى باقة Growth بـ 3,999 ريال/شهر لتحصل على إدارة كاملة للعملاء المحتملين، "
        "وسِجل قيمة شهري، ومراجعة استراتيجية كل أسبوعين.",
        "Upgrade to the Growth plan at 3,999 SAR/month for full pipeline management, "
        "a monthly value ledger, and bi-weekly strategy reviews.",
    ),
    "scale_4999": (
        "انضم إلى باقة Scale بـ 4,999 ريال/شهر وادفع نمو مؤسستك عبر عمليات ذكاء اصطناعي "
        "مُدارة بالكامل، وتقارير مجلس الإدارة، وتكامل مع أنظمة CRM.",
        "Join the Scale plan at 4,999 SAR/month to power your growth with fully managed "
        "AI operations, board-ready reports, and CRM system integration.",
    ),
}


def _determine_tier(proof_level: ProofLevel, satisfaction: float) -> RetainerTier:
    rank = _PROOF_LEVEL_RANK[proof_level]
    if rank >= 3 and satisfaction >= 9.0:
        return "scale_4999"
    if rank >= 2 and satisfaction >= 8.0:
        return "growth_3999"
    return "starter_2999"


class RetainerEligibilityEngine:
    """Evaluates post-sprint retainer eligibility. No external I/O."""

    def check(self, sprint_result: dict) -> RetainerEligibilityCheck:
        """Evaluate eligibility from a sprint result dict.

        Required keys in *sprint_result*:
            sprint_id (str), account_id (str), proof_level (str),
            satisfaction_score (float), measurable_result_achieved (bool).
        """
        sprint_id: str = str(sprint_result.get("sprint_id", ""))
        account_id: str = str(sprint_result.get("account_id", ""))
        proof_level_raw: str = str(sprint_result.get("proof_level", "L0"))
        satisfaction: float = float(sprint_result.get("satisfaction_score", 0.0))
        measurable: bool = bool(sprint_result.get("measurable_result_achieved", False))

        # Normalise proof level
        proof_level: ProofLevel = proof_level_raw if proof_level_raw in _PROOF_LEVEL_RANK else "L0"  # type: ignore[assignment]

        ineligibility_reasons: list[str] = []

        # Gate 1: proof level
        if _PROOF_LEVEL_RANK[proof_level] < _PROOF_LEVEL_RANK[_MIN_PROOF_LEVEL]:
            ineligibility_reasons.append(
                f"proof_level_too_low: {proof_level} < {_MIN_PROOF_LEVEL}"
            )

        # Gate 2: satisfaction
        if satisfaction < _MIN_SATISFACTION:
            ineligibility_reasons.append(
                f"satisfaction_below_threshold: {satisfaction} < {_MIN_SATISFACTION}"
            )

        # Gate 3: measurable result
        if not measurable:
            ineligibility_reasons.append("no_measurable_result_achieved")

        is_eligible = len(ineligibility_reasons) == 0
        recommended_tier: RetainerTier | None = None
        upsell_ar = ""
        upsell_en = ""

        if is_eligible:
            recommended_tier = _determine_tier(proof_level, satisfaction)
            upsell_ar, upsell_en = _TIER_PITCHES[recommended_tier]

        return RetainerEligibilityCheck(
            sprint_id=sprint_id,
            account_id=account_id,
            proof_level=proof_level,
            satisfaction_score=satisfaction,
            measurable_result_achieved=measurable,
            is_eligible=is_eligible,
            recommended_tier=recommended_tier,
            ineligibility_reasons=ineligibility_reasons,
            upsell_pitch_ar=upsell_ar,
            upsell_pitch_en=upsell_en,
        )


# ---------------------------------------------------------------------------
# RetainerPitch model
# ---------------------------------------------------------------------------


class RetainerPitch(BaseModel):
    """A complete bilingual retainer pitch derived from proven sprint outcomes.

    Governance: always requires founder review before client delivery.
    Copy doctrine: no revenue guarantees — ROI framing is time/effort based.
    """

    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1)
    recommended_tier: str = Field(
        ..., description="starter_2999 | growth_3999 | scale_4999"
    )
    monthly_sar: float = Field(..., ge=0.0, description="Monthly fee in SAR.")
    pitch_headline_ar: str = Field(..., min_length=1, description="Arabic pitch headline.")
    pitch_headline_en: str = Field(..., min_length=1, description="English pitch headline.")
    value_props_ar: list[str] = Field(
        default_factory=list,
        description="3-4 specific proven value propositions from the sprint (Arabic).",
    )
    value_props_en: list[str] = Field(
        default_factory=list,
        description="3-4 specific proven value propositions from the sprint (English).",
    )
    roi_framing_ar: str = Field(
        default="",
        description="Time/effort ROI framing — never a revenue promise.",
    )
    roi_framing_en: str = Field(
        default="",
        description="Time/effort ROI framing — never a revenue promise.",
    )
    what_included_ar: list[str] = Field(
        default_factory=list,
        description="Monthly deliverables (Arabic).",
    )
    what_included_en: list[str] = Field(
        default_factory=list,
        description="Monthly deliverables (English).",
    )
    requires_founder_review: bool = Field(
        default=True,
        description="Must always be True — pitch is never sent without founder sign-off.",
    )
    governance_note_ar: str = Field(
        default="يتطلب مراجعة المؤسس قبل المشاركة مع العميل",
    )
    governance_note_en: str = Field(
        default="Requires founder review before sharing with client",
    )


# ---------------------------------------------------------------------------
# Monthly deliverables per tier
# ---------------------------------------------------------------------------

_TIER_MONTHLY_AR: dict[str, list[str]] = {
    "starter_2999": [
        "مراجعة شهرية لمصادر العملاء المحتملين",
        "تقرير أداء موثَّق (4 صفحات)",
        "دعم عمليات متواصل (أسبوعياً)",
        "تحديث درجة جودة البيانات",
    ],
    "growth_3999": [
        "إدارة كاملة لقناة العملاء المحتملين",
        "سِجل قيمة شهري",
        "مراجعة استراتيجية كل أسبوعين",
        "تقرير صحة العملاء (Health Score)",
        "تدقيق الامتثال الشهري",
    ],
    "scale_4999": [
        "عمليات ذكاء اصطناعي مُدارة بالكامل",
        "تقارير جاهزة لمجلس الإدارة",
        "تكامل مع أنظمة CRM",
        "سِجل قيمة + تقرير صحة العملاء شهرياً",
        "مراجعة حوكمة أسبوعية",
        "أولوية في الدعم والاستجابة",
    ],
}

_TIER_MONTHLY_EN: dict[str, list[str]] = {
    "starter_2999": [
        "Monthly pipeline source review",
        "Documented performance report (4 pages)",
        "Ongoing operations support (weekly)",
        "Data quality score refresh",
    ],
    "growth_3999": [
        "Full pipeline management",
        "Monthly value ledger",
        "Bi-weekly strategy review",
        "Customer Health Score report",
        "Monthly compliance audit",
    ],
    "scale_4999": [
        "Fully managed AI operations",
        "Board-ready reports",
        "CRM system integration",
        "Monthly value ledger + customer health report",
        "Weekly governance review",
        "Priority support and response",
    ],
}

_TIER_SAR: dict[str, float] = {
    "starter_2999": 2999.0,
    "growth_3999": 3999.0,
    "scale_4999": 4999.0,
}

_TIER_HEADLINES_AR: dict[str, str] = {
    "starter_2999": "ابدأ رحلتك مع Starter — عمليات منتظمة بـ 2,999 ريال/شهر",
    "growth_3999": "ارتقِ إلى Growth — إدارة كاملة بـ 3,999 ريال/شهر",
    "scale_4999": "قُد نموّك مع Scale — عمليات AI مُدارة بـ 4,999 ريال/شهر",
}

_TIER_HEADLINES_EN: dict[str, str] = {
    "starter_2999": "Start with Starter — regular operations at 2,999 SAR/month",
    "growth_3999": "Upgrade to Growth — full management at 3,999 SAR/month",
    "scale_4999": "Power your growth with Scale — managed AI ops at 4,999 SAR/month",
}

_TIER_ROI_AR: dict[str, str] = {
    "starter_2999": (
        "هذا الاستثمار يعادل تقريباً 15 ساعة عمل محلَّل بيانات شهرياً — "
        "ادفع قيمة ساعة واحصل على الاطمئنان الكامل."
    ),
    "growth_3999": (
        "هذا الاستثمار يعادل تقريباً 25 ساعة عمل مدير عمليات شهرياً — "
        "مع توثيق كامل وسِجل قيمة يُبيِّن الأثر الفعلي لكل ريال."
    ),
    "scale_4999": (
        "هذا الاستثمار يعادل تقريباً 35 ساعة عمل فريق عمليات AI شهرياً — "
        "مع تقارير جاهزة لمجلس الإدارة وتكامل مع الأنظمة."
    ),
}

_TIER_ROI_EN: dict[str, str] = {
    "starter_2999": (
        "This investment is roughly equivalent to 15 hours of a data analyst's work per month — "
        "pay for one hour's value and get full peace of mind."
    ),
    "growth_3999": (
        "This investment is roughly equivalent to 25 hours of an operations manager's time per month — "
        "with full documentation and a value ledger showing the real impact of every riyal."
    ),
    "scale_4999": (
        "This investment is roughly equivalent to 35 hours of an AI operations team per month — "
        "with board-ready reports and system integrations."
    ),
}


# ---------------------------------------------------------------------------
# Pitch generator function
# ---------------------------------------------------------------------------


def generate_retainer_pitch(
    eligibility_result: RetainerEligibilityCheck,
    health_report: Optional[dict] = None,
    sprint_report: Optional[dict] = None,
) -> RetainerPitch:
    """Generate a complete retainer pitch based on proven sprint outcomes.

    :param eligibility_result: Output of RetainerEligibilityEngine.check().
    :param health_report: Optional dict from CustomerHealthEngine.calculate().
    :param sprint_report: Optional dict from SprintReportGenerator.to_dict().
    :returns: A RetainerPitch with bilingual copy, no revenue guarantees.
    """
    # Default to starter tier if not eligible or no tier assigned
    tier: str = eligibility_result.recommended_tier or "starter_2999"

    # Extract sprint-level proof signals to personalise value props
    value_props_en: list[str] = []
    value_props_ar: list[str] = []

    if sprint_report and isinstance(sprint_report, dict):
        findings_en = sprint_report.get("findings_en", [])
        findings_ar = sprint_report.get("findings_ar", [])
        # Use up to 3 sprint findings as value props
        value_props_en.extend(findings_en[:3])
        value_props_ar.extend(findings_ar[:3])

    if health_report and isinstance(health_report, dict):
        health_score = health_report.get("overall_score") or health_report.get("score")
        if health_score is not None:
            value_props_en.append(
                f"Customer health score baseline established: {health_score:.0f}/100."
            )
            value_props_ar.append(
                f"تأسيس قاعدة درجة صحة العملاء: {health_score:.0f}/100."
            )

    # Fall back to tier-generic value props if sprint produced no findings
    if not value_props_en:
        value_props_en = [
            "Data quality scored and documented.",
            "Top accounts ranked by ICP score.",
            "Proof Pack assembled with L0-L2 evidence.",
        ]
    if not value_props_ar:
        value_props_ar = [
            "تم تقييم وتوثيق جودة البيانات.",
            "تصنيف أعلى الحسابات بمعيار ICP.",
            "تجميع Proof Pack مع أدلة L0-L2.",
        ]

    return RetainerPitch(
        account_id=eligibility_result.account_id,
        recommended_tier=tier,
        monthly_sar=_TIER_SAR[tier],
        pitch_headline_ar=_TIER_HEADLINES_AR[tier],
        pitch_headline_en=_TIER_HEADLINES_EN[tier],
        value_props_ar=value_props_ar,
        value_props_en=value_props_en,
        roi_framing_ar=_TIER_ROI_AR[tier],
        roi_framing_en=_TIER_ROI_EN[tier],
        what_included_ar=_TIER_MONTHLY_AR[tier],
        what_included_en=_TIER_MONTHLY_EN[tier],
        requires_founder_review=True,
        governance_note_ar="يتطلب مراجعة المؤسس قبل المشاركة مع العميل",
        governance_note_en="Requires founder review before sharing with client",
    )
