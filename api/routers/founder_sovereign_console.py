"""
Founder Sovereign Console Router.
Serves the 6 pillars of the Dealix Alpha Command Center:
1. Sovereign Console
2. Growth & Revenue
3. Trust Control
4. Money & Deals
5. Assets & Products
6. Partners & Customers
"""
from __future__ import annotations

import logging
from typing import Any
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/sovereign-console", tags=["sovereign-console"])
log = logging.getLogger(__name__)

@router.get("/status")
async def console_status() -> dict[str, Any]:
    return {"status": "live", "version": "alpha"}

# 1. Sovereign Console
@router.get("/sovereign-summary")
async def get_sovereign_summary() -> dict[str, Any]:
    """Returns the top level metrics for the founder."""
    return {
        "fastest_cash_action": "Follow up with 3 agencies who completed diagnostic",
        "highest_strategic_opportunity": "Finalize AI Trust Kit playbook",
        "pending_approvals": 4,
        "risks": 1,
        "founder_time_leverage_score": 85
    }

# 2. Growth & Revenue
@router.get("/growth-metrics")
async def get_growth_metrics() -> dict[str, Any]:
    """Returns metrics for marketing, campaigns, and top of funnel."""
    return {
        "active_campaigns": 2,
        "verified_revenue_30d_sar": 150000,
        "pipeline_value_sar": 450000,
        "ai_visibility_score": "B+"
    }

# 3. Trust Control
@router.get("/trust-control")
async def get_trust_control() -> dict[str, Any]:
    """Returns governance and MCP Gateway stats."""
    return {
        "active_agents": 11,
        "mcp_gateway_blocks_24h": 3,
        "incidents": 0,
        "evidence_packs_generated": 14
    }

# 4. Money & Deals
@router.get("/money-deals")
async def get_money_deals() -> dict[str, Any]:
    """Returns financial and deal room data."""
    return {
        "active_deal_rooms": 5,
        "invoices_pending": 2,
        "cashflow_30d_sar": 120000,
        "revenue_quality_score": 92
    }

# 5. Assets & Products
@router.get("/assets-products")
async def get_assets_products() -> dict[str, Any]:
    """Returns metrics on the compounding asset library."""
    return {
        "total_assets": 24,
        "playbooks_created": 6,
        "assets_converted_to_products": 2
    }

# 6. Partners & Customers
@router.get("/partners-customers")
async def get_partners_customers() -> dict[str, Any]:
    """Returns partner ecosystem and customer health metrics."""
    return {
        "active_partners": 3,
        "partner_revenue_share_sar": 15000,
        "customer_health_average": "Healthy",
        "renewals_upcoming": 1
    }
