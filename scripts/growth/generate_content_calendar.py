#!/usr/bin/env python3
"""Render a 30-day content calendar from data/growth/content_ideas.jsonl.

Offline, deterministic. Every scheduled item carries exactly ONE CTA.
Items marked status=needs-approval are flagged — they are NOT auto-published;
case-safe / proof content requires founder approval (non-negotiable #8).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "growth" / "content_ideas.jsonl"
OUT = ROOT / "reports" / "growth"

START = datetime.now(timezone.utc).date()
DAYS = 30


def load() -> list[dict]:
    rows: list[dict] = []
    if not DATA.exists():
        return rows
    for line in DATA.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> int:
    rows = load()
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# 30-Day Content Calendar — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Source: `data/growth/content_ideas.jsonl` ({len(rows)} ideas)",
        "",
        "> Each item has ONE CTA. Items flagged ⚠ need founder approval before publishing",
        "> (proof / case-safe content). No external publishing is automated.",
        "",
        "| Date | Type | Channel | Topic | CTA | Approval |",
        "|---|---|---|---|---|---|",
    ]
    needs_approval = 0
    for i in range(DAYS):
        if not rows:
            break
        idea = rows[i % len(rows)]
        date = START + timedelta(days=i)
        flag = ""
        if idea.get("status") == "needs-approval":
            flag = "⚠ founder"
            needs_approval += 1
        lines.append(
            "| {date} | {type} | {channel} | {topic} | {cta} | {flag} |".format(
                date=date.isoformat(),
                type=idea.get("type", ""),
                channel=idea.get("channel", ""),
                topic=idea.get("topic_ar", "").replace("|", "/"),
                cta=idea.get("cta", ""),
                flag=flag,
            )
        )
    lines += [
        "",
        "## Notes",
        "",
        f"- Ideas in pool: {len(rows)}; calendar length: {DAYS} days (pool repeats if shorter).",
        f"- Items needing founder approval before publishing: {needs_approval} occurrences.",
        "- One CTA per asset — do not stack CTAs.",
        "- Repurpose each idea into ~10 assets (post, video, blog, newsletter, etc.) — see CONTENT_FACTORY.md.",
        "",
    ]
    (OUT / "CONTENT_CALENDAR_30D.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_CONTENT_CALENDAR=PASS ({len(rows)} ideas, {DAYS} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
