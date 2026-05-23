"""Render the Master CEO Dashboard from private ledgers.

Reads only. Writes a single Markdown report to
dealix-ops-private/founder/master_dashboard.md. Prints a concise summary
to stdout. Gracefully handles missing files (treats them as zeros).

See docs/founder/MASTER_DASHBOARD.md.
"""

from __future__ import annotations

import csv
import datetime as dt
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sum_amount(rows: list[dict[str, str]], field: str) -> float:
    total = 0.0
    for r in rows:
        try:
            total += float(r.get(field) or 0)
        except (TypeError, ValueError):
            continue
    return total


def _safe_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def render() -> str:
    today = dt.date.today()
    month_prefix = today.strftime("%Y-%m")

    cash = _read_csv(PRIVATE / "revenue" / "cash_collected.csv")
    pipeline = _read_csv(PRIVATE / "revenue" / "pipeline_value.csv")
    mrr = _read_csv(PRIVATE / "revenue" / "mrr_tracker.csv")
    pipeline_now = _read_csv(PRIVATE / "sales" / "pipeline.csv")
    dms = _read_csv(PRIVATE / "sales" / "dms_sent.csv")
    sprints = _read_csv(PRIVATE / "delivery" / "sprint_register.csv")
    retainers = _read_csv(PRIVATE / "client_success" / "retainers.csv")

    cash_mtd = sum(
        float(r.get("amount_sar") or 0)
        for r in cash
        if (r.get("date") or "").startswith(month_prefix)
        and (r.get("status") or "").lower() == "paid"
    )

    weighted_pipeline = 0.0
    if pipeline:
        latest_date = max((r.get("snapshot_date") or "") for r in pipeline)
        weighted_pipeline = sum(
            float(r.get("weighted_amount_sar") or 0)
            for r in pipeline
            if r.get("snapshot_date") == latest_date
        )

    active_retainers = [
        r
        for r in mrr
        if (r.get("month") or "").startswith(month_prefix)
        and (r.get("paid") or "").lower() in {"true", "1", "yes", "y"}
    ]
    mrr_total = sum(float(r.get("monthly_fee_sar") or 0) for r in active_retainers)

    stage_counts: Counter[str] = Counter(
        (r.get("stage") or "unknown") for r in pipeline_now
    )

    week_start = today - dt.timedelta(days=today.weekday())
    dms_this_week = sum(
        1
        for r in dms
        if (r.get("date_sent") or "") >= week_start.isoformat()
    )
    replies_this_week = sum(
        1
        for r in dms
        if (r.get("date_sent") or "") >= week_start.isoformat()
        and (r.get("reply") or "").lower() in {"y", "yes", "true", "1"}
    )

    sprints_in_flight = sum(
        1
        for r in sprints
        if (r.get("delivered_on") or "").strip() == ""
    )
    sprints_delivered_month = sum(
        1
        for r in sprints
        if (r.get("delivered_on") or "").startswith(month_prefix)
    )

    active_retainer_count = sum(
        1
        for r in retainers
        if (r.get("paid_current_month") or "").lower() in {"y", "yes", "true", "1"}
    )

    decision_queue_file = PRIVATE / "founder" / "decision_queue.md"
    approvals_file = PRIVATE / "founder" / "approvals_waiting.md"
    risks_file = PRIVATE / "founder" / "risk_log.md"
    decisions_open = (
        decision_queue_file.read_text(encoding="utf-8").count("\n- ")
        if decision_queue_file.exists()
        else 0
    )
    approvals_open = (
        approvals_file.read_text(encoding="utf-8").count("\n- ")
        if approvals_file.exists()
        else 0
    )
    risks_open = (
        risks_file.read_text(encoding="utf-8").count("\n- ")
        if risks_file.exists()
        else 0
    )

    lines: list[str] = []
    lines.append(f"# Master CEO Dashboard — {today.isoformat()}\n")
    lines.append(
        "> What must Sami do today to move Dealix closer to cash, proof, or retention?\n"
    )

    lines.append("## Revenue")
    lines.append(f"- Cash collected (MTD): **{cash_mtd:,.0f} SAR**")
    lines.append(f"- Pipeline value (weighted, latest snapshot): **{weighted_pipeline:,.0f} SAR**")
    lines.append(f"- MRR (paid active retainers, this month): **{mrr_total:,.0f} SAR**")
    lines.append(f"- Active retainers (paid current month): **{active_retainer_count}**")
    lines.append(f"- Sprints in flight: **{sprints_in_flight}**")
    lines.append(f"- Sprints delivered (this month): **{sprints_delivered_month}**\n")

    lines.append("## Pipeline (this week)")
    lines.append(f"- DMs sent: **{dms_this_week}** / target 25")
    lines.append(f"- Replies: **{replies_this_week}**")
    lines.append("- Stage counts:")
    for stage in (
        "new",
        "qualified",
        "contacted",
        "replied",
        "sample_sent",
        "call_booked",
        "proposal_sent",
        "paid",
        "delivered",
        "retainer",
        "lost",
    ):
        if stage_counts.get(stage):
            lines.append(f"  - {stage}: {stage_counts[stage]}")
    lines.append("")

    lines.append("## Trust")
    lines.append(f"- Decisions open: **{decisions_open}** (target ≤ 3)")
    lines.append(f"- Approvals open: **{approvals_open}** (target ≤ 5)")
    lines.append(f"- Risks open: **{risks_open}**\n")

    lines.append("## Linked Sources")
    lines.append("- `dealix-ops-private/revenue/cash_collected.csv`")
    lines.append("- `dealix-ops-private/revenue/mrr_tracker.csv`")
    lines.append("- `dealix-ops-private/sales/pipeline.csv`")
    lines.append("- `dealix-ops-private/sales/dms_sent.csv`")
    lines.append("- `dealix-ops-private/delivery/sprint_register.csv`")
    lines.append("- `dealix-ops-private/client_success/retainers.csv`")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    if not PRIVATE.exists():
        print("[dashboard] dealix-ops-private not staged. Run `make stage` first.")
        return 1
    out = render()
    target = PRIVATE / "founder" / "master_dashboard.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print(out)
    print(f"\n[dashboard] wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
