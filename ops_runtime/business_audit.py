"""CEO Business Score calculator.

Reads ``pipeline/pipeline_tracker.csv`` from the private-ops root and
derives the funnel counts the Priority Router needs. Missing files
return a zeroed score rather than raising — the router treats zero as
"start at the top of the funnel".
"""
from __future__ import annotations

import csv
from pathlib import Path


PIPELINE_CSV = "pipeline/pipeline_tracker.csv"

# Each stage adds points to the total, capped at 100.
_STAGE_WEIGHTS = {
    "lead_count": (25, 10),
    "contacted": (25, 15),
    "sample_sent": (3, 15),
    "proposal_sent": (1, 20),
    "paid": (1, 20),
    "delivered": (1, 10),
    "retainer": (1, 10),
}


def _empty_metrics() -> dict:
    return {
        "lead_count": 0,
        "contacted": 0,
        "sample_sent": 0,
        "proposal_sent": 0,
        "cash_collected": 0,
        "paid": 0,
        "delivered": 0,
        "retainer": 0,
    }


def _read_pipeline(csv_path: Path) -> dict:
    metrics = _empty_metrics()
    if not csv_path.exists():
        return metrics
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            metrics["lead_count"] += 1
            stage = (row.get("stage") or "").strip().lower()
            payment_status = (row.get("payment_status") or "").strip().lower()
            sample_status = (row.get("sample_status") or "").strip().lower()
            proposal_status = (row.get("proposal_status") or "").strip().lower()
            delivery_status = (row.get("delivery_status") or "").strip().lower()
            retainer_status = (row.get("retainer_status") or "").strip().lower()
            sent_at = (row.get("sent_at") or "").strip()
            revenue = (row.get("revenue_sar") or "0").strip() or "0"

            if sent_at or stage in {"contacted", "replied", "sample", "proposal", "paid", "delivered"}:
                metrics["contacted"] += 1
            if stage in {"sample", "proposal", "paid", "delivered"} or sample_status in {"sent", "delivered"}:
                metrics["sample_sent"] += 1
            if stage in {"proposal", "paid", "delivered"} or proposal_status in {"sent", "signed"}:
                metrics["proposal_sent"] += 1
            if payment_status in {"paid", "po", "approved"} or stage in {"paid", "delivered"}:
                metrics["paid"] += 1
                try:
                    metrics["cash_collected"] += int(float(revenue))
                except ValueError:
                    pass
            if delivery_status in {"delivered", "qa_passed"} or stage == "delivered":
                metrics["delivered"] += 1
            if retainer_status in {"signed", "active"}:
                metrics["retainer"] += 1
    return metrics


def _status_from_score(total: int) -> str:
    if total >= 80:
        return "Healthy"
    if total >= 50:
        return "Building"
    if total >= 20:
        return "Activating"
    return "Cold start"


def calculate_business_score(private_root: str) -> dict:
    """Return CEO Business Score for the given private-ops root."""
    root = Path(private_root)
    metrics = _read_pipeline(root / PIPELINE_CSV)

    total = 0
    for key, (target, weight) in _STAGE_WEIGHTS.items():
        if target <= 0:
            continue
        ratio = min(metrics.get(key, 0) / target, 1.0)
        total += int(round(ratio * weight))
    total = min(total, 100)

    return {
        "total_score": total,
        "status": _status_from_score(total),
        "metrics": metrics,
    }
