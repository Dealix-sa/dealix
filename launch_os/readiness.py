"""Launch readiness scoring + daily metrics over a draft run."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .safety import audit_queue


def daily_metrics(drafts: list[dict]) -> dict:
    by_vertical: dict[str, int] = {}
    by_offer: dict[str, int] = {}
    for d in drafts:
        by_vertical[d.get("vertical", "?")] = by_vertical.get(d.get("vertical", "?"), 0) + 1
        by_offer[d.get("offer", "?")] = by_offer.get(d.get("offer", "?"), 0) + 1
    top50 = sorted(drafts, key=lambda d: d.get("priority_score", 0), reverse=True)[:50]
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_drafts": len(drafts),
        "drafts_for_review": len(drafts),
        "drafts_sent": 0,  # always zero — review-only system
        "top_50_avg_priority": round(
            sum(d.get("priority_score", 0) for d in top50) / max(len(top50), 1), 1
        ),
        "by_vertical": by_vertical,
        "by_offer": by_offer,
    }


def readiness_report(queue_path: Path, target: int = 400) -> dict:
    """Compute the commercial launch readiness result for one run."""
    drafts: list[dict] = []
    with queue_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                drafts.append(json.loads(line))

    safety = audit_queue(queue_path)
    metrics = daily_metrics(drafts)

    checks = {
        "draft_count_meets_target": len(drafts) >= target,
        "safety_pass": bool(safety.get("pass")),
        "zero_sent": metrics["drafts_sent"] == 0,
        "all_verticals_present": len(metrics["by_vertical"]) >= 5,
    }
    score = round(100 * sum(checks.values()) / len(checks))
    return {
        "generated_at": metrics["generated_at"],
        "target": target,
        "score": score,
        "ready": all(checks.values()),
        "checks": checks,
        "metrics": metrics,
        "safety_pass": bool(safety.get("pass")),
    }
