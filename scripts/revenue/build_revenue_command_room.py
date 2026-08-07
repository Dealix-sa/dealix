#!/usr/bin/env python3
"""Build a Revenue Command Room HTML report.

Reads ledgers and outbox to produce a single self-contained HTML report at
``reports/revenue/command_room.html``. This script never sends anything
externally — it only reads local files and writes an HTML file for human
review.

Usage:
    python scripts/revenue/build_revenue_command_room.py
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import (
    REPO_ROOT,
    ensure_dirs,
    ensure_ledgers,
    load_csv,
    score_target,
    today_str,
)


def _esc(text: str) -> str:
    return html.escape(str(text or ""))


def build_html() -> str:
    ensure_dirs()
    ensure_ledgers()

    prospects = load_csv(REPO_ROOT / "ledgers" / "prospects.csv")
    pipeline = load_csv(REPO_ROOT / "ledgers" / "deals_pipeline.csv")
    outreach = load_csv(REPO_ROOT / "ledgers" / "outreach_log.csv")
    replies = load_csv(REPO_ROOT / "ledgers" / "reply_log.csv")
    proposals = load_csv(REPO_ROOT / "ledgers" / "proposal_log.csv")
    clients = load_csv(REPO_ROOT / "ledgers" / "clients.csv")

    scored = [score_target(r) for r in prospects]
    hot = sum(1 for s in scored if s["tier"] == "hot")
    warm = sum(1 for s in scored if s["tier"] == "warm")
    cold = sum(1 for s in scored if s["tier"] == "cold")

    sectors = Counter(r.get("sector", "unknown") for r in prospects)
    forecast = sum(
        float(row.get("value_sar", "0") or 0) * float(row.get("close_probability", "0") or 0)
        for row in pipeline
    )

    outbox_dir = REPO_ROOT / "outbox" / today_str()
    drafts = list(outbox_dir.glob("*.md")) if outbox_dir.exists() else []

    # Build HTML
    parts: list[str] = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="ar" dir="rtl">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8">')
    parts.append(f"<title>Dealix Revenue Command Room — {today_str()}</title>")
    parts.append("<style>")
    parts.append("body{font-family:system-ui,Arial,sans-serif;margin:24px;background:#f7f7f7;color:#222}")
    parts.append("h1{color:#1a3a5c}")
    parts.append(".card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px;margin:12px 0}")
    parts.append(".metric{display:inline-block;margin:8px 16px;text-align:center}")
    parts.append(".metric .num{font-size:28px;font-weight:bold;color:#1a3a5c}")
    parts.append(".metric .label{font-size:12px;color:#666}")
    parts.append("table{border-collapse:collapse;width:100%}")
    parts.append("th,td{border:1px solid #ddd;padding:6px 10px;text-align:right}")
    parts.append("th{background:#1a3a5c;color:#fff}")
    parts.append(".hot{color:#c0392b}.warm{color:#e67e22}.cold{color:#2980b9}")
    parts.append(".note{color:#666;font-size:12px}")
    parts.append("</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append("<h1>Dealix Revenue Command Room</h1>")
    parts.append(f"<p class='note'>Date: {today_str()} · Drafts only · No external send</p>")

    # Metrics row
    parts.append('<div class="card">')
    parts.append('<div class="metric"><div class="num">' + str(len(prospects)) + '</div><div class="label">Prospects</div></div>')
    parts.append('<div class="metric"><div class="num hot">' + str(hot) + '</div><div class="label">Hot</div></div>')
    parts.append('<div class="metric"><div class="num warm">' + str(warm) + '</div><div class="label">Warm</div></div>')
    parts.append('<div class="metric"><div class="num cold">' + str(cold) + '</div><div class="label">Cold</div></div>')
    parts.append('<div class="metric"><div class="num">' + str(len(drafts)) + '</div><div class="label">Drafts Today</div></div>')
    parts.append('<div class="metric"><div class="num">' + str(len(pipeline)) + '</div><div class="label">Pipeline Deals</div></div>')
    parts.append('<div class="metric"><div class="num">' + str(len(clients)) + '</div><div class="label">Clients</div></div>')
    parts.append("</div>")

    # Forecast
    parts.append('<div class="card">')
    parts.append("<h2>Pipeline Forecast</h2>")
    parts.append(f"<p>Weighted forecast: <strong>{forecast:,.0f} SAR</strong></p>")
    parts.append("</div>")

    # Sector breakdown
    parts.append('<div class="card">')
    parts.append("<h2>Sector Breakdown</h2>")
    if sectors:
        parts.append("<table><tr><th>Sector</th><th>Count</th></tr>")
        for sector, count in sectors.most_common():
            parts.append(f"<tr><td>{_esc(sector)}</td><td>{count}</td></tr>")
        parts.append("</table>")
    else:
        parts.append("<p class='note'>No prospects yet.</p>")
    parts.append("</div>")

    # Top prospects table
    parts.append('<div class="card">')
    parts.append("<h2>Top Prospects</h2>")
    if prospects:
        parts.append("<table><tr><th>Company</th><th>Sector</th><th>City</th><th>Source URL</th><th>Score</th><th>Tier</th></tr>")
        scored_rows = list(zip(prospects, scored))
        scored_rows.sort(key=lambda rs: rs[1]["score"], reverse=True)
        for row, result in scored_rows[:20]:
            tier_cls = result["tier"]
            parts.append(
                f"<tr><td>{_esc(row.get('company_name'))}</td>"
                f"<td>{_esc(row.get('sector'))}</td>"
                f"<td>{_esc(row.get('city'))}</td>"
                f"<td><a href='{_esc(row.get('source_url'))}'>{_esc(row.get('source_url'))}</a></td>"
                f"<td>{result['score']}</td>"
                f"<td class='{tier_cls}'>{tier_cls}</td></tr>"
            )
        parts.append("</table>")
    else:
        parts.append("<p class='note'>No prospects yet. Run seed_demo_revenue_data.py.</p>")
    parts.append("</div>")

    # Next actions
    parts.append('<div class="card">')
    parts.append("<h2>Next Actions Today</h2>")
    parts.append("<ul>")
    parts.append(f"<li>Review {len(drafts)} drafts in outbox/{today_str()}</li>")
    parts.append(f"<li>Contact {hot} hot prospects</li>")
    parts.append("<li>Update ledgers/deals_pipeline.csv after meetings</li>")
    parts.append("<li>Validate new prospects with validate_targets.py</li>")
    parts.append("</ul>")
    parts.append("</div>")

    parts.append('<p class="note">No external send. Drafts only. source_url required.</p>')
    parts.append("</body></html>")

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Revenue Command Room HTML report")
    parser.add_argument("--output", default="reports/revenue/command_room.html")
    args = parser.parse_args()

    report_html = build_html()
    out_path = REPO_ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_html, encoding="utf-8")
    print(f"Command Room report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
