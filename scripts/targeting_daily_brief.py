#!/usr/bin/env python3
"""
targeting_daily_brief.py — render the Daily Targeting Brief markdown.

Pure formatting over an already-scored company list. Produces the funnel
summary, top segments, strongest pain signals, top-10 targets table, tomorrow's
direction, and an explicit "Stop Doing" line. No network, no sends.

Usage:
    python scripts/targeting_daily_brief.py --in data/targeting/out/scored.jsonl \
        --raw 400 --out data/targeting/out/daily_targeting_brief.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def summarize(companies: list[dict[str, Any]], raw_candidates: int | None = None) -> dict[str, Any]:
    clean = len(companies)
    a_grade = [c for c in companies if str(c.get("grade")) in {"A+", "A"}]
    shortlist = [c for c in a_grade if float(c.get("targeting_score", 0)) >= 80]

    seg_scores: dict[str, list[float]] = defaultdict(list)
    for c in companies:
        seg_scores[str(c.get("sector") or "unknown")].append(float(c.get("targeting_score", 0)))
    segments = sorted(
        ((s, round(sum(v) / len(v), 1), len(v)) for s, v in seg_scores.items() if v),
        key=lambda t: t[1],
        reverse=True,
    )

    pain_counter: Counter[str] = Counter()
    for c in companies:
        pain_counter.update(c.get("pain_signals", []) or [])

    return {
        "raw_candidates": raw_candidates if raw_candidates is not None else clean,
        "clean_companies": clean,
        "a_grade": len(a_grade),
        "shortlist": len(shortlist),
        "segments": segments,
        "top_pains": pain_counter.most_common(5),
        "top_targets": sorted(
            companies, key=lambda c: float(c.get("targeting_score", 0)), reverse=True
        )[:10],
    }


def render_brief(
    companies: list[dict[str, Any]],
    *,
    raw_candidates: int | None = None,
    drafts: int = 0,
    manual_sends: int = 0,
    brief_date: str | None = None,
) -> str:
    s = summarize(companies, raw_candidates)
    d = brief_date or date.today().isoformat()
    lines = [
        "# Dealix Daily Targeting Brief",
        f"_Date: {d}_",
        "",
        "## Summary",
        f"- Raw candidates: {s['raw_candidates']}",
        f"- Clean companies: {s['clean_companies']}",
        f"- A-grade targets: {s['a_grade']}",
        f"- Founder shortlist: {s['shortlist']}",
        f"- Drafts generated: {drafts}",
        f"- Manual sends recommended: {manual_sends}",
        "",
        "## Top Segments",
    ]
    if s["segments"]:
        for i, (seg, avg, n) in enumerate(s["segments"][:5], 1):
            lines.append(f"{i}. {seg} — avg score {avg} ({n} companies)")
    else:
        lines.append("_no segments yet_")

    lines += ["", "## Strongest Pain Signals"]
    if s["top_pains"]:
        for pain, n in s["top_pains"]:
            lines.append(f"- {pain} ({n})")
    else:
        lines.append("_no pain signals yet_")

    lines += [
        "",
        "## Top 10 Targets",
        "| Company | Sector | Score | Pain | Offer | Evidence |",
        "|---|---|---:|---|---|---:|",
    ]
    for c in s["top_targets"]:
        pains = ", ".join((c.get("pain_signals") or [])[:2]) or "—"
        lines.append(
            f"| {c.get('company_name','—')} "
            f"| {c.get('sector','—')} "
            f"| {c.get('targeting_score',0)} "
            f"| {pains} "
            f"| {c.get('recommended_offer','—')} "
            f"| {c.get('evidence_count', len(c.get('source_urls',[]) or []))} |"
        )

    top_seg = s["segments"][0][0] if s["segments"] else "B2B consulting / training"
    lines += [
        "",
        "## Tomorrow's Targeting Direction",
        f"Focus on Riyadh-based **{top_seg}** companies with weak proof visibility "
        "and a clear official contact channel.",
        "",
        "## Stop Doing",
        "- Do not target companies with only one weak evidence source.",
        "- Do not send anything without founder approval.",
        "",
    ]
    return "\n".join(lines)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS daily brief")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--raw", type=int, default=None, help="raw candidate count")
    ap.add_argument("--drafts", type=int, default=0)
    ap.add_argument("--sends", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    companies = _read_jsonl(Path(args.infile))
    md = render_brief(
        companies, raw_candidates=args.raw, drafts=args.drafts, manual_sends=args.sends
    )
    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(md + "\n", encoding="utf-8")
        print(f"wrote brief -> {outp}", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
