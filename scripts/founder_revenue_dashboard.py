#!/usr/bin/env python3
"""Founder Revenue Dashboard — aggregates review-only artifacts into metrics.

Reads (best-effort; missing inputs degrade to zero / "manual input required"):
    outputs/commercial_launch/<latest>/draft_summary.json
    outputs/founder_action_queue/<latest>/founder_actions.csv
    data/revenue_manual_events.example.jsonl   (manual ledger, if present)

Writes:
    outputs/revenue_dashboard/latest_dashboard.md
    outputs/revenue_dashboard/latest_dashboard.json

Never assumes real numbers: if there is no manual ledger data, revenue/reply
metrics are reported as 0 with a "manual input required" note. No sending.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter

from _v7_revenue_common import (
    DATA,
    OUTPUTS,
    SAFETY_BANNER,
    latest_dated_dir,
    read_json,
    read_jsonl,
    today,
    write_json,
    write_text,
)


def _load_actions(date: str | None) -> list[dict]:
    base = OUTPUTS / "founder_action_queue"
    day = (base / date) if date and (base / date).exists() else latest_dated_dir(base)
    if not day:
        return []
    csv_path = day / "founder_actions.csv"
    if not csv_path.exists():
        return []
    with csv_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _load_draft_summary(date: str | None) -> dict:
    base = OUTPUTS / "commercial_launch"
    day = (base / date) if date and (base / date).exists() else latest_dated_dir(base)
    if not day:
        return {}
    return read_json(day / "draft_summary.json", {}) or {}


def build(date: str | None = None) -> dict:
    date = today(date)
    draft_summary = _load_draft_summary(date)
    actions = _load_actions(date)
    events = read_jsonl(DATA / "revenue_manual_events.example.jsonl")

    manual_data = bool(events)

    def count_event(etype: str) -> int:
        return sum(1 for e in events if e.get("event_type") == etype)

    def sum_amount(etype: str) -> float:
        return sum(float(e.get("amount_sar", 0) or 0) for e in events if e.get("event_type") == etype)

    approved = sum(1 for a in actions if a.get("status") == "approved_for_manual_copy")

    # Pipeline value = open diagnostics proposed + pilots proposed (illustrative,
    # derived only from recorded manual events; 0 when no ledger data).
    pipeline_value = sum_amount("diagnostic_sold") + sum_amount("pilot_sold")
    realized_revenue = sum_amount("diagnostic_sold") + sum_amount("pilot_sold")

    vert_counter = Counter(a.get("vertical", "") for a in actions if a.get("vertical"))
    chan_counter = Counter(a.get("channel", "") for a in actions if a.get("channel"))

    top_vertical = vert_counter.most_common(1)[0][0] if vert_counter else "manual input required"
    top_channel = chan_counter.most_common(1)[0][0] if chan_counter else "manual input required"

    metrics = {
        "date": date,
        "drafts_generated_today": int(draft_summary.get("drafts_generated", 0)),
        "founder_actions_today": len(actions),
        "approved_manual_actions": approved,
        "manual_sends_recorded": count_event("manual_send_recorded"),
        "positive_replies_recorded": count_event("reply_positive"),
        "discovery_calls_booked": count_event("discovery_booked"),
        "diagnostics_sold": count_event("diagnostic_sold"),
        "pilots_proposed": count_event("pilot_proposed"),
        "pilots_sold": count_event("pilot_sold"),
        "retainers_started": count_event("retainer_started"),
        "pipeline_value_sar": pipeline_value,
        "realized_revenue_sar": realized_revenue,
        "top_vertical": top_vertical,
        "top_channel": top_channel,
        "top_objection": "manual input required" if not manual_data else "review notes",
        "stuck_stage": "manual input required" if not manual_data else "review ledger",
        "next_best_action": (
            "Generate drafts → approve → send manually → record replies"
            if not manual_data
            else "Convert positive replies into booked discovery calls"
        ),
        "manual_input_required": not manual_data,
        "safety": SAFETY_BANNER,
    }

    write_json(OUTPUTS / "revenue_dashboard" / "latest_dashboard.json", metrics)

    md = [
        "# Founder Revenue Dashboard",
        "",
        f"> {SAFETY_BANNER}",
        "",
        f"Date: {date}",
        "",
        "| Metric | Value |",
        "| ------ | ----- |",
    ]
    label = {
        "drafts_generated_today": "Drafts generated today",
        "founder_actions_today": "Founder actions today",
        "approved_manual_actions": "Approved manual actions",
        "manual_sends_recorded": "Manual sends recorded",
        "positive_replies_recorded": "Positive replies recorded",
        "discovery_calls_booked": "Discovery calls booked",
        "diagnostics_sold": "Diagnostics sold",
        "pilots_proposed": "Pilots proposed",
        "pilots_sold": "Pilots sold",
        "retainers_started": "Retainers started",
        "pipeline_value_sar": "Pipeline value (SAR)",
        "realized_revenue_sar": "Realized revenue (SAR)",
        "top_vertical": "Top vertical",
        "top_channel": "Top channel",
        "top_objection": "Top objection",
        "stuck_stage": "Stuck stage",
        "next_best_action": "Next best action",
    }
    for key, text in label.items():
        md.append(f"| {text} | {metrics[key]} |")
    if not manual_data:
        md += [
            "",
            (
                "> No manual ledger data found. Revenue/reply metrics show 0 — "
                "**manual input required**. Record events in "
                "`data/revenue_manual_events.example.jsonl`."
            ),
        ]
    md.append("")
    write_text(OUTPUTS / "revenue_dashboard" / "latest_dashboard.md", "\n".join(md))
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    metrics = build(args.date)
    print("[revenue_dashboard] built → outputs/revenue_dashboard/latest_dashboard.md")
    print(f"[revenue_dashboard] drafts={metrics['drafts_generated_today']} "
          f"actions={metrics['founder_actions_today']} "
          f"realized_sar={metrics['realized_revenue_sar']}")
    print(f"[revenue_dashboard] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
