from pathlib import Path
import csv
from datetime import date


HEADERS = [
    "week_ending",
    "lead_count",
    "contacted",
    "replied",
    "call_booked",
    "sample_sent",
    "proposal_sent",
    "paid",
    "delivered",
    "retainer",
    "mrr",
    "approvals_pending",
]


def append_weekly_metrics(private_ops_root: str, metrics: dict) -> Path:
    root = Path(private_ops_root)
    path = root / "metrics_history/weekly_metrics.csv"
    path.parent.mkdir(parents=True, exist_ok=True)

    exists = path.exists() and path.stat().st_size > 0

    row = {
        "week_ending": date.today().isoformat(),
        "lead_count": metrics.get("lead_count", 0),
        "contacted": metrics.get("contacted", 0),
        "replied": metrics.get("replied", 0),
        "call_booked": metrics.get("call_booked", 0),
        "sample_sent": metrics.get("sample_sent", 0),
        "proposal_sent": metrics.get("proposal_sent", 0),
        "paid": metrics.get("paid", 0),
        "delivered": metrics.get("delivered", 0),
        "retainer": metrics.get("retainer", 0),
        "mrr": metrics.get("mrr", 0),
        "approvals_pending": metrics.get("approvals_pending", 0),
    }

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

    return path
