#!/usr/bin/env python3
"""Founder daily command — a single-screen operating scan for the founder.

Reads revenue/delivery state from ``data/revenue/*.jsonl`` and writes a
markdown command sheet to ``reports/founder/daily_command.md``. Degrades
gracefully when the data files are missing or empty. Supports ``--json``.

Self-contained: no third-party imports.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REVENUE_DIR = ROOT / "data" / "revenue"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSONL file, skipping blank/malformed lines. Empty if missing."""
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _load_revenue_state(revenue_dir: Path | None = None) -> dict[str, list[dict[str, Any]]]:
    base = revenue_dir if revenue_dir is not None else REVENUE_DIR
    return {
        "revenue_events": _read_jsonl(base / "revenue_events.jsonl"),
        "payments": _read_jsonl(base / "payments.jsonl"),
    }


def build_daily_command(revenue_dir: Path | None = None) -> dict[str, Any]:
    """Build the founder daily command structure.

    Returns a dict with today's date, revenue events today, proof packs
    delivered, open approvals, the next 3 actions, and a bilingual action line.
    """
    today = date.today().isoformat()
    state = _load_revenue_state(revenue_dir)
    events = state["revenue_events"]
    payments = state["payments"]

    revenue_events_today = [e for e in events if e.get("date") == today]
    proof_packs_delivered = [e for e in events if e.get("event") == "proof_pack_delivered"]

    # Open approvals: external actions still awaiting the founder. In this
    # founder-operations layer the count is derived defensively from any event
    # explicitly flagged as awaiting approval; absence means zero (not unknown).
    open_approvals = [
        e
        for e in events + payments
        if e.get("status") == "awaiting_approval" or e.get("awaiting_approval") is True
    ]

    next_actions = [
        "Review any external send still awaiting approval (do not auto-send).",
        "Confirm each paid event has a backing Source Passport and proof entry.",
        "Advance the next warm target through diagnostic to offer.",
    ]

    degraded = not events and not payments

    return {
        "date": today,
        "degraded": degraded,
        "revenue_events_today_count": len(revenue_events_today),
        "revenue_events_today": revenue_events_today,
        "proof_packs_delivered_count": len(proof_packs_delivered),
        "payments_count": len(payments),
        "open_approvals_count": len(open_approvals),
        "open_approvals": open_approvals,
        "next_actions": next_actions[:3],
        "founder_action_ar": "ابدأ بالموافقات المعلقة قبل أي إرسال خارجي.",
        "founder_action_en": "Start with pending approvals before any external send.",
    }


def render_markdown(command: dict[str, Any]) -> str:
    """Render the daily command as markdown."""
    lines = [
        "# Founder Daily Command | موجز قيادة المؤسس",
        "",
        f"Date: {command['date']}",
    ]
    if command["degraded"]:
        lines.append("")
        lines.append("Note: no revenue/delivery data found; showing baseline command sheet.")
    lines.extend(
        [
            "",
            "## Today | اليوم",
            "",
            f"- Paid revenue events today: {command['revenue_events_today_count']}",
            f"- Proof packs delivered (total): {command['proof_packs_delivered_count']}",
            f"- Payments recorded (total): {command['payments_count']}",
            f"- Open approvals awaiting founder: {command['open_approvals_count']}",
            "",
            "## Next 3 Actions | الإجراءات الثلاثة التالية",
            "",
        ]
    )
    for i, action in enumerate(command["next_actions"], start=1):
        lines.append(f"{i}. {action}")
    lines.extend(
        [
            "",
            "## Founder Action | إجراء المؤسس",
            "",
            f"- AR: {command['founder_action_ar']}",
            f"- EN: {command['founder_action_en']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(command: dict[str, Any]) -> Path:
    """Write the daily command markdown report and return its path."""
    report_dir = ROOT / "reports" / "founder"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "daily_command.md"
    report_path.write_text(render_markdown(command), encoding="utf-8")
    return report_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    command = build_daily_command()
    report_path = write_report(command)

    if args.json:
        print(json.dumps(command, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(command))
        print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
