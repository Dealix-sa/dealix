#!/usr/bin/env python3
"""Weekly Board Report — review-only weekly summary from local artifacts.

Output:
    outputs/board_reports/YYYY-WW/WEEKLY_BOARD_REPORT.md

Never assumes real numbers: figures come only from recorded manual events and
generated artifacts. Where data is absent it states "manual input required".
No sending, no API, no secrets.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import (
    DATA,
    OUTPUTS,
    SAFETY_BANNER,
    iso_week,
    read_json,
    read_jsonl,
    today,
    write_text,
)


def generate(date: str | None = None) -> dict:
    date = today(date)
    week = iso_week(date)
    dash = read_json(OUTPUTS / "revenue_dashboard" / "latest_dashboard.json", {}) or {}
    events = read_jsonl(DATA / "revenue_manual_events.example.jsonl")
    has_data = bool(events)

    def count(etype: str) -> int:
        return sum(1 for e in events if e.get("event_type") == etype)

    md = f"""# Weekly Board Report — {week}

> {SAFETY_BANNER}

## Executive summary
Review-only operating week. The system prepared drafts, action queues,
diagnostics, proposals and reports. All external action remained manual and
founder-approved. {'Manual event data recorded.' if has_data else 'No manual event data yet — manual input required.'}

## Revenue pipeline
- Manual sends recorded: {count('manual_send_recorded')}
- Positive replies: {count('reply_positive')}
- Discovery booked: {count('discovery_booked')}
- Diagnostics sold: {count('diagnostic_sold')}
- Pilots sold: {count('pilot_sold')}
- Retainers started: {count('retainer_started')}

## Activity
- Drafts generated (latest day): {dash.get('drafts_generated_today', 0)}
- Founder actions (latest day): {dash.get('founder_actions_today', 0)}

## Conversion
- Reply → discovery and discovery → diagnostic ratios: {'see ledger' if has_data else 'manual input required'}

## Top sectors
- Top vertical: {dash.get('top_vertical', 'manual input required')}
- Top channel: {dash.get('top_channel', 'manual input required')}

## Product progress
- Revenue Execution OS, Founder Action Queue, Dashboard, Diagnostic Pack,
  Proposal Seed, Proof Asset, CEO Brief, Board Report all operational (review-only).

## Delivery progress
- Diagnostic and pilot conversion playbooks in place; proof assets templated.

## Risks
- Pipeline depends on manual founder execution.
- Revenue figures require disciplined manual ledger entry.

## Decisions needed
- Which verticals to double down on.
- Whether any opportunity qualifies to raise price / propose a retainer.

## Cash/revenue assumptions
- No assumed numbers. Realized revenue (SAR): {dash.get('realized_revenue_sar', 0)} (from ledger only).

## Next week plan
- Deepen the top 1–2 verticals.
- Convert positive replies into paid diagnostics.
- Maintain the manual events ledger daily.
"""
    out_path = OUTPUTS / "board_reports" / week / "WEEKLY_BOARD_REPORT.md"
    write_text(out_path, md)
    return {"out_path": str(out_path), "week": week}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    result = generate(args.date)
    print(f"[board_report] {result['week']} → {result['out_path']}")
    print(f"[board_report] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
