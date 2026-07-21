"""Founder Command Room — one aggregated, read-only snapshot for the founder.

Composes the live war-room operating summary (the same source the existing
``/api/v1/ops-autopilot/war-room/summary`` endpoint uses) with launch readiness
and the offer ladder, so the front-end can render the whole command room from a
single, stable call.

Doctrine-safe: read-only. It never sends anything and issues no invoices. The
non-negotiables surface back to the UI via ``summary["risks"]``.

Note: this lives as a standalone module (not under an ``api/routers/founder/``
package) so it does not shadow the existing ``api/routers/founder.py`` module,
which the admin domain imports as ``founder.router``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from api.security.api_key import require_admin_key
from dealix.revenue_ops_autopilot.store import get_autopilot_store
from dealix.revenue_ops_autopilot.war_room import build_daily_summary
from fastapi import APIRouter, Depends
from intelligence import Deal, RevenueIntelligenceEngine
from intelligence.saudi_market_intelligence import SaudiMarketIntelligence
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/founder",
    dependencies=[Depends(require_admin_key)],
    tags=["founder-command-room"],
)

# Paid customers needed to trip the commercial gate (Article 13).
ARTICLE_13_TARGET = 3

# The 4 pending founder launch actions (docs/WAVE17_FOUNDER_DAY1_LAUNCH_KIT.md).
FOUNDER_ACTIONS: list[dict[str, str]] = [
    {"ar": "توقيع اتفاقية معالجة البيانات (DPA)", "en": "Sign the Data Processing Agreement (DPA)"},
    {"ar": "إرسال 5 رسائل واتساب دافئة + تسجيلها", "en": "Send 5 warm-intro WhatsApp messages + log them"},
    {"ar": "ضبط سجلات DNS (SPF/DKIM/DMARC) على dealix.me", "en": "Set DNS records (SPF/DKIM/DMARC) at dealix.me"},
    {"ar": "دمج PR الانحدار المعلّق", "en": "Merge the pending regression PR"},
]

# The 6-rung offer ladder (docs/DEALIX_BUSINESS_MODEL.md).
OFFER_LADDER: list[dict[str, str]] = [
    {"name": "التشخيص المجاني / Free Diagnostic", "detail": "مغناطيس عملاء · 30 دقيقة"},
    {"name": "Micro Sprint", "detail": "499 SAR · إثبات سريع"},
    {"name": "Data Pack", "detail": "1,500 SAR · أصل بيانات لمرة واحدة"},
    {"name": "Managed Ops", "detail": "2,999–4,999 SAR/شهر"},
    {"name": "Transformation Diagnostic Sprint", "detail": "7,500–25,000 SAR · المدخل المدفوع الأساسي"},
    {"name": "Custom Enterprise System", "detail": "25,000–100,000+ SAR"},
]


class LaunchReadiness(BaseModel):
    status: str = Field(description="Overall launch gate status, e.g. PARTIAL / READY")
    paid: int = Field(description="Paid customers so far (from the live war-room summary)")
    article13_target: int = ARTICLE_13_TARGET
    founder_actions: list[dict[str, str]] = FOUNDER_ACTIONS


class FounderCommandRoomOut(BaseModel):
    generated_at: str
    mode: str = "draft_only"
    launch: LaunchReadiness
    offer_ladder: list[dict[str, str]] = OFFER_LADDER
    summary: dict[str, Any] = Field(
        description="Live war-room operating summary (today/revenue/queues/risks/top_targets)",
    )


@router.get("/command-room", response_model=FounderCommandRoomOut)
async def founder_command_room() -> dict[str, Any]:
    """Return the unified founder command room snapshot."""
    store = get_autopilot_store()
    summary = build_daily_summary(store.list_leads(limit=600))
    paid = int(summary.get("revenue", {}).get("paid", 0) or 0)

    # Build intelligence snapshot from current pipeline data
    leads = store.list_leads(limit=600)
    engine = RevenueIntelligenceEngine()
    deals = []
    now = datetime.now(UTC)
    for lead in leads:
        stage = lead.get("stage", "lead")
        value = float(lead.get("estimated_value_sar", 2500) or 2500)
        last_activity = lead.get("last_activity_at")
        if last_activity is None:
            last_activity = now
        elif isinstance(last_activity, str):
            last_activity = datetime.fromisoformat(last_activity.replace("Z", "+00:00"))
        deals.append(Deal(
            deal_id=lead.get("id", "unknown"),
            company_name=lead.get("company_name", "Unknown"),
            stage=stage,
            value_sar=value,
            created_at=now,
            last_activity_at=last_activity,
            activities_count=lead.get("activities_count", 0),
            days_in_stage=lead.get("days_in_stage", 0),
        ))
    engine.load_deals(deals)
    intel = engine.analyze()

    market_intel = SaudiMarketIntelligence()
    top_sectors = [
        {"sector": s, "momentum": market_intel.sector_momentum(s).value}
        for s in ["fintech", "logistics", "software", "healthcare_tech", "proptech"]
    ]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "draft_only",
        "launch": {
            "status": "PARTIAL",
            "paid": paid,
            "article13_target": ARTICLE_13_TARGET,
            "founder_actions": FOUNDER_ACTIONS,
        },
        "offer_ladder": OFFER_LADDER,
        "intelligence": {
            "pipeline_health": intel.pipeline_health,
            "total_pipeline_sar": intel.total_pipeline_sar,
            "weighted_pipeline_sar": intel.weighted_pipeline_sar,
            "revenue_at_risk_sar": intel.revenue_at_risk_sar,
            "recommended_actions": intel.recommended_actions,
            "top_sector_signals": top_sectors,
        },
        "summary": summary,
    }

