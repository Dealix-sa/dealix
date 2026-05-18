"""Founder executive day — governed commercial + GTM + Railway ops snapshot."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.gtm_public_surfaces import verify_gtm_public_surfaces_repo
from dealix.commercial_ops.railway_launch import (
    check_paid_launch_integrations,
    check_railway_api_env,
    check_railway_frontend_env,
)
from dealix.commercial_ops.railway_production import analyze_railway_production


def build_founder_executive_snapshot(
    *,
    api_base: str | None = "https://api.dealix.me",
    skip_live: bool = False,
) -> dict[str, Any]:
    """Single JSON-friendly snapshot for CEO/founder morning review."""
    railway = analyze_railway_production(api_base=False if skip_live else api_base)
    gtm = verify_gtm_public_surfaces_repo()
    first_paid = analyze_first_paid_diagnostic()
    api_env = check_railway_api_env()
    fe_env = check_railway_frontend_env()
    integrations = check_paid_launch_integrations()

    blockers: list[str] = []
    if not railway["repo"]["ok"]:
        blockers.extend(railway["repo"]["issues"])
    if railway.get("live_failures"):
        blockers.append(f"live_api: {','.join(railway['live_failures'])}")
    if not gtm["ok"]:
        blockers.extend(gtm["issues"])
    if not first_paid.get("first_close_ready"):
        blockers.append(f"first_paid_diagnostic:{first_paid['verdict']}")
    if api_env["missing_required"]:
        blockers.append(f"api_env:{','.join(api_env['missing_required'])}")
    if integrations["missing"]:
        blockers.append(f"paid_integrations:{','.join(integrations['missing'])}")

    return {
        "railway": railway,
        "gtm_surfaces": gtm,
        "first_paid": first_paid,
        "api_env": api_env,
        "frontend_env": fe_env,
        "paid_integrations": integrations,
        "blockers": blockers,
        "verdict": "BLOCKED" if blockers else "CLEAR",
        "anchors": {
            "commercial_plan": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
            "war_room": "docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md",
            "evidence_csv": first_paid["evidence_path"],
            "railway_settings": railway["settings_doc"],
            "gtm_atlas": "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
        },
    }
