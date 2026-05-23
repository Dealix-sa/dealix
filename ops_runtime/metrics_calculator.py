from __future__ import annotations

"""Compute KPI metrics from raw private ops state."""

from collections import Counter
from pathlib import Path
from typing import Any


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", "")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def compute_pipeline_metrics(pipeline: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate pipeline rows."""
    total = len(pipeline)
    by_stage: Counter = Counter()
    by_sector: Counter = Counter()
    pipeline_value = 0.0
    priority_high = 0

    for row in pipeline:
        stage = (row.get("stage") or "unknown").strip() or "unknown"
        sector = (row.get("sector") or "unknown").strip() or "unknown"
        by_stage[stage] += 1
        by_sector[sector] += 1
        pipeline_value += _to_float(row.get("deal_value_sar"))
        priority = (row.get("priority") or "").strip().lower()
        if priority in {"high", "p0", "p1"}:
            priority_high += 1

    return {
        "total_leads": total,
        "by_stage": dict(by_stage),
        "by_sector": dict(by_sector),
        "pipeline_value_sar": round(pipeline_value, 2),
        "priority_high": priority_high,
    }


def compute_revenue_metrics(actions: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate revenue action rows."""
    counts: dict[str, int] = {
        "dms_sent": 0,
        "samples_sent": 0,
        "proposals_sent": 0,
        "payments_pursued": 0,
    }
    cash_collected = 0.0

    mapping = {
        "dm_sent": "dms_sent",
        "sample_sent": "samples_sent",
        "proposal_sent": "proposals_sent",
        "payment_pursued": "payments_pursued",
        "po_pursued": "payments_pursued",
    }

    for row in actions:
        action_type = (row.get("action_type") or "").strip().lower()
        bucket = mapping.get(action_type)
        if bucket:
            counts[bucket] += 1
        if action_type in {"payment_received", "cash_collected"}:
            cash_collected += _to_float(row.get("amount_sar"))

    counts["cash_collected_sar"] = round(cash_collected, 2)
    return counts


def compute_delivery_metrics(clients_paths: list[Path]) -> dict[str, Any]:
    """Read each client's status.md (frontmatter `status:` line) to classify."""
    active = 0
    in_delivery = 0
    completed = 0
    at_risk = 0

    for client_dir in clients_paths:
        status = _read_client_status(client_dir).lower()
        if status in {"completed", "done", "closed"}:
            completed += 1
            continue
        # anything else is "active" in some form
        active += 1
        if status in {"in_delivery", "delivering", "delivery"}:
            in_delivery += 1
        if status in {"at_risk", "blocked", "stalled"}:
            at_risk += 1

    return {
        "active_clients": active,
        "in_delivery": in_delivery,
        "completed": completed,
        "at_risk": at_risk,
    }


def _read_client_status(client_dir: Path) -> str:
    """Look in `status.md` frontmatter for a `status:` value."""
    status_file = client_dir / "status.md"
    if not status_file.exists():
        return "active"
    try:
        text = status_file.read_text(encoding="utf-8")
    except OSError:
        return "active"
    in_frontmatter = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            break
        if in_frontmatter and stripped.lower().startswith("status:"):
            return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return "active"
