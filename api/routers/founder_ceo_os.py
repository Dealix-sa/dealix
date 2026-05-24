# This router NEVER triggers external sends. Local JSONL/CSV only.
"""CEO Operating System router — daily brief, weekly review, decisions, assumptions.

GET  /api/v1/founder/ceo-os/daily-brief
GET  /api/v1/founder/ceo-os/weekly-review
GET  /api/v1/founder/ceo-os/decisions?limit=N
POST /api/v1/founder/ceo-os/decisions     (PRIVATE_OPS required; 503 if disabled)
GET  /api/v1/founder/ceo-os/assumptions

All endpoints are admin-key gated. Sensitive data lives in PRIVATE_OPS and
is exposed via `dealix.private_ops` resolution.
"""
from __future__ import annotations

import csv
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.private_ops import (
    is_enabled,
    missing_private_ops_note,
    resolve_csv,
    resolve_jsonl,
    write_jsonl_append,
)

router = APIRouter(prefix="/api/v1/founder/ceo-os", tags=["founder", "ceo-os"])

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_CSV = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
PIPELINE_CSV = REPO_ROOT / "docs/ops/pipeline_tracker.csv"


def _read_jsonl(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _read_csv(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@router.get("/daily-brief", dependencies=[Depends(require_admin_key)])
async def daily_brief() -> dict[str, Any]:
    enabled = is_enabled()
    decisions = _read_jsonl(resolve_jsonl("ceo/decisions.jsonl")) if enabled else []
    pending = [d for d in decisions if d.get("status") == "pending"]
    pending.sort(key=lambda d: d.get("recorded_at", ""), reverse=True)
    pipeline_rows = _read_csv(PIPELINE_CSV)
    evidence_rows = _read_csv(EVIDENCE_CSV)
    return {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "top_focus": [pending[0]["decision"]] if pending else [],
        "decisions_pending": {"count": len(pending), "items": pending[:5]},
        "pipeline_signal": {"rows": len(pipeline_rows)},
        "evidence_signal": {"rows": len(evidence_rows)},
        "is_estimate": True,
        "governance_decision": "allow",
    }


@router.get("/weekly-review", dependencies=[Depends(require_admin_key)])
async def weekly_review() -> dict[str, Any]:
    questions: list[str] = []
    try:
        import yaml  # type: ignore[import-not-found]
        reg_path = REPO_ROOT / "dealix/execution_assurance/registry.yaml"
        if reg_path.exists():
            data = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
            questions = list(data.get("weekly_ceo_review_questions_en", []))
    except Exception:  # noqa: BLE001
        questions = []
    return {
        "week_end": datetime.now(UTC).strftime("%Y-%m-%d"),
        "private_ops_enabled": is_enabled(),
        "questions": questions,
        "scorecard_link": "docs/founder/CEO_WEEKLY_REVIEW.md",
        "is_estimate": True,
    }


@router.get("/decisions", dependencies=[Depends(require_admin_key)])
async def list_decisions(limit: int = 20) -> dict[str, Any]:
    enabled = is_enabled()
    items: list[dict[str, Any]] = []
    if enabled:
        decisions = _read_jsonl(resolve_jsonl("ceo/decisions.jsonl"))
        decisions.sort(key=lambda d: d.get("recorded_at", ""), reverse=True)
        items = decisions[: max(0, min(limit, 200))]
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "count": len(items),
        "items": items,
    }


VALID_TYPES = {
    "bet", "cut", "delegate", "hire", "automate",
    "pricing", "partnership", "policy", "other",
}
VALID_STATUS = {"pending", "executing", "done", "reversed"}


class DecisionAppend(BaseModel):
    decision: str = Field(..., min_length=3)
    type: str
    owner: str
    reversible: bool = False
    expected_outcome: str | None = None
    kill_trigger: str | None = None
    assumption_ids: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)
    supersedes: str | None = None
    status: str = "pending"


@router.post("/decisions", dependencies=[Depends(require_admin_key)])
async def append_decision(payload: DecisionAppend) -> dict[str, Any]:
    if not is_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=missing_private_ops_note("en"),
        )
    if payload.type not in VALID_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"type must be one of: {sorted(VALID_TYPES)}",
        )
    if payload.status not in VALID_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"status must be one of: {sorted(VALID_STATUS)}",
        )
    record = payload.model_dump()
    record["id"] = str(uuid.uuid4())
    target = write_jsonl_append("ceo/decisions.jsonl", record)
    return {
        "id": record["id"],
        "path": str(target),
        "recorded_at": datetime.now(UTC).isoformat(),
        "governance_decision": "allow",
    }


@router.get("/assumptions", dependencies=[Depends(require_admin_key)])
async def assumptions() -> dict[str, Any]:
    enabled = is_enabled()
    items: list[dict[str, str]] = []
    if enabled:
        items = _read_csv(resolve_csv("ceo/strategic_assumptions.csv"))
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "count": len(items),
        "items": items,
    }
