"""Pipeline Analytics — pipeline health for Dealix's Saudi B2B sales pipeline.

Provides conversion benchmarks, stage playbooks, velocity adjustments, and
a health-check endpoint that classifies a pipeline snapshot as Healthy,
At Risk, or Critical.

Endpoints
---------
GET  /api/v1/pipeline-analytics/benchmarks           — Saudi B2B benchmarks
GET  /api/v1/pipeline-analytics/stage-playbooks      — all 5 stage playbooks
GET  /api/v1/pipeline-analytics/stage-playbooks/{stage} — single playbook
POST /api/v1/pipeline-analytics/health-check         — analyse pipeline snapshot
GET  /api/v1/pipeline-analytics/conversion-guide     — conversion benchmarks + tips

All data is static; no LLM or external API calls.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/pipeline-analytics", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Governance constant
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Saudi B2B SaaS benchmarks
# ---------------------------------------------------------------------------

_SAUDI_BENCHMARKS: dict[str, Any] = {
    "avg_deal_cycle_days": 45,
    "note_en": (
        "Benchmark accounts for Ramadan/Eid calendar effects on decision timelines."
    ),
    "note_ar": (
        "المعيار يأخذ في الاعتبار تأثير رمضان والعيد على جداول اتخاذ القرار."
    ),
    "typical_stages": ["Prospect", "Qualify", "Validate", "Commit", "Close"],
    "stage_conversion_rates_pct": {
        "Prospect_to_Qualify": 40,
        "Qualify_to_Validate": 55,
        "Validate_to_Commit": 60,
        "Commit_to_Close": 75,
    },
    "avg_deal_size_sar": {
        "sprint": 499,
        "data_pack": 1500,
        "managed_ops": 3500,
        "custom_ai": 12500,
    },
    "velocity_multipliers": {
        "ramadan_period": 0.6,
        "post_eid_period": 1.4,
        "note_en": (
            "Deals slow approximately 40% during Ramadan; "
            "accelerate approximately 40% in the two weeks post-Eid."
        ),
        "note_ar": (
            "تتباطأ الصفقات بنحو 40% خلال رمضان؛ "
            "وتتسارع بنحو 40% في الأسبوعين التاليين للعيد."
        ),
    },
}

# ---------------------------------------------------------------------------
# Stage playbooks
# ---------------------------------------------------------------------------

_STAGE_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "Prospect": {
        "stage_en": "Prospect",
        "stage_ar": "استكشاف",
        "exit_criteria_en": [
            "Confirmed company fits ICP (sector, size, geography).",
            "At least one named contact identified with a valid touchpoint.",
            "Prospect is aware of Dealix (warm or inbound; no cold outreach without governance approval).",
        ],
        "top_activities_en": [
            "Research sector pain points and map to Dealix service catalogue.",
            "Identify warm introduction paths or inbound lead source.",
            "Log prospect in CRM with full ICP qualification fields.",
        ],
        "avg_days_in_stage": 7,
        "risk_signals_en": [
            "Contact went silent after first message — possible bad-fit signal.",
            "Unable to identify any internal champion after two attempts.",
        ],
    },
    "Qualify": {
        "stage_en": "Qualify",
        "stage_ar": "تأهيل",
        "exit_criteria_en": [
            "Pain explicitly articulated by the prospect in their own words.",
            "Budget signal confirmed (asked about pricing, scope, or ROI).",
            "A champion with access to the economic buyer has been identified.",
        ],
        "top_activities_en": [
            "Run structured discovery call using BANT+ framework.",
            "Share a relevant one-page case study matching their vertical.",
            "Confirm or disconfirm ZATCA / Nitaqat compliance pressure.",
        ],
        "avg_days_in_stage": 10,
        "risk_signals_en": [
            "Champion is junior with no line to the economic buyer.",
            "Prospect avoids all budget or timeline questions.",
        ],
    },
    "Validate": {
        "stage_en": "Validate",
        "stage_ar": "تحقق",
        "exit_criteria_en": [
            "Economic buyer has attended at least one meeting or reviewed a proposal.",
            "Technical requirements and integration scope are documented.",
            "Prospect has confirmed they are evaluating Dealix as a shortlisted vendor.",
        ],
        "top_activities_en": [
            "Deliver a Mini Diagnostic or Proof Pack tailored to their pain.",
            "Run a live product walkthrough with the economic buyer present.",
            "Gather written or verbal confirmation of shortlisting.",
        ],
        "avg_days_in_stage": 14,
        "risk_signals_en": [
            "Economic buyer has not engaged after three outreach attempts.",
            "Scope keeps expanding without budget confirmation — scope creep risk.",
        ],
    },
    "Commit": {
        "stage_en": "Commit",
        "stage_ar": "التزام",
        "exit_criteria_en": [
            "Commercial proposal sent and acknowledged by the economic buyer.",
            "Legal/procurement review has started (NDA or MSA in motion).",
            "Verbal or written commitment to move forward received.",
        ],
        "top_activities_en": [
            "Send a clean one-page commercial proposal with no guaranteed-result claims.",
            "Proactively resolve procurement or legal blockers.",
            "Agree on a mutual action plan with shared milestones and owners.",
        ],
        "avg_days_in_stage": 10,
        "risk_signals_en": [
            "Proposal has been with procurement for more than 10 days with no update.",
            "New stakeholder introduced late — potential deal re-opener.",
        ],
    },
    "Close": {
        "stage_en": "Close",
        "stage_ar": "إغلاق",
        "exit_criteria_en": [
            "Contract signed or purchase order issued.",
            "Onboarding scheduled and kickoff date confirmed.",
            "First payment received or payment terms agreed in writing.",
        ],
        "top_activities_en": [
            "Confirm contract terms; ensure no guaranteed-result language appears.",
            "Schedule onboarding kickoff call within 5 business days of signing.",
            "Hand off to delivery team with a full context brief.",
        ],
        "avg_days_in_stage": 4,
        "risk_signals_en": [
            "Signing delayed past agreed date without explanation.",
            "Economic buyer is on leave during the closing window (Ramadan/Eid risk).",
        ],
    },
}

# ---------------------------------------------------------------------------
# Conversion guide reference data
# ---------------------------------------------------------------------------

_CONVERSION_GUIDE: dict[str, Any] = {
    "title_en": "Saudi B2B SaaS Pipeline Conversion Guide",
    "title_ar": "دليل معدلات تحويل خط أنابيب B2B SaaS السعودي",
    "benchmarks_table": [
        {
            "transition": "Prospect → Qualify",
            "benchmark_pct": 40,
            "below_threshold_pct": 30,
            "improvement_tip_en": (
                "Tighten ICP filters before adding prospects. "
                "Low conversion here usually means poor list quality."
            ),
            "improvement_tip_ar": (
                "شدّد فلاتر ICP قبل إضافة العملاء المحتملين. "
                "انخفاض التحويل هنا يعني عادةً ضعف جودة القائمة."
            ),
        },
        {
            "transition": "Qualify → Validate",
            "benchmark_pct": 55,
            "below_threshold_pct": 40,
            "improvement_tip_en": (
                "Improve discovery depth. Reps who skip ZATCA/Nitaqat pain "
                "questions lose prospects at this stage."
            ),
            "improvement_tip_ar": (
                "عمّق مرحلة الاستكشاف. المندوبون الذين يتجاوزون أسئلة ألم "
                "ZATCA/نطاقات يفقدون العملاء في هذه المرحلة."
            ),
        },
        {
            "transition": "Validate → Commit",
            "benchmark_pct": 60,
            "below_threshold_pct": 45,
            "improvement_tip_en": (
                "Ensure the economic buyer is in the room during Validate. "
                "Deals without EB presence rarely reach Commit."
            ),
            "improvement_tip_ar": (
                "تأكد من حضور متخذ القرار المالي أثناء التحقق. "
                "الصفقات التي تفتقر لحضوره نادراً ما تصل إلى الالتزام."
            ),
        },
        {
            "transition": "Commit → Close",
            "benchmark_pct": 75,
            "below_threshold_pct": 60,
            "improvement_tip_en": (
                "Procurement delays drive most losses here. "
                "Pre-position an NDA/MSA template early in Validate."
            ),
            "improvement_tip_ar": (
                "تأخيرات المشتريات هي السبب الأكبر للخسائر هنا. "
                "ضع نموذج اتفاقية السرية/الإطار مبكراً في مرحلة التحقق."
            ),
        },
    ],
    "calendar_tips_en": [
        "Allow 20–30% extra cycle time for deals touching Ramadan.",
        "Post-Eid (first two weeks) is the highest-velocity window of the year; use it for Commit→Close pushes.",
        "Q1 (Jan–Mar) sees the highest new-pipeline starts due to fiscal year budgets.",
        "ZATCA compliance deadlines in H2 often create urgency — track them for your prospects.",
    ],
    "calendar_tips_ar": [
        "خصّص وقتاً إضافياً بنسبة 20–30% لدورات الصفقات التي تمر برمضان.",
        "ما بعد العيد (أسبوعان) هو أعلى نافذة سرعة في السنة؛ استخدمها للدفع من الالتزام إلى الإغلاق.",
        "الربع الأول (يناير–مارس) يشهد أعلى بدايات خط أنابيب جديدة بسبب ميزانيات السنة المالية.",
        "مواعيد الامتثال لهيئة الزكاة والضريبة في النصف الثاني تخلق إلحاحاً في كثير من الأحيان — تتبّعها لعملائك المحتملين.",
    ],
    "governance_decision": _GOV_REVIEW,
}

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class PipelineHealthInput(BaseModel):
    """Snapshot of the sales pipeline for health analysis."""

    total_pipeline_sar: float = Field(ge=0, description="Total pipeline value in SAR.")
    deals_by_stage: dict[str, int] = Field(
        description="Stage name mapped to number of open deals in that stage."
    )
    avg_deal_age_days: float = Field(ge=0, description="Average age of open deals in days.")
    won_deals_last_90d: int = Field(ge=0, description="Deals closed-won in the last 90 days.")
    lost_deals_last_90d: int = Field(ge=0, description="Deals closed-lost in the last 90 days.")
    open_deals_total: int = Field(ge=0, description="Total number of currently open deals.")
    is_ramadan_period: bool = Field(
        default=False,
        description="Set to true when the snapshot is taken during Ramadan.",
    )


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _analyze_pipeline(inp: PipelineHealthInput) -> dict[str, Any]:
    """Analyse a pipeline snapshot and return health classification with actions.

    Parameters
    ----------
    inp:
        Validated ``PipelineHealthInput`` from the request body.

    Returns
    -------
    dict[str, Any]
        Win rate, health classification, coverage ratio, velocity adjustment,
        recommended actions, and governance decision.
    """
    closed_total = inp.won_deals_last_90d + inp.lost_deals_last_90d
    win_rate_pct = (
        round((inp.won_deals_last_90d / closed_total) * 100, 1)
        if closed_total > 0
        else 0.0
    )

    # Coverage ratio: pipeline value relative to a notional monthly quota.
    # Use avg managed_ops deal size as a proxy unit (3 500 SAR × 12 = 42 000/yr ~ 3 500/mo).
    # A ratio >= 3.0 is considered healthy (3× pipeline coverage).
    monthly_quota_proxy_sar = 3_500.0
    coverage_ratio = (
        round(inp.total_pipeline_sar / monthly_quota_proxy_sar, 2)
        if monthly_quota_proxy_sar > 0
        else 0.0
    )

    # Velocity adjustment for Ramadan
    velocity_adjustment = 0.6 if inp.is_ramadan_period else 1.0
    effective_cycle_days = round(
        _SAUDI_BENCHMARKS["avg_deal_cycle_days"] / velocity_adjustment, 1
    )

    # Health classification
    if win_rate_pct >= 50 and inp.avg_deal_age_days <= _SAUDI_BENCHMARKS["avg_deal_cycle_days"]:
        pipeline_health = "Healthy"
        pipeline_health_ar = "سليم"
    elif win_rate_pct >= 30 or inp.avg_deal_age_days <= _SAUDI_BENCHMARKS["avg_deal_cycle_days"] * 1.5:
        pipeline_health = "At Risk"
        pipeline_health_ar = "في خطر"
    else:
        pipeline_health = "Critical"
        pipeline_health_ar = "حرج"

    recommended_actions: list[str] = _build_pipeline_actions(
        pipeline_health=pipeline_health,
        win_rate_pct=win_rate_pct,
        avg_deal_age_days=inp.avg_deal_age_days,
        coverage_ratio=coverage_ratio,
        is_ramadan_period=inp.is_ramadan_period,
    )

    return {
        "win_rate_pct": win_rate_pct,
        "pipeline_health": pipeline_health,
        "pipeline_health_ar": pipeline_health_ar,
        "coverage_ratio": coverage_ratio,
        "velocity_adjustment": velocity_adjustment,
        "effective_cycle_days_estimate": effective_cycle_days,
        "total_pipeline_sar": inp.total_pipeline_sar,
        "open_deals_total": inp.open_deals_total,
        "avg_deal_age_days": inp.avg_deal_age_days,
        "won_deals_last_90d": inp.won_deals_last_90d,
        "lost_deals_last_90d": inp.lost_deals_last_90d,
        "is_ramadan_period": inp.is_ramadan_period,
        "deals_by_stage": inp.deals_by_stage,
        "recommended_actions": recommended_actions,
        "governance_decision": _GOV_REVIEW,
    }


def _build_pipeline_actions(
    *,
    pipeline_health: str,
    win_rate_pct: float,
    avg_deal_age_days: float,
    coverage_ratio: float,
    is_ramadan_period: bool,
) -> list[str]:
    """Build a list of 3–4 context-aware recommended actions."""
    actions: list[str] = []

    if pipeline_health == "Healthy":
        actions.append(
            "Pipeline is healthy. Maintain current cadence and log all activity in CRM."
        )
        actions.append(
            "Focus on moving Commit-stage deals to Close before end of current quarter."
        )
    elif pipeline_health == "At Risk":
        actions.append(
            "Win rate or deal age is below benchmark. Conduct a deal-by-deal review this week."
        )
        actions.append(
            "Identify all deals older than 45 days and confirm economic buyer is still engaged."
        )
    else:  # Critical
        actions.append(
            "Pipeline is in a critical state. Escalate to founder for a portfolio review."
        )
        actions.append(
            "Disqualify deals with no champion contact in the last 30 days to clean the forecast."
        )

    if coverage_ratio < 3.0:
        actions.append(
            f"Coverage ratio is {coverage_ratio}×, below the 3× minimum. "
            "Accelerate top-of-funnel activity to add new Prospect-stage deals."
        )

    if is_ramadan_period:
        actions.append(
            "Ramadan velocity multiplier is active (0.6×). "
            "Avoid pushing for commitments; use this period for relationship building and discovery."
        )
    elif win_rate_pct < 30 and pipeline_health != "Healthy":
        actions.append(
            "Win rate below 30%. Review lost-deal reasons and tighten ICP filters on incoming prospects."
        )

    return actions[:4]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/benchmarks", summary="Saudi B2B SaaS pipeline benchmarks")
async def get_benchmarks() -> dict[str, Any]:
    """Return deal cycle, stage conversion rates, deal sizes, and velocity multipliers."""
    return {
        **_SAUDI_BENCHMARKS,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/stage-playbooks", summary="All five stage playbooks")
async def get_all_stage_playbooks() -> dict[str, Any]:
    """Return playbooks for all five pipeline stages."""
    return {
        "stage_playbooks": _STAGE_PLAYBOOKS,
        "stages_in_order": _SAUDI_BENCHMARKS["typical_stages"],
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/stage-playbooks/{stage}", summary="Single stage playbook")
async def get_stage_playbook(stage: str) -> dict[str, Any]:
    """Return the playbook for a single pipeline stage.

    Parameters
    ----------
    stage:
        Stage name — one of Prospect, Qualify, Validate, Commit, Close.
        Case-sensitive.
    """
    playbook = _STAGE_PLAYBOOKS.get(stage)
    if playbook is None:
        valid = list(_STAGE_PLAYBOOKS.keys())
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Stage '{stage}' not found.",
                "valid_stages": valid,
            },
        )
    return {
        "stage": stage,
        "playbook": playbook,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/health-check", summary="Analyse a pipeline snapshot")
async def pipeline_health_check(body: PipelineHealthInput) -> dict[str, Any]:
    """Accept a ``PipelineHealthInput`` snapshot and return a health analysis."""
    return _analyze_pipeline(body)


@router.get("/conversion-guide", summary="Conversion rate benchmarks and improvement tips")
async def get_conversion_guide() -> dict[str, Any]:
    """Return stage-to-stage conversion benchmarks and improvement tips for Saudi B2B."""
    return _CONVERSION_GUIDE
