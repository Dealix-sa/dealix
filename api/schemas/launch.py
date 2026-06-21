"""Pydantic v2 request/response schemas for the Launch OS router.

Arabic Field descriptions are provided where the concept maps directly to a
Saudi-market-specific notion; English is used for purely technical fields.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# ICP Scoring
# ---------------------------------------------------------------------------


class AccountIn(BaseModel):
    """Single account to score against the ICP rubric."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1, max_length=200, description="اسم الشركة")
    sector: str = Field(..., min_length=1, max_length=64, description="القطاع")
    city: str = Field(default="Riyadh", max_length=64, description="المدينة")
    employee_count: int | None = Field(default=None, ge=1, description="عدد الموظفين")
    annual_revenue_sar: float | None = Field(
        default=None, ge=0, description="الإيراد السنوي بالريال السعودي"
    )
    b2b_service_fit: int = Field(
        default=50, ge=0, le=100, description="مدى ملاءمة خدمات B2B (0–100)"
    )
    data_maturity: int = Field(
        default=50, ge=0, le=100, description="نضج البيانات (0–100)"
    )
    governance_posture: int = Field(
        default=50, ge=0, le=100, description="موقف الحوكمة (0–100)"
    )
    budget_signal: int = Field(
        default=50, ge=0, le=100, description="إشارة الميزانية (0–100)"
    )
    decision_velocity: int = Field(
        default=50, ge=0, le=100, description="سرعة صنع القرار (0–100)"
    )
    raw_request_text: str = Field(
        default="", max_length=2000, description="نص الطلب الخام لفحص المذهب"
    )
    customer_id: str = Field(default="", max_length=64, description="معرّف المستأجر")


class AccountScore(BaseModel):
    """ICP score result for a single account."""

    company_name: str
    icp_score: int = Field(..., ge=0, le=100)
    tier: str = Field(..., description="platinum | gold | silver | bronze")
    qualification_decision: str
    recommended_offer: str
    reasons: list[str]
    doctrine_violations: list[str]
    breakdown: dict[str, int]
    governance_decision: str


class BatchScoreRequest(BaseModel):
    """Batch ICP score request — up to 50 accounts."""

    model_config = ConfigDict(extra="forbid")

    accounts: list[AccountIn] = Field(..., min_length=1, max_length=50)
    customer_id: str = Field(default="", max_length=64)


class BatchScoreResponse(BaseModel):
    """Batch ICP score response."""

    total: int
    scored: list[AccountScore]
    governance_decision: str


# ---------------------------------------------------------------------------
# Vertical Selection
# ---------------------------------------------------------------------------


class VerticalOut(BaseModel):
    """A single Saudi vertical with its full score card."""

    rank: int
    sector: str
    label_ar: str
    label_en: str
    icp_fit: int = Field(..., ge=0, le=100, description="ملاءمة ICP (0–100)")
    data_maturity: int = Field(..., ge=0, le=100, description="نضج البيانات")
    governance_posture: int = Field(..., ge=0, le=100, description="موقف الحوكمة")
    budget_signal: int = Field(..., ge=0, le=100, description="إشارة الميزانية")
    decision_velocity: int = Field(..., ge=0, le=100, description="سرعة القرار")
    composite_score: int = Field(..., ge=0, le=100, description="النقاط المركبة")
    why_now_ar: str
    why_now_en: str
    recommended_wedge_offer: str


class VerticalListOut(BaseModel):
    """Ranked list of all 15 Saudi verticals."""

    count: int
    verticals: list[VerticalOut]
    governance_decision: str


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


class PipelineAccountIn(BaseModel):
    """Add an account to the launch pipeline."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1, max_length=200, description="اسم الشركة")
    sector: str = Field(..., min_length=1, max_length=64, description="القطاع")
    city: str = Field(default="Riyadh", max_length=64, description="المدينة")
    stage: str = Field(
        default="prospect",
        description="prospect | diagnostic | proposal | negotiation | closed_won | closed_lost",
    )
    contact_name: str = Field(default="", max_length=200, description="اسم جهة الاتصال")
    contact_email: str = Field(default="", max_length=200)
    icp_score: int = Field(default=0, ge=0, le=100)
    notes: str = Field(default="", max_length=2000)
    customer_id: str = Field(default="", max_length=64, description="معرّف المستأجر")


class PipelineAccountOut(BaseModel):
    """A single account in the launch pipeline."""

    id: str
    company_name: str
    sector: str
    city: str
    stage: str
    contact_name: str
    contact_email: str
    icp_score: int
    notes: str
    created_at: str
    updated_at: str
    governance_decision: str


class StageUpdateIn(BaseModel):
    """Move a pipeline account to a new stage."""

    model_config = ConfigDict(extra="forbid")

    stage: str = Field(
        ...,
        description="prospect | diagnostic | proposal | negotiation | closed_won | closed_lost",
    )
    reason: str = Field(default="", max_length=500)
    customer_id: str = Field(default="", max_length=64)


class PipelineSummaryOut(BaseModel):
    """Full pipeline summary with stage counts and aggregate value."""

    total_accounts: int
    by_stage: dict[str, int]
    governance_decision: str
    accounts: list[PipelineAccountOut]


# ---------------------------------------------------------------------------
# Outreach
# ---------------------------------------------------------------------------


class OutreachDraftRequest(BaseModel):
    """Generate an outreach draft for a given account, offer, and channel."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1, max_length=200, description="اسم الشركة")
    sector: str = Field(default="", max_length=64, description="القطاع")
    city: str = Field(default="Riyadh", max_length=64, description="المدينة")
    offer_slug: str = Field(
        default="capability_diagnostic",
        description="capability_diagnostic | revenue_intelligence_sprint | mini_diagnostic",
    )
    channel: str = Field(
        default="email_warm",
        description="email_warm | linkedin_manual | phone_task | in_person",
    )
    contact_name: str = Field(default="", max_length=200)
    language: str = Field(default="ar", pattern="^(ar|en)$")
    customer_id: str = Field(default="", max_length=64, description="معرّف المستأجر")


class OutreachDraftOut(BaseModel):
    """Outreach draft output — always draft-only, never auto-sent."""

    draft_ar: str
    draft_en: str
    channel: str
    offer_slug: str
    approval_required: bool
    governance_decision: str
    action_mode: str = "draft_only"


class PreflightRequest(BaseModel):
    """Run trust preflight checks on an outreach draft."""

    model_config = ConfigDict(extra="forbid")

    draft_text: str = Field(..., min_length=1, max_length=5000)
    channel: str = Field(default="email_warm", max_length=64)
    customer_id: str = Field(default="", max_length=64)


class PreflightResult(BaseModel):
    """Preflight check result for an outreach draft."""

    passed: bool
    governance_decision: str
    violations: list[str]
    warnings: list[str]
    action_mode: str


# ---------------------------------------------------------------------------
# Proposals
# ---------------------------------------------------------------------------


class ProposalRequest(BaseModel):
    """Build a proposal pack for a client."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1, max_length=200, description="اسم الشركة")
    sector: str = Field(default="", max_length=64, description="القطاع")
    sprint_name: str = Field(
        default="capability_diagnostic",
        description="اسم البرنامج المقترح",
    )
    pain_points: list[str] = Field(default_factory=list, max_length=10)
    budget_sar: float | None = Field(default=None, ge=0, description="الميزانية بالريال")
    customer_id: str = Field(default="", max_length=64, description="معرّف المستأجر")


class ProposalOut(BaseModel):
    """Proposal pack output."""

    id: str
    company_name: str
    sprint_name: str
    sections: dict[str, str]
    created_at: str
    governance_decision: str
    action_mode: str = "draft_only"


# ---------------------------------------------------------------------------
# Daily Command
# ---------------------------------------------------------------------------


class DailyCommandOut(BaseModel):
    """Today's founder daily command brief."""

    date: str
    top_priority_ar: str
    top_priority_en: str
    pipeline_actions: list[dict[str, Any]]
    outreach_queue: list[dict[str, Any]]
    proof_alerts: list[str]
    governance_decision: str
    generated_at: str
