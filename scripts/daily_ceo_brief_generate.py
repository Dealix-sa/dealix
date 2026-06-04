#!/usr/bin/env python3
"""Daily CEO Brief — one page that reads all V7 review-only outputs.

Aggregates (best-effort) from:
    outputs/commercial_launch/<latest>/draft_summary.json
    outputs/founder_action_queue/<latest>/
    outputs/revenue_dashboard/latest_dashboard.json
    outputs/market_intelligence/<latest>/

Writes:
    outputs/ceo_briefs/YYYY-MM-DD/CEO_DAILY_BRIEF.md

Pure summarization of local artifacts. No sending, no API, no secrets.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import (
    OUTPUTS,
    SAFETY_BANNER,
    latest_dated_dir,
    read_json,
    today,
    write_text,
)


def _draft_status(date: str) -> dict:
    base = OUTPUTS / "commercial_launch"
    day = (base / date) if (base / date).exists() else latest_dated_dir(base)
    if not day:
        return {"status": "not generated", "count": 0}
    summary = read_json(day / "draft_summary.json", {}) or {}
    return {"status": "ready (review-only)", "count": summary.get("drafts_generated", 0)}


def _dashboard() -> dict:
    return read_json(OUTPUTS / "revenue_dashboard" / "latest_dashboard.json", {}) or {}


def generate(date: str | None = None) -> dict:
    date = today(date)
    drafts = _draft_status(date)
    dash = _dashboard()
    aq = latest_dated_dir(OUTPUTS / "founder_action_queue")
    mi = latest_dated_dir(OUTPUTS / "market_intelligence")

    actions_today = dash.get("founder_actions_today", 0)
    realized = dash.get("realized_revenue_sar", 0)

    md = f"""# CEO Daily Brief — {date}

> {SAFETY_BANNER}

## Top 5 priorities
1. Review today's draft queue and approve the strongest.
2. Send approved messages **manually** from your own accounts.
3. Convert positive replies into booked discovery calls.
4. Turn discovery into a paid diagnostic where fit is real.
5. Record every manual event in the ledger.

## Revenue status
- Drafts generated: {drafts['count']} ({drafts['status']})
- Founder actions today: {actions_today}
- Realized revenue (SAR): {realized}
- Pipeline value (SAR): {dash.get('pipeline_value_sar', 0)}
- Next best action: {dash.get('next_best_action', 'manual input required')}

## Draft factory status
{drafts['status']} — review-only, send-blocked.

## Delivery status
Diagnostics sold: {dash.get('diagnostics_sold', 0)} · Pilots sold: {dash.get('pilots_sold', 0)} · Retainers: {dash.get('retainers_started', 0)}

## Market/social status
Market brief: {'ready' if mi else 'not generated (manual input required)'}

## Action queue status
{'ready: ' + str(aq.name) if aq else 'not generated'}

## Safety status
All external action manual + founder-approved. No automated sending. No scraping. No secrets.

## Blocked items
{'Manual ledger empty — record events.' if dash.get('manual_input_required') else 'None flagged.'}

## Today decision required
- Which prospects to advance to a paid diagnostic.
- Which weak opportunities to mark `suppressed`.

## What NOT to do today
- Do not auto-send anything.
- Do not run cold WhatsApp/LinkedIn automation.
- Do not claim guaranteed ROI or fake traction.

## Tomorrow focus
- Follow up on positive replies.
- Prepare diagnostic packs for booked discovery calls.
"""
    out_path = OUTPUTS / "ceo_briefs" / date / "CEO_DAILY_BRIEF.md"
    write_text(out_path, md)
    return {"out_path": str(out_path), "date": date}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    result = generate(args.date)
    print(f"[ceo_brief] {result['date']} → {result['out_path']}")
    print(f"[ceo_brief] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
