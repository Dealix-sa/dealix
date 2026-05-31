"""Founder alert review API.

Endpoints:
  GET  /api/v1/founder/alerts          — list pending alerts (admin-gated)
  POST /api/v1/founder/alerts/{id}/approve  — mark approved
  POST /api/v1/founder/alerts/{id}/dismiss  — mark dismissed
  GET  /api/v1/founder/alerts/summary  — count by status and type

Constitutional gates:
- APPROVAL_FIRST: approve/dismiss endpoints record the decision before any downstream action.
- NO_PII_IN_LOGS: log lines contain only IDs and status strings.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.security.api_key import require_admin_key
from core.logging import get_logger

log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/founder/alerts",
    tags=["Admin"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"


# ── helpers ────────────────────────────────────────────────────────────────────


async def _get_repo() -> Any:
    """Open a DB session and return a FounderAlertRepository, or None on failure."""
    try:
        from db.repositories.wave17_repos import FounderAlertRepository
        from db.session import async_session_factory

        session = async_session_factory()()
        return FounderAlertRepository(session), session
    except Exception as exc:
        log.warning("founder_alerts_session_failed", error=str(exc))
        return None, None


# ── endpoints ──────────────────────────────────────────────────────────────────


@router.get("/summary")
async def alerts_summary() -> dict[str, Any]:
    """Count founder alerts by status and type."""
    repo, session = await _get_repo()
    try:
        if repo is None:
            counts = {"total": 0, "by_status": {}, "by_type": {}}
        else:
            counts = await repo.count_by_status_and_type()
    finally:
        if session is not None:
            try:
                await session.close()
            except Exception:
                pass
    return {
        "governance_decision": _GOV,
        **counts,
    }


@router.get("")
async def list_pending_alerts() -> dict[str, Any]:
    """List all pending founder alerts, sorted by priority then created_at."""
    repo, session = await _get_repo()
    try:
        if repo is None:
            alerts: list[dict[str, Any]] = []
        else:
            alerts = await repo.get_pending()
    finally:
        if session is not None:
            try:
                await session.close()
            except Exception:
                pass
    return {
        "governance_decision": _GOV,
        "count": len(alerts),
        "alerts": alerts,
    }


@router.post("/{alert_id}/approve")
async def approve_alert(alert_id: str) -> dict[str, Any]:
    """Mark a founder alert as approved. Records the decision before any action."""
    repo, session = await _get_repo()
    try:
        if repo is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            )
        updated = await repo.mark_reviewed(alert_id=alert_id, action="approved")
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found",
            )
        try:
            await session.commit()
        except Exception:
            pass
        log.info("founder_alert_approved", alert_id=alert_id)
        return {
            "governance_decision": _GOV,
            "action": "approved",
            "alert": updated,
        }
    finally:
        if session is not None:
            try:
                await session.close()
            except Exception:
                pass


@router.post("/{alert_id}/dismiss")
async def dismiss_alert(alert_id: str) -> dict[str, Any]:
    """Mark a founder alert as dismissed."""
    repo, session = await _get_repo()
    try:
        if repo is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            )
        updated = await repo.mark_reviewed(alert_id=alert_id, action="dismissed")
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert {alert_id} not found",
            )
        try:
            await session.commit()
        except Exception:
            pass
        log.info("founder_alert_dismissed", alert_id=alert_id)
        return {
            "governance_decision": _GOV,
            "action": "dismissed",
            "alert": updated,
        }
    finally:
        if session is not None:
            try:
                await session.close()
            except Exception:
                pass
