#!/usr/bin/env python3
"""Run one revenue day: validate, seed, score, generate drafts, report.

This orchestrator never sends anything externally. All outreach artifacts are
drafts written to disk for human review. It produces ``latest.md`` and
``latest.json`` in ``reports/revenue/`` plus a dated report folder.

Usage:
    python scripts/revenue/run_revenue_day.py
"""
from __future__ import annotations

import argparse
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
    write_csv,
)
from scripts.revenue.validate_targets import validate_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one revenue day — drafts only, never sends")
    parser.add_argument("--prospects", default="ledgers/prospects.csv")
    args, _unknown = parser.parse_known_args()

    ensure_dirs()
    ensure_ledgers()

    prospects_path = REPO_ROOT / args.prospects
    prospects = load_csv(prospects_path)

    # Validate — no source, no entry
    issues, valid = validate_rows(prospects)
    if issues:
        print("Validation issues found:")
        for issue in issues:
            print(f"  {issue}")

    # Score
    scored = [score_target(r) for r in valid]
    hot = sum(1 for s in scored if s["tier"] == "hot")
    warm = sum(1 for s in scored if s["tier"] == "warm")
    cold = sum(1 for s in scored if s["tier"] == "cold")

    sectors = Counter(r.get("sector", "unknown") for r in valid)

    outbox_dir = REPO_ROOT / "outbox" / today_str()
    drafts = list(outbox_dir.glob("*.md")) if outbox_dir.exists() else []

    pipeline = load_csv(REPO_ROOT / "ledgers" / "deals_pipeline.csv")
    forecast = sum(
        float(row.get("value_sar", "0") or 0) * float(row.get("close_probability", "0") or 0)
        for row in pipeline
    )

    report = {
        "date": today_str(),
        "prospects": {
            "total": len(valid),
            "hot": hot,
            "warm": warm,
            "cold": cold,
            "rejected_no_source": len(prospects) - len(valid),
        },
        "drafts_generated_today": len(drafts),
        "pipeline_forecast_sar": round(forecast, 2),
        "sector_breakdown": dict(sectors),
        "next_actions_today": [
            f"Review {len(drafts)} drafts in outbox/{today_str()}",
            f"Contact {hot} hot prospects",
            "Update ledgers/deals_pipeline.csv after meetings",
            "Validate new prospects with validate_targets.py",
        ],
    }

    # Write dated report
    dated_dir = REPO_ROOT / "reports" / "revenue" / today_str()
    dated_dir.mkdir(parents=True, exist_ok=True)
    (dated_dir / "daily_ceo_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Write latest.md and latest.json (symlinks not used for Windows portability)
    reports_dir = REPO_ROOT / "reports" / "revenue"
    reports_dir.mkdir(parents=True, exist_ok=True)

    latest_json = reports_dir / "latest.json"
    latest_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# Dealix Revenue Day — {today_str()}",
        "",
        "Drafts only. No external send. source_url required.",
        "",
        "## Summary",
        f"- Total prospects: {report['prospects']['total']}",
        f"- Hot: {report['prospects']['hot']}",
        f"- Warm: {report['prospects']['warm']}",
        f"- Cold: {report['prospects']['cold']}",
        f"- Rejected (no source_url): {report['prospects']['rejected_no_source']}",
        f"- Drafts today: {report['drafts_generated_today']}",
        f"- Pipeline forecast: {report['pipeline_forecast_sar']:,.0f} SAR",
        "",
        "## Next Actions",
    ]
    md_lines.extend(f"- {a}" for a in report["next_actions_today"])
    md_lines.append("")

    latest_md = reports_dir / "latest.md"
    latest_md.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Revenue day complete — {today_str()}")
    print(f"  Prospects: {len(valid)} (rejected: {len(prospects) - len(valid)})")
    print(f"  Hot: {hot}  Warm: {warm}  Cold: {cold}")
    print(f"  Drafts today: {len(drafts)}")
    print(f"  Report: {latest_md}")
    print("  No external send. Drafts only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())