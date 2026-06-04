#!/usr/bin/env python3
"""Market Intelligence Brief — summarizes manually-maintained signals.

Reads config/market_intelligence_signals.json (manual/research input; NOT
scraped) and writes a review brief. No web access, no scraping, no sending.

Output:
    outputs/market_intelligence/YYYY-MM-DD/market_brief.md
    outputs/market_intelligence/YYYY-MM-DD/market_brief.json

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import (
    CONFIG,
    OUTPUTS,
    SAFETY_BANNER,
    read_json,
    today,
    write_json,
    write_text,
)


def build(date: str | None = None) -> dict:
    date = today(date)
    cfg = read_json(CONFIG / "market_intelligence_signals.json", {}) or {}
    verticals = cfg.get("verticals", [])
    backlog = cfg.get("research_backlog", [])
    competitors = cfg.get("competitor_watch", [])

    high_signals = []
    for v in verticals:
        for s in v.get("signals", []):
            if s.get("priority") == "high":
                high_signals.append((v.get("vertical"), s.get("signal")))

    md = [
        "# Market Intelligence Brief",
        "",
        f"> {SAFETY_BANNER}",
        "> Source: manual/research input only. No scraping.",
        "",
        f"Date: {date} · Verticals tracked: {len(verticals)}",
        "",
        "## High-priority signals",
        "",
    ]
    if high_signals:
        for vert, sig in high_signals:
            md.append(f"- **{vert}**: {sig}")
    else:
        md.append("- None recorded — manual input required.")
    md += ["", "## Competitor watch (manual)", ""]
    for c in competitors or [{"name": "none", "note": "manual input required"}]:
        md.append(f"- {c.get('name')}: {c.get('note', '')}")
    md += ["", "## Research backlog", ""]
    for item in backlog or ["manual input required"]:
        md.append(f"- [ ] {item}")
    md.append("")
    write_text(OUTPUTS / "market_intelligence" / date / "market_brief.md", "\n".join(md))

    payload = {
        "date": date,
        "verticals_tracked": len(verticals),
        "high_priority_signals": [{"vertical": v, "signal": s} for v, s in high_signals],
        "competitors_watched": len(competitors),
        "research_backlog_items": len(backlog),
        "source": "manual_research_only",
        "safety": SAFETY_BANNER,
    }
    write_json(OUTPUTS / "market_intelligence" / date / "market_brief.json", payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    payload = build(args.date)
    print(f"[market_intelligence] verticals={payload['verticals_tracked']} "
          f"high_signals={len(payload['high_priority_signals'])}")
    print(f"[market_intelligence] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
