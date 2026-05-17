"""Daily operating engine — the single orchestrator for the daily loop.

Runs, in order: outreach drafting (revenue machine) → social content
drafting → partner-intro surfacing → approval expire-sweep → founder
action list. Everything lands in the approval queue; nothing is sent and
nothing is charged. Idempotent per day via a marker file under
``data/daily_engine/``. Designed to be triggered by an external cron.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.content_os.action_list import build_action_list
from auto_client_acquisition.content_os.drafting import draft_daily_social_posts
from auto_client_acquisition.content_os.queue_bridge import enqueue_social_drafts
from core.logging import get_logger

logger = get_logger(__name__)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_MARKER_DIR = _REPO_ROOT / "data" / "daily_engine"


def _marker_path(day: _dt.date) -> Path:
    return _MARKER_DIR / f"{day.isoformat()}.json"


async def _run_revenue_machine() -> tuple[dict[str, Any], int]:
    """Run the outreach revenue machine. Returns (stage_summary, partner_pool)."""
    try:
        from api.routers.drafts import revenue_machine_run

        rm = await revenue_machine_run({})
        produced = rm.get("produced", {}) if isinstance(rm, dict) else {}
        return (
            {"status": rm.get("status", "unknown"), "produced": produced},
            int(produced.get("partner_drafts_pool", 0)),
        )
    except Exception as exc:
        logger.warning("daily_engine_revenue_machine_failed", error=str(exc))
        return {"status": "error", "error": str(exc)}, 0


async def run_daily_engine(
    *, date: _dt.date | None = None, force: bool = False
) -> dict[str, Any]:
    """Run the full daily loop once. Idempotent per day unless ``force``."""
    day = date or _dt.datetime.now(_dt.UTC).date()
    label = day.isoformat()
    marker = _marker_path(day)

    if marker.exists() and not force:
        try:
            prior = json.loads(marker.read_text(encoding="utf-8"))
        except Exception:
            prior = {}
        return {"status": "already_ran", "date": label, "prior": prior}

    stages: dict[str, Any] = {}

    # Stage 1 — outreach drafts (Gmail / LinkedIn / call scripts / partner pool).
    stages["revenue_machine"], partner_pool = await _run_revenue_machine()

    # Stage 2 — social content drafts into the approval queue.
    try:
        drafts = draft_daily_social_posts(date=day)
        enqueued = enqueue_social_drafts(drafts)
        stages["social_content"] = {
            "status": "ok",
            "drafted": len(drafts),
            "enqueued": len(enqueued),
        }
    except Exception as exc:
        logger.warning("daily_engine_social_content_failed", error=str(exc))
        stages["social_content"] = {"status": "error", "error": str(exc)}

    # Stage 3 — partner intros (surfaced from the revenue machine, not rebuilt).
    stages["partner_intros"] = {"status": "ok", "pool": partner_pool}

    # Stage 4 — expire overdue approvals.
    expired = get_default_approval_store().expire_overdue()
    stages["approval_expire_sweep"] = {"status": "ok", "expired": expired}

    # Stage 5 — founder action list.
    action_list = build_action_list(day)
    stages["action_list"] = {"status": "ok", "chars": len(action_list)}

    result = {
        "status": "ok",
        "date": label,
        "force": force,
        "stages": stages,
        "action_list": action_list,
    }

    _MARKER_DIR.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    logger.info("daily_engine_completed", date=label, force=force)
    return result


__all__ = ["run_daily_engine"]
