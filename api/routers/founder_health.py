"""Founder Health Score + Action Inbox — admin-gated HTTP surface.

GET /api/v1/founder/health-score
    Single 0-100 founder operating-health score with sub-scores + top actions.

GET /api/v1/founder/health-score.md
    Markdown render — copy-paste-friendly Arabic + English brief.

GET /api/v1/founder/action-inbox
    Prioritized list (P0/P1/P2/P3) of items needing founder attention,
    aggregated across approvals, leads, evidence, PDPL, paid traction,
    and strongest-plan wiring.

GET /api/v1/founder/action-inbox.md
    Markdown render of the action inbox.

Doctrine:
  - Article 4: read-only, never auto-sends.
  - Article 8: counts are operational estimates (is_estimate=True).
  - Article 11: compose-only — no new business logic.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder-health"])


@router.get("/health-score", dependencies=[Depends(require_admin_key)])
async def founder_health_score_endpoint(
    stale_hours: int = Query(24, ge=1, le=168),
) -> dict[str, Any]:
    """0-100 founder operating-health score with sub-scores and top actions."""
    from dealix.commercial_ops.founder_health_score import compute_founder_health_score

    return compute_founder_health_score(stale_hours=stale_hours)


@router.get("/health-score.md", dependencies=[Depends(require_admin_key)])
async def founder_health_score_markdown(
    stale_hours: int = Query(24, ge=1, le=168),
) -> dict[str, Any]:
    """Markdown brief — for copy-paste / weekly proof archive."""
    from dealix.commercial_ops.founder_health_score import (
        compute_founder_health_score,
        render_health_brief_markdown,
    )

    snap = compute_founder_health_score(stale_hours=stale_hours)
    return {
        "markdown": render_health_brief_markdown(snap),
        "overall_score": snap.get("overall_score"),
        "verdict": snap.get("verdict"),
        "generated_at": snap.get("generated_at"),
    }


@router.get("/action-inbox", dependencies=[Depends(require_admin_key)])
async def founder_action_inbox_endpoint(
    stale_hours: int = Query(24, ge=1, le=168),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    """Prioritized inbox of items needing founder attention across subsystems."""
    from dealix.commercial_ops.founder_action_inbox import build_action_inbox

    return build_action_inbox(stale_hours=stale_hours, limit=limit)


@router.get("/action-inbox.md", dependencies=[Depends(require_admin_key)])
async def founder_action_inbox_markdown(
    stale_hours: int = Query(24, ge=1, le=168),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    """Markdown render of the action inbox — for daily founder brief."""
    from dealix.commercial_ops.founder_action_inbox import (
        build_action_inbox,
        render_inbox_markdown,
    )

    snap = build_action_inbox(stale_hours=stale_hours, limit=limit)
    return {
        "markdown": render_inbox_markdown(snap),
        "verdict": snap.get("verdict"),
        "total_items": snap.get("total_items"),
        "by_priority": snap.get("by_priority"),
        "generated_at": snap.get("generated_at"),
    }
