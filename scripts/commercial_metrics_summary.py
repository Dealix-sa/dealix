#!/usr/bin/env python3
"""Daily metrics summary -> daily_metrics.json.

Aggregates counts from the daily queue and gates. No real revenue numbers are
invented; revenue/pipeline fields are placeholders for manual founder input.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import now_iso, output_day_dir, read_jsonl, today_str, write_json  # noqa: E402


def run(day: str) -> dict:
    d = output_day_dir(day)
    drafts = read_jsonl(d / "draft_queue.jsonl") if (d / "draft_queue.jsonl").exists() else []
    rejected = read_jsonl(d / "rejected_drafts.jsonl") if (d / "rejected_drafts.jsonl").exists() else []
    needs_research = read_jsonl(d / "needs_research.jsonl") if (d / "needs_research.jsonl").exists() else []

    quality = _load(d / "quality_report.json")
    compliance = _load(d / "compliance_report.json")
    safety = _load(d / "safety_audit.json")

    metrics = {
        "generated_at": now_iso(),
        "day": day,
        "drafts_generated": len(drafts),
        "drafts_by_channel": {
            c: sum(1 for x in drafts if x["channel"] == c)
            for c in ("cold_email", "follow_up", "linkedin_manual", "website_form")
        },
        "founder_review_count": len(drafts),
        "compliance_rejections": len(rejected),
        "needs_research": len(needs_research),
        "quality_pass_rate": quality.get("pass_rate") if quality else None,
        "safety_violations": len(safety.get("violations", [])) if safety else None,
        "manual_sends": 0,
        "replies": 0,
        "positive_replies": 0,
        "booked_diagnostics": 0,
        "paid_diagnostics": 0,
        "pilots_proposed": 0,
        "pilots_sold": 0,
        "retainer_starts": 0,
        "pipeline_sar": None,
        "realized_revenue_sar": None,
        "_note": "Revenue, pipeline, and reply metrics are populated from manual founder input; not auto-assumed.",
    }
    write_json(d / "daily_metrics.json", metrics)
    return metrics


def _load(p: Path) -> dict:
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    m = run(args.day)
    print(f"Daily metrics: {m['drafts_generated']} drafts, {m['compliance_rejections']} rejected, {m['needs_research']} need research")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
