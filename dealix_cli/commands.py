"""Priority CLI commands.

These commands are intentionally simple. They drive the daily and weekly
operating loop and assume a private ops directory layout:

    <private-ops>/
        pipeline/pipeline_tracker.csv
        revenue/cash_collected.csv
        revenue/pipeline_value.csv
        revenue/mrr_tracker.csv
        founder/daily_brief.md
        founder/decision_queue.md
        learning/weekly_intelligence_review.md
        dashboard_data/company_metrics.json
        trust/approval_log.csv
"""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"private-ops path does not exist: {path}")
    return path


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def verify(private_ops: str) -> None:
    """Verify the private ops layout is healthy."""
    root = ensure_private_ops(private_ops)

    required = [
        "pipeline/pipeline_tracker.csv",
        "revenue/cash_collected.csv",
        "revenue/pipeline_value.csv",
        "revenue/mrr_tracker.csv",
        "founder/daily_brief.md",
        "founder/decision_queue.md",
    ]

    missing = [name for name in required if not (root / name).exists()]
    if missing:
        print("Private ops verification failed. Missing:")
        for item in missing:
            print("-", item)
        raise SystemExit(1)

    leads = _read_csv(root / "pipeline/pipeline_tracker.csv")
    bad = [row.get("lead_id") or row.get("name") or "<unknown>" for row in leads if not row.get("next_action")]
    if bad:
        print("Leads without next_action:")
        for item in bad:
            print("-", item)
        raise SystemExit(1)

    print("PASS: private ops layout is healthy.")


def daily(private_ops: str) -> None:
    """Refresh the founder daily brief and decision queue."""
    root = ensure_private_ops(private_ops)
    leads = _read_csv(root / "pipeline/pipeline_tracker.csv")
    today = date.today().isoformat()

    brief = root / "founder/daily_brief.md"
    brief.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Daily Brief — {today}",
        "",
        "## Revenue Focus",
        f"- Active leads: {len(leads)}",
    ]

    by_stage: dict[str, int] = {}
    for row in leads:
        stage = (row.get("stage") or "").strip() or "Unknown"
        by_stage[stage] = by_stage.get(stage, 0) + 1
    if by_stage:
        lines.append("- By stage:")
        for stage, count in sorted(by_stage.items()):
            lines.append(f"  - {stage}: {count}")

    actions_today = [
        row for row in leads
        if (row.get("next_action_date") or "").strip() == today and row.get("next_action")
    ]
    lines += ["", "## Today's Actions"]
    if actions_today:
        for row in actions_today:
            name = row.get("name") or row.get("lead_id") or "<lead>"
            lines.append(f"- {name}: {row.get('next_action')}")
    else:
        lines.append("- (none scheduled for today)")

    lines += ["", "## End-of-day Result", "- ", "", "## Learning Note", "- "]
    brief.write_text("\n".join(lines) + "\n", encoding="utf-8")

    queue = root / "founder/decision_queue.md"
    if not queue.exists():
        queue.write_text(f"# Decision Queue\n\nLast updated: {today}\n", encoding="utf-8")

    print(f"PASS: daily brief written to {brief}")


def dashboard(private_ops: str) -> None:
    """Refresh dashboard_data/company_metrics.json from the operating files."""
    root = ensure_private_ops(private_ops)
    leads = _read_csv(root / "pipeline/pipeline_tracker.csv")
    cash = _read_csv(root / "revenue/cash_collected.csv")
    pipeline_value = _read_csv(root / "revenue/pipeline_value.csv")
    mrr = _read_csv(root / "revenue/mrr_tracker.csv")

    def _sum(rows: list[dict[str, str]], column: str) -> float:
        total = 0.0
        for row in rows:
            value = (row.get(column) or "0").replace(",", "").strip()
            try:
                total += float(value)
            except ValueError:
                continue
        return total

    metrics = {
        "as_of": date.today().isoformat(),
        "leads_total": len(leads),
        "cash_collected_sar": _sum(cash, "amount_sar"),
        "pipeline_value_sar": _sum(pipeline_value, "amount_sar"),
        "mrr_sar": _sum(mrr, "amount_sar"),
    }

    out = root / "dashboard_data/company_metrics.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print(f"PASS: dashboard metrics written to {out}")


def weekly(private_ops: str) -> None:
    """Refresh the weekly intelligence review and remind the founder of the loop."""
    root = ensure_private_ops(private_ops)
    today = date.today().isoformat()

    review = root / "learning/weekly_intelligence_review.md"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(
        "\n".join(
            [
                f"# Weekly Intelligence Review — {today}",
                "",
                "## 1. Metrics this week",
                "- leads added: ",
                "- DMs sent: ",
                "- replies: ",
                "- calls: ",
                "- proposals: ",
                "- payments: ",
                "",
                "## 2. What worked",
                "- ",
                "",
                "## 3. What did not work",
                "- ",
                "",
                "## 4. One learning decision",
                "- ",
                "",
                "## 5. System update applied (file changed)",
                "- ",
                "",
                "## 6. Next-week experiment",
                "- ",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"PASS: weekly review scaffold written to {review}")
    print("Remember: the week is not closed without one learning decision and one system update.")


def close_day(private_ops: str) -> None:
    """Display the end-of-day close checklist."""
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Daily Close Checklist")
    print("- Did you update pipeline stages?")
    print("- Did you send/follow up on revenue actions?")
    print("- Did you review approvals?")
    print("- Did you record blockers?")
    print("- Did you write end-of-day result in founder/daily_brief.md?")
    print("- Did any repeated issue need a checklist/playbook update?")

    daily_brief = private_ops_path / "founder/daily_brief.md"
    if daily_brief.exists():
        print(f"\nUpdate this file before closing: {daily_brief}")

    print("\nPASS: close-day checklist displayed.")
