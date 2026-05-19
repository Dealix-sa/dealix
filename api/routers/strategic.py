"""Strategic-layer HTTP surface — read strategic briefs on demand.

Thin router over the strategic-automation layer
(``auto_client_acquisition.automation.strategic_runner``). It lets the
founder / portal read the briefs the weekly ARQ crons persist, instead
of waiting for the founder email.

Endpoints:
- GET  /api/v1/strategic/briefs          — list recent strategic briefs
- GET  /api/v1/strategic/briefs/latest   — the most recent brief
- POST /api/v1/strategic/synthesis/run   — run the strategy synthesis

This surface is INTERNAL READ / ANALYSIS ONLY: no external sends, no
prospect contact. ``run_strategy_synthesis_core`` recommends; the
founder decides (autonomy level L3).
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from api.security.api_key import require_admin_key
from auto_client_acquisition.automation.strategic_runner import (
    run_strategy_synthesis_core,
)
from db.models import StrategicBriefRecord
from db.session import async_session_factory

# Strategic briefs carry internal CEO/finance/strategy data — founder-only.
# The whole router requires the admin key, not just any customer API key.
router = APIRouter(
    prefix="/api/v1/strategic",
    tags=["Strategic Layer"],
    dependencies=[Depends(require_admin_key)],
)
log = logging.getLogger(__name__)


_HARD_GATES = {
    "internal_read_only": True,
    "no_external_send": True,
    "no_prospect_contact": True,
    "autonomy_level_recommend_only": True,
    "graceful_degradation_on_failure": True,
}


def _row_to_dict(row: StrategicBriefRecord) -> dict[str, Any]:
    """Serialize one ``StrategicBriefRecord`` for the HTTP envelope."""
    return {
        "id": row.id,
        "artifact_type": row.artifact_type,
        "period_label": row.period_label,
        "title": row.title,
        "payload": row.payload,
        "autonomy_level": row.autonomy_level,
        "external_send": row.external_send,
        "emailed_to_founder": row.emailed_to_founder,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


@router.get("/briefs")
async def list_briefs(
    brief_type: str | None = Query(
        default=None, description="Filter by artifact_type."
    ),
    limit: int = Query(default=20, ge=1, le=200),
) -> dict[str, Any]:
    """List recent strategic briefs, most recent first.

    Standard envelope: ``{data, meta, errors}``. Returns 503 when the
    brief store is unreachable (the caller can retry).
    """
    try:
        async with async_session_factory()() as session:
            stmt = select(StrategicBriefRecord).order_by(
                StrategicBriefRecord.created_at.desc()
            )
            if brief_type:
                stmt = stmt.where(
                    StrategicBriefRecord.artifact_type == brief_type
                )
            rows = (
                await session.execute(stmt.limit(limit))
            ).scalars().all()
    except Exception as exc:  # noqa: BLE001
        log.warning("list_briefs_store_unavailable: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="strategic brief store temporarily unavailable",
        ) from exc

    data = [_row_to_dict(r) for r in rows]
    return {
        "data": data,
        "meta": {
            "count": len(data),
            "limit": limit,
            "brief_type": brief_type,
            "hard_gates": _HARD_GATES,
        },
        "errors": [],
    }


@router.get("/briefs/latest")
async def latest_brief(
    brief_type: str | None = Query(
        default=None, description="Filter by artifact_type."
    ),
) -> dict[str, Any]:
    """Return the most recent strategic brief, optionally filtered.

    Standard envelope: ``{data, meta, errors}``. ``data`` is ``None``
    when no brief matches. Returns 503 when the store is unreachable.
    """
    try:
        async with async_session_factory()() as session:
            stmt = select(StrategicBriefRecord).order_by(
                StrategicBriefRecord.created_at.desc()
            )
            if brief_type:
                stmt = stmt.where(
                    StrategicBriefRecord.artifact_type == brief_type
                )
            row = (
                await session.execute(stmt.limit(1))
            ).scalars().first()
    except Exception as exc:  # noqa: BLE001
        log.warning("latest_brief_store_unavailable: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="strategic brief store temporarily unavailable",
        ) from exc

    data = _row_to_dict(row) if row is not None else None
    return {
        "data": data,
        "meta": {
            "found": data is not None,
            "brief_type": brief_type,
            "hard_gates": _HARD_GATES,
        },
        "errors": [],
    }


@router.post("/synthesis/run")
async def run_synthesis(
    customer_handle: str = Query(default="dealix"),
) -> dict[str, Any]:
    """Run the strategy synthesis on demand and return the result.

    Internal analysis only — ``run_strategy_synthesis_core`` aggregates
    the weekly artifacts into a founder strategy brief. No external send;
    the engine recommends, the founder decides.
    """
    try:
        result = await run_strategy_synthesis_core(
            customer_handle=customer_handle
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("strategy_synthesis_run_failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="strategy synthesis temporarily unavailable",
        ) from exc

    return {
        "data": result,
        "meta": {
            "customer_handle": customer_handle,
            "hard_gates": _HARD_GATES,
        },
        "errors": [],
    }
