"""Research & Discovery Engine — autonomous prospect research and profiling.

Pure-logic engine that discovers potential clients from registered data sources,
profiles companies against ICP criteria, identifies decision-makers, assesses
data quality, and generates research briefs ready for qualification.

No database, network, or LLM calls. All external data acquisition requires
human approval. The engine works on data already collected through approved
sources.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``auto_contact_allowed=False`` always.
- Research briefs are proposals, never direct outreach triggers.
- Saudi B2B ICP focus with Arabic-first context.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class CompanySize(StrEnum):
    """Company size classification."""

    MICRO = "micro"  # 1-10
    SMALL = "small"  # 11-50
    MEDIUM = "medium"  # 51-200
    LARGE = "large"  # 201-1000
    ENTERPRISE = "enterprise"  # 1000+


class SectorFit(StrEnum):
    """How well a company's sector fits the ICP."""

    IDEAL = "ideal"
    GOOD = "good"
    POSSIBLE = "possible"
    POOR = "poor"
    EXCLUDED = "excluded"


class DataQuality(StrEnum):
    """Quality of available data about a prospect."""

    EXCELLENT = "excellent"
    GOOD = "good"
    PARTIAL = "partial"
    MINIMAL = "minimal"
    INSUFFICIENT = "insufficient"


class ResearchDepth(StrEnum):
    """How thoroughly a prospect has been researched."""

    DEEP = "deep"
    STANDARD = "standard"
    SURFACE = "surface"
    UNRESEARCHED = "unresearched"


class DecisionMakerRole(StrEnum):
    """Role of a potential decision maker."""

    FOUNDER_CEO = "founder_ceo"
    GENERAL_MANAGER = "general_manager"
    VP_SALES = "vp_sales"
    VP_OPERATIONS = "vp_operations"
    CTO = "cto"
    CFO = "cfo"
    DEPARTMENT_HEAD = "department_head"
    UNKNOWN = "unknown"


class PainSignal(StrEnum):
    """Identifiable pain signals in a prospect."""

    REVENUE_LEAKAGE = "revenue_leakage"
    FOLLOW_UP_GAPS = "follow_up_gaps"
    NO_CRM = "no_crm"
    MANUAL_PROCESSES = "manual_processes"
    SCALING_PAINS = "scaling_pains"
    HIRING_DIFFICULTY = "hiring_difficulty"
    DATA_SCATTERED = "data_scattered"
    NO_REPORTING = "no_reporting"
    CUSTOMER_CHURN = "customer_churn"
    SLOW_RESPONSE = "slow_response"


class ProspectPriority(StrEnum):
    """Priority classification for a prospect."""

    HOT = "hot"
    WARM = "warm"
    COOL = "cool"
    COLD = "cold"
    DISQUALIFIED = "disqualified"


# ---------------------------------------------------------------------------
# ICP criteria — Saudi B2B focus
# ---------------------------------------------------------------------------

IDEAL_SECTORS = (
    "saas",
    "business_services",
    "professional_services",
    "technology",
    "fintech",
    "logistics_tech",
    "edtech",
    "healthtech",
    "ecommerce_b2b",
    "consulting",
)

EXCLUDED_SECTORS = (
    "banking",
    "government",
    "military",
    "heavily_regulated",
    "consumer_retail",
    "crypto_gambling",
)

ICP_SIZE_RANGE = (20, 200)  # employees


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class DecisionMaker(BaseModel):
    """A potential decision-maker at a prospect company."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = ""
    role: DecisionMakerRole = DecisionMakerRole.UNKNOWN
    title: str = ""
    email: str = ""
    phone: str = ""
    whatsapp: str = ""
    linkedin: str = ""
    is_primary: bool = False
    source: str = ""


class CompanyProfile(BaseModel):
    """Profile of a researched prospect company."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    profile_id: str = ""
    company_name: str = ""
    company_name_ar: str = ""
    sector: str = ""
    sub_sector: str = ""
    employee_count: int = 0
    city: str = ""
    country: str = "SA"
    website: str = ""
    cr_number: str = ""  # commercial registration
    founded_year: int = 0
    annual_revenue_estimate: float = 0.0
    tech_stack: tuple[str, ...] = ()
    current_crm: str = ""
    current_erp: str = ""
    pain_signals: tuple[PainSignal, ...] = ()
    decision_makers: tuple[DecisionMaker, ...] = ()
    sector_fit: SectorFit = SectorFit.POSSIBLE
    company_size: CompanySize = CompanySize.SMALL
    data_quality: DataQuality = DataQuality.MINIMAL
    research_depth: ResearchDepth = ResearchDepth.UNRESEARCHED
    source_url: str = ""
    source_id: NonEmptyString = ""
    notes: str = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    def model_post_init(self, _context: Any) -> None:
        if not self.profile_id:
            object.__setattr__(
                self,
                "profile_id",
                _stable_id(
                    "profile",
                    {
                        "tenant": self.tenant_id,
                        "company": self.company_name,
                        "source": self.source_id,
                    },
                ),
            )


class ICPScore(BaseModel):
    """ICP fit score for a prospect."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    score_id: str = ""
    profile_id: str = ""
    sector_score: float = 0.0  # 0-25
    size_score: float = 0.0  # 0-20
    access_score: float = 0.0  # 0-20 (founder/GM access)
    pain_score: float = 0.0  # 0-20
    data_score: float = 0.0  # 0-15
    total_score: float = 0.0  # 0-100
    priority: ProspectPriority = ProspectPriority.COLD
    qualified: bool = False
    disqualification_reasons: tuple[str, ...] = ()
    source_id: NonEmptyString = ""
    auto_contact_allowed: bool = False

    @model_validator(mode="after")
    def _never_auto_contact(self) -> ICPScore:
        if self.auto_contact_allowed:
            raise ValueError(
                "ICPScore.auto_contact_allowed must be False — "
                "all contact requires human approval"
            )
        return self


class ResearchBrief(BaseModel):
    """Complete research brief for a prospect — ready for founder review."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    brief_id: str = ""
    profile: CompanyProfile
    icp_score: ICPScore
    recommended_approach: str = ""
    recommended_channel: str = "email"
    talking_points: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    next_steps: tuple[str, ...] = ()
    summary_ar: str = ""
    summary_en: str = ""
    approval_required: bool = True
    auto_contact_allowed: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _safety_invariants(self) -> ResearchBrief:
        if self.auto_contact_allowed:
            raise ValueError(
                "ResearchBrief.auto_contact_allowed must be False — "
                "all outreach requires human approval"
            )
        if not self.approval_required:
            raise ValueError(
                "ResearchBrief.approval_required must be True — "
                "founder must approve before any contact"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.brief_id:
            object.__setattr__(
                self,
                "brief_id",
                _stable_id(
                    "research",
                    {
                        "tenant": self.tenant_id,
                        "profile": self.profile.profile_id,
                        "source": self.source_id,
                    },
                ),
            )


# ---------------------------------------------------------------------------
# Scoring functions
# ---------------------------------------------------------------------------


def score_sector_fit(sector: str) -> tuple[SectorFit, float]:
    """Score how well a sector matches the ICP."""
    s = sector.lower().strip()
    if s in EXCLUDED_SECTORS:
        return SectorFit.EXCLUDED, 0.0
    if s in IDEAL_SECTORS:
        return SectorFit.IDEAL, 25.0
    # Partial matches
    for ideal in IDEAL_SECTORS:
        if ideal in s or s in ideal:
            return SectorFit.GOOD, 18.0
    return SectorFit.POSSIBLE, 10.0


def score_company_size(employee_count: int) -> tuple[CompanySize, float]:
    """Score company size against ICP range (20-200)."""
    if employee_count <= 0:
        return CompanySize.MICRO, 5.0
    if employee_count < 10:
        return CompanySize.MICRO, 8.0
    if employee_count < 20:
        return CompanySize.SMALL, 12.0
    if employee_count <= 200:
        # Sweet spot
        if 50 <= employee_count <= 150:
            return CompanySize.MEDIUM, 20.0
        return CompanySize.MEDIUM if employee_count > 50 else CompanySize.SMALL, 16.0
    if employee_count <= 1000:
        return CompanySize.LARGE, 10.0
    return CompanySize.ENTERPRISE, 5.0


def score_access(decision_makers: tuple[DecisionMaker, ...]) -> float:
    """Score quality of access to decision makers."""
    if not decision_makers:
        return 0.0
    score = 0.0
    for dm in decision_makers:
        if dm.role in (DecisionMakerRole.FOUNDER_CEO, DecisionMakerRole.GENERAL_MANAGER):
            score += 10.0
        elif dm.role in (DecisionMakerRole.VP_SALES, DecisionMakerRole.VP_OPERATIONS):
            score += 7.0
        else:
            score += 3.0
        if dm.email or dm.whatsapp:
            score += 2.0
        if dm.is_primary:
            score += 3.0
    return min(score, 20.0)


def score_pain_signals(signals: tuple[PainSignal, ...]) -> float:
    """Score relevance and intensity of pain signals."""
    if not signals:
        return 0.0
    high_value = {
        PainSignal.REVENUE_LEAKAGE,
        PainSignal.FOLLOW_UP_GAPS,
        PainSignal.NO_REPORTING,
        PainSignal.DATA_SCATTERED,
    }
    score = 0.0
    for sig in signals:
        if sig in high_value:
            score += 6.0
        else:
            score += 3.0
    return min(score, 20.0)


def score_data_quality(profile: CompanyProfile) -> tuple[DataQuality, float]:
    """Score data completeness and quality."""
    points = 0.0
    if profile.company_name:
        points += 2.0
    if profile.sector:
        points += 2.0
    if profile.employee_count > 0:
        points += 2.0
    if profile.website:
        points += 1.0
    if profile.city:
        points += 1.0
    if profile.source_url:
        points += 2.0
    if profile.decision_makers:
        points += 3.0
    if profile.pain_signals:
        points += 2.0

    if points >= 12:
        return DataQuality.EXCELLENT, 15.0
    if points >= 9:
        return DataQuality.GOOD, 12.0
    if points >= 6:
        return DataQuality.PARTIAL, 8.0
    if points >= 3:
        return DataQuality.MINIMAL, 4.0
    return DataQuality.INSUFFICIENT, 1.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def score_prospect(
    *,
    tenant_id: str,
    profile: CompanyProfile,
    source_id: str,
) -> ICPScore:
    """Score a prospect against ICP criteria."""
    sector_fit, sector_score = score_sector_fit(profile.sector)
    size_class, size_score = score_company_size(profile.employee_count)
    access_sc = score_access(profile.decision_makers)
    pain_sc = score_pain_signals(profile.pain_signals)
    dq, data_sc = score_data_quality(profile)

    total = sector_score + size_score + access_sc + pain_sc + data_sc

    # Determine priority
    disqualification_reasons: list[str] = []
    if sector_fit == SectorFit.EXCLUDED:
        disqualification_reasons.append(f"sector '{profile.sector}' is excluded from ICP")
    if profile.country and profile.country.upper() not in ("SA", "SAU", ""):
        disqualification_reasons.append(f"country '{profile.country}' is outside Saudi focus")

    if disqualification_reasons:
        priority = ProspectPriority.DISQUALIFIED
        qualified = False
    elif total >= 70:
        priority = ProspectPriority.HOT
        qualified = True
    elif total >= 50:
        priority = ProspectPriority.WARM
        qualified = True
    elif total >= 30:
        priority = ProspectPriority.COOL
        qualified = False
    else:
        priority = ProspectPriority.COLD
        qualified = False

    return ICPScore(
        tenant_id=tenant_id,
        score_id=_stable_id(
            "icpscore",
            {"tenant": tenant_id, "profile": profile.profile_id, "source": source_id},
        ),
        profile_id=profile.profile_id,
        sector_score=sector_score,
        size_score=size_score,
        access_score=access_sc,
        pain_score=pain_sc,
        data_score=data_sc,
        total_score=total,
        priority=priority,
        qualified=qualified,
        disqualification_reasons=tuple(disqualification_reasons),
        source_id=source_id,
        auto_contact_allowed=False,
    )


def rank_prospects(
    scores: list[ICPScore],
) -> list[ICPScore]:
    """Rank prospects by ICP score, highest first. Disqualified last."""
    priority_order = {
        ProspectPriority.HOT: 0,
        ProspectPriority.WARM: 1,
        ProspectPriority.COOL: 2,
        ProspectPriority.COLD: 3,
        ProspectPriority.DISQUALIFIED: 4,
    }
    return sorted(
        scores,
        key=lambda s: (priority_order.get(s.priority, 5), -s.total_score),
    )


def generate_research_brief(
    *,
    tenant_id: str,
    profile: CompanyProfile,
    icp_score: ICPScore,
    source_id: str,
) -> ResearchBrief:
    """Generate a complete research brief for founder review."""
    # Determine recommended approach
    if icp_score.priority == ProspectPriority.DISQUALIFIED:
        approach = "لا يُنصح بالتواصل — غير مؤهل"
        channel = "none"
    elif icp_score.priority == ProspectPriority.HOT:
        approach = "تواصل فوري — فرصة قوية تستحق الأولوية"
        channel = _best_channel(profile)
    elif icp_score.priority == ProspectPriority.WARM:
        approach = "تواصل خلال أسبوع — فرصة جيدة تحتاج متابعة"
        channel = _best_channel(profile)
    else:
        approach = "أضف للقائمة — راقب وانتظر إشارات أقوى"
        channel = "email"

    # Generate talking points
    points = _generate_talking_points(profile, icp_score)
    risks = _identify_risks(profile, icp_score)
    next_steps = _suggest_next_steps(profile, icp_score)

    # Bilingual summaries
    summary_ar = _summary_ar(profile, icp_score)
    summary_en = _summary_en(profile, icp_score)

    return ResearchBrief(
        tenant_id=tenant_id,
        profile=profile,
        icp_score=icp_score,
        recommended_approach=approach,
        recommended_channel=channel,
        talking_points=tuple(points),
        risks=tuple(risks),
        next_steps=tuple(next_steps),
        summary_ar=summary_ar,
        summary_en=summary_en,
        approval_required=True,
        auto_contact_allowed=False,
        source_id=source_id,
    )


def batch_research(
    *,
    tenant_id: str,
    profiles: list[CompanyProfile],
    source_id: str,
) -> list[ResearchBrief]:
    """Research and score a batch of prospects, return sorted briefs."""
    briefs = []
    for profile in profiles:
        score = score_prospect(
            tenant_id=tenant_id,
            profile=profile,
            source_id=source_id,
        )
        brief = generate_research_brief(
            tenant_id=tenant_id,
            profile=profile,
            icp_score=score,
            source_id=source_id,
        )
        briefs.append(brief)

    # Sort by ICP score descending
    briefs.sort(key=lambda b: -b.icp_score.total_score)
    return briefs


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _best_channel(profile: CompanyProfile) -> str:
    """Determine the best outreach channel for a prospect."""
    for dm in profile.decision_makers:
        if dm.whatsapp:
            return "whatsapp"
        if dm.email:
            return "email"
    if profile.website:
        return "email"
    return "email"


def _generate_talking_points(
    profile: CompanyProfile,
    score: ICPScore,
) -> list[str]:
    """Generate relevant talking points for the prospect."""
    points: list[str] = []

    if PainSignal.REVENUE_LEAKAGE in profile.pain_signals:
        points.append(
            "تسرب الإيرادات — نقدر نحدد وين بالضبط تضيع الفرص ونبني نظام متابعة محكم"
        )
    if PainSignal.FOLLOW_UP_GAPS in profile.pain_signals:
        points.append(
            "فجوات المتابعة — نبني تسلسل متابعة آلي مع موافقة المؤسس على كل رسالة"
        )
    if PainSignal.NO_CRM in profile.pain_signals:
        points.append(
            "بدون CRM — ديلكس يعمل فوق أي نظام موجود بدون ما تغير شيء"
        )
    if PainSignal.MANUAL_PROCESSES in profile.pain_signals:
        points.append(
            "عمليات يدوية — نأتمت التحضير والتحليل والتقارير ونخلي القرارات للمؤسس"
        )
    if PainSignal.DATA_SCATTERED in profile.pain_signals:
        points.append(
            "بيانات مبعثرة — نجمع كل شيء في دماغ مؤسسي واحد يعطيك صورة كاملة"
        )
    if PainSignal.NO_REPORTING in profile.pain_signals:
        points.append(
            "بدون تقارير — نبني تقرير قيادة يومي ثنائي اللغة مع حزم إثبات أسبوعية"
        )

    if not points:
        points.append("نبدأ بتشخيص مجاني نحدد فيه أكبر فرصة تحسين في عملياتكم")

    return points


def _identify_risks(
    profile: CompanyProfile,
    score: ICPScore,
) -> list[str]:
    """Identify risks in pursuing this prospect."""
    risks: list[str] = []

    if score.data_score < 5:
        risks.append("بيانات غير كافية — نحتاج بحث إضافي قبل التواصل")
    if score.access_score < 5:
        risks.append("صعوبة الوصول لصانع القرار — نحتاج واسطة أو تعريف")
    if not profile.decision_makers:
        risks.append("لم نحدد صانع القرار بعد")
    if profile.employee_count > 200:
        risks.append("حجم الشركة أكبر من ICP المثالي — قد تحتاج تخصيص إضافي")
    if profile.employee_count < 20 and profile.employee_count > 0:
        risks.append("حجم الشركة أصغر من ICP المثالي — تأكد من القدرة على الدفع")

    return risks


def _suggest_next_steps(
    profile: CompanyProfile,
    score: ICPScore,
) -> list[str]:
    """Suggest concrete next steps."""
    steps: list[str] = []

    if score.priority == ProspectPriority.DISQUALIFIED:
        steps.append("أرشف هذا العميل المحتمل — لا يطابق المعايير الحالية")
        return steps

    if score.data_score < 8:
        steps.append("أكمل بيانات الشركة: الموقع، الحجم، صانع القرار")
    if not profile.decision_makers:
        steps.append("حدد صانع القرار الرئيسي وطريقة التواصل")
    if score.priority in (ProspectPriority.HOT, ProspectPriority.WARM):
        steps.append("راجع المسودة واعتمد التواصل الأولي")
        steps.append("حضّر عرض التشخيص المجاني")
    else:
        steps.append("أضف للمراقبة — تابع عبر LinkedIn أو الأخبار")

    return steps


def _summary_ar(profile: CompanyProfile, score: ICPScore) -> str:
    """Generate Arabic summary."""
    name = profile.company_name_ar or profile.company_name
    parts = [f"ملخص بحث: {name}"]
    parts.append(f"القطاع: {profile.sector} | الحجم: {profile.employee_count} موظف")
    parts.append(f"درجة التأهيل: {score.total_score:.0f}/100 ({score.priority.value})")
    if score.qualified:
        parts.append("✅ مؤهل للتواصل — يحتاج موافقة المؤسس")
    else:
        parts.append("⏸️ غير مؤهل حالياً — يحتاج مزيد من البحث أو المراقبة")
    return " | ".join(parts)


def _summary_en(profile: CompanyProfile, score: ICPScore) -> str:
    """Generate English summary."""
    parts = [f"Research brief: {profile.company_name}"]
    parts.append(f"Sector: {profile.sector} | Size: {profile.employee_count} employees")
    parts.append(f"ICP score: {score.total_score:.0f}/100 ({score.priority.value})")
    if score.qualified:
        parts.append("✅ Qualified — requires founder approval to contact")
    else:
        parts.append("⏸️ Not qualified — needs more research or monitoring")
    return " | ".join(parts)
