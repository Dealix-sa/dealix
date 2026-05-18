"""Weekly founder decision analysis."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import yaml

from dealix.commercial_ops.paths import FOUNDER_WEEKLY_DIR, REPO_ROOT


def analyze_weekly_one_decision() -> dict[str, Any]:
    FOUNDER_WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(
        FOUNDER_WEEKLY_DIR.glob("decision_*.yaml"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    latest: dict[str, Any] | None = None
    latest_path: str | None = None
    if files:
        latest_path = str(files[0].relative_to(REPO_ROOT)).replace("\\", "/")
        try:
            latest = yaml.safe_load(files[0].read_text(encoding="utf-8"))
        except yaml.YAMLError:
            latest = None
    week_id = datetime.now(UTC).strftime("%Y-W%V")
    has_this_week = any(week_id in f.name for f in files[:3])
    if latest and isinstance(latest, dict) and (latest.get("one_decision") or "").strip():
        verdict = "FILLED" if has_this_week else "STALE"
    else:
        verdict = "MISSING"
    return {
        "verdict": verdict,
        "week_id": week_id,
        "has_this_week": has_this_week,
        "latest_path": latest_path,
        "latest": latest,
    }
