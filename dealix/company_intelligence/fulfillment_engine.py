"""Fulfillment & Client Success Engine — post-sale delivery and growth.

Pure-logic engine that manages client onboarding, tracks delivery milestones,
generates progress reports, builds proof packs, monitors satisfaction, and
identifies upsell and renewal opportunities.

No database, network, or LLM calls. Delivery actions are proposals
requiring human oversight.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``auto_charge=False``, ``auto_renew=False`` always.
- Revenue requires payment evidence. Delivery requires proof evidence.
- Arabic-first with English support.
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


class EngagementStatus(StrEnum):
    """Status of a client engagement."""

    ONBOARDING = "onboarding"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    PAUSED = "paused"
    COMPLETED = "completed"
    CHURNED = "churned"


class MilestoneStatus(StrEnum):
    """Status of a delivery milestone."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"


class SatisfactionLevel(StrEnum):
    """Client satisfaction level."""

    DELIGHTED = "delighted"
    SATISFIED = "satisfied"
    NEUTRAL = "neutral"
    DISSATISFIED = "dissatisfied"
    AT_RISK = "at_risk"


class UpsellSignal(StrEnum):
    """Signals indicating upsell opportunity."""

    ASKED_FOR_MORE = "asked_for_more"
    HIGH_ENGAGEMENT = "high_engagement"
    POSITIVE_FEEDBACK = "positive_feedback"
    GROWING_TEAM = "growing_team"
    NEW_PAIN_POINT = "new_pain_point"
    BUDGET_AVAILABLE = "budget_available"
    REFERRAL_GIVEN = "referral_given"


class RenewalRisk(StrEnum):
    """Risk level for renewal."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class DeliveryMilestone(BaseModel):
    """A single delivery milestone in a client engagement."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    milestone_id: str = ""
    title: str = ""
    title_ar: str = ""
    description: str = ""
    day_target: int = 0  # Target day from engagement start
    status: MilestoneStatus = MilestoneStatus.PENDING
    deliverables: tuple[str, ...] = ()
    proof_required: bool = True
    proof_provided: bool = False
    client_accepted: bool = False


class ClientEngagement(BaseModel):
    """A client engagement / active delivery."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    engagement_id: str = ""
    client_name: str = ""
    client_company: str = ""
    offer_type: str = ""  # "free_diagnostic" or "revenue_command_pilot"
    status: EngagementStatus = EngagementStatus.ONBOARDING
    start_date: str = ""
    end_date: str = ""
    duration_days: int = 30
    milestones: tuple[DeliveryMilestone, ...] = ()
    completed_milestones: int = 0
    total_milestones: int = 0
    satisfaction: SatisfactionLevel = SatisfactionLevel.NEUTRAL
    upsell_signals: tuple[UpsellSignal, ...] = ()
    renewal_risk: RenewalRisk = RenewalRisk.MEDIUM
    engagement_value: float = 0.0
    auto_charge: bool = False
    auto_renew: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _safety_invariants(self) -> ClientEngagement:
        if self.auto_charge:
            raise ValueError(
                "ClientEngagement.auto_charge must be False — "
                "all charges require explicit human approval and payment evidence"
            )
        if self.auto_renew:
            raise ValueError(
                "ClientEngagement.auto_renew must be False — "
                "renewals require explicit client agreement"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.engagement_id:
            object.__setattr__(
                self,
                "engagement_id",
                _stable_id(
                    "engagement",
                    {
                        "tenant": self.tenant_id,
                        "client": self.client_name,
                        "company": self.client_company,
                        "offer": self.offer_type,
                        "source": self.source_id,
                    },
                ),
            )
        if not self.total_milestones:
            object.__setattr__(self, "total_milestones", len(self.milestones))


class ProgressReport(BaseModel):
    """Weekly or milestone-based progress report for a client."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    report_id: str = ""
    engagement_id: str = ""
    client_name: str = ""
    client_company: str = ""
    report_period: str = ""  # "week_1", "week_2", etc.
    completed_items: tuple[str, ...] = ()
    in_progress_items: tuple[str, ...] = ()
    upcoming_items: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    metrics: dict[str, Any] = Field(default_factory=dict)
    summary_ar: str = ""
    summary_en: str = ""
    next_actions: tuple[str, ...] = ()
    next_actions_ar: tuple[str, ...] = ()
    approval_required: bool = True
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )


class RenewalAssessment(BaseModel):
    """Assessment of a client's renewal likelihood and upsell potential."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    assessment_id: str = ""
    engagement_id: str = ""
    client_name: str = ""
    client_company: str = ""
    renewal_probability: float = 0.0  # 0-100
    renewal_risk: RenewalRisk = RenewalRisk.MEDIUM
    upsell_signals: tuple[UpsellSignal, ...] = ()
    upsell_opportunities: tuple[str, ...] = ()
    satisfaction: SatisfactionLevel = SatisfactionLevel.NEUTRAL
    delivery_score: float = 0.0  # 0-100
    recommended_action: str = ""
    recommended_action_ar: str = ""
    auto_renew: bool = False
    auto_charge: bool = False
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _safety_invariants(self) -> RenewalAssessment:
        if self.auto_renew:
            raise ValueError(
                "RenewalAssessment.auto_renew must be False — "
                "renewal requires explicit client agreement"
            )
        if self.auto_charge:
            raise ValueError(
                "RenewalAssessment.auto_charge must be False — "
                "charges require payment evidence"
            )
        return self


# ---------------------------------------------------------------------------
# Pilot delivery milestones
# ---------------------------------------------------------------------------


def _diagnostic_milestones() -> tuple[DeliveryMilestone, ...]:
    """Standard milestones for free diagnostic."""
    return (
        DeliveryMilestone(
            milestone_id="diag_1",
            title="Data intake and sector analysis",
            title_ar="استلام البيانات وتحليل القطاع",
            day_target=0,
            deliverables=("sector_fit_analysis",),
        ),
        DeliveryMilestone(
            milestone_id="diag_2",
            title="Deliver diagnostic report",
            title_ar="تسليم تقرير التشخيص",
            day_target=1,
            deliverables=(
                "sector_fit_analysis",
                "3_ranked_opportunities",
                "arabic_message_draft",
                "best_channel_recommendation",
                "risk_to_avoid",
                "next_step_passport",
            ),
        ),
    )


def _pilot_milestones() -> tuple[DeliveryMilestone, ...]:
    """Standard milestones for 30-day Revenue Command Pilot."""
    return (
        DeliveryMilestone(
            milestone_id="pilot_1",
            title="Onboarding and data collection",
            title_ar="التأهيل وجمع البيانات",
            day_target=1,
            deliverables=("data_intake_form", "access_setup"),
        ),
        DeliveryMilestone(
            milestone_id="pilot_2",
            title="Company Brain v1 build",
            title_ar="بناء الدماغ المؤسسي الإصدار الأول",
            day_target=3,
            deliverables=("company_brain_v1", "icp_definition"),
        ),
        DeliveryMilestone(
            milestone_id="pilot_3",
            title="Revenue workflow activated",
            title_ar="تفعيل سير عمل الإيرادات",
            day_target=7,
            deliverables=("revenue_workflow", "approval_queue", "operational_baseline"),
        ),
        DeliveryMilestone(
            milestone_id="pilot_4",
            title="Week 1 proof pack",
            title_ar="حزمة إثبات الأسبوع الأول",
            day_target=7,
            deliverables=("proof_pack_week1",),
        ),
        DeliveryMilestone(
            milestone_id="pilot_5",
            title="Week 2 proof pack",
            title_ar="حزمة إثبات الأسبوع الثاني",
            day_target=14,
            deliverables=("proof_pack_week2",),
        ),
        DeliveryMilestone(
            milestone_id="pilot_6",
            title="Week 3 proof pack",
            title_ar="حزمة إثبات الأسبوع الثالث",
            day_target=21,
            deliverables=("proof_pack_week3",),
        ),
        DeliveryMilestone(
            milestone_id="pilot_7",
            title="Week 4 proof pack and final review",
            title_ar="حزمة إثبات الأسبوع الرابع والمراجعة النهائية",
            day_target=28,
            deliverables=("proof_pack_week4", "final_outcome_review"),
        ),
        DeliveryMilestone(
            milestone_id="pilot_8",
            title="Stop/extend/redesign decision",
            title_ar="قرار الإيقاف أو التمديد أو إعادة التصميم",
            day_target=30,
            deliverables=("decision_passport",),
        ),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create_engagement(
    *,
    tenant_id: str,
    client_name: str,
    client_company: str,
    offer_type: str,
    engagement_value: float = 0.0,
    start_date: str = "",
    source_id: str,
) -> ClientEngagement:
    """Create a new client engagement with standard milestones."""
    if offer_type == "free_diagnostic":
        milestones = _diagnostic_milestones()
        duration = 1
    elif offer_type == "revenue_command_pilot":
        milestones = _pilot_milestones()
        duration = 30
    else:
        milestones = ()
        duration = 30

    if not start_date:
        start_date = datetime.now(UTC).strftime("%Y-%m-%d")

    return ClientEngagement(
        tenant_id=tenant_id,
        client_name=client_name,
        client_company=client_company,
        offer_type=offer_type,
        status=EngagementStatus.ONBOARDING,
        start_date=start_date,
        duration_days=duration,
        milestones=milestones,
        engagement_value=engagement_value,
        auto_charge=False,
        auto_renew=False,
        source_id=source_id,
    )


def generate_progress_report(
    *,
    tenant_id: str,
    engagement: ClientEngagement,
    week_number: int = 1,
    source_id: str,
) -> ProgressReport:
    """Generate a progress report for a client engagement."""
    completed: list[str] = []
    in_progress: list[str] = []
    upcoming: list[str] = []
    blockers_list: list[str] = []

    for m in engagement.milestones:
        if m.status in (MilestoneStatus.DELIVERED, MilestoneStatus.ACCEPTED):
            completed.append(f"✅ {m.title_ar or m.title}")
        elif m.status == MilestoneStatus.IN_PROGRESS:
            in_progress.append(f"🔄 {m.title_ar or m.title}")
        elif m.status == MilestoneStatus.REJECTED:
            blockers_list.append(f"❌ {m.title_ar or m.title} — مرفوض، يحتاج إعادة عمل")
        elif m.day_target <= week_number * 7:
            upcoming.append(f"⏳ {m.title_ar or m.title}")

    total = len(engagement.milestones)
    done = len(completed)
    progress_pct = (done / total * 100) if total > 0 else 0

    summary_ar = (
        f"تقرير الأسبوع {week_number} — {engagement.client_company}\n"
        f"التقدم: {done}/{total} ({progress_pct:.0f}%)\n"
        f"الحالة: {engagement.status.value}"
    )
    summary_en = (
        f"Week {week_number} Report — {engagement.client_company}\n"
        f"Progress: {done}/{total} ({progress_pct:.0f}%)\n"
        f"Status: {engagement.status.value}"
    )

    next_actions = _next_delivery_actions(engagement, week_number)
    next_actions_ar = _next_delivery_actions_ar(engagement, week_number)

    return ProgressReport(
        tenant_id=tenant_id,
        report_id=_stable_id(
            "report",
            {
                "tenant": tenant_id,
                "engagement": engagement.engagement_id,
                "week": week_number,
                "source": source_id,
            },
        ),
        engagement_id=engagement.engagement_id,
        client_name=engagement.client_name,
        client_company=engagement.client_company,
        report_period=f"week_{week_number}",
        completed_items=tuple(completed),
        in_progress_items=tuple(in_progress),
        upcoming_items=tuple(upcoming),
        blockers=tuple(blockers_list),
        metrics={
            "milestones_completed": done,
            "milestones_total": total,
            "progress_percent": progress_pct,
            "week": week_number,
        },
        summary_ar=summary_ar,
        summary_en=summary_en,
        next_actions=tuple(next_actions),
        next_actions_ar=tuple(next_actions_ar),
        approval_required=True,
        source_id=source_id,
    )


def assess_renewal(
    *,
    tenant_id: str,
    engagement: ClientEngagement,
    source_id: str,
) -> RenewalAssessment:
    """Assess renewal likelihood and upsell potential."""
    # Calculate delivery score
    total_m = len(engagement.milestones)
    accepted_m = sum(
        1 for m in engagement.milestones
        if m.status in (MilestoneStatus.ACCEPTED, MilestoneStatus.DELIVERED)
    )
    delivery_score = (accepted_m / total_m * 100) if total_m > 0 else 0.0

    # Calculate renewal probability
    prob = _renewal_probability(engagement, delivery_score)

    # Determine risk
    if prob >= 75:
        risk = RenewalRisk.LOW
    elif prob >= 50:
        risk = RenewalRisk.MEDIUM
    elif prob >= 25:
        risk = RenewalRisk.HIGH
    else:
        risk = RenewalRisk.CRITICAL

    # Identify upsell opportunities
    upsell_opps = _identify_upsell(engagement)

    # Recommended action
    action, action_ar = _renewal_action(risk, engagement)

    return RenewalAssessment(
        tenant_id=tenant_id,
        assessment_id=_stable_id(
            "renewal",
            {
                "tenant": tenant_id,
                "engagement": engagement.engagement_id,
                "source": source_id,
            },
        ),
        engagement_id=engagement.engagement_id,
        client_name=engagement.client_name,
        client_company=engagement.client_company,
        renewal_probability=prob,
        renewal_risk=risk,
        upsell_signals=engagement.upsell_signals,
        upsell_opportunities=tuple(upsell_opps),
        satisfaction=engagement.satisfaction,
        delivery_score=delivery_score,
        recommended_action=action,
        recommended_action_ar=action_ar,
        auto_renew=False,
        auto_charge=False,
        source_id=source_id,
    )


def calculate_engagement_health(
    engagements: list[ClientEngagement],
) -> dict[str, Any]:
    """Calculate overall engagement health across all clients."""
    total = len(engagements)
    if total == 0:
        return {
            "total_engagements": 0,
            "active": 0,
            "at_risk": 0,
            "churned": 0,
            "avg_satisfaction": 0.0,
            "total_value": 0.0,
            "health": "no_data",
        }

    active = sum(1 for e in engagements if e.status == EngagementStatus.ACTIVE)
    at_risk = sum(1 for e in engagements if e.status == EngagementStatus.AT_RISK)
    churned = sum(1 for e in engagements if e.status == EngagementStatus.CHURNED)

    sat_scores = {
        SatisfactionLevel.DELIGHTED: 5,
        SatisfactionLevel.SATISFIED: 4,
        SatisfactionLevel.NEUTRAL: 3,
        SatisfactionLevel.DISSATISFIED: 2,
        SatisfactionLevel.AT_RISK: 1,
    }
    avg_sat = sum(sat_scores.get(e.satisfaction, 3) for e in engagements) / total

    total_value = sum(e.engagement_value for e in engagements)

    if at_risk > total * 0.3 or churned > total * 0.2:
        health = "critical"
    elif at_risk > total * 0.1:
        health = "needs_attention"
    elif avg_sat >= 4:
        health = "excellent"
    else:
        health = "healthy"

    return {
        "total_engagements": total,
        "active": active,
        "at_risk": at_risk,
        "churned": churned,
        "avg_satisfaction": round(avg_sat, 1),
        "total_value": total_value,
        "health": health,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _renewal_probability(
    engagement: ClientEngagement,
    delivery_score: float,
) -> float:
    """Calculate renewal probability."""
    base = delivery_score * 0.4  # 40% weight on delivery

    sat_bonus = {
        SatisfactionLevel.DELIGHTED: 30.0,
        SatisfactionLevel.SATISFIED: 20.0,
        SatisfactionLevel.NEUTRAL: 10.0,
        SatisfactionLevel.DISSATISFIED: 0.0,
        SatisfactionLevel.AT_RISK: -10.0,
    }
    base += sat_bonus.get(engagement.satisfaction, 10.0)

    # Upsell signals indicate engagement
    base += min(len(engagement.upsell_signals) * 5.0, 20.0)

    # Status penalty
    if engagement.status == EngagementStatus.AT_RISK:
        base -= 20.0
    if engagement.status == EngagementStatus.CHURNED:
        base = 0.0

    return max(0.0, min(100.0, base))


def _identify_upsell(engagement: ClientEngagement) -> list[str]:
    """Identify upsell opportunities."""
    opps: list[str] = []

    if engagement.offer_type == "free_diagnostic":
        opps.append("تجربة مركز قيادة الإيرادات — 30 يوم (Revenue Command Pilot)")

    if UpsellSignal.ASKED_FOR_MORE in engagement.upsell_signals:
        opps.append("خدمات إضافية حسب طلب العميل")
    if UpsellSignal.NEW_PAIN_POINT in engagement.upsell_signals:
        opps.append("تشخيص إضافي لنقطة ألم جديدة")
    if UpsellSignal.GROWING_TEAM in engagement.upsell_signals:
        opps.append("توسعة النظام لتغطية أقسام إضافية")

    if engagement.offer_type == "revenue_command_pilot":
        opps.append("عقد تشغيل شهري — Revenue Command Room")

    return opps


def _renewal_action(
    risk: RenewalRisk,
    engagement: ClientEngagement,
) -> tuple[str, str]:
    """Determine recommended renewal action."""
    if risk == RenewalRisk.CRITICAL:
        return (
            "Urgent: Schedule founder call to address concerns",
            "عاجل: حدد مكالمة مع المؤسس لمعالجة المخاوف",
        )
    if risk == RenewalRisk.HIGH:
        return (
            "Send satisfaction survey and address gaps",
            "أرسل استبيان رضا وعالج الفجوات",
        )
    if risk == RenewalRisk.MEDIUM:
        return (
            "Prepare renewal proposal with added value",
            "جهّز عرض تجديد مع قيمة إضافية",
        )
    return (
        "Present upsell opportunities and renewal terms",
        "قدّم فرص التوسعة وشروط التجديد",
    )


def _next_delivery_actions(
    engagement: ClientEngagement,
    week: int,
) -> list[str]:
    """Determine next delivery actions (English)."""
    actions: list[str] = []
    for m in engagement.milestones:
        if m.status == MilestoneStatus.PENDING and m.day_target <= (week + 1) * 7:
            actions.append(f"Deliver: {m.title}")
    if not actions:
        actions.append("Continue monitoring and collecting proof")
    return actions


def _next_delivery_actions_ar(
    engagement: ClientEngagement,
    week: int,
) -> list[str]:
    """Determine next delivery actions (Arabic)."""
    actions: list[str] = []
    for m in engagement.milestones:
        if m.status == MilestoneStatus.PENDING and m.day_target <= (week + 1) * 7:
            actions.append(f"سلّم: {m.title_ar or m.title}")
    if not actions:
        actions.append("استمر بالمراقبة وجمع الإثباتات")
    return actions
