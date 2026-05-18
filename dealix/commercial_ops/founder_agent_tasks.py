"""Founder agent daily queue — seed from YAML templates."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

from dealix.commercial_ops.paths import (
    FOUNDER_AGENT_LEARNING_YAML,
    FOUNDER_AGENT_QUEUE_JSON,
    FOUNDER_AGENT_STATE_DIR,
    FOUNDER_AGENT_TASK_QUEUE_YAML,
)


def _today() -> str:
    return date.today().isoformat()


def _load_templates() -> dict[str, Any]:
    if not FOUNDER_AGENT_TASK_QUEUE_YAML.is_file():
        return {}
    return yaml.safe_load(FOUNDER_AGENT_TASK_QUEUE_YAML.read_text(encoding="utf-8")) or {}


def seed_today_queue(*, force: bool = False) -> dict[str, Any]:
    FOUNDER_AGENT_STATE_DIR.mkdir(parents=True, exist_ok=True)
    if FOUNDER_AGENT_QUEUE_JSON.is_file() and not force:
        existing = json.loads(FOUNDER_AGENT_QUEUE_JSON.read_text(encoding="utf-8"))
        if existing.get("date") == _today():
            return existing
    tpl = _load_templates()
    tasks: list[dict[str, Any]] = []
    for row in tpl.get("daily_templates") or []:
        if not isinstance(row, dict):
            continue
        tasks.append(
            {
                "id": row.get("id"),
                "agent": row.get("agent"),
                "priority": row.get("priority", "P2"),
                "title_ar": row.get("title_ar"),
                "status": "pending",
                "commands": row.get("commands") or [],
                "inputs": row.get("inputs") or [],
                "outputs": row.get("outputs") or [],
                "approval_required": bool(row.get("approval_required")),
            }
        )
    for row in tpl.get("weekly_templates") or []:
        if not isinstance(row, dict):
            continue
        tasks.append(
            {
                "id": row.get("id"),
                "agent": row.get("agent"),
                "priority": row.get("priority", "P2"),
                "title_ar": row.get("title_ar"),
                "status": "pending",
                "cadence": "weekly",
                "commands": row.get("commands") or [],
                "approval_required": bool(row.get("approval_required")),
            }
        )
    payload = {
        "date": _today(),
        "seeded_at": datetime.now(UTC).isoformat(),
        "policy_ar": tpl.get("policy_ar"),
        "tasks": tasks,
    }
    FOUNDER_AGENT_QUEUE_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def build_queue_status() -> dict[str, Any]:
    if not FOUNDER_AGENT_QUEUE_JSON.is_file():
        payload = seed_today_queue(force=True)
    else:
        payload = json.loads(FOUNDER_AGENT_QUEUE_JSON.read_text(encoding="utf-8"))
        if payload.get("date") != _today():
            payload = seed_today_queue(force=True)
    tasks = payload.get("tasks") or []
    pending = [t for t in tasks if t.get("status") != "done"]
    by_agent: dict[str, list[str]] = {}
    for t in pending:
        agent = str(t.get("agent") or "?")
        by_agent.setdefault(agent, []).append(str(t.get("title_ar") or t.get("id")))
    stats = {
        "total": len(tasks),
        "pending": len(pending),
        "done": len(tasks) - len(pending),
    }
    pending_p0 = [t for t in pending if t.get("priority") == "P0"]
    return {
        "date": payload.get("date"),
        "seeded": bool(tasks),
        "stats": stats,
        "pending_total": len(pending),
        "pending_p0_count": len(pending_p0),
        "pending_p0_ids": [str(t.get("id")) for t in pending_p0],
        "pending_by_agent": by_agent,
        "tasks": tasks,
        "policy_ar": payload.get("policy_ar"),
        "verdict": "PASS" if stats["total"] >= 3 and not pending else ("PARTIAL" if tasks else "WARN"),
    }


def templates_as_packets() -> dict[str, dict[str, Any]]:
    """Map YAML templates to print_agent_work_packets packet shape."""
    tpl = _load_templates()
    packets: dict[str, dict[str, Any]] = {}
    for row in tpl.get("daily_templates") or []:
        if not isinstance(row, dict):
            continue
        pid = str(row.get("id") or "unknown")
        packets[pid] = {
            "agent": row.get("agent"),
            "cadence": "daily",
            "inputs": row.get("inputs") or [],
            "outputs": row.get("outputs") or [],
            "verify_commands": row.get("commands") or [],
        }
    for row in tpl.get("weekly_templates") or []:
        if not isinstance(row, dict):
            continue
        pid = str(row.get("id") or "unknown")
        packets[pid] = {
            "agent": row.get("agent"),
            "cadence": "weekly",
            "inputs": row.get("inputs") or [],
            "outputs": row.get("outputs") or [],
            "verify_commands": row.get("commands") or [],
        }
    return packets


def update_task_status(task_id: str, status: str) -> dict[str, Any]:
    if not FOUNDER_AGENT_QUEUE_JSON.is_file():
        return {"ok": False, "error": "queue_not_seeded", "task_id": task_id}
    payload = json.loads(FOUNDER_AGENT_QUEUE_JSON.read_text(encoding="utf-8"))
    updated = False
    for t in payload.get("tasks") or []:
        if str(t.get("id")) == task_id:
            t["status"] = status
            t["updated_at"] = datetime.now(UTC).isoformat()
            updated = True
            break
    if not updated:
        return {"ok": False, "error": "task_not_found", "task_id": task_id}
    FOUNDER_AGENT_QUEUE_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    out = build_queue_status()
    out["ok"] = True
    out["task_id"] = task_id
    out["status"] = status
    return out


def load_today_queue() -> dict[str, Any]:
    if not FOUNDER_AGENT_QUEUE_JSON.is_file():
        return seed_today_queue()
    data = json.loads(FOUNDER_AGENT_QUEUE_JSON.read_text(encoding="utf-8"))
    if data.get("date") != _today():
        return seed_today_queue(force=True)
    return data


def load_weekly_learning() -> dict[str, Any]:
    if not FOUNDER_AGENT_LEARNING_YAML.is_file():
        return {"entries": [], "prompt_hints": {}, "external_refs": {}}
    return yaml.safe_load(FOUNDER_AGENT_LEARNING_YAML.read_text(encoding="utf-8")) or {}


def apply_learning_hints_to_playbook_snippet() -> str:
    hints = load_weekly_learning().get("prompt_hints") or {}
    if not hints:
        return ""
    lines = ["## تلميحات prompts (مراجعة أسبوعية)", ""]
    for agent, text in hints.items():
        lines.extend([f"### {agent}", str(text).strip(), ""])
    return "\n".join(lines)


def seed_quarterly_external_refs() -> dict[str, Any]:
    data = load_weekly_learning()
    if data.get("external_refs"):
        return data
    data["external_refs"] = {
        "quarterly_doc": "docs/commercial/EXTERNAL_GTM_QUARTERLY_REVIEW_AR.md",
        "b2d": ["https://www.reo.dev/blog/b2d-sales"],
        "agent_fleet": [
            "https://resources.github.com/enterprise/ai-powered-workforce-playbook/"
        ],
    }
    data.setdefault("entries", []).append(
        {
            "at": datetime.now(UTC).isoformat(),
            "agent": "dealix-pm",
            "worked_ar": "بذرة مراجع ربع سنوية",
            "failed_ar": "",
            "prompt_delta_ar": "راجع EXTERNAL_GTM_QUARTERLY_REVIEW_AR.md",
        }
    )
    FOUNDER_AGENT_STATE_DIR.mkdir(parents=True, exist_ok=True)
    FOUNDER_AGENT_LEARNING_YAML.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return data
