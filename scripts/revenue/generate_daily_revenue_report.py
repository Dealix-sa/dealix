#!/usr/bin/env python3
"""
Generate daily CEO revenue report from ledgers and outbox.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, score_target, today_str


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate daily CEO revenue report")
    parser.add_argument("--prospects", default="ledgers/prospects.csv")
    parser.add_argument("--pipeline", default="ledgers/deals_pipeline.example.csv")
    args = parser.parse_args()

    prospects = load_csv(REPO_ROOT / args.prospects)
    pipeline = load_csv(REPO_ROOT / args.pipeline)

    scored = [score_target(r) for r in prospects]
    hot = sum(1 for s in scored if s["tier"] == "hot")
    warm = sum(1 for s in scored if s["tier"] == "warm")
    cold = sum(1 for s in scored if s["tier"] == "cold")

    sectors = Counter(r.get("sector", "unknown") for r in prospects)
    pains = Counter(
        (r.get("pain") or r.get("pain_hypothesis", ""))[:40]
        for r in prospects
        if r.get("pain") or r.get("pain_hypothesis")
    )

    outbox_dir = REPO_ROOT / "outbox" / today_str()
    drafts = list(outbox_dir.glob("*.md")) if outbox_dir.exists() else []

    forecast = sum(
        float(row.get("deal_value_sar", "0") or 0) * float(row.get("probability", "0") or 0)
        for row in pipeline
    )

    report = {
        "date": today_str(),
        "prospects": {"total": len(prospects), "hot": hot, "warm": warm, "cold": cold},
        "drafts_generated_today": len(drafts),
        "pipeline_forecast_sar": round(forecast, 2),
        "sector_breakdown": dict(sectors),
        "top_pain_patterns": [p for p, _ in pains.most_common(5)],
        "next_actions_today": [
            f"Review {len(drafts)} drafts in outbox/{today_str()}",
            f"Contact {hot} hot prospects",
            "Update ledgers/deals_pipeline.csv after meetings",
        ],
    }

    out_dir = REPO_ROOT / "reports" / "revenue" / today_str()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "daily_ceo_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# تقرير CEO اليومي — {today_str()}",
        "",
        "## ملخص الفرص",
        f"- إجمالي الشركات: {report['prospects']['total']}",
        f"- ساخنة: {report['prospects']['hot']}",
        f"- دافئة: {report['prospects']['warm']}",
        f"- باردة: {report['prospects']['cold']}",
        "",
        f"## مسودات اليوم: {report['drafts_generated_today']}",
        "",
        f"## توقع الأنابيب: {report['pipeline_forecast_sar']:,.0f} ريال",
        "",
        "## توزيع القطاعات",
        json.dumps(report["sector_breakdown"], ensure_ascii=False, indent=2),
        "",
        "## أهم أنماط الألم",
    ]
    md_lines.extend(f"- {p}" for p in report["top_pain_patterns"])
    md_lines.extend(["", "## الإجراءات التالية"])
    md_lines.extend(f"- {a}" for a in report["next_actions_today"])
    md_lines.append("")

    md_path = out_dir / "daily_ceo_report.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Report: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
