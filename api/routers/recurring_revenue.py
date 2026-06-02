"""Recurring Revenue Radar HTTP surface — portfolio expansion scanner.

Draft-first and approval-guarded: the radar only *recommends* which accounts to
convert into recurring Managed-Ops retainers. It never sends or charges. All
figures honour no-revenue-before-paid and proof-before-upsell.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.revenue_ops_autopilot.recurring_revenue_radar import (
    RETAINER_TIER_MRR_SAR,
    AccountSnapshot,
    RecurringRevenueRadar,
    RecurringRevenueRadarLedger,
    render_radar_markdown,
)

router = APIRouter(
    prefix="/api/v1/recurring-revenue",
    dependencies=[Depends(require_admin_key)],
    tags=["recurring-revenue-radar"],
)


class RadarRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    accounts: list[AccountSnapshot] = Field(default_factory=list)
    top_n: int = Field(default=10, ge=1, le=100)
    record: bool = Field(
        default=False, description="Append this run to the radar ledger (default off)."
    )


@router.post("/radar")
async def post_radar(body: RadarRequest) -> dict[str, Any]:
    """Evaluate a portfolio and return the ranked expansion radar."""
    summary = RecurringRevenueRadar().evaluate(body.accounts)
    if body.record:
        RecurringRevenueRadarLedger().append_run(summary)
    return summary.model_dump(mode="json")


@router.post("/radar/markdown")
async def post_radar_markdown(body: RadarRequest) -> dict[str, Any]:
    """Evaluate a portfolio and return the founder-pack markdown."""
    summary = RecurringRevenueRadar().evaluate(body.accounts)
    return {
        "generated_at": summary.generated_at,
        "opportunities_count": summary.opportunities_count,
        "pipeline_incremental_mrr_sar": summary.pipeline_incremental_mrr_sar,
        "markdown": render_radar_markdown(summary, top_n=body.top_n),
    }


@router.get("/doctrine")
async def get_doctrine() -> dict[str, Any]:
    """Public contract for the radar: thresholds, tier prices, guardrails."""
    return {
        "tier_mrr_sar": dict(RETAINER_TIER_MRR_SAR),
        "eligibility": {
            "min_proof_level": "L1",
            "min_satisfaction_score": 7.0,
            "measurable_result_required": True,
        },
        "guardrails": {
            "no_revenue_before_paid": True,
            "proof_before_upsell": True,
            "approval_first": True,
            "no_auto_send": True,
        },
        "policy_ar": (
            "أرقام التوسّع فرصة (PIPELINE) وليست إيراداً محقّقاً. الإيراد المحقّق بعد السداد "
            "فقط. كل إجراء مسودة بانتظار موافقة المؤسس."
        ),
        "policy_en": (
            "Expansion figures are PIPELINE opportunity, not realised revenue. Realised "
            "revenue counts only after payment. Every action is a draft awaiting approval."
        ),
    }


@router.get("/history")
async def get_history(limit: Annotated[int, Query(ge=1, le=365)] = 30) -> dict[str, Any]:
    """Recent radar runs from the append-only ledger."""
    ledger = RecurringRevenueRadarLedger()
    return {"runs": ledger.history(limit=limit), "latest": ledger.latest()}
