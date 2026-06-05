#!/usr/bin/env python3
"""Learning loop — weekly retrospective that makes the machine smarter.

Reads the outcomes ledger (data/targeting/outcomes.jsonl) and answers:
    - which sector scored / replied / converted best?
    - which message angle produced diagnostics?
    - which offer closed?
    - which source produced bad (rejected) companies?
    - which queries to stop, which to double down on?

Output: out/weekly_targeting_retrospective.md and tomorrow's targeting plan
deltas. Pure aggregation — no sending, no scraping.

Usage:
    python scripts/targeting_learning_loop.py --out data/targeting/out
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from scripts.targeting_common import OUT_DIR, OUTCOMES_FILE, load_outcomes

# Stages that count as progress, in order of value.
PROGRESS_STAGES = ["no_reply", "replied", "diagnostic", "paid"]


def analyze(outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate the outcomes ledger into learning signals."""
    by_sector_scores: dict[str, list[int]] = defaultdict(list)
    sector_replies: Counter[str] = Counter()
    sector_paid: Counter[str] = Counter()
    angle_diagnostics: Counter[str] = Counter()
    offer_closed: Counter[str] = Counter()
    bad_sources: Counter[str] = Counter()
    angle_total: Counter[str] = Counter()

    for o in outcomes:
        sector = o.get("sector") or "unknown"
        stage = o.get("stage")
        angle = o.get("message_angle") or "unknown"
        if isinstance(o.get("score"), int):
            by_sector_scores[sector].append(o["score"])
        if stage in ("replied", "diagnostic", "paid"):
            sector_replies[sector] += 1
        if stage == "diagnostic":
            angle_diagnostics[angle] += 1
        angle_total[angle] += 1
        if stage == "paid":
            sector_paid[sector] += 1
            if o.get("offer"):
                offer_closed[o["offer"]] += 1
        if stage == "rejected" and o.get("source_type"):
            bad_sources[o["source_type"]] += 1

    avg_scores = {s: round(sum(v) / len(v), 1) for s, v in by_sector_scores.items() if v}
    best_sector = max(avg_scores, key=avg_scores.get) if avg_scores else "—"
    worst_sector = min(avg_scores, key=avg_scores.get) if avg_scores else "—"
    best_angle = angle_diagnostics.most_common(1)[0][0] if angle_diagnostics else "—"
    best_offer = offer_closed.most_common(1)[0][0] if offer_closed else "—"
    most_replied = sector_replies.most_common(1)[0][0] if sector_replies else "—"

    return {
        "avg_scores": avg_scores,
        "best_sector": best_sector,
        "worst_sector": worst_sector,
        "most_replied_sector": most_replied,
        "best_message_angle": best_angle,
        "best_offer": best_offer,
        "sector_paid": dict(sector_paid),
        "bad_sources": dict(bad_sources),
        "totals": {
            "outcomes": len(outcomes),
            "replied": sum(sector_replies.values()),
            "paid": sum(sector_paid.values()),
        },
    }


def render(report: dict[str, Any]) -> str:
    today = date.today().isoformat()
    avg = "\n".join(f"  - {s}: {v}" for s, v in sorted(
        report["avg_scores"].items(), key=lambda kv: kv[1], reverse=True))
    bad = "\n".join(f"  - {s}: {n} rejects" for s, n in report["bad_sources"].items()) or "  - none"
    double_down = report["most_replied_sector"]
    stop = max(report["bad_sources"], key=report["bad_sources"].get) if report["bad_sources"] else "—"
    return f"""# Weekly Targeting Retrospective — {today}

## ماذا نجح / What worked
- **أفضل قطاع (score):** `{report['best_sector']}`
- **أكثر قطاع ردًّا / most replied:** `{report['most_replied_sector']}`
- **أفضل زاوية رسالة / best angle:** `{report['best_message_angle']}`
- **أفضل عرض أغلق / best closing offer:** `{report['best_offer']}`

## أرقام / Numbers
- outcomes logged: {report['totals']['outcomes']}
- replied: {report['totals']['replied']}
- paid: {report['totals']['paid']}

## متوسط score لكل قطاع / Avg score per sector
{avg or "  - none"}

## مصادر سيئة / Sources that produced rejects
{bad}

## خطة الأسبوع القادم / Next week plan
- **Double down on:** `{double_down}`
- **De-prioritise / worst sector:** `{report['worst_sector']}`
- **Stop ingesting from:** `{stop}`
- **Lead with angle:** `{report['best_message_angle']}`
- **Lead with offer:** `{report['best_offer']}`
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix targeting weekly learning loop")
    ap.add_argument("--in", dest="infile", default=str(OUTCOMES_FILE))
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    args = ap.parse_args(argv)

    outcomes = load_outcomes(Path(args.infile))
    report = analyze(outcomes)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "weekly_targeting_retrospective.md"
    path.write_text(render(report), encoding="utf-8")
    print(f"retrospective → {path}  "
          f"(best_sector={report['best_sector']}, best_offer={report['best_offer']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
