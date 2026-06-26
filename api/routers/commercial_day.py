"""Commercial day operations router — /api/v1/commercial/*"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/commercial", tags=["Commercial Operations"])

_EXTERNAL_SEND_ENABLED: bool = os.getenv("EXTERNAL_SEND_ENABLED", "false").lower() in (
    "true",
    "1",
    "yes",
)


# ---------------------------------------------------------------------------
# Pydantic response models
# ---------------------------------------------------------------------------


class RevenueKPI(BaseModel):
    mtd_actual_sar: float = Field(0.0, description="Month-to-date actual revenue in SAR")
    mtd_target_sar: float = Field(50000.0, description="Month-to-date target revenue in SAR")
    attainment_pct: float = Field(0.0, description="Percentage of target achieved")
    label_ar: str = Field("الإيرادات الشهرية", description="Arabic label")


class PipelineStages(BaseModel):
    prospect: int = 0
    qualified: int = 0
    proposal_sent: int = 0
    negotiation: int = 0
    won: int = 0
    label_ar: str = "مراحل خط الأنابيب"


class CommercialStatusResponse(BaseModel):
    governance_decision: str
    status: str
    date: str
    external_send_enabled: bool
    outbound_mode: str
    systems_online: list[str]
    label_ar: str = "حالة اليوم التجاري"


class PipelineResponse(BaseModel):
    governance_decision: str
    pipeline: PipelineStages
    total_active: int
    label_ar: str = "خط الأنابيب"


class KPIResponse(BaseModel):
    governance_decision: str
    revenue: RevenueKPI
    pipeline: PipelineStages
    label_ar: str = "مؤشرات الأداء الرئيسية"


class RunDayRequest(BaseModel):
    customer_id: str = Field(..., description="Tenant / founder identifier")
    operator: str = Field("founder", description="Operator name for audit log")


class RunDayResponse(BaseModel):
    governance_decision: str
    task_queued: bool
    message: str
    external_send_enabled: bool
    label_ar: str = "تشغيل اليوم التجاري"


class CEOBriefResponse(BaseModel):
    governance_decision: str
    date: str
    generated_at: str
    revenue: dict[str, Any]
    pipeline: dict[str, Any]
    top_priorities: list[str]
    top_priorities_ar: list[str]
    risk_flags: list[str]
    founder_decisions_needed: list[str]
    what_not_to_do_today: list[str]
    label_ar: str = "موجز المدير التنفيذي"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_runtime_json(filename: str, default: Any) -> Any:
    p = Path("company/runtime") / filename
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _build_pipeline() -> PipelineStages:
    data = _load_runtime_json("pipeline.json", {})
    if isinstance(data, dict):
        return PipelineStages(**{k: int(v) for k, v in data.items() if k in PipelineStages.model_fields})
    return PipelineStages()


def _build_revenue() -> RevenueKPI:
    data = _load_runtime_json("revenue_mtd.json", {})
    actual = float(data.get("mtd_actual_sar", 0)) if isinstance(data, dict) else 0.0
    target = float(data.get("mtd_target_sar", 50000)) if isinstance(data, dict) else 50000.0
    pct = round((actual / target) * 100, 1) if target else 0.0
    return RevenueKPI(mtd_actual_sar=actual, mtd_target_sar=target, attainment_pct=pct)


def _run_day_background(operator: str) -> None:
    """Background task: import and run the commercial day runner."""
    import sys
    from pathlib import Path as _Path

    scripts_dir = _Path(__file__).parents[2] / "scripts" / "commercial"
    sys.path.insert(0, str(scripts_dir))
    try:
        from run_commercial_day import run_commercial_day  # type: ignore[import]
        run_commercial_day()
    except Exception:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).exception("background commercial day run failed")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/status", response_model=CommercialStatusResponse)
async def get_commercial_status() -> CommercialStatusResponse:
    """Return commercial day system status and safety gate state."""
    return CommercialStatusResponse(
        governance_decision="APPROVED",
        status="operational",
        date=datetime.now(UTC).strftime("%Y-%m-%d"),
        external_send_enabled=_EXTERNAL_SEND_ENABLED,
        outbound_mode=os.getenv("OUTBOUND_MODE", "draft_only"),
        systems_online=[
            "account_scoring",
            "ceo_brief",
            "crm",
            "pipeline",
            "kpi_tracker",
        ],
    )


@router.get("/pipeline", response_model=PipelineResponse)
async def get_pipeline() -> PipelineResponse:
    """Return pipeline stage counts."""
    pipeline = _build_pipeline()
    total_active = (
        pipeline.prospect
        + pipeline.qualified
        + pipeline.proposal_sent
        + pipeline.negotiation
    )
    return PipelineResponse(
        governance_decision="APPROVED",
        pipeline=pipeline,
        total_active=total_active,
    )


@router.get("/kpis", response_model=KPIResponse)
async def get_kpis() -> KPIResponse:
    """Return key commercial KPIs."""
    return KPIResponse(
        governance_decision="APPROVED",
        revenue=_build_revenue(),
        pipeline=_build_pipeline(),
    )


@router.post("/run-day", response_model=RunDayResponse)
async def run_commercial_day_endpoint(
    body: RunDayRequest, background_tasks: BackgroundTasks
) -> RunDayResponse:
    """
    Trigger the commercial day runner as a background task.
    Blocked if EXTERNAL_SEND_ENABLED is True.
    """
    if _EXTERNAL_SEND_ENABLED:
        raise HTTPException(
            status_code=403,
            detail="EXTERNAL_SEND_ENABLED is True. Set it to false before triggering commercial day.",
        )
    background_tasks.add_task(_run_day_background, body.operator)
    return RunDayResponse(
        governance_decision="APPROVED",
        task_queued=True,
        message="Commercial day runner queued as background task. Check reports/commercial/ for output.",
        external_send_enabled=False,
    )


@router.get("/ceo-brief", response_model=CEOBriefResponse)
async def get_ceo_brief() -> CEOBriefResponse:
    """Return latest CEO brief. Generates on the fly if no cached brief exists."""
    brief_path = Path("reports/ceo_brief/latest.json")
    if brief_path.exists():
        try:
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            brief = None
    else:
        brief = None

    if brief is None:
        import sys
        scripts_dir = Path(__file__).parents[2] / "scripts" / "commercial"
        sys.path.insert(0, str(scripts_dir))
        from generate_ceo_brief import build_brief  # type: ignore[import]
        brief = build_brief()

    return CEOBriefResponse(
        governance_decision="APPROVED",
        date=brief.get("date", ""),
        generated_at=brief.get("generated_at", ""),
        revenue=brief.get("revenue", {}),
        pipeline=brief.get("pipeline", {}),
        top_priorities=brief.get("top_priorities", []),
        top_priorities_ar=brief.get("top_priorities_ar", []),
        risk_flags=brief.get("risk_flags", []),
        founder_decisions_needed=brief.get("founder_decisions_needed", []),
        what_not_to_do_today=brief.get("what_not_to_do_today", []),
    )
