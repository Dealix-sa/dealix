"""SOAEN loop compliance — war room, evidence, weekly board."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import (
    load_evidence_rows,
    real_evidence_rows,
)
from dealix.commercial_ops.paths import (
    FOUNDER_WEEKLY_ONE_DECISION_YAML,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)

WEEKLY_BOARD_QUESTIONS_AR = [
    {"id": "icp_this_week", "question_ar": "من ICP هذا الأسبوع؟", "field": "icp_focus_ar"},
    {"id": "weakest_soaen_link", "question_ar": "ما أضعف حلقة في SOAEN؟", "field": "weakest_soaen_link_ar"},
    {
        "id": "evidence_before_scale",
        "question_ar": "ما الدليل المطلوب قبل التوسعة؟",
        "field": "evidence_before_scale_ar",
    },
]


def _load_war_room_targets() -> list[dict[str, Any]]:
    if not WAR_ROOM_TODAY_JSON.is_file():
        return []
    try:
        data = json.loads(WAR_ROOM_TODAY_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    targets = data.get("targets") or {}
    items = targets.get("items") if isinstance(targets, dict) else None
    return list(items) if isinstance(items, list) else []


def _row_soaen_checks(row: dict[str, str]) -> dict[str, bool]:
    return {
        "owner": bool((row.get("owner") or "").strip()),
        "source": bool((row.get("source_channel") or "").strip()),
        "next_action": bool((row.get("next_action") or "").strip()),
    }


def analyze_soaen_loop(*, evidence_days: int = 7) -> dict[str, Any]:
    today = datetime.now(UTC).date()
    since = today - timedelta(days=max(1, evidence_days) - 1)

    war_gaps: list[str] = []
    for item in _load_war_room_targets():
        company = (item.get("company") or "?").strip()
        na = (item.get("next_action") or "").strip()
        if not na:
            war_gaps.append(f"War Room: {company} — بدون next_action")
        elif "موافقة" not in na and "مسودة" not in na:
            war_gaps.append(f"War Room: {company} — next_action بلا موافقة/مسودة")

    evidence_gaps: list[str] = []
    recent = 0
    for row in real_evidence_rows(load_evidence_rows()):
        raw = (row.get("event_date") or "")[:10]
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date() if raw else None
        except ValueError:
            d = None
        if d is None or d < since or d > today:
            continue
        recent += 1
        checks = _row_soaen_checks(row)
        label = (row.get("company") or row.get("event_type") or "?").strip()
        if not checks["owner"]:
            evidence_gaps.append(f"Evidence: {label} — بدون owner")
        if not checks["source"]:
            evidence_gaps.append(f"Evidence: {label} — بدون source_channel")

    board: dict[str, Any] = {}
    if FOUNDER_WEEKLY_ONE_DECISION_YAML.is_file():
        board = yaml.safe_load(FOUNDER_WEEKLY_ONE_DECISION_YAML.read_text(encoding="utf-8")) or {}

    board_gaps: list[str] = []
    for q in WEEKLY_BOARD_QUESTIONS_AR:
        if not (board.get(q["field"]) or "").strip():
            board_gaps.append(f"لوحة الأسبوع: {q['question_ar']} — غير مملوءة")
    if not (board.get("one_decision_ar") or "").strip():
        board_gaps.append("one_decision_ar فارغ في founder_weekly_one_decision.yaml")

    blockers = war_gaps + evidence_gaps + board_gaps
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "date": today.isoformat(),
        "verdict": "PASS" if not blockers else "ACTION_REQUIRED",
        "war_room": {"p0_count": len(_load_war_room_targets()), "gaps": war_gaps},
        "evidence": {"recent_real_rows": recent, "gaps": evidence_gaps},
        "weekly_board": {
            "filled": {q["id"]: bool((board.get(q["field"]) or "").strip()) for q in WEEKLY_BOARD_QUESTIONS_AR},
            "gaps": board_gaps,
        },
        "blockers_ar": blockers,
    }
